#!/usr/bin/env python
#a Copyright
#  
#  This file 'leds.py' copyright Gavin J Stark 2017
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
import sys, os, unittest
import simple_tb
import structs

#a Test classes
#c c_base_th
class c_base_th(simple_tb.base_th):
    config = {"filter_period":128,
              "filter_level":16,
              }
    test_input_values = ( [(128,1),
                           (128,0),
                           (32,1),
                           (32,0),

                           (256,0),
                           (2,1),
                           (2,0),
                           (32,0),
                           (2,1),
                           (2,0),
                           (32,0),
                           ] +
                          [(1<<(i/2),(i&1)) for i in range(20)] + 
                          [(1<<(i/2),(i&1)) for i in range(19,-1,-1)] + 
                          [(128,0),
                           ]+
                          []
                          )
    expectation = []
    #f bfm_tick
    def bfm_tick(self, cycles):
        for i in range(cycles):
            t = self.ios.output_value.value()
            if t != self.output_values[-1]:
                self.output_values.append(t)
                pass
            self.bfm_wait(1)
            pass
        pass
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.output_values=[self.ios.output_value.value()]
        self.ios.clk_enable.drive(1)
        self.ios.filter_level.drive(self.config["filter_level"])
        self.ios.filter_period.drive(self.config["filter_period"])
        self.bfm_wait(10)
        for (delay, value) in self.test_input_values:
            self.bfm_tick(delay)
            self.ios.input_value.drive(value)
            pass
        self.bfm_tick(1000)
        self.compare_expected_list("output changes", self.expectation, self.output_values)
        self.finishtest(0,"")
        pass
    pass

#c c_test_hysteresis_0
class c_test_hysteresis_0(c_base_th):
    config = {"filter_period":128,"filter_level":16, }
    expectation = [0,1]*7+[0]
    pass
#c c_test_hysteresis_1
class c_test_hysteresis_1(c_base_th):
    config = {"filter_period":32,"filter_level":16, }
    expectation = [0,1]*9+[0]
    pass
#c c_test_hysteresis_2
class c_test_hysteresis_2(c_base_th):
    config = {"filter_period":64,"filter_level":60, }
    expectation = [0,1]*6+[0]
    pass
#c c_test_hysteresis_3
class c_test_hysteresis_3(c_base_th):
    config = {"filter_period":16,"filter_level":30, }
    expectation = [0,1]*7+[0]
    pass
#c c_test_hysteresis_4
class c_test_hysteresis_4(c_base_th):
    config = {"filter_period":16,"filter_level":33, }
    expectation = [0,]
    pass
#c c_test_hysteresis_5
class c_test_hysteresis_5(c_base_th):
    config = {"filter_period":16,"filter_level":0, }
    expectation = [0,1]*14+[0]
    pass

