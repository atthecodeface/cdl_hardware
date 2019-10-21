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
import structs
import i2c

#a Test classes
#c c_rom_th
class c_rom_th(simple_tb.base_th, apb_rom.rom):
    pass

#c c_apb_proc_test_one
class c_apb_proc_test_one(c_rom_th):
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

#c apb_target_test_base
class apb_target_test_base(simple_tb.base_th):
    #f apb_request
    def apb_request(self, address, write_data=None):
        pwrite = 1
        pwdata = write_data
        if write_data is None:
            pwrite = 0
            pwdata = 0
            pass
        self.ios.apb_request__paddr.drive(address)
        self.ios.apb_request__penable.drive(0)
        self.ios.apb_request__psel.drive(1)
        self.ios.apb_request__pwrite.drive(pwrite)
        self.ios.apb_request__pwdata.drive(pwdata)
        self.bfm_wait(1)
        self.ios.apb_request__penable.drive(1)
        self.bfm_wait(1)
        while self.ios.apb_response__pready.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.apb_request__penable.drive(0)
        self.ios.apb_request__psel.drive(0)
        read_data = self.ios.apb_response__prdata.value()
        err       = self.ios.apb_response__perr.value()
        return (err, read_data)
    #f apb_read_no_error
    def apb_read_no_error(self, address):
        (err, data) = self.apb_request(address)
        if err:
            self.failtest(0,"Expected apb error response of 0")
            pass
        return data
    #f apb_write_no_error
    def apb_write_no_error(self, address, data):
        (err, data) = self.apb_request(address, data)
        if err:
            self.failtest(0,"Expected apb error response of 0")
            pass
        pass
#c apb_target_rv_timer_test_base
class apb_target_rv_timer_test_base(apb_target_test_base):
    #f timer_control
    def timer_control(self, mode="enable", mult=1, div=1, lock=False):
        reset = (mode == "reset")
        enable = (mode == "enable")
        add_per_tick = (16 * mult) / div
        rem_per_tick = (16 * mult) % div
        self.ios.timer_control__reset_counter.drive(reset)
        self.ios.timer_control__enable_counter.drive(enable)
        self.ios.timer_control__block_writes.drive(lock)
        self.ios.timer_control__integer_adder.drive(add_per_tick/16)
        self.ios.timer_control__fractional_adder.drive(add_per_tick%16)
        if rem_per_tick==0:
            self.ios.timer_control__bonus_subfraction_numer.drive(0)
            self.ios.timer_control__bonus_subfraction_denom.drive(0)
            pass
        else:
            self.ios.timer_control__bonus_subfraction_numer.drive(div-rem_per_tick-1)
            self.ios.timer_control__bonus_subfraction_denom.drive(div-1)
            pass
        pass
    #f read_timer
    def read_timer(self):
        timer = self.apb_read_no_error(0)
        timer = (self.apb_read_no_error(1)<<32) | timer
        return timer
    #f read_comparator
    def read_comparator(self):
        comparator = self.apb_read_no_error(2)
        comparator = (self.apb_read_no_error(3)<<32) | comparator
        return comparator
    #f write_timer
    def write_timer(self, timer):
        self.apb_write_no_error(0, (timer >> 0) & 0xffffffff)
        self.apb_write_no_error(1, (timer >> 32) & 0xffffffff)
        pass
    #f write_comparator
    def write_comparator(self, comparator):
        self.apb_write_no_error(2, (comparator >> 0) & 0xffffffff)
        self.apb_write_no_error(3, (comparator >> 32) & 0xffffffff)
        pass
    #f check_timer
    def check_timer(self, exp_timer, skip_value_check=False):
        timer = self.read_timer()
        if timer!=exp_timer:
            self.failtest(0,"Unexpected timer value %d expected %d (exp-actual=%d)"%(timer,exp_timer,exp_timer-timer))
            pass
        if skip_value_check: return
        timer = (self.ios.timer_value__value.value() & 0xffffffffffffffff)
        if timer!=exp_timer:
            self.failtest(0,"Unexpected timer value on timer_value.timer_value %d expected %d (exp-actual=%d)"%(timer,exp_timer,exp_timer-timer))
            pass
        pass
    #f check_comparator
    def check_comparator(self, exp_comparator):
        comparator = self.read_comparator()
        if comparator!=exp_comparator:
            self.failtest(0,"Unexpected comparator value %d expected %d (exp-actual=%d)"%(comparator,exp_comparator,exp_comparator-comparator))
            pass
        pass
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.sim_msg = self.sim_message()
        print self.apb_request(0)
        self.finishtest(0,"")
        pass
    pass

