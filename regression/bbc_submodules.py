#!/usr/bin/env python
#a Copyright
#  
#  This file 'bbc_submodules.py' copyright Gavin J Stark 2016
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
    def ctest_init(self):
        hw = bbc_submodules_hw.hw_6845()
        self.run_test(hw, 2000000, pass_fail=lambda:hw.check_pass([]))
        pass
    #b All done

#a FDC 8271 testing
#c c_test_fdc8271
class c_test_fdc8271(SimulationTestBase):
    #f test_init
    def xtest_init(self):
        hw = bbc_submodules_hw.hw_8271()
        self.run_test(hw, 5*1000000, pass_fail=lambda:hw.check_pass([]))
        pass
    #b All done

#a BBC display SRAM
import simple_tb
#c display
class display(object):
    #b Variables
    # times in ticks at 2MHz
    h_back_porch  = 14*2 # 8us teletext + 6us
    h_width       = 40*2 # 40*12=480 pixels, 12MHz pixel clock, 40us
    h_front_porch = 10*2  # 4us teletext + 6us
    v_back_porch  = 5
    v_height      = 305
    v_front_porch = 5
    pixels_per_clock = 6 # or 8
    #f parse_scanline_data
    def parse_scanline_data(self, data):
        """
        The data supplied should be a list of 48-bit values with R in
        the bottom 16 bits, G in the next 16 bits, and B in the top 16
        bits; the left-most pixel is in the highest bit.
        This method attempts to parse this data to produce:
        * scanline number
        * offset in to scanline of first bit of data

        The data that is in the scanline is set so that the top-bit of
        every @pixels_per_clock is a 1 in the red, hence the red can
        be used as a synchronization sequence.

        So find the 'leftmost' red bit that is set as the alignment

        Then the green should give the bottom 6 bits of the pixel
        number within the line, and the blue should give the scanline number.

        The scanline may then be validated with this data.
        """
        result = {"valid": False,
                  "scanline": 0,
                  "pixel_offset": 0,
                  }
        alignment = 0 # Assume that R[15] is pixel 0 of the scanline - i.e. perfectly aligned
        for d in data:
            d = d&0xffff
            if (d==0):
                alignment = alignment+16
                continue
            while (d>>15)==0:
                alignment = alignment+1
                d = d<<1
                pass
            break
        if alignment>=len(data)*16-16: return result
        rgb0 = data[0+alignment/16]
        rgb1 = data[1+alignment/16]
        r = (( (rgb0>> 0)&0xffff)<<16) | (( (rgb1>> 0)&0xffff)<<0) 
        g = (( (rgb0>>16)&0xffff)<<16) | (( (rgb1>>16)&0xffff)<<0) 
        b = (( (rgb0>>32)&0xffff)<<16) | (( (rgb1>>32)&0xffff)<<0) 
        r = r << (alignment&15)
        g = g << (alignment&15)
        b = b << (alignment&15)
        r = r >> (32-self.pixels_per_clock)
        g = g >> (32-self.pixels_per_clock)
        b = b >> (32-self.pixels_per_clock)
        result["rgb"] = (r,g,b)
        result["pixel_offset"] = alignment - self.pixels_per_clock*g
        result["scanline"]     = b
        result["valid"] = True
        return result
    #f display_scanline
    def display_scanline(self, vsync=0, data=False, driver=None, wait=None):
        driver(vsync=vsync, hsync=1, red=0, green=0, blue=0)
        wait(1)
        driver(hsync=0)
        if data is False:
            wait(self.h_back_porch-1 + self.h_front_porch + self.h_width)
            return
        wait(self.h_back_porch-1)
        for i in range(self.h_width):
            # output self.pixels_per_clock, left pixel at msb
            driver(red=self.pixel_left, green=(i&63)<<self.pixel_6_shift, blue=(data&63)<<self.pixel_6_shift)
            wait(1)
            pass
        driver(red=0,green=0,blue=0)
        wait(self.h_front_porch)
        pass
    #f display_screen
    def display_screen(self, driver, wait):
        self.pixel_mask = (1<<self.pixels_per_clock)-1
        self.pixel_left = 1<<(self.pixels_per_clock-1)
        self.pixel_6_shift = 0 #8-self.pixels_per_clock
        driver(red=0, green=0, blue=0, vsync=0, hsync=0)
        self.display_scanline(vsync=1, driver=driver, wait=wait)
        for i in range(self.v_back_porch-1):
            self.display_scanline(driver=driver, wait=wait)
            pass
        for i in range(self.v_height):
            self.display_scanline(data=i, driver=driver, wait=wait)
            pass
        for i in range(self.v_front_porch):
            self.display_scanline(driver=driver, wait=wait)
            pass
        pass
    #b All done
    pass