#c c_test_dprintf_base
class c_test_dprintf_base(simple_tb.base_th):
    test_ctl_setting = 0
    writes_to_do = [
        ]
    expected_sram_ops = [
        ]
    #f bfm_tick
    def bfm_tick(self, cycles):
        for i in range(cycles):
            if (self.ios.dprintf_byte__valid.value()):
                if (self.ios.dprintf_byte__last.value()==0):
                    self.sram_writes.append( (self.ios.dprintf_byte__address.value(),
                                              self.ios.dprintf_byte__data.value(),) )
                pass
            self.bfm_wait(1)
            pass
        pass
    #f dprintf
    def dprintf(self, address, data):
        self.ios.dprintf_req__valid.drive(1)
        self.ios.dprintf_req__address.drive(address)
        self.ios.dprintf_req__data_0.drive(data[0])
        self.ios.dprintf_req__data_1.drive(data[1])
        self.bfm_tick(1)
        while self.ios.dprintf_ack.value()==0:
            self.bfm_tick(1)
            pass
        self.ios.dprintf_req__valid.drive(0)
        pass
    #f run
    def run(self):
        self.sram_writes = []
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.ios.test_ctl.drive(self.test_ctl_setting)
        self.bfm_wait(10)
        for (address, data) in self.writes_to_do:
            self.dprintf(address, data)
            pass
        self.bfm_tick(1000)
        if len(self.sram_writes) != len(self.expected_sram_ops):
            self.failtest(0,"Mismatch in number of SRAM writes %d/%d"%(len(self.sram_writes),len(self.expected_sram_ops)))
            for s in self.sram_writes:
                print "(0x%04x, 0x%02x),"%(s[0],s[1])
                pass
            pass
        else:
            for i in range(len(self.sram_writes)):
                if self.expected_sram_ops[i][0] != self.sram_writes[i][0]:
                    self.failtest(i,"Mismatch in SRAM %d write address %04x/%04x"%(i,self.expected_sram_ops[i][0], self.sram_writes[i][0]))
                    pass
                if self.expected_sram_ops[i][1] != self.sram_writes[i][1]:
                    self.failtest(i,"Mismatch in SRAM %d write data %02x/%02x"%(i,self.expected_sram_ops[i][1], self.sram_writes[i][1]))
                    pass
                pass
            pass
        self.passtest(self.global_cycle(),"Test passed")
        self.finishtest(0,"")
        pass

#c c_test_dprintf_one
class c_test_dprintf_one(c_test_dprintf_base):
    writes_to_do = [ (0x1234, ((0x4142434445464748,0xff00ff00ff00ff00)) ),
                     (0xfedc, ((0x4100420043004400,0x0045460047000048)) ),
                     (0xf00f, ((0x80feffffffffffff,0)) ),
                     (0xf00f, ((0x80fe81dcffffffff,0)) ),
                     (0xf00f, ((0x80fe81dc0082a9bc,0x87deadbeefff0000)) ),
                     ]
    expected_sram_ops = [(0x1234, 0x41),
                         (0x1235, 0x42),
                         (0x1236, 0x43),
                         (0x1237, 0x44),
                         (0x1238, 0x45),
                         (0x1239, 0x46),
                         (0x123a, 0x47),
                         (0x123b, 0x48),
                         (0xfedc, 0x41),
                         (0xfedd, 0x42),
                         (0xfede, 0x43),
                         (0xfedf, 0x44),
                         (0xfee0, 0x45),
                         (0xfee1, 0x46),
                         (0xfee2, 0x47),
                         (0xfee3, 0x48),

                         (0xf00f, 0x45),

                         (0xf00f, 0x45),
                         (0xf010, 0x44),
                         (0xf011, 0x43),

                         (0xf00f, 0x45),
                         (0xf010, 0x44),
                         (0xf011, 0x43),
                         (0xf012, 0x39),
                         (0xf013, 0x42),
                         (0xf014, 0x43),
                         (0xf015, 0x44),
                         (0xf016, 0x45),
                         (0xf017, 0x41),
                         (0xf018, 0x44),
                         (0xf019, 0x42),
                         (0xf01a, 0x45),
                         (0xf01b, 0x45),
                         (0xf01c, 0x46),
        ]
#c c_test_dprintf_two
class c_test_dprintf_two(c_test_dprintf_base):
    writes_to_do = [ (0x1234, ((0xc041c00041424344,0xc3ffffffff00ffff)) ),
                     ]
    expected_sram_ops = [(0x1234, 0x36),
                         (0x1235, 0x35),
                         (0x1236, 0x30),
                         (0x1237, 0x41),
                         (0x1238, 0x42),
                         (0x1239, 0x43),
                         (0x123a, 0x44),
                         (0x123b, 0x34),
                         (0x123c, 0x32),
                         (0x123d, 0x39),
                         (0x123e, 0x34),
                         (0x123f, 0x39),
                         (0x1240, 0x36),
                         (0x1241, 0x37),
                         (0x1242, 0x32),
                         (0x1243, 0x39),
                         (0x1244, 0x35),
        ]
