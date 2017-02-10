#!/usr/bin/env python
#a Copyright
#
#  This file 'bbc.py' copyright Gavin J Stark 2016, 2017
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
import bbc_hw
import tempfile

#a Simulation test classes
#c SimulationTestBase
class SimulationTestBase(unittest.TestCase):
    pass

#a 6502 Test class extended for hardware
#c c_TestBBC_HW
class c_TestBBC_HW(SimulationTestBase):
    #f test_run
    def test_run(self):
        waves_delay = None
        if ("WAVES" in os.environ.keys()):
            waves_delay = int(os.environ["WAVES"])
            pass
        do_waves = waves_delay is not None
        hw = bbc_hw.cdl_test(os_rom_mif  ="roms/os12.rom.mif",
                             basic_rom_mif ="roms/basic2.rom.mif",
                             adfs_rom_mif ="roms/dfs.rom.mif",
                             teletext_rom_mif ="roms/teletext.mif",
                             disk_mif="disks/elite.mif"
                             )
        if do_waves:
            waves = hw.waves()
            waves.reset()
            waves.open(hw.wave_file)
            waves.add_hierarchy(hw.wave_hierarchies)
            pass
        hw.reset()
        hw.set_run_time(0xffffffffff)
        # dec 11 lunchtime - 100 million step takes 40 seconds, debug build; 25 seconds optimized build
        # each 10 steps is one system clock = 4MHz = 250ns => 25ns/step
        # -> 40Msteps / bbc second => 100 million steps is 2.5 bbc seconds => 40/2.5 = runs at 1/16th realtime debug
        # -> 40Msteps / bbc second => 100 million steps is 2.5 bbc seconds => 25/2.5 = runs at 1/10th realtime
        # without getting screen every 100k steps saves 8% performance
        #hw.step(72600000)
        while not do_waves:
        #for i in range(10):
        #for i in range(0):
            hw.step(4*1000*1000)
            hw.th.display_screen()
            pass
        if do_waves:
            hw.step(waves_delay)
            print "Waves enabled - running for 3*1000*1000"
            waves.enable()
            hw.step(3*1000*1000)
            print "Waves stopped"
            pass
        pass

