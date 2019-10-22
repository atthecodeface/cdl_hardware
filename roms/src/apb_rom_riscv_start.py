#!/usr/bin/env python
import apb_rom
import clock_divider
from standard_apb_regs import *

def program(defines):
    clk = apb_rom.get_define_int(defines,"clk",100)
    brg_config = clock_divider.config_for_frequency(f=0.1152*16, clk=clk, accuracy=0.005)

    program = {}
    program["code"] = []
    program["code"] += [
                         (apb_rom.rom.op_set("address",apb_dprintf_uart_brg),),
                         (apb_rom.rom.op_req("write_arg",brg_config),),
                         #(apb_rom.rom.op_set("address",apb_uart_brg),),
                         #(apb_rom.rom.op_req("write_arg",brg_config),),
        ]
    program["code"] += [ (apb_rom.rom.op_set("address",apb_rv_sram_control),),
                         (apb_rom.rom.op_req("write_arg",1),), # Enable clock on RISC-V
                         (apb_rom.rom.op_set("address",apb_rv_debug_dmcontrol),),
                         (apb_rom.rom.op_req("write_arg",1),), # select HART 0 enable debug
                         (apb_rom.rom.op_set("address",apb_rv_debug_data0),),
                         (apb_rom.rom.op_req("write_arg",0),), # Set data0 to 0
                         (apb_rom.rom.op_set("address",apb_rv_debug_abstract_cmd),),
                         (apb_rom.rom.op_req("write_arg",0),), # set program counter to data0
                         (apb_rom.rom.op_set("address",apb_rv_debug_dmcontrol),),
                         (apb_rom.rom.op_req("write_arg",(1<<30)|1),), # Resume hart
                         ]
    program["code"] += [
        (apb_rom.rom.op_finish(),),
        ]
    return program