#c c_test_dprintf_three
class c_test_dprintf_three(c_test_dprintf_base):
    writes_to_do = [ (0x1234, ((0xc001c401c801cc01,0xc000c400c800cc00)) ),
                     (0x2000, ((0xc0ffc4ffc8ffccff,0xff00c400c800cc00)) ),
                     (0x3000, ((0xc1ffff00c5ffff00,0xc9ffff00cdffffff)) ),
                     (0x3100, ((0xd1ffff00d5ffff00,0xd9ffff00ddffffff)) ),
                     (0x4000, ((0xc3ffffffffff0000,0)) ),
                     (0x4100, ((0xe7ffffffffff0000,0)) ),
                     (0x5000, ((0xc300000000ff0000,0)) ),
                     (0x5100, ((0xe700000000ff0000,0)) ),
                     ]
    expected_sram_ops = [(0x1234, 0x31),
                         (0x1235, 0x20),
                         (0x1236, 0x31),
                         (0x1237, 0x20),
                         (0x1238, 0x20),
                         (0x1239, 0x31),
                         (0x123a, 0x20),
                         (0x123b, 0x20),
                         (0x123c, 0x20),
                         (0x123d, 0x31),
                         (0x123e, 0x30),
                         (0x123f, 0x20),
                         (0x1240, 0x30),
                         (0x1241, 0x20),
                         (0x1242, 0x20),
                         (0x1243, 0x30),
                         (0x1244, 0x20),
                         (0x1245, 0x20),
                         (0x1246, 0x20),
                         (0x1247, 0x30),

                         (0x2000, 0x32),
                         (0x2001, 0x35),
                         (0x2002, 0x35),
                         (0x2003, 0x32),
                         (0x2004, 0x35),
                         (0x2005, 0x35),
                         (0x2006, 0x32),
                         (0x2007, 0x35),
                         (0x2008, 0x35),
                         (0x2009, 0x20),
                         (0x200a, 0x32),
                         (0x200b, 0x35),
                         (0x200c, 0x35),

                         (0x3000, 0x36),
                         (0x3001, 0x35),
                         (0x3002, 0x35),
                         (0x3003, 0x33),
                         (0x3004, 0x35),
                         (0x3005, 0x36),
                         (0x3006, 0x35),
                         (0x3007, 0x35),
                         (0x3008, 0x33),
                         (0x3009, 0x35),
                         (0x300a, 0x36),
                         (0x300b, 0x35),
                         (0x300c, 0x35),
                         (0x300d, 0x33),
                         (0x300e, 0x35),
                         (0x300f, 0x36),
                         (0x3010, 0x35),
                         (0x3011, 0x35),
                         (0x3012, 0x33),
                         (0x3013, 0x35),

                         (0x3100, 0x36),
                         (0x3101, 0x35),
                         (0x3102, 0x35),
                         (0x3103, 0x33),
                         (0x3104, 0x35),
                         (0x3105, 0x20),
                         (0x3106, 0x36),
                         (0x3107, 0x35),
                         (0x3108, 0x35),
                         (0x3109, 0x33),
                         (0x310a, 0x35),
                         (0x310b, 0x20),
                         (0x310c, 0x20),
                         (0x310d, 0x36),
                         (0x310e, 0x35),
                         (0x310f, 0x35),
                         (0x3110, 0x33),
                         (0x3111, 0x35),
                         (0x3112, 0x20),
                         (0x3113, 0x20),
                         (0x3114, 0x20),
                         (0x3115, 0x36),
                         (0x3116, 0x35),
                         (0x3117, 0x35),
                         (0x3118, 0x33),
                         (0x3119, 0x35),

                         (0x4000, 0x34),
                         (0x4001, 0x32),
                         (0x4002, 0x39),
                         (0x4003, 0x34),
                         (0x4004, 0x39),
                         (0x4005, 0x36),
                         (0x4006, 0x37),
                         (0x4007, 0x32),
                         (0x4008, 0x39),
                         (0x4009, 0x35),

                         (0x4100, 0x34),
                         (0x4101, 0x32),
                         (0x4102, 0x39),
                         (0x4103, 0x34),
                         (0x4104, 0x39),
                         (0x4105, 0x36),
                         (0x4106, 0x37),
                         (0x4107, 0x32),
                         (0x4108, 0x39),
                         (0x4109, 0x35),

                         (0x5000, 0x30),
                         (0x5100, 0x20),
                         (0x5101, 0x20),
                         (0x5102, 0x20),
                         (0x5103, 0x20),
                         (0x5104, 0x20),
                         (0x5105, 0x20),
                         (0x5106, 0x20),
                         (0x5107, 0x20),
                         (0x5108, 0x20),
                         (0x5109, 0x30),

        ]
