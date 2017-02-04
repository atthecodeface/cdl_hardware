#!/usr/bin/env python
#a Copyright
#
#  This file 'base6502' copyright Gavin J Stark 2016, 2017
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
import base6502_hw
import tempfile
import test6502

#a Simulation test classes
#c SimulationTestBase
class SimulationTestBase(unittest.TestCase):
    #f run_test
    def run_test(self, hw, num_cycles, pass_fail=None):
        do_waves = ("WAVES" in os.environ.keys())
        if do_waves:
            waves = hw.waves()
            waves.reset()
            waves.open(hw.wave_file)
            waves.add_hierarchy(hw.wave_hierarchies)
            pass
        hw.reset()
        hw.set_run_time(num_cycles-100)
        if do_waves:
            waves.enable()
            pass
        hw.step(num_cycles)
        print "Stepped",num_cycles
        if pass_fail!=None:
            pass_fail()
            hw.step(1)
            pass
        self.assertTrue(hw.passed())
        pass
    pass

#a 6502 Test class extended for hardware
#c c_Test6502Base_HW
class c_Test6502Base_HW(test6502.Test6502Base, SimulationTestBase):
    #f as_mif_file
    def as_mif_file(self, compiled_test):
        f = tempfile.NamedTemporaryFile(mode='w+b')
        for (s,m) in compiled_test.load_data:
            print >>f, "%x:"%s
            for md in m: print >> f, "%02x"%md
            pass
        f.flush()
        return f
    #f run_cpu_test
    def run_cpu_test(self, test):
        ct = self.compile_cpu_test(test)
        f = self.as_mif_file(ct)
        print "Running %s.%s.%s"%(self.__module__,self.__class__.__name__,test.__name__)
        if False:
            d_mif = "%s__%s__%s.mif"%(self.__module__,self.__class__.__name__,test.__name__)
            from shutil import copyfile
            copyfile(f.name, d_mif)
            pass
        hw = base6502_hw.cdl_test(sram_mif=f.name)
        self.run_test(hw, ct.num_cycles*20, pass_fail=lambda:hw.check_memory(ct.expected_memory_data))
        pass

#a Regression tests
#c Regress6502
class Regress6502(SimulationTestBase):
    #f test_6502_init
    def xtest_6502_init(self):
        f = tempfile.NamedTemporaryFile(mode='w+b')
        print >>f, "0: a9 32"
        print >>f, "4c 00 00"
        f.flush()
        hw = base6502_hw.cdl_test(sram_mif=f.name)
        self.run_test(hw, 300)
        f.close()

#c Regressions from test6502
class Regress6502_Test6502_Base(test6502.Test6502_Base, c_Test6502Base_HW): pass
class Regress6502_Test6502_ALU(test6502.Test6502_ALU, c_Test6502Base_HW): pass
class Regress6502_Test6502_Memory(test6502.Test6502_Memory, c_Test6502Base_HW): pass
class Regress6502_Test6502_Stack(test6502.Test6502_Stack, c_Test6502Base_HW): pass
class Regress6502_Test6502_Branch(test6502.Test6502_Branch, c_Test6502Base_HW): pass
class Regress6502_Test6502_Reg(test6502.Test6502_Reg, c_Test6502Base_HW): pass
class Regress6502_Test6502_Addressing(test6502.Test6502_Addressing, c_Test6502Base_HW): pass
class Regress6502_Test6502_Interrupt(test6502.Test6502_Interrupt, c_Test6502Base_HW): pass
