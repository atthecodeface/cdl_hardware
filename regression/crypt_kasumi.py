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
import riscv_internal

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
#c c_crypt_kasumi_test_base
class c_crypt_kasumi_test_base(simple_tb.base_th):
    verbose = False
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c c_crypt_kasumi_test_simple
class c_crypt_kasumi_test_simple(c_crypt_kasumi_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        failures = 0
        self.kasumi_input__k0.drive(0x0001020304050607)
        self.kasumi_input__k1.drive(0x08090A0B0C0D0E0F)
        self.kasumi_input__data.drive(0x664C1099C1232C0E)
        self.kasumi_input__valid.drive(1)
        self.bfm_wait(1)
        self.kasumi_input__valid.drive(0)
        self.bfm_wait(10)
        while self.kasumi_output__valid.value()==0:
            self.bfm_wait(1)
            pass
        k_d = self.kasumi_output__data.value()
        if k_d != 0x0011223344556677:
            self.failtest(0, "Mismatch in ciphertext : 0x%08x got 0x%08x" % (0x0011223344556677, k_d))
            failures += 1
        if failures==0:
            self.passtest(self.global_cycle(),"Ran all ciphertexts")
            pass
        self.finishtest(0,"")
        pass

#a Hardware classes
#c crypt_kasumi_test_hw
class crypt_kasumi_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of Kasumi cipher testbench
    """
    loggers = {#"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    kasumi_input  = pycdl.wirebundle({"data":64, "k0":64, "k1":64, "valid":1})
    kasumi_output = pycdl.wirebundle({"data":64, "valid":1})
    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(kasumi_input._name_list("kasumi_input")) + " " +
                                " kasumi_output_ack" +
                               " "),
                  "th.inputs":(" ".join(kasumi_output._name_list("kasumi_output")) + " " +
                                " kasumi_input_ack" +
                                " "),
                  }
    module_name = "tb_kasumi_cipher"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c crypt_kasumi
class crypt_kasumi(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(crypt_kasumi_test_hw(c_crypt_kasumi_test_simple()), num_cycles=500)
        pass
    pass

