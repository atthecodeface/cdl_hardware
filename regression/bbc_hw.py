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

#c cdl_test_th
class cdl_test_th(pycdl.th):
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(1000) # to get past reset... :-)
        self.sim_msg.send_value("bbc_micro.bbc.os",9,0,0xd9f9&0x3fff,0xa2) # ldx #&0x80 to stop it having to init all memory to zero
        self.sim_msg.send_value("bbc_micro.bbc.os",9,0,0xd9fa&0x3fff,0x80) # ldx #&0x80 to stop it having to init all memory to zero
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
                self.sim_msg.send_value("bbc_micro.bbc.ram_1",8,0,0x3c00+y*40+x)
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
            

#c old_cdl_test
class old_cdl_test(pycdl.hw):
    """
    Simple instantiation of BBC micro for testing
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    #f __init__
    def __init__(self, os_rom_mif, basic_rom_mif, adfs_rom_mif, teletext_rom_mif):

        system_clock       = pycdl.clock(0, 5, 5)
        self.system_clock_div_2 = pycdl.clock(0, 10, 10)
        reset_n      = pycdl.wire()

        #self.reset_driver = pycdl.timed_assign( signal      = reset_n,
        #                                        init_value  = 0,
        #                                        wait        = 33,
        #                                        later_value = 1 )

        hw_forces = dict( )
        hw_forces = { "saa.character_rom.filename":teletext_rom_mif,
                      "saa.character_rom.verbose":0,
                      "basic.filename":basic_rom_mif,
                      "basic.verbose":0,
                      "adfs.filename":adfs_rom_mif,
                      "adfs.verbose":0,
                      "ram_0.reset_type":1,
                      "ram_0.reset_value":0,
                      "os.filename":os_rom_mif,
                      "os.verbose":0,
                      }
        keyboard_reset_n = pycdl.wire()
        display = pycdl.wirebundle({"clock_enable":1,
                                    "hsync":1,
                                    "vsync":1,
                                    "pixels_per_clock":3,
                                    "green":8,
                                    "red":8,
                                    "blue":8})
        display_sram_write = pycdl.wirebundle({"enable":1,
                                    "data":48,
                                    "address":16,
            })
        keyboard = pycdl.wirebundle({"keys_down_cols_0_to_7":64,
                                     "keys_down_cols_8_to_9":16,
                                     "reset_pressed":1,
                                     })
        csr_request = pycdl.wirebundle({"valid":1,
                                        "read_not_write":1,
                                        "select":16,
                                        "address":16,
                                        "data":32,
        })
        floppy_op = pycdl.wirebundle({"step_out":1,
                                     "step_in":1,
                                     "next_id":1,
                                     "read_data_enable":1,
                                     "write_data_enable":1,
                                     "write_data":32,
                                     "write_sector_id_enable":1,
                                     "sector_id":{"track":7,
                                                  "head":1,
                                                  "sector_number":6,
                                                  "sector_length":2,
                                                  "bad_crc":1,
                                                  "bad_data_crc":1,
                                                  "deleted_data":1,
                                                  },
                                     })
        floppy_response_dict = {"disk_ready":1,
                                           "write_protect":1,
                                           "track_zero":1,
                                           "index":1,
                                            "read_data_valid":1,
                                            "read_data":32,
                                            "sector_id_valid":1,
                                            "sector_id":{"track":7,
                                                  "head":1,
                                                  "sector_number":6,
                                                  "sector_length":2,
                                                  "bad_crc":1,
                                                  "bad_data_crc":1,
                                                  "deleted_data":1,
                                                  },
                                     }
        floppy_sram_request_dict = {"enable":1,
                                    "read_not_write":1,
                                    "address":20,
                                    "data":32,
        }
        floppy_sram_response_dict = {"ack":1,
                                     "read_data_valid":1,
                                     "read_data":32,
        }

        floppy_response = pycdl.wirebundle(floppy_response_dict)
        floppy_response2 = pycdl.wirebundle(floppy_response_dict)
        floppy_sram_request = pycdl.wirebundle(floppy_sram_request_dict)
        floppy_sram_response = pycdl.wirebundle(floppy_sram_response_dict)
        clock_status = pycdl.wirebundle({"cpu_1MHz_access":1,
                                            })
        clock_control = pycdl.wirebundle({"enable_cpu":1,
                                          "will_enable_2MHz_video":1,
                                          "enable_2MHz_video":1,
                                          "enable_1MHz_rising":1,
                                          "enable_1MHz_falling":1,
                                          "phi":2,
                                            })
        self.bbc_micro_clocking = pycdl.module("bbc_micro_clocking",
                                    clocks = {"clk":system_clock,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              "clock_status":clock_status,
                                              },
                                    outputs = {"clock_control":clock_control,
                                              },
                                               )
        self.bbc_micro = pycdl.module("bbc_micro",
                                    clocks = {"clk":system_clock,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              "clock_control":clock_control,
                                              "keyboard":keyboard,
                                               "floppy_response":floppy_response,
                                              },
                                    outputs = {"clock_status":clock_status,
                                              "display":display,
                                               "keyboard_reset_n":keyboard_reset_n,
                                               "floppy_op":floppy_op,
                                              },

                                    forces = hw_forces,
                                    )
        self.bbc_display = pycdl.module("bbc_display",
                                    clocks = {"clk":self.system_clock_div_2,
                                              },
                                    inputs = {"display_sram_write":display_sram_write,
                                              "floppy_sram_request":floppy_sram_request,
                                              },
                                    outputs = {"keyboard":keyboard,
                                               "reset_n":reset_n,
                                              "floppy_sram_response":floppy_sram_response,
                                              },
                                        #forces = display_forces,
                                    )
        self.bbc_display_sram = pycdl.module("bbc_display_sram",
                                    clocks = {"clk":self.system_clock_div_2,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              "display":display,
                                              },
                                    outputs = {"sram_write":display_sram_write,
                                              },
                                    )
        self.bbc_floppy_sram = pycdl.module("bbc_floppy_sram",
                                    clocks = {"clk":self.system_clock_div_2,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              "floppy_op":floppy_op,
                                              "csr_request":csr_request,
                                               "sram_response":floppy_sram_response,
                                              },
                                    outputs = {"floppy_response":floppy_response,
                                               "sram_request":floppy_sram_request,
                                              },
                                    )
        self.bbc_floppy = pycdl.module("bbc_floppy",
                                    clocks = {"clk":system_clock,
                                              },
                                    inputs = {"floppy_op":floppy_op,
                                              },
                                    outputs = {"floppy_response":floppy_response2,
                                              },
                                        #forces = display_forces,
                                    )
        self.th = cdl_test_th(clocks = {"clk":system_clock},inputs={},outputs={})

        self.log = pycdl.module( "se_logger",
                                 options = {"verbose":1,
                                            "filename":"itrace.log",
                                            "modules":("bbc_micro.fdc "
                                                       #"bbc_micro.main_cpu "
                                                       ),
                                            })
        thread_mapping = {"th_cpu":("bbc_micro.main_cpu",),
                          "th_rams":("bbc_micro.basic",
                                     "bbc_micro.os",
                                     "bbc_micro.ram_0",
                                     "bbc_micro.ram_1",),
                          }
        #thread_mapping = {"th_cpu":("bbc_micro",),
        #                  }
        # Currently multithreading slows down by a factor of 8 - so don't do it
        # This will be because of mutex calltime probably
        thread_mapping = None
        pycdl.hw.__init__(self,
                          thread_mapping=thread_mapping,
                          children=[self.bbc_micro,
                                    self.bbc_micro_clocking,
                                    self.bbc_display,
                                    self.bbc_display_sram,
                                    self.bbc_floppy_sram,
                                    self.bbc_floppy,
                                    self.th,
                                    self.log,
                                    self.system_clock_div_2,
                                    system_clock,
                                    #self.reset_driver,
                            ],
                          )
        #self.wave_hierarchies = [self.bbc_micro]
        #self.wave_hierarchies = [self.bbc_display_sram]
        #self.wave_hierarchies = [self.bbc_display, self.bbc_floppy_sram, self.bbc_floppy]
        self.wave_hierarchies = [self.bbc_micro_clocking]
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        pass
    #f check_memory
    def check_memory(self, expected_memory_data):
        self.sim_msg = self.th.sim_message()
        for (a,ed) in expected_memory_data:
            self.sim_msg.send_value("bbc_micro.ram_0",8,0,a)
            d = self.sim_msg.get_value(2)
            if (d!=ed):
                self.th.failtest(a,"Mismatch in data for %04x (got %02x expected %02x)"%(a,d,ed))
                pass
            pass
        pass

#c cdl_test
class cdl_test(pycdl.hw):
    """
    Simple instantiation of BBC micro for testing
    """
    wave_file = __name__+".vcd"
    wave_hierarchies = []
    floppy_sram_request_dict = {"enable":1,
                                "read_not_write":1,
                                "address":20,
                                "data":32,
    }
    floppy_sram_response_dict = {"ack":1,
                                 "read_data_valid":1,
                                 "read_data":32,
    }
    csr_request_dict = {"valid":1,
                        "read_not_write":1,
                        "select":16,
                        "address":16,
                        "data":32,
    }
    csr_response_dict = {"ack":1,
                         "read_data_valid":1,
                         "read_data":32,
    }
    sram_request_dict = {"valid":1,
                        "read_enable":1,
                        "write_enable":1,
                         "select":8,
                        "address":24,
                        "write_data":64,
    }
    sram_response_dict = {"ack":1,
                         "read_data_valid":1,
                         "read_data":64,
    }
    keyboard_dict = {"keys_down_cols_0_to_7":64,
                     "keys_down_cols_8_to_9":16,
                     "reset_pressed":1,
    }
    #f __init__
    def __init__(self, os_rom_mif, basic_rom_mif, adfs_rom_mif, teletext_rom_mif, disk_mif="disks/elite.mif"):

        system_clock   = pycdl.clock(0, 5, 5)
        video_clock    = pycdl.clock(0, 7, 7)
        self.system_clock_div_2 = pycdl.clock(0, 10, 10)
        reset_n        = pycdl.wire()

        #self.reset_driver = pycdl.timed_assign( signal      = reset_n,
        #                                        init_value  = 0,
        #                                        wait        = 33,
        #                                        later_value = 1 )

        hw_forces = dict( )
        hw_forces = { "bbc.saa.character_rom.filename":teletext_rom_mif,
                      "bbc.saa.character_rom.verbose":0,
                      "bbc.basic.filename":basic_rom_mif,
                      "bbc.basic.verbose":0,
                      "bbc.adfs.filename":adfs_rom_mif,
                      "bbc.adfs.verbose":0,
                      "bbc.ram_0.reset_type":1,
                      "bbc.ram_0.reset_value":0,
                      "bbc.os.filename":os_rom_mif,
                      "bbc.os.verbose":0,
                      "rams.floppy.filename":disk_mif,
                      "rams.os.verbose":1,
                      }
        keyboard_reset_n = pycdl.wire()
        display_sram_write = pycdl.wirebundle({"enable":1,
                                    "data":48,
                                    "address":16,
            })

        keyboard           = pycdl.wirebundle(self.keyboard_dict)
        host_sram_request  = pycdl.wirebundle(self.sram_request_dict)
        host_sram_response = pycdl.wirebundle(self.sram_response_dict)
        csr_request        = pycdl.wirebundle(self.csr_request_dict)
        csr_response       = pycdl.wirebundle(self.csr_response_dict)
        self.bbc_micro = pycdl.module("bbc_micro_with_rams",
                                    clocks = {"clk":system_clock,
                                              "video_clk":video_clock,
                                              },
                                    inputs = {"reset_n":reset_n,
                                              "host_sram_request":host_sram_request,
                                              "csr_request":csr_request,
                                              },
                                    outputs = {"display_sram_write":display_sram_write,
                                               "host_sram_response":host_sram_response,
                                               "csr_response":csr_response,
                                              },
                                      forces = hw_forces,
                                    )
        self.bbc_display = pycdl.module("bbc_display",
                                    clocks = {"clk":self.system_clock_div_2,
                                              },
                                    inputs = {"display_sram_write":display_sram_write,
                                               "host_sram_response":host_sram_response,
                                              "csr_response":csr_response,
                                              },
                                    outputs = {"reset_n":reset_n,
                                              "csr_request":csr_request,
                                              "host_sram_request":host_sram_request,
                                              },
                                        #forces = display_forces,
                                    )
        self.th = cdl_test_th(clocks = {"clk":system_clock},inputs={},outputs={})

        self.log = pycdl.module( "se_logger",
                                 options = {"verbose":1,
                                            "filename":"itrace.log",
                                            "modules":("bbc_micro.bbc.fdc "
                                                       #"bbc_micro.main_cpu "
                                                       ),
                                            })
        thread_mapping = None
        pycdl.hw.__init__(self,
                          thread_mapping=thread_mapping,
                          children=[self.bbc_micro,
                                    self.bbc_display,
                                    self.th,
                                    self.log,
                                    system_clock,
                                    self.system_clock_div_2,
                                    #self.reset_driver,
                            ],
                          )
        #self.wave_hierarchies = [self.bbc_micro]
        #self.wave_hierarchies = [self.bbc_display_sram]
        #self.wave_hierarchies = [self.bbc_display, self.bbc_floppy_sram, self.bbc_floppy]
        self.wave_hierarchies = [self.bbc_micro]
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        pass
    #f check_memory
    def check_memory(self, expected_memory_data):
        self.sim_msg = self.th.sim_message()
        for (a,ed) in expected_memory_data:
            self.sim_msg.send_value("bbc_micro.ram_0",8,0,a)
            d = self.sim_msg.get_value(2)
            if (d!=ed):
                self.th.failtest(a,"Mismatch in data for %04x (got %02x expected %02x)"%(a,d,ed))
                pass
            pass
        pass