#c display_teletext
class display_teletext(display):
    #b Variables
    # times in ticks at 2MHz
    h_back_porch  = 14*2 # 8us teletext + 6us
    h_width       = 40*2 # 40*12=480 pixels, 12MHz pixel clock, 40us
    h_front_porch = 10*2  # 4us teletext + 6us
    v_back_porch  = 5
    v_height      = 305
    v_front_porch = 5
    pixels_per_clock = 6 # or 8
    pass
#c display_graphics
class display_graphics(display):
    #b Variables
    # times in ticks at 2MHz
    h_back_porch  = 14*2 # 8us teletext + 6us
    h_width       = 40*2 # 40*12=480 pixels, 12MHz pixel clock, 40us
    h_front_porch = 10*2  # 4us teletext + 6us
    v_back_porch  = 5
    v_height      = 305
    v_front_porch = 5
    pixels_per_clock = 8
    pass
#c bbc_display_test_base
class bbc_display_test_base(simple_tb.base_th):
    ppc = { "bbc_ppc_1":0,
            "bbc_ppc_2":1,
            "bbc_ppc_4":2,
            "bbc_ppc_6":3,
            "bbc_ppc_8":4,
            }
    #f apb_write
    def apb_write(self, address, data):
        self.apb_request__psel.drive(1)
        self.apb_request__pwrite.drive(1)
        self.apb_request__penable.drive(0)
        self.apb_request__paddr.drive(address)
        self.apb_request__pwdata.drive(data)
        self.bfm_wait(1)
        self.apb_request__penable.drive(1)
        self.bfm_wait(1)
        while self.apb_response__pready.value()==0:
            self.bfm_wait(1)
            pass
        self.apb_request__psel.drive(0)
        self.apb_request__penable.drive(0)
        pass
    #f apb_read
    def apb_read(self, address):
        self.apb_request__psel.drive(1)
        self.apb_request__pwrite.drive(1)
        self.apb_request__penable.drive(0)
        self.apb_request__paddr.drive(address)
        self.bfm_wait(1)
        self.apb_request__penable.drive(1)
        self.bfm_wait(1)
        while self.apb_response__pready.value()==0:
            self.bfm_wait(1)
            pass
        self.apb_request__psel.drive(0)
        self.apb_request__penable.drive(0)
        return self.apb_response__prdata.value()
    #f display_driver
    def display_driver(self, vsync=None, hsync=None, red=None, green=None, blue=None ):
        if vsync is not None: self.display__vsync.drive(vsync)
        if hsync is not None: self.display__hsync.drive(hsync)
        if red   is not None: self.display__red.drive(red)
        if green is not None: self.display__green.drive(green)
        if blue  is not None: self.display__blue.drive(blue)
        pass
    #f read_scanline
    def read_scanline(self, framebuffer, scanline):
        data = []
        for i in range(self.cfg["writes_per_scanline"]):
            self.sim_msg.send_value("dut.framebuffer",8,0,scanline*self.cfg["offset_per_scanline"]+i)
            data.append(self.sim_msg.get_value(2))
            pass
        return data
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.display__clock_enable.drive(1)
        self.display__pixels_per_clock.drive(self.display_cfg["pixels_per_clock"])
        self.bfm_wait(10)
        self.apb_write((1<<16)|(0<<0), self.cfg["base"] | (self.cfg["base_odd"]<<16))
        self.apb_write((1<<16)|(1<<0), self.cfg["writes_per_scanline"] |
                       (self.cfg["offset_per_scanline"]<<10) |
                       (self.cfg["interlace_in_same_buffer"]<<30) |
                       (self.cfg["sram_scanlines"]<<20))
        self.apb_write((1<<16)|(2<<0), (self.cfg["h_back_porch"]&0xffff) |
                       ((self.cfg["v_back_porch"]&0xffff)<<16))
        self.bfm_wait(25)
        self.display_data.display_screen(driver=self.display_driver, wait=self.bfm_wait)
        self.bfm_wait(25)
        self.sim_msg = self.sim_message()
        for i in range(self.cfg["sram_scanlines"]):
            data = self.read_scanline("dut.framebuffer", i)
            data = self.display_data.parse_scanline_data(data)
            if data["valid"]:
                if ((i+self.expectation["scanline_offset"])&63 != data["scanline"]):
                    self.failtest(i,"Mismatch in scanline offset (%d/%d) for line %d"%(data["scanline"]-i,self.expectation["scanline_offset"],i))
                    pass
                if (self.expectation["pixel_offset"] != data["pixel_offset"]):
                    self.failtest(i,"Mismatch in pixel offset (%d/%d) for line %d"%(data["pixel_offset"],self.expectation["pixel_offset"],i))
                    pass
                pass
            else:
                if ((i+self.expectation["scanline_offset"]>=0) and
                    (i+self.expectation["scanline_offset"]<self.display_data.v_height)
                    ):
                    self.failtest(i,"Got invalid data for line %d but expected scanline %d"%(i,i+self.expectation["scanline_offset"]))
                    pass
                pass
            pass
        self.finishtest(0,"")
        pass
    #b All done
    pass

