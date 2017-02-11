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

#a Test classes
#c th_interacting
class th_interacting(pycdl._thfile):
    _auto_wire_same_name = False
    #f exec_run
    def exec_run(self):
        self._th = self
        self.run()
        pass
    def bfm_wait(self, cycles):
        self.cdlsim_sim.bfm_wait(cycles)

    def spawn(self, boundfn, *args):
        self.py.pyspawn(boundfn, args)

    def global_cycle(self):
        return self.cdlsim_sim.global_cycle()

    def passtest(self, code, message):
        return self.py.pypass(code, message)

    def failtest(self, code, message):
        return self.py.pyfail(code, message)

    def passed(self):
        return self.py.pypassed()

    def __init__(self, th=None):
        pycdl._thfile.__init__(self, th)
        pass
    def th_interacting_init(self, th_master=False):
        self.bfm_wait(1)
        self.ios = self
        self.th_master = th_master
        pass
    def th_interact_request(self):
        self.ios.th_request.drive(1)
        self.bfm_wait(1)
        while self.ios.th_acknowledge.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.th_request.drive(0)
        self.bfm_wait(1)
        pass
    def th_interact_wait_for_request(self):
        self.bfm_wait(1)
        while self.ios.th_acknowledge.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.th_request.drive(1)
        self.bfm_wait(1)
        self.ios.th_request.drive(0)
        self.bfm_wait(1)
        pass
    pass
#c c_test_one
class c_test_one(th_interacting):
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
        th_interacting.th_interacting_init(self, th_master=False)
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
        self.passtest(0,"")
        pass
#a Hardware classes
#c cdl_test_hw
class cdl_test_hw(pycdl.hw):
    """
    Simple instantiation of LED chain
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    #f __init__
    def __init__(self, test):

        system_clock   = pycdl.clock(0, 1, 1)
        reset_n        = pycdl.wire()

        self.drivers = [pycdl.timed_assign( signal=reset_n, init_value=0, wait=33, later_value=1),
                        ]

        hw_forces = dict()
        hw_forces = { "th.clock":"clk",
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
                      "th.object":test,
                      }
        self.dut = pycdl.module("tb_led_ws2812_chain",
                                    clocks = {"clk":system_clock,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              },
                                      forces = hw_forces,
                                    )
        pycdl.hw.__init__(self,
                          thread_mapping=None,
                          children=[self.dut,
                                    system_clock,
                            ] + self.drivers,
                          )
        self.wave_hierarchies = [self.dut]
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        pass

#a Simulation test classes
#c SimulationTestBase
class SimulationTestBase(unittest.TestCase):
    #f do_test_run
    def do_test_run(self, hw, num_cycles, num_cycles_with_waves=None):
        if num_cycles_with_waves is None:
            num_cycles_with_waves = num_cycles
            pass
        waves_delay = None
        if ("WAVES" in os.environ.keys()):
            waves_delay = int(os.environ["WAVES"])
            pass
        do_waves = waves_delay is not None
        if do_waves:
            waves = hw.waves()
            waves.reset()
            waves.open(hw.wave_file)
            waves.add_hierarchy(hw.wave_hierarchies)
            pass
        hw.reset()
        hw.set_run_time(0xffffffffff)
        if not do_waves:
            hw.step(num_cycles)
            pass
        else:
            hw.step(waves_delay)
            print "Waves enabled - running for ",num_cycles_with_waves
            waves.enable()
            hw.step(num_cycles_with_waves)
            print "Waves stopped"
            pass
        pass
    pass

#c c_Test_LedChain
class c_Test_LedChain(SimulationTestBase):
    def test_one(self):
        test = c_test_one()
        hw = cdl_test_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
        pass
    pass
