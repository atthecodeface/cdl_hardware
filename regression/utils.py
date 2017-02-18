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
