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
#c base_th
class base_th(pycdl._thfile):
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
    def run_start(self):
        self.bfm_wait(1)
        self.ios = self
        pass
    pass

#a Hardware classes
#c cdl_test_hw
class cdl_test_hw(pycdl.hw):
    """
    Simple instantiation of a module with just clock and reset, and some specified th ports
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    th_forces = {}
    module_name = ""
    #f __init__
    def __init__(self, test):

        system_clock   = pycdl.clock(0, 1, 1)
        reset_n        = pycdl.wire()

        self.drivers = [pycdl.timed_assign( signal=reset_n, init_value=0, wait=33, later_value=1),
                        ]

        hw_forces = dict(self.th_forces.items())
        hw_forces["th.object"] = test
        self.dut = pycdl.module( self.module_name,
                                 clocks = {"clk":system_clock},
                                 inputs = {"reset_n":reset_n},
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
#c base_test
class base_test(unittest.TestCase):
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

