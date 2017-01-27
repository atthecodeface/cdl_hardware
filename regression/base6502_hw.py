#!/usr/bin/env python
#a Copyright
#  
#  This file 'base6502_hw' copyright Gavin J Stark 2016, 2017
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

#c cdl_test_th
class cdl_test_th(pycdl.th):
    def run(self):
        self.passtest(0,"")
        pass

#c cdl_test
class cdl_test(pycdl.hw):
    """
    Simple instantiation of cdl/src/tb_6502 for testing
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    #f __init__
    def __init__(self, sram_mif=""):

        system_clock = pycdl.clock(0, 5, 5)
        reset_n      = pycdl.wire()

        self.reset_driver = pycdl.timed_assign( signal      = reset_n,
                                                init_value  = 0,
                                                wait        = 33,
                                                later_value = 1 )

        hw_forces = dict( )
        hw_forces = { "imem.filename":sram_mif,
                      "imem.verbose":0,
                      }
        self.tb_6502 = pycdl.module("tb_6502",
                                    clocks = {"clk":system_clock,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              },
                                    forces = hw_forces,
                                    )
        self.th = cdl_test_th(clocks = {"clk":system_clock},inputs={},outputs={})
        pycdl.hw.__init__(self,
                          self.tb_6502,
                          self.th,
                          system_clock,
                          self.reset_driver )
        self.wave_hierarchies = [self.tb_6502]
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        pass
    #f check_memory
    def check_memory(self, expected_memory_data):
        self.sim_msg = self.th.sim_message()
        for (a,ed) in expected_memory_data:
            self.sim_msg.send_value("tb_6502.imem",8,0,a)
            d = self.sim_msg.get_value(2)
            if (d!=ed):
                self.th.failtest(a,"Mismatch in data for %04x (got %02x expecte %02x)"%(a,d,ed))
                pass
            pass
        pass

