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
import encdec_8b10b

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
#c eth_8b10b_test_base
class eth_8b10b_test_base(simple_tb.base_th):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c eth_8b10b_test_encode
class eth_8b10b_test_encode(eth_8b10b_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        for e in encdec_8b10b.encodings_8b10b:
            self.enc_data__data.drive(e.data)
            self.enc_data__is_control.drive(e.is_control)
            self.enc_data__disparity.drive(e.disparity_in)
            self.bfm_wait(2)
            dut_disparity_out = self.enc_symbol__disparity_positive.value()
            dut_encoding      = self.enc_symbol__symbol.value()
            self.compare_expected("Encoding of symbol %s"%(str(e)),e.encoding,dut_encoding)
            self.compare_expected("Disparity out of symbol %s"%(str(e)),e.disparity_out,dut_disparity_out)
            pass
        self.bfm_wait(self.run_time_remaining())
        self.finishtest(0,"")
        pass

#c eth_8b10b_test_decode_0
class eth_8b10b_test_decode_0(eth_8b10b_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        for e in encdec_8b10b.encodings_8b10b:
            self.enc_data__data.drive(e.data)
            self.enc_data__is_control.drive(e.is_control)
            self.enc_data__disparity.drive(e.disparity_in)
            self.bfm_wait(2)
            dut_disparity_out = self.enc_symbol__disparity_positive.value()
            dut_encoding      = self.enc_symbol__symbol.value()
            self.dec_symbol__disparity_positive.drive(e.disparity_in)
            self.dec_symbol__symbol.drive(dut_encoding)
            self.bfm_wait(2)
            dut_valid = self.dec_data__valid.value()
            dut_data = self.dec_data__data.value()
            dut_is_control = self.dec_data__is_control.value()
            dut_is_data = self.dec_data__is_data.value()
            dut_disparity_out = self.dec_data__disparity_positive.value()
            self.compare_expected("Decoding of symbol %s valid"%(str(e)),1,dut_valid)
            self.compare_expected("Data of symbol %s"%(str(e)),e.data,dut_data)
            self.compare_expected("Is control of symbol %s"%(str(e)),e.is_control,dut_is_control)
            self.compare_expected("Is data of symbol %s"%(str(e)),1^e.is_control,dut_is_data)
            self.compare_expected("Disparity out of symbol %s"%(str(e)),e.disparity_out,dut_disparity_out)
            pass
        self.bfm_wait(self.run_time_remaining())
        self.enc_data__data.drive(0)
        self.bfm_wait(1)
        self.finishtest(0,"")
        pass

#c eth_8b10b_test_decode_1
class eth_8b10b_test_decode_1(eth_8b10b_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        for symbol in range(1024):
            for disp in range(2):
                e = encdec_8b10b.find_encoding(encdec_8b10b.encodings_8b10b, {"encoding":symbol, "disparity_in":disp})
                self.dec_symbol__disparity_positive.drive(disp)
                self.dec_symbol__symbol.drive(symbol)
                self.bfm_wait(2)
                dut_valid = self.dec_data__valid.value()
                dut_data = self.dec_data__data.value()
                dut_is_control = self.dec_data__is_control.value()
                dut_is_data = self.dec_data__is_data.value()
                dut_disparity_out = self.dec_data__disparity_positive.value()
                if e is None:
                    self.compare_expected("Decoding of code %03d should be invalid"%(symbol),0,dut_valid)
                    pass
                else:
                    self.compare_expected("Decoding of code %s valid"%(str(e)),1,dut_valid)
                    self.compare_expected("Data of symbol %s"%(str(e)),e.data,dut_data)
                    self.compare_expected("Is control of symbol %s"%(str(e)),e.is_control,dut_is_control)
                    self.compare_expected("Is data of symbol %s"%(str(e)),1^e.is_control,dut_is_data)
                    self.compare_expected("Disparity out of symbol %s"%(str(e)),e.disparity_out,dut_disparity_out)
                    pass
                pass
            pass
        self.bfm_wait(self.run_time_remaining())
        self.enc_data__data.drive(0)
        self.bfm_wait(1)
        self.finishtest(0,"")
        pass

#c sgmii_test_base
class sgmii_test_base(simple_tb.base_th):
    verbose = False
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
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c sgmii_test_0
class sgmii_test_0(sgmii_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        self.bfm_wait(100)
        self.sgmii_gasket_control__write_config.drive(1)
        self.sgmii_gasket_control__write_address.drive(0)
        self.sgmii_gasket_control__write_data.drive(100)
        self.bfm_wait(1)
        self.sgmii_gasket_control__write_config.drive(0)
        self.bfm_wait(10)

        self.sgmii_gasket_control__write_config.drive(1)
        self.sgmii_gasket_control__write_address.drive(2)
        self.sgmii_gasket_control__write_data.drive(1)
        self.bfm_wait(1)
        self.sgmii_gasket_control__write_config.drive(0)
        self.bfm_wait(10)

        self.bfm_wait(100)

        self.sgmii_gasket_control__write_config.drive(1)
        self.sgmii_gasket_control__write_address.drive(1)
        self.sgmii_gasket_control__write_data.drive(0x20)
        self.bfm_wait(1)
        self.sgmii_gasket_control__write_config.drive(0)
        self.bfm_wait(10)

        self.bfm_wait(1000)
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

#c gbe_test_base
class gbe_test_base(simple_tb.base_th):
    verbose = False
    #f run_init
    def run_init(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        self.rx_timer_control__integer_adder.drive(1)
        self.rx_timer_control__fractional_adder.drive(0)
        self.rx_timer_control__bonus_subfraction_add.drive(0)
        self.rx_timer_control__bonus_subfraction_sub.drive(0)
        self.bfm_wait(1)
        self.rx_timer_control__reset_counter.drive(1)
        self.bfm_wait(1)
        self.rx_timer_control__reset_counter.drive(0)
        self.bfm_wait(1)
        self.rx_timer_control__enable_counter.drive(1)
    #f run
    def run(self):
        self.run_init()
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c gbe_test_0
class gbe_test_0(gbe_test_base):
    #f run
    def run(self):
        # FCS: 7A D5 6B B3
        pkt = [ (0xF0E60A00,0xf,0),
                (0x1200A305,0xf,0),
                (0x90785634,0xf,0),
                (0x00450008,0xf,0),
                (0xFEB33000,0xf,0),
                (0x11800000,0xf,0),
                (0x000ABA72,0xf,0),
                (0x000A0300,0xf,0),
                (0x00040200,0xf,0),
                (0x1C000004,0xf,0),
                (0x01004D89,0xf,0),
                (0x05040302,0xf,0),
                (0x09080706,0xf,0),
                (0x09080706,0xf,0),
                (0x0D0C0B0A,0xf,0),
                (0x11100F0E,0xf,0),
                (0x00001312,0x3,1),
                ]
        self.run_init()
        self.axi_bfm.axi4s("axi4s")
        self.axi4s.set("strb",0xf)
        self.axi4s.set("keep",0xf)
        self.axi4s.set("user",0)
        self.axi4s.set("id",0)
        self.axi4s.set("dest",0)
        self.axi4s.set("last",0)
        
        for i in range(2):
            for (d,s,l) in pkt:
                self.axi4s.set("data",d)
                self.axi4s.set("strb",s)
                self.axi4s.set("last",l)
                self.axi4s.master_enqueue()
                pass
            self.bfm_wait(100)
            pass
            self.sys_cfg.drive(i)
        self.bfm_wait(100)
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
#c eth_8b10b_test_hw
class eth_8b10b_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of tb_8b10b
    """
    dec_8b10b_data = pycdl.wirebundle(structs.dec_8b10b_data)
    symbol_8b10b   = pycdl.wirebundle(structs.symbol_8b10b)
    enc_8b10b_data = pycdl.wirebundle(structs.enc_8b10b_data)
    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(symbol_8b10b._name_list("dec_symbol")) + " " +
                                " ".join(enc_8b10b_data._name_list("enc_data")) + " " +
                                " "),
                  "th.inputs":(" ".join(dec_8b10b_data._name_list("dec_data")) + " " +
                               " ".join(symbol_8b10b._name_list("enc_symbol")) + " " +
                               " "),
                  }
    module_name = "tb_8b10b"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

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
    sgmii_gasket_control    = pycdl.wirebundle(structs.sgmii_gasket_control)
    sgmii_gasket_status     = pycdl.wirebundle(structs.sgmii_gasket_status)

    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(gmii_tx._name_list("gmii_tx")) + " " +
                                " ".join(tbi_valid._name_list("tbi_rx")) + " " +
                                " ".join(sgmii_gasket_control._name_list("sgmii_gasket_control")) + " " +
                                " sgmii_rxd[4]"+
                                " "),
                  "th.inputs":(" ".join(tbi_valid._name_list("tbi_tx")) + " " +
                               " ".join(gmii_rx._name_list("gmii_rx")) + " " +
                                " ".join(sgmii_gasket_status._name_list("sgmii_gasket_status")) + " " +
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

#c gbe_test_hw
class gbe_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of tb_sgmii
    """
    loggers = {"gmii_sgmii": {"verbose":0, "filename":"gmii_sgmii.log", "modules":("dut.sgg "),},
               }
    timer_control           = pycdl.wirebundle(structs.timer_control)
    tbi_valid               = pycdl.wirebundle(structs.tbi_valid)
    gmii_tx                 = pycdl.wirebundle(structs.gmii_tx)
    gmii_rx                 = pycdl.wirebundle(structs.gmii_rx)
    sgmii_gasket_control    = pycdl.wirebundle(structs.sgmii_gasket_control)
    sgmii_gasket_status     = pycdl.wirebundle(structs.sgmii_gasket_status)

    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(timer_control._name_list("rx_timer_control")) + " " +
                                " ".join(tbi_valid._name_list("tbi_rx")) + " " +
                                " ".join(sgmii_gasket_control._name_list("sgmii_gasket_control")) + " " +
                                " sgmii_rxd[4]"+
                                " sys_cfg[32]"+
                                " "),
                  "th.inputs":(" ".join(tbi_valid._name_list("tbi_tx")) + " " +
                                " ".join(sgmii_gasket_status._name_list("sgmii_gasket_status")) + " " +
                               " sgmii_txd[4]"+
                               " "),
                  }
    module_name = "tb_gbe"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c eth_8b10b
class eth_8b10b(simple_tb.base_test):
    def test_encode(self):
        self.do_test_run(eth_8b10b_test_hw(eth_8b10b_test_encode()), num_cycles=10000)
        pass
    def test_decode_0(self):
        self.do_test_run(eth_8b10b_test_hw(eth_8b10b_test_decode_0()), num_cycles=10000)
        pass
    def test_decode_1(self):
        self.do_test_run(eth_8b10b_test_hw(eth_8b10b_test_decode_1()), num_cycles=20*1000)
        pass
    pass
#c sgmii
class sgmii(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(sgmii_test_hw(sgmii_test_0()), num_cycles=10000)
        pass
    pass

#c gbe
class gbe(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(gbe_test_hw(gbe_test_0()), num_cycles=10000)
        pass
    pass
