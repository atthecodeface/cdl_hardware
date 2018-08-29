#a Copyright
#  
#  This file 'Makefile' copyright Gavin J Stark 2016, 2017
#  
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# @file  Makefile
# @brief Basic makefile for CDL builds with extra targets
#
# Basic CDL makefile with additional targets for test regressions, help, etc
#


#a Global variables
# Note: make Q= EXTRA_CXXFLAGS='-I ~/Git/brew/include' EXTRA_LIBS='-L ~/Git/brew/lib'
# Note: make RISCV_ATCF_REGRESSION_DIR=../atthecodeface_riscv_tests SUITE=riscv_minimal.riscv_i32mc_pipeline3.test_c_arith test_regress
CYCLICITY := ../cdl/
CYCLICITY_ROOT := ${CYCLICITY}
MODEL_LIST  := $(CURDIR)/model_list
MODELS_MAKE := $(CURDIR)/models.make
SRC_ROOT    := $(CURDIR)/
PREFIX_OBJ_DIR := $(CURDIR)/build/
DEBUG_BUILD := no
EXTRA_CDLFLAGS := --extra_cdlflags="--v_clkgate_type='banana' --v_use_always_at_star --v_clks_must_have_enables "

LOCAL_CFLAGS   := -I/usr/local/include ${EXTRA_CFLAGS}
LOCAL_CXXFLAGS := -I/usr/local/include ${EXTRA_CXXFLAGS}
LOCAL_LINKLIBS := -L/usr/local/lib  -L/lib -L/lib/x86_64-linux-gnu -L/usr/lib/x86_64-linux-gnu -lpng12 -ljpeg
LOCAL_LINKLIBS :=  ${EXTRA_LIBS} -lpng12 -ljpeg
OS := $(shell uname)
ifeq ($(OS),Darwin)
LOCAL_LINKLIBS :=  ${EXTRA_LIBS} -L/usr/local/lib -lpng16 -ljpeg
endif

#a Include standard build makefile
include ${CYCLICITY}/scripts/simulation_build_make

verilog: ${VERILOG_FILES}

${TARGET_DIR}/bbc_display_vnc.o: ${SRC_ROOT}/cmodel/src/bbc_display_vnc.cpp
	$(Q)$(CXX) $(CXXFLAGS) -c -o ${TARGET_DIR}/bbc_display_vnc.o ${SRC_ROOT}/cmodel/src/bbc_display_vnc.cpp -Icmodel/inc

SHM_VNC_OBJS := ${TARGET_DIR}/fb.o ${TARGET_DIR}/vnc_rfb.o ${TARGET_DIR}/bbc_display_vnc.o ${TARGET_DIR}/bbc_shm.o
shm_vnc: ${SHM_VNC_OBJS}
	@echo "Building shm_vnc"
	${Q}${LINKASBIN} shm_vnc $(SHM_VNC_OBJS) ${LOCAL_LINKLIBS}

#a Test targets
.PHONY: regression
regression:
	$(MAKE) clean ALL
	./regress_all

test_python_6502: ${TARGET_DIR}/py_engine.so
	echo "Currently fails one test test_atc_test_6502_brk_rti"
	./python/test6502.py

test_regress_6502: ${TARGET_DIR}/py_engine.so
	./regress_all regression.base6502

test_6502_adc: ${TARGET_DIR}/py_engine.so
	./regress_all regression.base6502.Regress6502_Test6502_ALU.test_atc_test_6502_adc

test_regress: ${TARGET_DIR}/py_engine.so
	./regress_all regression.${SUITE}

test_regress_riscv: ${TARGET_DIR}/py_engine.so
	./regress_all regression.riscv_minimal

#a Operational targets
.PHONY: roms
roms:
	python python/teletext_font.py > roms/teletext.mif
	python python/apb_speed_selection.py > roms/apb_rom.mif
	python python/ps2_bbc_kbd_map.py
	python python/rom_to_mif.py

bbc_run: ${TARGET_DIR}/py_engine.so
	BBC=1 ./regress_all

bbc_waves: ${TARGET_DIR}/py_engine.so
	WAVES=1 BBC=1 ./regress_all

riscv_flows: ${TARGET_DIR}/py_engine.so
	./regress_all regression.riscv_minimal.riscv_i32c_pipeline3.${TEST}
	./python/rv_flow.py > min_pipe3_${TEST}.flow
	./regress_all regression.riscv_minimal.riscv_minimal.${TEST}
	./python/rv_flow.py > min_min_${TEST}.flow
	diff min_pipe3_${TEST}.flow min_min_${TEST}.flow

#a Help
DOLLAR := $$
help:
	@echo "This makefile permits making, testing and running of the BBC micro"
	@echo "The standard ROMs and disk images are not included in a standard distribution"
	@echo "due to copyright reasons"
	@echo "The BBC micro operation depends on an OS1.2 ROM, Basic2 ROM and a DFS ROM"
	@echo "These need to be in MIF file format in roms as 'os12.rom.mif', 'basic2.rom.mif' and 'dfs.rom.mif'"
	@echo "To convert roms from binary to MIF, use python/rom_to_mif or just 'make roms'"
	@echo "This expects binary ROMs in ../roms/os12.rom, basic2.rom, and dfs.rom"
	@echo "The DFS tested with is 0.9"
	@echo "The BBC micro operation uses floppy disk images as MIF files"
	@echo "Elite is included (as it is freely distributed)"
	@echo "To convert other disk images to appropriate MIF format (which includes disk track descriptors,"
	@echo "not just the data - the 'SSD' format is just 40 track, 10 265 byte sectors) use the python/disk_to_mif"
	@echo ""
	@echo "To run a regression, use 'make regression'"
	@echo ""
	@echo "To run a specific subset of the regression, use 'make SUITE=<suite> test_regress'"
	@echo "with suite being base6502, riscv_minimal, or any other .py file from the regression directory"
	@echo ""
	@echo "To run a particular RISC-V test with waves do something like:"
	@echo "make WAVES=1 SUITE=riscv_minimal.riscv_i32mc_pipeline3.test_c_arith test_regress"
	@echo "and to view its instruction trace do"
	@echo "PYTHONPATH=`pwd`/../cdl:\${DOLLAR}PYTHONPATH ./python/rv_trace.py --logfile=itrace.log"
	@echo ""
	@echo "To run the JTAG apb timer with OpenOcd (to demonstrate JTAG running remotely)"
	@echo "use 'make SUITE=jtag.jtag_apb_timer.openocd test_regress'"
	@echo "In another termina run 'openocd scripts/bitbang.cfg'"
	@echo "In a third terminal telnet in to openocd using 'telnet 127.0.0.1 4444"
	@echo "From the third terminal you should be able to see the JTAG chain in the simulation"
	@echo "and you can read the timer in the sim with 'apb_read_timer'; try 'help', and 'scan_chain'"

#a Documentation
include doc/Makefile

#a Editor preferences and notes
# Local Variables: ***
# mode: Makefile ***
# outline-regexp: "#[a!]\\\|#[\t ]*[b-z][\t ]" ***
# End: ***

