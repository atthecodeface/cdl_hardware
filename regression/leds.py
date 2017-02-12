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
    cfg_divider_400ns = 20
    #f drive_led
    def drive_led(self, rgb, last=False):
        self.ios.led_data__valid.drive(1)
        self.ios.led_data__last.drive(int(last))
        self.ios.led_data__red.drive(rgb[0])
        self.ios.led_data__green.drive(rgb[1])
        self.ios.led_data__blue.drive(rgb[2])
        self.bfm_wait(1)
        while self.ios.led_request__ready.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.led_data__valid.drive(0)
        self.bfm_wait(1)
        pass
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(25)
        self.ios.divider_400ns.drive(self.cfg_divider_400ns)
        self.bfm_wait(25)
        self.drive_led((0,0,0))
        self.drive_led((255,255,255))
        self.drive_led((128,64,32),True)
        self.drive_led((255,255,255))
        self.drive_led((0,0,0))
        self.drive_led((128,64,32),True)
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
                  "th.inputs":("led_request__ready "+
                               "led_request__first "+
                               "led_request__led_number[8] "+
                               "led_data_pin "+
                               ""),
                  "th.outputs":("led_data__valid "+
                                "led_data__last "+
                                "led_data__red[8] "+
                                "led_data__green[8] "+
                                "led_data__blue[8] "+
                                "divider_400ns[8] "+
                                ""),
                  }
    module_name = "tb_led_ws2812_chain"
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
