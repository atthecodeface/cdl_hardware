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
riscv_regression_dir      = "../riscv_tests_built/isa/"
riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"

#a Test classes
#c c_jtag_apb_time_test_base
class c_jtag_apb_time_test_base(simple_tb.base_th):
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

#c c_jtag_apb_time_test
class c_jtag_apb_time_test(c_jtag_apb_time_test_base):
    def __init__(self, **kwargs):
        c_jtag_apb_time_test_base.__init__(self, **kwargs)
        pass
    pass

#a Hardware classes
#c jtag_apb_timer_hw
class jtag_apb_timer_hw(simple_tb.cdl_test_hw):
    """
    
    """
    loggers = {#"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("tdo"),
                  "th.outputs":("jtag__ntrst jtag__tms jtag__tdi" ),
                  }
    module_name = "tb_jtag_apb_timer"
    clocks = {"jtag_tck":(0,3,3),
              "apb_clock":(0,2,2),
              }
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c jtag_apb_timer
class jtag_apb_timer(simple_tb.base_test):
    pass


#c Add tests to riscv_minimal and riscv_minimal_single_memory
test_dir = ""
tests = {         "sltu":("rv32ui-p-sltu.dump",3*1000),
           }
for tc in tests:
    (tf,num_cycles) = tests[tc]
    tf = test_dir+tf
    def test_fn(c, tf=tf, num_cycles=num_cycles):
        test = c_jtag_apb_time_test()
        hw = jtag_apb_timer_hw(test)
        c.do_test_run(hw, num_cycles=num_cycles)
        pass
    setattr(jtag_apb_timer, "test_"+tc, test_fn)
    pass
pass
