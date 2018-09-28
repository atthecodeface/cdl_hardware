#!/usr/bin/env python
#a Copyright
#  
#  This file 'bbc_hw' copyright Gavin J Stark 2016
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
import simple_tb

#c cdl_test_th
class cdl_test_th(pycdl.th):
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(1000) # to get past reset... :-)
        self.sim_msg.send_value(self.bbc_hier+".os",9,0,0xd9f9&0x3fff,0xa2) # ldx #&0x80 to stop it having to init all memory to zero
        self.sim_msg.send_value(self.bbc_hier+".os",9,0,0xd9fa&0x3fff,0x80) # ldx #&0x80 to stop it having to init all memory to zero
        self.passtest(0,"")
        pass
    def save_screen(self, filename):
        #self.sim_msg.send_value("bbc.bbc_display",8,0,0,0)
        pass
    def display_screen(self):
        print "-"*60,self.global_cycle()
        for y in range(25):
            r = ""
            for x in range(40):
                self.sim_msg.send_value(self.bbc_hier+".ram_1",8,0,0x3c00+y*40+x)
                d = self.sim_msg.get_value(2)
                if d>=32 and d<=127:
                    r+=chr(d)
                    pass
                else:
                    r+=" "
                    pass
                pass
            print r
            pass
        pass

#c hps_debug_fpga_hw
class hps_debug_fpga_hw(simple_tb.cdl_test_hw):
    module_name = "tb_hps_fpga_debug"
    teletext_rom_mif = "roms/teletext.mif"
    apb_vga_rom_mif  = "roms/apb_vga_rom.mif"
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.dut.trace "),},
               }
    #f __init__
    def __init__(self, test ):
        self.th_forces = { "dut.ftb.character_rom.filename":self.teletext_rom_mif,
                      "dut.ftb.character_rom.verbose":0,
                      "dut.apb_rom.filename":self.apb_vga_rom_mif,
                      "dut.apb_rom.verbose":-1,
                      }
        simple_tb.cdl_test_hw.__init__(self, test)
        pass

#c c_test_one
import axi
import dump
class c_test_one(axi.c_axi_test_base):
    dump_filename = "../riscv-atcf-tests/build/dump/hps_ps2_term2.dump"
    #f run
    def run(self):
        axi.c_axi_test_base.run_start(self)
        d = dump.c_dump()
        f = open(self.dump_filename)
        d.load(f, base_address=0, address_mask=0x7fffffff)
        f.close()
        self.bfm_wait(100)
        (resp, timer) = self.simple_read(address=0)
        print "Response to write", self.simple_write(address=16, data=timer+30)
        print "Response to read", self.simple_read(address=16)
        print "Response to read", self.simple_read(address=16)
        print "Response to read", self.simple_read(address=16)

        for (base, data) in d.package_data():
            print "Write RISC-V SRAM address to %08x"%base, self.simple_write(address=0x40000, data=base)
            n = 0
            for d in data:
                print "Write RISC-V SRAM code at %08x to %08x"%((base+n), d)
                self.simple_write(address=0x4000c, data=d)
                n += 1
                pass
            pass
        print "Response to read", self.simple_read(address=0x40010)
        print "Response to read", self.simple_read(address=0x40010)
        print "Response to read", self.simple_read(address=0x40010)
        print "Response to read", self.simple_read(address=0x40010)
        print "Start RISC-V", self.simple_write(address=0x40008, data=1)
        self.finishtest(0,"")
        pass

#c hps_debug_fpga_blah
class hps_debug_fpga_blah(simple_tb.base_test):
    def test_(self):
        test = c_test_one()
        hw = hps_debug_fpga_hw(test)
        #self.do_test_run(hw, 200*1000)
    pass