#c c_test_dprintf_four
class c_test_dprintf_four(c_test_dprintf_three):
    test_ctl_setting = 1

#c c_test_dprintf_five
class c_test_dprintf_five(c_test_dprintf_three):
    test_ctl_setting = 2

#c c_test_dprintf_mux_one
class c_test_dprintf_mux_one(simple_tb.base_th):
    sram_reqs = {0:[(0x1010, 0x41),
                    (0x1011, 0x42),
                    (0x1012, 0x43),
                    (0x1013, 0x44),
                    (0x1014, 0x45),
                    (0x1015, 0x46),
                    (0x1016, 0x47),
                    (0x1017, 0x48),
                    (0x1018, 0x44),
                    (0x1019, 0x45),
                    (0x101a, 0x41),
                    (0x101b, 0x44),
                    (0x101c, 0x42),
                    (0x101d, 0x45),
                    (0x101e, 0x45),
                    (0x101f, 0x46),
                    ],
                 1:[(0x2010, 0x20),],
                 2:[(0x3010, 0x22),
                    ],
                 3:[(0x4010, 0x33),
                    (0x4011, 0x34),
                    (0x4012, 0x35),
                    ],
                 }
    requests = {50:(1,),
                52:(0,),
                80:(0,1,),
                90:(0,1,2,3),
                180:(0,1,2,3),
                240:(3,),
                300:(0,1),
                301:(2,),
                302:(3,),
                }
    responses = [1,0,1,0,3,2,1,0,
                 3,2,1,0,
                 3,
                 2,3,1,0,]
    expected_sram_ops = []
    for i in responses:
        expected_sram_ops.extend(sram_reqs[i])
        pass
    #f bfm_tick
    def bfm_tick(self, cycles):
        for i in range(cycles):
            acks = self.ios.acks.value()
            if acks!=0:
                if (acks &~ self.current_reqs)!=0:
                    self.failtest(0,"Ack of unrequested data %d/%d"%(acks, self.current_reqs))
                    pass
                self.current_reqs = self.current_reqs &~ acks
                self.ios.reqs.drive(self.current_reqs)
                pass
            if self.tick in self.requests:
                for j in self.requests[self.tick]:
                    self.current_reqs = self.current_reqs | (1<<j)
                    pass
                self.ios.reqs.drive(self.current_reqs)
                pass
            self.tick = self.tick + 1
            if (self.ios.dprintf_byte__valid.value()):
                if (self.ios.dprintf_byte__last.value()==0):
                    self.sram_writes.append( (self.ios.dprintf_byte__address.value(),
                                              self.ios.dprintf_byte__data.value(),) )
                    pass
                pass
            self.bfm_wait(1)
            pass
        pass
    #f run
    def run(self):
        self.sram_writes = []
        self.tick = 0
        self.current_reqs = 0
        simple_tb.base_th.run_start(self)
        self.ios.reqs.drive(0)
        self.bfm_wait(10)
        self.bfm_tick(10000)
        if len(self.sram_writes) != len(self.expected_sram_ops):
            self.failtest(0,"Mismatch in number of SRAM writes %d/%d"%(len(self.sram_writes),len(self.expected_sram_ops)))
            for s in self.sram_writes:
                print "(0x%04x, 0x%02x),"%(s[0],s[1])
                pass
            pass
        else:
            for i in range(len(self.sram_writes)):
                if self.expected_sram_ops[i][0] != self.sram_writes[i][0]:
                    self.failtest(i,"Mismatch in SRAM %d write address %04x/%04x"%(i,self.expected_sram_ops[i][0], self.sram_writes[i][0]))
                    pass
                if self.expected_sram_ops[i][1] != self.sram_writes[i][1]:
                    self.failtest(i,"Mismatch in SRAM %d write data %02x/%02x"%(i,self.expected_sram_ops[i][1], self.sram_writes[i][1]))
                    pass
                pass
            pass
        self.finishtest(0,"")
        pass