#c apb_target_rv_timer_test_mult_div
class apb_target_rv_timer_test_mult_div(apb_target_rv_timer_test_base):
    mult_divs = [ (1,1), (10,1), (1,10), (17,13), (13,17),
                  (10,6), # 1ns @ 600MHz
                  (10,8), # 1ns @ 800MHz
                  (50,1), # 1ns @ 50MHz
    ]
    ticks_to_wait = 1000
    #f check_mult_div
    def check_mult_div(self, mult, div):
        self.timer_control(mode="reset")
        self.bfm_wait(5)
        timer_r = self.read_timer()
        if (timer_r!=0):
            self.failtest(0,"Expected timer to be 0 at reset got %d"%(timer_r))
            pass
        self.timer_control(mode="hold", mult=mult, div=div, lock=False)
        self.apb_write_no_error(0, 0xfffffff0 )
        timer0 = self.read_timer()
        self.timer_control(mode="enable", mult=mult, div=div, lock=False)
        self.bfm_wait(self.ticks_to_wait)
        self.timer_control(mode="hold", mult=mult, div=div, lock=False)
        timer1 = self.read_timer()
        delta = timer1-timer0
        exp_delta = self.ticks_to_wait * mult / div
        diff = delta - exp_delta
        print "Delta %d for %d ticks with mult %d and div %d"%(delta, self.ticks_to_wait, mult, div)
        if (diff<-1) or (diff>1):
            self.failtest(0,"Expected delta %d got delta %d; diff of %d out of range [-1,1]"%(exp_delta,delta,diff))
            pass
        pass
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.sim_msg = self.sim_message()
        for (m,d) in self.mult_divs:
            self.check_mult_div(m,d)
            pass
        self.finishtest(0,"")
        pass

#c apb_target_rv_timer_test_comparator
class apb_target_rv_timer_test_comparator(apb_target_rv_timer_test_base):
    idle = 10
    comparison_values = [(0,0), # Note the test checks both a,b and b,
                         (1,0),
                         (0xffffffff,0),
                         (0xffffffff,0xffffffff),
                         (0xffffffffffffffff,0),
                         (0xffffffff00000000,0),
                         (0xffffffff00000000,0xffffffff00000000),
                         (0xffffffff00000000,0xfffffffffffffffe),
                         (0x100000000,0),
                         (0x100000000,0xffffffff),
                         (0x100000000,0x100000000),
                         (0xffffffff00000000,0x100000000),
                         (0xffffffffffffffff,0x100000000),
                         ]
                            
    #f check_comparison
    def check_comparison(self, timer, comparator):
        self.timer_control(mode="hold", lock=False)
        self.bfm_wait(self.idle)
        self.write_timer(timer)
        self.write_comparator(comparator)
        self.bfm_wait(self.idle)
        self.check_timer(timer)
        self.check_comparator(comparator)
        expected_irq = 0
        if (timer>comparator): expected_irq=1
        irq = self.ios.timer_value__irq.value()
        if expected_irq!=irq:
            self.failtest(0,"Mismatch in expected irq comparison (got %d expected %d) for %x v %x"%(irq,expected_irq,timer,comparator))
        pass
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.sim_msg = self.sim_message()
        for (t,c) in self.comparison_values:
            self.check_comparison(t,c)
            self.check_comparison(c,t)
            pass
        self.finishtest(0,"")
        pass

