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
import structs

#a Useful functions
def int_of_bits(bits):
    l = len(bits)
    m = 1<<(l-1)
    v = 0
    for b in bits:
        v = (v>>1) | (m*b)
        pass
    return v

def bits_of_n(nbits, n):
    bits = []
    for i in range(nbits):
        bits.append(n&1)
        n >>= 1
        pass
    return bits

def signed32(n):
    if (n>>31)&1:
        n = (((-1) &~ 0x7fffffff) | n)
        pass
    return n

#a Globals
riscv_regression_dir      = "../riscv_tests_built/isa/"
riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"

#a Test classes
#c c_clocking_phase_measure_test_base
class c_clocking_phase_measure_test_base(simple_tb.base_th):
    verbose = False
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c c_clocking_phase_measure_test_base
class c_clocking_phase_measure_test_0(c_clocking_phase_measure_test_base):
    def wait_for_delay(self):
        toggle = 0
        if self.delay in self.stable_values:
            self.sync_value = self.stable_values[self.delay]
        else:
            toggle = 1
            pass
        while not self.delay_config__load.value():
            self.sync_value = self.sync_value ^ toggle
            self.delay_response__sync_value.drive(self.sync_value)
            if self.measure_response__valid.value():
                return True
            self.bfm_wait(1)
            pass
        self.measure_request__valid.drive(0)
        self.delay_response__load_ack.drive(1)
        self.bfm_wait(1)
        self.delay_response__load_ack.drive(0)
        self.bfm_wait(4)
        self.delay = self.delay_config__value.value()
        return False
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        self.stable_values = {0:0,1:0,2:0,
                              31:1,32:1,33:1,34:1,35:1,
                              66:0,67:0,68:0,69:0,70:0,
                              101:1,102:1,103:1,104:1}
        self.delay = 0
        self.sync_value = 0
        failures = 0
        self.measure_request__valid.drive(1)
        self.wait_for_delay()
        self.measure_request__valid.drive(0)
        while True:
            if self.wait_for_delay():
                break
            pass

        result = { "initial_value":self.measure_response__initial_value.value(),
                   "initial_delay":self.measure_response__initial_delay.value(),
                   "delay":self.measure_response__delay.value(),
                   }
        self.compare_expected("initial value", 1,  result["initial_value"])
        self.compare_expected("initial delay", 31, result["initial_delay"])
        self.compare_expected("delay",         35, result["delay"])
        self.bfm_wait(10)
        self.measure_request__valid.drive(1)
        if failures==0:
            self.passtest(self.global_cycle(),"Ran okay")
            pass
        else:
            self.failtest(self.global_cycle(),"Failed")
            pass
        self.finishtest(0,"")
        pass

#a Hardware classes
#c clocking_test_hw
class clocking_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of clocking testbench
    """
    loggers = {#"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    bit_delay_config        = pycdl.wirebundle(structs.bit_delay_config)
    bit_delay_response      = pycdl.wirebundle(structs.bit_delay_response)
    phase_measure_request   = pycdl.wirebundle(structs.phase_measure_request)
    phase_measure_response  = pycdl.wirebundle(structs.phase_measure_response)
    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(phase_measure_request._name_list("measure_request")) + " " +
                                " ".join(bit_delay_response._name_list("delay_response")) + " " +
                                " "),
                  "th.inputs":(" ".join(phase_measure_response._name_list("measure_response")) + " " +
                               " ".join(bit_delay_config._name_list("delay_config")) + " " +
                               " "),
                  }
    module_name = "tb_clocking"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c clocking_phase_measure
class clocking_phase_measure(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(clocking_test_hw(c_clocking_phase_measure_test_0()), num_cycles=10000)
        pass
    pass