#a Hardware classes
#c hysteresis_switch_hw
class hysteresis_switch_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of APB ROM processor with a timer and GPIO
    """
    th_forces = { "th.clock":"clk",
                  "th.inputs":("output_value "+
                               ""),
                  "th.outputs":("clk_enable "+
                                "input_value "+
                                "filter_period[16] "+
                                "filter_level[16] "+
                                ""),
                  }
    module_name = "tb_hysteresis_switch"
    pass

#c teletext_dprintf_hw
class teletext_dprintf_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of the teletext dprintf module
    """
    dprintf_req_4  = pycdl.wirebundle(structs.dprintf_req_4)
    dprintf_byte   = pycdl.wirebundle(structs.dprintf_byte)
    clocks = { "clk":(0,None,None),
               "clk_async":(0,7,13)
    }               
    th_forces = { "th.clock":"clk",
                  "th.inputs":" ".join( dprintf_byte._name_list("dprintf_byte") +
                                ["dprintf_ack"]
                               ),
                  "th.outputs": " ".join( dprintf_req_4._name_list("dprintf_req") +
                                          ["test_ctl[4]"]
                               ),
                  }
    module_name = "tb_dprintf"
    pass

#c teletext_dprintf_mux_hw
class teletext_dprintf_mux_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of the teletext dprintf mux module
    """
    dprintf_byte   = pycdl.wirebundle(structs.dprintf_byte)
    th_forces = { "th.clock":"clk",
                  "th.inputs":" ".join( dprintf_byte._name_list("dprintf_byte") +
                                ["acks[4]"]
                               ),
                  "th.outputs":("" +
                                "reqs[4] "+
                                ""),
                  }
    module_name = "tb_dprintf_mux"
    pass

#a Simulation test classes
#c hysteresis_switch
class hysteresis_switch(simple_tb.base_test):
    def hysteresis(self,test,num_cycles):
        hw = hysteresis_switch_hw(test=test)
        self.do_test_run(hw, num_cycles=num_cycles)
        pass
    def test_hysteresis_0(self): self.hysteresis(c_test_hysteresis_0(),100*1000)
    def test_hysteresis_1(self): self.hysteresis(c_test_hysteresis_1(),100*1000)
    def test_hysteresis_2(self): self.hysteresis(c_test_hysteresis_2(),100*1000)
    def test_hysteresis_3(self): self.hysteresis(c_test_hysteresis_3(),100*1000)
    def test_hysteresis_4(self): self.hysteresis(c_test_hysteresis_4(),100*1000)
    def test_hysteresis_5(self): self.hysteresis(c_test_hysteresis_5(),100*1000)
    pass
#c dprintf
class dprintf(simple_tb.base_test):
    def test_one(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_one()), num_cycles=10*1000)
    def test_two(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_two()), num_cycles=10*1000)
    def test_three(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_three()), num_cycles=10*1000)
    def test_four(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_four()), num_cycles=10*1000)
    def test_five(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_five()), num_cycles=10*1000)
    pass
#c dprintf_mux
class dprintf_mux(simple_tb.base_test):
    def test_one(self):
        test = c_test_dprintf_mux_one()
        hw = teletext_dprintf_mux_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass
