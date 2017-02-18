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

#c c_test_one
class c_test_one(c_rom_th):
    #f Stuff
    program = {}
    program["code"] = [(c_rom_th.op_set("accumulator",0),["timer_start:"]),
                       (c_rom_th.op_branch("bne",0),["fail"]),
                       (c_rom_th.op_alu("xor",0xffffffff),),
                       (c_rom_th.op_branch("beq",0),["fail"]),
                       (c_rom_th.op_branch("branch",0),["skip0"]),
                       (c_rom_th.op_branch("bne",0),["fail"]),
                       (c_rom_th.op_alu("bic",0xdeadbeef),["skip0:"]),
                       (c_rom_th.op_branch("beq",0),["fail"]),
                       (c_rom_th.op_alu("bic",0xdeadffff),),
                       (c_rom_th.op_branch("beq",0),["fail"]),
                       (c_rom_th.op_alu("bic",0x21520000),),
                       (c_rom_th.op_branch("bne",0),["fail"]),
                       (c_rom_th.op_set("repeat",5),),
                       (c_rom_th.op_set("address",0x00000004),["loop_start:"]),
                       (c_rom_th.op_req("write_acc",0x00000204),),
                       (c_rom_th.op_req("write_arg",0x00000054),),
                       (c_rom_th.op_wait(0x00000050),),
                       (c_rom_th.op_req("write_arg",0x000000a0),),
                       (c_rom_th.op_branch("loop",0),["loop_start"]),
                       (c_rom_th.op_req("write_arg",0x00000300),),
                       (c_rom_th.op_wait(0x000000a0),),
                       (c_rom_th.op_set("address",0,),["timer_poll:"]),
                       (c_rom_th.op_req("read",0),),
                       (c_rom_th.op_alu("add",256),),
                       (c_rom_th.op_set("address",4,),),
                       (c_rom_th.op_req("write_acc_inc",0),),
                       (c_rom_th.op_req("write_acc_inc",0),),
                       (c_rom_th.op_req("write_acc",0),),
                       (c_rom_th.op_set("address",4,),),
                       (c_rom_th.op_req("read",0),["read_loop:"]),
                       (c_rom_th.op_alu("and",0x80000000),),
                       (c_rom_th.op_branch("beq",0),["read_loop"]),
                       (c_rom_th.op_req("read_inc",0),),
                       (c_rom_th.op_req("read_inc",0),),
                       (c_rom_th.op_req("read_inc",0),),
                       (c_rom_th.op_finish(),["fail:"]),
                       ]
    program["entry_points"] = ["timer_start", "timer_poll", "timer_start"]
    expectation = [7, 6, 7, 6, 7, 6, 7, 6, 4, 0, 7, 6, 4, 0] + [7, 6, 4, 0] + [7, 6, 4, 0]
    #f fill_rom
    def fill_rom(self, program, address=0):
        compilation = apb_rom.rom.compile_program(program,address)
        for (prog_address, op) in compilation["object"]:
            self.sim_msg.send_value("dut.apb_rom",9,0,prog_address,op)
            pass
        entry_addresses = []
        for ep in program["entry_points"]:
            entry_addresses.append(compilation["labels"][ep+":"])
            pass
        return entry_addresses
    #f bfm_tick
    def bfm_tick(self, cycles):
        for i in range(cycles):
            t = self.ios.timer_equalled.value()
            if t != self.timers[-1]:
                self.timers.append(t)
                pass
            self.bfm_wait(1)
            pass
        pass
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
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.sim_msg = self.sim_message()
        self.bfm_wait(25)
        executions = self.fill_rom(self.program)
        self.timers = [self.ios.timer_equalled.value()]
        for address in executions:
            self.execute(address)
            pass
        self.bfm_tick(2000)
        self.compare_expected_list("timer change", self.expectation, self.timers)
        self.bfm_wait(25)
        self.finishtest(0,"")
        pass

#a Hardware classes
#c apb_processor_hw
class apb_processor_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of APB ROM processor with a timer and GPIO
    """
    th_forces = { "th.clock":"clk",
                  "th.inputs":("apb_processor_response__acknowledge "+
                               "apb_processor_response__rom_busy "+
                               "timer_equalled[3] "+
                               ""),
                  "th.outputs":("apb_processor_request__valid "+
                                "apb_processor_request__address[16] "+
                                ""),
                  }
    module_name = "tb_apb_processor"
    pass

#a Simulation test classes
#c apb_processor
class apb_processor(simple_tb.base_test):
    def test_one(self):
        test = c_test_one()
        hw = apb_processor_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass
