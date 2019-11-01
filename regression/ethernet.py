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
import math

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
#c sgmii_test_base
class sgmii_test_base(simple_tb.base_th):
    verbose = False
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c sgmii_test_0
class sgmii_test_0(sgmii_test_base):
    #f gmii_bfm_wait
    def gmii_bfm_wait(self, delay):
        for i in range(delay):
            self.bfm_wait(1)
            while self.gmii_tx_enable.value()==0:
                self.bfm_wait(1)
                pass
            pass
        pass
    #f send_packet
    def send_packet(self, pkt):
        self.gmii_tx__tx_en.drive(1)
        self.gmii_tx__tx_er.drive(0)
        self.gmii_tx__txd.drive(0x55)
        self.gmii_bfm_wait(7)
        self.gmii_tx__txd.drive(0xd5)
        self.gmii_bfm_wait(1)
        for p in pkt:
            self.gmii_tx__txd.drive(p)
            self.gmii_bfm_wait(1)
            pass
        self.gmii_tx__tx_en.drive(0)
        self.gmii_tx__tx_er.drive(0)
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        for i in range(10):
            self.send_packet([0,1,2,3,4,5,6,7])
            self.gmii_bfm_wait(i+1)
            pass
        for i in range(10,1,-1):
            self.send_packet([0,1,2,3,4,5,6,7])
            self.gmii_bfm_wait(i+1)
            pass
        for i in range(5):
            self.send_packet([0,1,2,3,4,5,6,7])
            self.gmii_bfm_wait(1)
            pass
        self.gmii_bfm_wait(30)
                      
        failures = 0
        if failures==0:
            self.passtest(self.global_cycle(),"Ran okay")
            pass
        else:
            self.failtest(self.global_cycle(),"Failed")
            pass
        self.finishtest(0,"")
        pass

#a Hardware classes
#c sgmii_test_hw
class sgmii_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of tb_sgmii
    """
    loggers = {#"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    tbi_valid               = pycdl.wirebundle(structs.tbi_valid)
    gmii_tx                 = pycdl.wirebundle(structs.gmii_tx)
    gmii_rx                 = pycdl.wirebundle(structs.gmii_rx)

    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(gmii_tx._name_list("gmii_tx")) + " " +
                                " ".join(tbi_valid._name_list("tbi_rx")) + " " +
                                " sgmii_rxd[4]"+
                                " "),
                  "th.inputs":(" ".join(tbi_valid._name_list("tbi_tx")) + " " +
                               " ".join(gmii_rx._name_list("gmii_rx")) + " " +
                               " gmii_tx_enable"+
                               " sgmii_txd[4]"+
                               " "),
                  }
    module_name = "tb_sgmii"
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
        self.do_test_run(sgmii_test_hw(sgmii_test_0()), num_cycles=10000)
        pass
    pass
