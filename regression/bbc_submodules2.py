#!/usr/bin/env python
#a Copyright
#  
#  This file 'bbc.py' copyright Gavin J Stark 2016
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
import sys, os, unittest
import pycdl
import bbc_submodules_hw

#a Simulation test classes
#c SimulationTestBase
class SimulationTestBase(unittest.TestCase):
    def fred(self, hw, num_cycles, pass_fail=None):
        if "WAVES" in os.environ.keys():
            waves = hw.waves()
            waves.reset()
            waves.open(hw.wave_file)
            waves.add_hierarchy(hw.wave_hierarchies)
            waves.enable()
            pass
        hw.reset()
        hw.set_run_time(num_cycles-100)
        hw.step(num_cycles)
        print "Stepped",num_cycles
        if pass_fail!=None:
            pass_fail()
            hw.step(1)
            pass
        return hw.passed()
    #f run_test
    def run_test(self, hw, num_cycles, **kwargs):
        test_passed = self.fred(hw=hw, num_cycles=num_cycles, **kwargs);
        self.assertTrue(test_passed)
        pass
    pass

#a Crtc 6845 testing
#c c_test_crtc6845
class c_test_crtc6845(SimulationTestBase):
    #f test_init
    def test_init(self):
        hw = bbc_submodules_hw.hw_6845()
        self.run_test(hw, 2000000, pass_fail=lambda:hw.check_pass([]))
        pass
    #b All done

#a FDC 8271 testing
#c c_test_fdc8271
class c_test_fdc8271(SimulationTestBase):
    #f test_init
    def test_init(self):
        hw = bbc_submodules_hw.hw_8271()
        self.run_test(hw, 5*1000*1000, pass_fail=lambda:hw.check_pass([]))
        pass
    #b All done
