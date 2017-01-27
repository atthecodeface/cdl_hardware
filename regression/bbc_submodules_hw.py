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

#c th_interacting
class th_interacting(pycdl.th):
    _auto_wire_same_name = False
    def th_interacting_init(self, th_master=False):
        self.bfm_wait(1)
        self.ios = self._thfile
        self.th_master = th_master
        self.ios.th_request.drive(0)
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

#c th_mot_bus
class th_mot_bus(th_interacting):
    def bus_init(self, chip_select_name, active_high, **kwargs):
        th_interacting.th_interacting_init(self)
        self.cs = (getattr(self.ios,chip_select_name), 1 and active_high)
        self.bfm_wait(1) # skip reset
        self.cs[0].drive(1^self.cs[1])
        self.bfm_wait(100) # skip reset
        self.cs[0].drive(1^self.cs[1])
        pass
    def bus_write(self, address, data):
        self.ios.read_not_write.drive(0)
        self.ios.address.drive(address)
        self.cs[0].drive(self.cs[1])
        self.ios.data_in.drive(data)
        self.bfm_wait(1)
        self.cs[0].drive(1^self.cs[1])
        pass
    pass

#c th_int_bus
class th_int_bus(th_interacting):
    def bus_init(self, chip_select_name, active_high, **kwargs):
        th_interacting.th_interacting_init(self)
        self.cs = (getattr(self.ios,chip_select_name), 1 and active_high)
        self.ios.write_n.drive(1)
        self.ios.read_n.drive(1)
        self.bfm_wait(1) # skip reset
        self.cs[0].drive(1^self.cs[1])
        self.bfm_wait(100) # skip reset
        self.cs[0].drive(1^self.cs[1])
        pass
    def bus_write(self, address, data):
        self.ios.write_n.drive(0)
        self.ios.address.drive(address)
        self.ios.data_in.drive(data)
        self.cs[0].drive(self.cs[1])
        self.bfm_wait(1)
        self.cs[0].drive(1^self.cs[1])
        self.ios.write_n.drive(1)
        pass
    def bus_read(self, address):
        self.ios.read_n.drive(0)
        self.ios.address.drive(address)
        self.cs[0].drive(self.cs[1])
        self.bfm_wait(1)
        read_data = self.ios.data_out.value()
        self.cs[0].drive(1^self.cs[1])
        self.ios.read_n.drive(1)
        return read_data
    def data_ack(self, data=None, address=None):
        if data is None:
            self.ios.read_n.drive(0)
            pass
        else:
            self.ios.write_n.drive(0)
            self.ios.data_in.drive(data)
            pass
        self.ios.data_ack_n.drive(0)
        self.bfm_wait(1)
        read_data = self.ios.data_out.value()
        self.ios.data_ack_n.drive(1)
        self.ios.read_n.drive(1)
        self.ios.write_n.drive(1)
        return read_data
    pass

#c config_6845
class config_6845(object):
    h_total =         30     # 30-1 for 30 characters across
    h_displayed =     20     # 20 characters displayed
    h_sync_pos =      15     # hsync starts at start of character 15 (counting from 0)
    h_sync_width =     6     # 6 characters (note if 0, no hsync) - and vsync default of 16 rows
    v_total =         52     # 52 scanlines = 10 rows and 2 adjust
    v_displayed =      7     # 7 rows of characters displayed
    v_sync_pos =       5     # 5 rows in, start vsync
    v_sync_width =    16     # Default value
    interlace_mode =   0     # non-interlaced
    max_scan_line =    5     # 5-1 for 5 scanlines
    def __init__(self, **kwargs):
        for (a,v) in kwargs.iteritems():
            setattr(self, a, v)
            pass
        pass
    def get_register_values(self):
        config = {"h_total":         self.h_total-1,
                  "h_displayed":     self.h_displayed,
                  "h_sync_pos":      self.h_sync_pos,
                  "h_sync_width":    (self.v_sync_width<<4) | self.h_sync_width,
                  "v_total":         self.v_total/self.max_scan_line-1,
                  "v_total_adjust":  self.v_total%self.max_scan_line,
                  "v_displayed":     self.v_displayed,
                  "v_sync_pos":      self.v_sync_pos,
                  "interlace_mode":  self.interlace_mode,
                  "max_scan_line":   self.max_scan_line-1
                  }
        return config

#c th_6845_bus
class th_6845_bus(th_mot_bus):
    #b Registers
    registers = {"h_total":         0,
                 "h_displayed":     1,
                 "h_sync_pos":      2,
                 "h_sync_width":    3,
                 "v_total":         4,
                 "v_total_adjust":  5,
                 "v_displayed":     6,
                 "v_sync_pos":      7,
                 "interlace_mode":  8,
                 "max_scan_line":   9,
                 "cursor_start":   10,
                 "cursor_end":     11,
                 "start_addr_h":   12,
                 "start_addr_l":   13,
                 "cursor_addr_h":  14,
                 "cursor_addr_l":  15,
                 "lpen_addr_h":    16,
                 "lpen_addr_l":    17,
                 }
    #b write_register
    def write_register(self, register, value):
        self.bus_write(0,self.registers[register])
        self.bus_write(1,value)
        pass
    #b write_config
    def write_config(self, config):
        for (r,v) in config.iteritems():
            self.write_register(r,v)
            pass
        pass
    #b run
    def run(self):
        th_mot_bus.bus_init(self, "chip_select_n",0, th_master=True)
        config = config_6845(interlace_mode=3)
        self.write_config( config.get_register_values() )
        self.bfm_wait(100) # to get it to settle
        self.hw.current_config = config
        self.th_interact_request()
        self.th_interact_wait_for_request()
        self.check_config_with_trace(config, self.hw.config_sig_trace)
        self.passtest(0,"")
        pass
    def check_config_with_trace(self, config, trace ):
        analysis = trace.analyze()
        vsync_interval = self.check_config_with_analysis_vsync(config, analysis)
        hsync_interval = self.check_config_with_analysis_hsync(config, analysis)
        print 2*vsync_interval, hsync_interval*config.v_total*2
        print vsync_interval*2 / (hsync_interval+0.0)
        print vsync_interval, vsync_interval/(hsync_interval+0.0)
        pass
    def check_config_with_analysis_vsync(self, config, analysis ):
        vsync_interval = None
        last_sync = None
        for (s,e) in analysis["vsync"]:
            if last_sync is None:
                last_sync = s
                pass
            elif vsync_interval is None:
                vsync_interval = s-last_sync
                pass
            elif (s-last_sync) != vsync_interval:
                self.failtest(0,"Vsync interval change - got %d (%f) expected %d (%f)"%(s-last_sync, (s-last_sync+0.0)/config.h_total, vsync_interval, (vsync_interval+0.0)/config.h_total))
                pass
            last_sync = s
            if e==0: continue
            if (e-s) != config.h_total * config.v_sync_width:
                self.failtest(0,"Vsync mismatch - got %d expected %d"%(e-s,config.h_total * config.v_sync_width))
                pass
            pass
        if vsync_interval != config.h_total * config.v_total:
            self.failtest(0,"Vsync interval mismatch - got %d expected %d"%(vsync_interval,config.h_total * config.v_total))
            pass
        return vsync_interval
    def check_config_with_analysis_hsync(self, config, analysis ):
        hsync_interval = None
        last_sync = None
        for (s,e) in analysis["hsync"]:
            if last_sync is None:
                last_sync = s
                pass
            elif hsync_interval is None:
                hsync_interval = s-last_sync
                pass
            elif (s-last_sync) != hsync_interval:
                self.failtest(0,"Hsync interval change - got %d expected %d"%(s-last_sync, hsync_interval))
                pass
            last_sync = s
            if e==0: continue
            if (e-s) != config.h_sync_width:
                self.failtest(0,"Hsync mismatch - got %d expected %d"%(e-s,config.h_sync_width))
                pass
            pass
        if hsync_interval != config.h_total:
            self.failtest(0,"Hsync interval mismatch - got %d expected %d"%(hsync_interval,config.h_total))
            pass
        return hsync_interval
        
class c_6845_trace(object):
    def __init__(self):
        self.data = []
        pass
    def add_data(self, data):
        self.data.append(data)
        pass
    def analyze_pulses(self, index):
        last_v = 0
        pulses = []
        for i in range(len(self.data)):
            v = self.data[i][index]
            if v==1 and last_v==0:
                pulses.append((i,0))
                pass
            if v==0 and last_v==1:
                start = pulses[-1][0]
                pulses[-1] = (start, i)
                pass
            last_v = v
            pass
        return pulses
    def analyze(self):
        self.analysis = {}
        self.analysis["vsync"]   = self.analyze_pulses(index=0)
        self.analysis["hsync"]   = self.analyze_pulses(index=1)
        self.analysis["display"] = self.analyze_pulses(index=2)
        return self.analysis
    def __repr__(self):
        self.analyze()
        r  = "vsync:%s\n"  %(str(self.analysis["vsync"]))
        r += "hsync:%s\n"  %(str(self.analysis["hsync"]))
        r += "display:%s\n"%(str(self.analysis["display"]))
        return r

