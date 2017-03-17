#!/usr/bin/env python
#a Copyright
#  
#  This file 'riscv_minimal.py' copyright Gavin J Stark 2017
#  
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, version 2.0.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#  for more details.

#a Imports
import pycdl
import sys, os, unittest, tempfile
import simple_tb
import dump

#a Globals
riscv_regression_dir = "../riscv_tests_built/isa/"

#a Test classes
#c c_riscv_minimal_test_base
class c_riscv_minimal_test_base(simple_tb.base_th):
    mif_filename = None
    dump_filename = None
    base_address = 0
    test_memory = "dmem"
    memory_expectation = {}
    #f get_image
    def get_image(self):
        self.mif = None
        self.test_image = dump.c_dump()
        if self.mif_filename is not None:
            f = open(self.mif_filename)
            self.test_image.load_mif(f, self.base_address)
            f.close()
            return self.mif_filename
        f = open(self.dump_filename)
        self.test_image.load(f, self.base_address)
        f.close()
        self.mif = tempfile.NamedTemporaryFile(mode='w')
        self.test_image.write_mif(self.mif)
        self.mif.flush()
        return self.mif.name
    #f release_image
    def release_image(self):
        if self.mif is not None:
            self.mif.close()
            self.mif = None
            pass
        del self.test_image
        pass
    #f read_memory
    def read_memory(self,memory,address):
        """
        memory should be 'imem' or 'dmem' or 'mem'
        address is word address
        """
        self.sim_msg.send_value("dut."+memory,8,0,address)
        return self.sim_msg.get_value(2)
    #f write_memory
    def write_memory(self,memory,address,data):
        """
        memory should be 'imem' or 'dmem'
        address is word address
        data is data to write
        """
        self.sim_msg.send_value("dut."+memory,9,0,address,data)
        pass
    #f check_memory
    def check_memory(self, reason):
        for a in self.memory_expectation:
            e = self.memory_expectation[a]
            address = a
            if type(a)==str:
                address = self.test_image.resolve_label(a)
                pass
            d = []
            for i in range(len(e)):
                d.append(self.read_memory(self.test_memory,address/4+i))
                pass
            self.compare_expected_list(reason+":"+str(a), e, d)
            pass
        pass
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        #self.ios.b.drive(1)
        self.check_memory("Check memory after run complete (%d)"%self.global_cycle())
        self.finishtest(0,"")
        pass

#c c_riscv_minimal_test_dump
class c_riscv_minimal_test_dump(c_riscv_minimal_test_base):
    dump_filename = riscv_regression_dir+"rv32ui-p-or.dump"
    base_address = 0x80000000
    memory_expectation = { "tohost":(1337,),
                           }
    def __init__(self, dump_filename, test_memory="dmem", **kwargs):
        self.dump_filename = dump_filename
        self.test_memory = test_memory
        c_riscv_minimal_test_base.__init__(self, **kwargs)
        pass
    pass

#c c_riscv_minimal_test_one
class c_riscv_minimal_test_one(c_riscv_minimal_test_base):
    dump_filename = riscv_regression_dir+"rv32ui-p-or.dump"
    base_address = 0x80000000
    memory_expectation = { "tohost":(1337,),
                           }
    pass

#a Hardware classes
#c riscv_minimal_test_hw
class riscv_minimal_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("a"),
                  "th.outputs":("b"),
                  }
    module_name = "tb_riscv_minimal"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["imem.filename"] = mif_filename
        self.th_forces["dmem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c riscv_minimal_single_memory_test_hw
class riscv_minimal_single_memory_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("a"),
                  "th.outputs":("b"),
                  }
    module_name = "tb_riscv_minimal_single_memory"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["mem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c riscv_minimal
class riscv_minimal(simple_tb.base_test):
    pass

#c riscv_minimal_single_memory
class riscv_minimal_single_memory(simple_tb.base_test):
    pass

#c Add tests to riscv_minimal and riscv_minimal_single_memory
tests = {"or":("rv32ui-p-or.dump",3*1000),
         "simple":("rv32ui-p-simple.dump",3*1000),
         "jalr":("rv32ui-p-jalr.dump",3*1000),
         "jal":("rv32ui-p-jal.dump",3*1000),
         "fence_i":("rv32ui-p-fence_i.dump",3*1000), #Note that Fence does not work on the riscv_minimal as that does not have writable instruction memory
         "bne":("rv32ui-p-bne.dump",3*1000),
         "bltu":("rv32ui-p-bltu.dump",3*1000),
         "blt":("rv32ui-p-blt.dump",3*1000),
         "bgeu":("rv32ui-p-bgeu.dump",3*1000),
         "bge":("rv32ui-p-bge.dump",3*1000),
         "beq":("rv32ui-p-beq.dump",3*1000),
         "auipc":("rv32ui-p-auipc.dump",3*1000),
         "andi":("rv32ui-p-andi.dump",3*1000),
         "and":("rv32ui-p-and.dump",3*1000),
         "addi":("rv32ui-p-addi.dump",3*1000),
         "add":("rv32ui-p-add.dump",3*1000),
         "sw":("rv32ui-p-sw.dump",3*1000),
         "sltiu":("rv32ui-p-sltiu.dump",3*1000),
         "slti":("rv32ui-p-slti.dump",3*1000),
         "slt":("rv32ui-p-slt.dump",3*1000),
         "slli":("rv32ui-p-slli.dump",3*1000),
         "sll":("rv32ui-p-sll.dump",3*1000),
         "sh":("rv32ui-p-sh.dump",3*1000),
         "sb":("rv32ui-p-sb.dump",3*1000),
         "ori":("rv32ui-p-ori.dump",3*1000),
         "or":("rv32ui-p-or.dump",3*1000),
         "lw":("rv32ui-p-lw.dump",3*1000),
         "lui":("rv32ui-p-lui.dump",3*1000),
         "lhu":("rv32ui-p-lhu.dump",3*1000),
         "lh":("rv32ui-p-lh.dump",3*1000),
         "lbu":("rv32ui-p-lbu.dump",3*1000),
         "lb":("rv32ui-p-lb.dump",3*1000),
         "xori":("rv32ui-p-xori.dump",3*1000),
         "xor":("rv32ui-p-xor.dump",3*1000),
         "sub":("rv32ui-p-sub.dump",3*1000),
         "srli":("rv32ui-p-srli.dump",3*1000),
         "srl":("rv32ui-p-srl.dump",3*1000),
         "srai":("rv32ui-p-srai.dump",3*1000),
         "sra":("rv32ui-p-sra.dump",3*1000),
         "sltu":("rv32ui-p-sltu.dump",3*1000),
           }
for tc in tests:
    (tf,num_cycles) = tests[tc]
    tf = riscv_regression_dir+tf
    def test_fn(c, tf=tf, num_cycles=num_cycles):
        c.do_test_run(riscv_minimal_test_hw(c_riscv_minimal_test_dump(dump_filename=tf)), num_cycles=num_cycles)
        pass
    def test_smem_fn(c, tf=tf, num_cycles=num_cycles):
        c.do_test_run(riscv_minimal_single_memory_test_hw(c_riscv_minimal_test_dump(dump_filename=tf,test_memory="mem")), num_cycles=num_cycles)
        pass
    if tc not in ["fence_i"]:
        setattr(riscv_minimal,               "test_"+tc, test_fn)
    setattr(riscv_minimal_single_memory, "test_"+tc, test_smem_fn)
    pass