#c bbc_display_test_0
class bbc_display_test_0(bbc_display_test_base):
    cfg = {"base":0,
           "base_odd":0,
           "writes_per_scanline":30, # 16 pixels per write
           "offset_per_scanline":40, # 16 pixels per write
           "interlace_in_same_buffer":0,
           "sram_scanlines":5,
           "h_back_porch":-14*12+10, # pixels from end of hsync to first valid pixel
           "v_back_porch":-5, # scan lines
           }
    display_cfg = {"pixels_per_clock":bbc_display_test_base.ppc["bbc_ppc_6"],
                   }
    display_data = display_teletext()
    expectation = {"pixel_offset":0,
                   "scanline_offset":0,}
    #b All done
#c bbc_display_test_1
class bbc_display_test_1(bbc_display_test_base):
    cfg = {"base":0,
           "base_odd":0,
           "writes_per_scanline":30, # 16 pixels per write
           "offset_per_scanline":40, # 16 pixels per write
           "interlace_in_same_buffer":0,
           "sram_scanlines":5,
           "h_back_porch":-13*16, # pixels from end of hsync to first valid pixel
           "v_back_porch":-5, # scan lines
           }
    display_cfg = {"pixels_per_clock":bbc_display_test_base.ppc["bbc_ppc_8"],
                   }
    display_data = display_graphics()
    expectation = {"pixel_offset":0,
                   "scanline_offset":0,}
    #b All done
#c bbc_display_test_2
class bbc_display_test_2(bbc_display_test_base):
    cfg = {"base":0,
           "base_odd":0,
           "writes_per_scanline":30, # 16 pixels per write
           "offset_per_scanline":40, # 16 pixels per write
           "interlace_in_same_buffer":0,
           "sram_scanlines":5,
           "h_back_porch":-13*16 + 12, # pixels from end of hsync to first valid pixel
           "v_back_porch":-3, # scan lines
           }
    display_cfg = {"pixels_per_clock":bbc_display_test_base.ppc["bbc_ppc_8"],
                   }
    display_data = display_graphics()
    expectation = {"pixel_offset":12,
                   "scanline_offset":-2,}
    #b All done
#c bbc_display_test_3
class bbc_display_test_3(bbc_display_test_base):
    cfg = {"base":0,
           "base_odd":0,
           "writes_per_scanline":30, # 16 pixels per write
           "offset_per_scanline":30, # 16 pixels per write
           "interlace_in_same_buffer":0,
           "sram_scanlines":310,
           "h_back_porch":-13*16 + 12, # pixels from end of hsync to first valid pixel
           "v_back_porch":-3, # scan lines
           }
    display_cfg = {"pixels_per_clock":bbc_display_test_base.ppc["bbc_ppc_8"],
                   }
    display_data = display_graphics()
    expectation = {"pixel_offset":12,
                   "scanline_offset":-2}
    #b All done
#c bbc_display_sram_hw
class bbc_display_sram_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of BBC display SRAM testbench
    """
    apb_request_signals  = " ".join(["apb_request__"+ss for ss in ("psel", "penable", "paddr[32]", "pwrite", "pwdata[32]")])
    apb_response_signals = " ".join(["apb_response__"+ss for ss in ("prdata[32]", "pready", "perr")])
    display_signals      = " ".join(["display__"+ss for ss in ("red[8]", "green[8]", "blue[8]", "vsync", "hsync", "clock_enable", "pixels_per_clock[3]")])
    sram_write_signals   = " ".join(["sram_write__"+ss for ss in ("address[16]", "data[48]", "enable")])
    th_forces = { "th.clock":"clk",
                  "th.inputs":(apb_response_signals+" "+
                               sram_write_signals+" "+
                               ""),
                  "th.outputs":(apb_request_signals+" "+
                                display_signals+" "+
                                ""),
                  }
    module_name = "tb_bbc_display_sram"
    system_clock_half_period = 250 # 2MHz video clock
    pass

#c bbc_display_sram
class bbc_display_sram(simple_tb.base_test):
    def test_display_0(self): self.do_test_run(bbc_display_sram_hw(test=bbc_display_test_0()), num_cycles=25*1000*1000)
    def test_display_1(self): self.do_test_run(bbc_display_sram_hw(test=bbc_display_test_1()), num_cycles=25*1000*1000)
    def test_display_2(self): self.do_test_run(bbc_display_sram_hw(test=bbc_display_test_2()), num_cycles=25*1000*1000)
    def test_display_3(self): self.do_test_run(bbc_display_sram_hw(test=bbc_display_test_3()), num_cycles=25*1000*1000)
    pass