#c th_6845_pixels
class th_6845_pixels(th_interacting):
    #f run
    def run(self):
        th_interacting.th_interacting_init(self, th_master=False)
        self.bfm_wait(5) # to get past reset... :-)
        self.th_interact_wait_for_request()
        self.bfm_wait(10)
        self.ios.crtc_clock_enable.drive(1)
        self.bfm_wait(10)
        while self.ios.vsync.value()==0:
            self.bfm_wait(1)
            pass
        sig_trace = c_6845_trace()
        vsync_rising_edges = 0
        last_vsync = 0
        while vsync_rising_edges<10:
            signals = (self.ios.vsync.value(),
                       self.ios.hsync.value(),
                       self.ios.de.value(),
                       self.ios.cursor.value(),
                       self.ios.ma.value(),
                       self.ios.ra.value(),
                       )
            sig_trace.add_data(signals)
            if (self.ios.vsync.value()==1) and (last_vsync==0):
                vsync_rising_edges = vsync_rising_edges + 1
                pass
            last_vsync = self.ios.vsync.value()
            self.bfm_wait(1)
            pass
        self.bfm_wait(10)
        self.ios.crtc_clock_enable.drive(0)
        self.hw.config_sig_trace = sig_trace
        self.th_interact_request()
        self.passtest(0,"")
        pass

#c th_8271_bus
class th_8271_bus(th_int_bus):
    #b Registers
    registers = {"command":    0,
                 "status":     0,
                 "parameter":  1,
                 "result":     1,
                 "reset":      2,
                 }
    #b write_register
    def write_register(self, register, value):
        self.bus_write(self.registers[register],value)
        pass
    #b read_register
    def read_register(self, register):
        return self.bus_read(self.registers[register])
    #f wait_for_command_done
    def wait_for_command_done(self, delay=10):
        while True:
            if self.ios.nmi.value()==0:
                self.nmi_data.append(self.data_ack())
                pass
            s = self.read_register("status") & 0xc0
            if s==0: return
            self.bfm_wait(delay)
            pass
        pass
    #f wait_for_parameter_empty
    def wait_for_parameter_empty(self, delay=10):
        while True:
            s = self.read_register("status") & 0x20
            if s==0: return
            self.bfm_wait(delay)
            pass
        pass
    #f perform_command
    def perform_command(self, command, parameters):
        print self.ios.cdlsim_sim.global_cycle(),": Command start",command,parameters
        self.nmi_data = []
        self.wait_for_command_done()
        self.write_register("command",command)
        for p in parameters:
            self.wait_for_parameter_empty()
            self.write_register("parameter",p)
            pass
        self.wait_for_command_done()
        print self.ios.cdlsim_sim.global_cycle(),": Command complete",command,parameters
        pass
    #b run
    def run(self):
        th_int_bus.bus_init(self, "chip_select_n",0, th_master=True)
        self.ios.data_ack_n.drive(1)
        self.bfm_wait(100) # to get it to settle
        self.write_register("reset",1)
        self.bfm_wait(100)
        self.write_register("reset",0)
        step_rate = 2
        head_settling_time = 9
        index_count = 3
        head_load_time = 13
        self.write_register("command",0)
        self.perform_command( 0x35, [0x0d, step_rate, head_settling_time, (index_count<<4)|(head_load_time<<0)] )
        self.perform_command( 0x35, [0x10, 3,4,48] ) # surface 0 bad tracks and current track
        self.perform_command( 0x35, [0x10, 3,4,48] ) # surface 0 bad tracks and current track
        self.perform_command( 0x3a, [0x17, 0xc3] )   # write mode register

        self.bfm_wait(10)

        self.perform_command( 0x3d, [0x12] )
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x3d, [0x17] )
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x69, [0x0] ) # seek track 0 on select==2b01
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x69, [0x11] ) # seek track 17 on select==2b01
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x5b, [0x10,0,6] ) # read 6 ids on select==2b01
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x5b, [0x10,0,6] ) # read 6 ids on select==2b01
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x52, [0x10,1] ) # read data from track 16 sector 1
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x53, [0x0,1,(1<<5)|(2<<0)] ) # read two sectors of 256 bytes of data from track 16 sector 1
        print "Result %02x"%self.read_register("result")

        self.perform_command( 0x53, [0x1,0,(1<<5)|(10<<0)] ) # read two sectors of 256 bytes of data from track 0 sector 0
        print "Result %02x"%self.read_register("result")
        while len(self.nmi_data)>0:
            for i in range(16):
                print "%02x "%self.nmi_data.pop(0),
                pass
            print
            pass

        #self.hw.current_config = config
        #self.th_interact_request()
        #self.th_interact_wait_for_request()
        #self.check_config_with_trace(config, self.hw.config_sig_trace)
        self.passtest(0,"")
        # left horse at -5279, 5200
        # desert temple village -6980 6840 (nether fortress -860,52,860)
        # spruce village -8900, 9300 (nether -1100,49,1100)
        # edge of sea -11500, 12000
        # woodland mansion -12600 13500 (nether -1580, 77, 1693)

        # pokemon world - PC fix-er-upper at -1500, -1000
        pass
        
#c th_8271_drive
class th_8271_drive(th_interacting):
    #f run
    def run(self):
        th_interacting.th_interacting_init(self, th_master=False)
        self.bfm_wait(5) # to get past reset... :-)
        self.th_interact_wait_for_request()
        self.bfm_wait(10)
        self.passtest(0,"")
        pass

#c hw_6845
class hw_6845(pycdl.hw):
    """
    Simple instantiation of gjs6845 for unittest
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    #f __init__
    def __init__(self):

        clk_2MHz         = pycdl.clock(0, 5, 5)
        clk_1MHz_falling = pycdl.clock(0, 10, 10)
        reset_n      = pycdl.wire()

        read_not_write    = pycdl.wire()
        chip_select_n     = pycdl.wire()
        address           = pycdl.wire()
        data_in           = pycdl.wire(8)
        lpstb_n           = pycdl.wire()
        crtc_clock_enable = pycdl.wire()
        ma                = pycdl.wire(14)
        ra                = pycdl.wire(5)
        data_out          = pycdl.wire(8)
        display_enable    = pycdl.wire()
        cursor            = pycdl.wire()
        hsync             = pycdl.wire()
        vsync             = pycdl.wire()

        th_req_bus_to_pixel  = pycdl.wire()
        th_req_pixel_to_bus  = pycdl.wire()

        self.reset_driver = pycdl.timed_assign( signal      = reset_n,
                                                init_value  = 0,
                                                wait        = 193,
                                                later_value = 1 )

        hw_forces = dict( )
        hw_forces = { }

        display = pycdl.wirebundle({"clock_enable":1,
                                    "hsync":1,
                                    "vsync":1,
                                    "pixels_per_clock":3,
                                    "green":8,
                                    "red":8,
                                    "blue":8})
        self.dut = pycdl.module("crtc6845",
                                clocks = {"clk_2MHz":clk_2MHz,
                                          "clk_1MHz":clk_1MHz_falling,
                                          },
                                inputs = {"reset_n":reset_n,
                                          "read_not_write":read_not_write,
                                          "chip_select_n":chip_select_n,
                                          "rs":address,
                                          "data_in":data_in,
                                          "lpstb_n":lpstb_n,
                                          "crtc_clock_enable":crtc_clock_enable,
                                          },
                                outputs = {"data_out":data_out,
                                           "ma":ma,
                                           "ra":ra,
                                           "de":display_enable,
                                           "cursor":cursor,
                                           "hsync":hsync,
                                           "vsync":vsync,
                                           },
                                forces = hw_forces,
                                )
        self.th_pixels = th_6845_pixels(clocks = {"clk":clk_2MHz
                                        },
                              inputs = {"ma":ma,
                                        "ra":ra,
                                        "de":display_enable,
                                        "cursor":cursor,
                                        "hsync":hsync,
                                        "vsync":vsync,
                                        "th_acknowledge":th_req_bus_to_pixel,
                                        },
                              outputs = { "lpstb_n":lpstb_n,
                                          "crtc_clock_enable":crtc_clock_enable,
                                          "th_request":th_req_pixel_to_bus,
                                          },
                              )
        self.th_bus = th_6845_bus(clocks = {"clk":clk_1MHz_falling,
                                        },
                              inputs = {"data_out":data_out,
                                        "th_acknowledge":th_req_pixel_to_bus,
                                           },
                              outputs = { "read_not_write":read_not_write,
                                          "chip_select_n":chip_select_n,
                                          "address":address,
                                          "data_in":data_in,
                                          "th_request":th_req_bus_to_pixel,
                                          },
                              )
        self.th_bus.hw    = self
        self.th_pixels.hw = self
        thread_mapping = None
        pycdl.hw.__init__(self,
                          thread_mapping=thread_mapping,
                          children=[self.dut,
                                    self.th_pixels,
                                    self.th_bus,
                                    clk_2MHz,
                                    clk_1MHz_falling,
                                    self.reset_driver],
                          )
        self.wave_hierarchies = [self.dut, self.th_bus, self.th_pixels]
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        pass
    #f check_pass
    def check_pass(self, data):
        pass


#c hw_8271
class hw_8271(pycdl.hw):
    """
    Simple instantiation of gjs8271 for unittest
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    #f __init__
    def __init__(self):

        clk          = pycdl.clock(0, 5, 5)
        reset_n      = pycdl.wire()

        chip_select_n     = pycdl.wire()
        read_n            = pycdl.wire()
        write_n           = pycdl.wire()
        address           = pycdl.wire(2)
        data_in           = pycdl.wire(8)
        data_out          = pycdl.wire(8)

        data_ack_n        = pycdl.wire()
        ready             = pycdl.wire(2)
        track_0_n         = pycdl.wire()
        write_protect_n   = pycdl.wire()
        index_n           = pycdl.wire()

        nmi               = pycdl.wire()

        th_req_bus_to_drive  = pycdl.wire()
        th_req_drive_to_bus  = pycdl.wire()

        self.reset_driver = pycdl.timed_assign( signal      = reset_n,
                                                init_value  = 0,
                                                wait        = 193,
                                                later_value = 1 )

        hw_forces = dict( )
        hw_forces = { }

        bbc_drive_op = pycdl.wirebundle({"sector_id":{"deleted_data":1,
                                                      "bad_data_crc":1,
                                                      "bad_crc":1,
                                                      "sector_length":2,
                                                      "sector_number":6,
                                                      "head":1,
                                                      "track":7,
                                                      },
                                         "write_sector_id_enable":1,
                                         "write_data":32,
                                         "write_data_enable":1,
                                         "read_data_enable":1,
                                         "next_id":1,
                                         "step_in":1,
                                         "step_out":1,
                                         })
        bbc_drive_response = pycdl.wirebundle({"sector_id":{"deleted_data":1,
                                                      "bad_data_crc":1,
                                                      "bad_crc":1,
                                                      "sector_length":2,
                                                      "sector_number":6,
                                                      "head":1,
                                                      "track":7,
                                                      },
                                               "index":1,
                                               "sector_id_valid":1,
                                               "read_data_valid":1,
                                               "read_data":32,
                                               "track_zero":1,
                                               "disk_ready":1,
                                               "write_protect":1,
                                         })
        self.dut = pycdl.module("fdc8271",
                                clocks = {"clk":clk,
                                          },
                                inputs = {"reset_n":reset_n,
                                          "read_n":read_n,
                                          "write_n":write_n,
                                          "chip_select_n":chip_select_n,
                                          "address":address,
                                          "data_in":data_in,
                                          "data_ack_n":data_ack_n,
                                          "ready":ready,
                                          "track_0_n":track_0_n,
                                          "write_protect_n":write_protect_n,
                                          "index_n":index_n,
                                          "bbc_floppy_response":bbc_drive_response,
                                          },
                                outputs = {"data_out":data_out,
                                            "irq_n":nmi,
                                          "bbc_floppy_op":bbc_drive_op,
                                           },
                                forces = hw_forces,
                                )
        self.th_drive= pycdl.module("bbc_floppy",
                                    clocks = {"clk":clk,
                                               },
                                     inputs = {"floppy_op":bbc_drive_op,
                                               #"th_acknowledge":th_req_bus_to_drive,
                                               },
                                     outputs = { "floppy_response":bbc_drive_response,
                                                 # "th_request":th_req_drive_to_bus,
                                                 },
                                     )
        self.th_bus = th_8271_bus(clocks = {"clk":clk,
                                        },
                              inputs = {"data_out":data_out,
                                        "nmi":nmi,
                                        },
                              outputs = { "read_n":read_n,
                                          "write_n":write_n,
                                          "chip_select_n":chip_select_n,
                                          "address":address,
                                          "data_in":data_in,
                                          "data_ack_n":data_ack_n,
                                          "ready":ready,
                                          "track_0_n":track_0_n,
                                          "write_protect_n":write_protect_n,
                                          "index_n":index_n,
                                          "th_request":th_req_bus_to_drive,
                                          },
                              )
        self.th_bus.hw    = self
        self.th_drive.hw = self
        thread_mapping = None
        pycdl.hw.__init__(self,
                          thread_mapping=thread_mapping,
                          children=[self.dut,
                                    self.th_drive,
                                    self.th_bus,
                                    clk,
                                    self.reset_driver],
                          )
        self.wave_hierarchies = [self.dut,
                                 self.th_bus,
                                 self.th_drive,
                                 ]
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        pass
    #f check_pass
    def check_pass(self, data):
        pass