#c apb_target_i2c_test_base
class apb_target_i2c_test_base(apb_target_test_base, i2c.i2c_mixin):
    pass
#c apb_target_i2c_test_one
class apb_target_i2c_test_one(apb_target_i2c_test_base):
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        self.i2c_init(scl    = self.ios.i2c_out__scl,
                      sda    = self.ios.i2c_out__sda,
                      scl_in = self.ios.i2c_in__scl,
                      sda_in = self.ios.i2c_in__sda,
                      cfg    = {"divider":3})
        self.i2c_idle()
        
        i2c_conf = 0x02460a03
        self.apb_write_no_error( address=0, data=i2c_conf )
        d = self.apb_read_no_error( address=0 )
        if d != i2c_conf:
            self.failtest(self.global_cycle(),"Mismatch in reading back I2C conf")
            pass
        self.apb_write_no_error( address=0, data=i2c_conf )
        self.apb_write_no_error( address=3, data=0xf00020 )
        self.apb_write_no_error( address=2, data=0x203 )
        for i in range(20):
            status = self.apb_read_no_error( address=1 )
            print "Status %08x"%status
            if (status&3)==0: break
            self.bfm_wait(1000)
            pass
        if i>18:
            self.failtest(self.global_cycle(),"Expected I2C transaction to complete")
            pass
        if self.ios.gpio_output.value()!=0xc:
            self.failtest(self.global_cycle(),"Expected GPIO to have been written over I2C to 0xc")
            pass
        self.finishtest(0,"")
        pass
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

#c apb_target_rv_timer_hw
class apb_target_rv_timer_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of APB target timer hw
    """
    
    apb_request   = pycdl.wirebundle(structs.apb_request)
    apb_response  = pycdl.wirebundle(structs.apb_response)
    timer_control = pycdl.wirebundle(structs.timer_control)
    timer_value   = pycdl.wirebundle(structs.timer_value)
    th_forces = { "th.clock":"clk",
                  "th.inputs":(" ".join(apb_response._name_list("apb_response")) + " " +
                               " ".join(timer_value._name_list("timer_value")) + " " +
                               ""),
                  "th.outputs":(" ".join(apb_request._name_list("apb_request")) + " " +
                               " ".join(timer_control._name_list("timer_control")) + " " +
                               ""),
                  }
    module_name = "tb_apb_target_rv_timer"
    pass

#c apb_target_i2c_hw
class apb_target_i2c_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of APB target timer hw
    """
    apb_request   = pycdl.wirebundle(structs.apb_request)
    apb_response  = pycdl.wirebundle(structs.apb_response)
    i2c           = pycdl.wirebundle(structs.i2c)
    i2c_conf      = pycdl.wirebundle(structs.i2c_conf)
    th_forces = { "th.clock":"clk",
                  "th.inputs":(" ".join(apb_response._name_list("apb_response")) + " " +
                               " ".join(i2c._name_list("i2c_in")) + " " +
                               "gpio_output[16] "+
                               ""),
                  "th.outputs":(" ".join(apb_request._name_list("apb_request")) + " " +
                               " ".join(i2c._name_list("i2c_out")) + " " +
                               " ".join(i2c_conf._name_list("i2c_conf")) + " " +
                               ""),
                  }
    module_name = "tb_apb_target_i2c"
    pass

#a Simulation test classes
#c apb_processor - not working at present
class apb_processor(simple_tb.base_test):
    def xtest_one(self):
        test = c_apb_proc_test_one()
        hw = apb_processor_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass

#c apb_target_rv_timer
class apb_target_rv_timer(simple_tb.base_test):
    def test_mult_div(self):
        test = apb_target_rv_timer_test_mult_div()
        hw = apb_target_rv_timer_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    def test_comparator(self):
        test = apb_target_rv_timer_test_comparator()
        hw = apb_target_rv_timer_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass
#c apb_target_i2c
class apb_target_i2c(simple_tb.base_test):
    def test_i2c(self):
        test = apb_target_i2c_test_one()
        hw = apb_target_i2c_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass
