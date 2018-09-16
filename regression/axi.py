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
import apb_rom
import simple_tb

#a Test classes
#c c_rom_th
class c_rom_th(simple_tb.base_th, apb_rom.rom):
    pass

#c c_axi_test_base
class c_axi_test_base(simple_tb.base_th):
    #f simple_write
    def simple_write(self, address, data, req_id=0, size=32, byte_enables=None, wait_fn=None):
        if byte_enables is None:
            byte_enables = 1<<(address & 3)
            if size==32: byte_enables=0xff
            if size==64: byte_enables=0xffff
            pass
        axi_size = {1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 64:6, 128:7}[size]
        if wait_fn is None:
            wait_fn = lambda: self.bfm_wait(10)
        self.axi_wreq.set("id",     req_id)
        self.axi_wreq.set("addr",   address)
        self.axi_wreq.set("len",    0)
        self.axi_wreq.set("size",   axi_size)
        self.axi_wreq.set("burst",  0)
        self.axi_wreq.set("lock",   0)
        self.axi_wreq.set("cache",  0)
        self.axi_wreq.set("prot",   0)
        self.axi_wreq.set("qos",    0)
        self.axi_wreq.set("region", 0)
        self.axi_wreq.set("user", 0)
        self.axi_wdata.set("id",    req_id+1)
        self.axi_wdata.set("data",  data)
        self.axi_wdata.set("strb",  byte_enables)
        self.axi_wdata.set("last",  1)
        self.axi_wdata.set("user",  0)

        self.axi_wreq.enqueue_write()
        self.axi_wdata.enqueue()
        while self.axi_wresp.empty():
            wait_fn()
            pass
        self.axi_wresp.dequeue()
        return self.axi_wresp.get("resp")
    #f simple_read
    def simple_read(self, address, req_id=0, size=32, wait_fn=None):
        axi_size = {1:0, 2:1, 4:2, 8:3, 16:4, 32:5, 64:6, 128:7}[size]
        if wait_fn is None:
            wait_fn = lambda: self.bfm_wait(10)
        self.axi_rreq.set("id",     req_id)
        self.axi_rreq.set("addr",   address)
        self.axi_rreq.set("len",    0)
        self.axi_rreq.set("size",   axi_size)
        self.axi_rreq.set("burst",  0)
        self.axi_rreq.set("lock",   0)
        self.axi_rreq.set("cache",  0)
        self.axi_rreq.set("prot",   0)
        self.axi_rreq.set("qos",    0)
        self.axi_rreq.set("region", 0)
        self.axi_rreq.set("user", 0)

        self.axi_rreq.enqueue_read()
        while self.axi_rresp.empty():
            wait_fn()
            pass
        self.axi_rresp.dequeue()
        return (self.axi_rresp.get("resp"), self.axi_rresp.get("data"))
    #f run_start
    def run_start(self):
        simple_tb.base_th.run_start(self)
        self.sim_msg = self.sim_message()
        self.axi_bfm.axi_request("axi_wreq")
        self.axi_bfm.axi_request("axi_rreq")
        self.axi_bfm.axi_write_data("axi_wdata")
        self.axi_bfm.axi_write_response("axi_wresp")
        self.axi_bfm.axi_read_response("axi_rresp")
        self.bfm_wait(20) # wait for reset to go away

#c c_test_one
class c_test_one(c_axi_test_base, c_rom_th):
    #f execute
    def execute(self, address):
        self.ios.apb_processor_request__valid.drive(1)
        self.ios.apb_processor_request__address.drive(address)
        self.bfm_tick(1)
        while self.ios.apb_processor_response__acknowledge.value()==0:
            self.bfm_tick(1)
            pass
        self.ios.apb_processor_request__valid.drive(0)
        pass
    #f run
    def run(self):
        self.run_start()
        (resp, timer) = self.simple_read(address=0)
        print "Response to write", self.simple_write(address=4, data=timer+30)
        print "Response to read", self.simple_read(address=4)
        print "Response to read", self.simple_read(address=4)
        print "Response to read", self.simple_read(address=4)
        print "Response to read", self.simple_read(address=4)
        self.finishtest(0,"")
        pass

#a Hardware classes
#c axi_hw
class axi_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of APB ROM processor with a timer and GPIO
    """
    th_forces = { "axim.address_width":"32",
                  "axim.data_width":"32",
                  "axim.id_width":"12",
                  "axim.len_width":"4",
                  }
    module_name = "tb_axi"
    clocks = {"aclk":(0,None,None)}
    def __init__(self, test):
        self.th_forces = dict(self.th_forces.items())
        self.th_forces["axim.object"] = test
        simple_tb.cdl_test_hw.__init__(self, test)
        pass
    pass

#a Simulation test classes
#c axi
class axi(simple_tb.base_test):
    def test_one(self):
        test = c_test_one()
        hw = axi_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=10*1000)
        pass
    pass
