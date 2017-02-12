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

#a Test classes
#c c_test_one
class c_test_one(simple_tb.base_th):
    #f apb_write
    def apb_write(self, address, data):
        self.ios.apb_request__psel.drive(1)
        self.ios.apb_request__penable.drive(0)
        self.ios.apb_request__paddr.drive(address)
        self.ios.apb_request__pwdata.drive(data)
        self.ios.apb_request__pwrite.drive(1)
        self.bfm_wait(1)
        self.ios.apb_request__penable.drive(1)
        self.bfm_wait(1)
        while self.ios.apb_response__pready.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.apb_request__psel.drive(0)
        pass
    #f apb_read
    def apb_read(self, address):
        self.ios.apb_request__psel.drive(1)
        self.ios.apb_request__penable.drive(0)
        self.ios.apb_request__paddr.drive(address)
        self.ios.apb_request__pwdata.drive(0xdeadbeef)
        self.ios.apb_request__pwrite.drive(0)
        self.bfm_wait(1)
        self.ios.apb_request__penable.drive(1)
        self.bfm_wait(1)
        while self.ios.apb_response__pready.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.apb_request__psel.drive(0)
        return self.ios.apb_response__prdata.value()
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(25)
        self.apb_write(0xfc001234,0x2)
        self.apb_write(0xab010004,0xdeedbeef)
        self.apb_write(0xfc001234,0x3)
        self.apb_write(0xab015678,0xdeedbeef)
        print "Read %08x"%self.apb_read(0xab010004)
        timers = []
        for i in range(10):
            timers.append(self.apb_read(0xab010000))
            pass
        print timers
        self.apb_write(0xab010004,timers[-1]+5*(timers[-1]-timers[-2]))
        comparators = []
        for i in range(10):
            comparators.append( (self.apb_read(0xab010004),self.apb_read(0xab010000)) )
            pass
        print comparators

        self.bfm_wait(10)
        self.finishtest(0,"")
        pass

#a Hardware classes
#c cdl_test_hw
class cdl_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of LED chain
    """
    th_forces = { "th.clock":"clk",
                  "th.inputs":("apb_response__pready "+
                               "apb_response__prdata[32] "+
                               "apb_response__perr "+
                               ""),
                  "th.outputs":("apb_request__psel "+
                                "apb_request__penable "+
                                "apb_request__pwrite "+
                                "apb_request__paddr[32] "+
                                "apb_request__pwdata[32] "+
                                ""),
                  }
    module_name = "tb_csrs"
    pass

#a Simulation test classes
#c c_Test_LedChain
class c_Test_LedChain(simple_tb.base_test):
    def test_one(self):
        test = c_test_one()
        hw = cdl_test_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass
