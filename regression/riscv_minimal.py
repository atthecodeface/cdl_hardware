#!/usr/bin/env python
#a Copyright
#  
#  This file 'riscv_minimal.py' copyright Gavin J Stark 2017
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
import sys, os, unittest, tempfile
import simple_tb
import dump
import jtag_support

#a Useful functions
def int_of_bits(bits):
    l = len(bits)
    m = 1<<(l-1)
    v = 0
    for b in bits:
        v = (v>>1) | (m*b)
        pass
    return v

def bits_of_n(nbits, n):
    bits = []
    for i in range(nbits):
        bits.append(n&1)
        n >>= 1
        pass
    return bits

#a Globals
import os
riscv_zephyr_dir          = "../riscv_tests_built/"
riscv_regression_dir      = "../riscv_tests_built/isa/"
riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"
if "RISCV_REGRESSION_DIR" in os.environ.keys():
    riscv_regression_dir      = os.environ["RISCV_REGRESSION_DIR"]+"/"
if "RISCV_ATCF_REGRESSION_DIR" in os.environ.keys():
    riscv_atcf_regression_dir      = os.environ["RISCV_ATCF_REGRESSION_DIR"]+"/build/dump/"

#a Test classes
#c c_riscv_minimal_test_base
class c_riscv_minimal_test_base(simple_tb.base_th):
    mif_filename = None
    dump_filename = None
    base_address = 0
    test_memory = "dmem"
    memory_expectation = {}
    #f get_image
    def get_image(self):
        self.mif = None
        self.test_image = dump.c_dump()
        if self.mif_filename is not None:
            f = open(self.mif_filename)
            self.test_image.load_mif(f, self.base_address, address_mask=0x7fffffff)
            f.close()
            return self.mif_filename
        f = open(self.dump_filename)
        self.test_image.load(f, self.base_address, address_mask=0x7fffffff)
        f.close()
        self.mif = tempfile.NamedTemporaryFile(mode='w')
        self.test_image.write_mif(self.mif)
        self.mif.flush()
        return self.mif.name
    #f release_image
    def release_image(self):
        if self.mif is not None:
            self.mif.close()
            self.mif = None
            pass
        del self.test_image
        pass
    #f read_memory
    def read_memory(self,memory,address):
        """
        memory should be 'imem' or 'dmem' or 'mem'
        address is word address
        """
        self.sim_msg.send_value("dut."+memory,8,0,address)
        return self.sim_msg.get_value(2)
    #f write_memory
    def write_memory(self,memory,address,data):
        """
        memory should be 'imem' or 'dmem'
        address is word address
        data is data to write
        """
        self.sim_msg.send_value("dut."+memory,9,0,address,data)
        pass
    #f check_memory
    def check_memory(self, reason):
        for a in self.memory_expectation:
            e = self.memory_expectation[a]
            address = a
            if type(a)==str:
                address = self.test_image.resolve_label(a)
                pass
            d = []
            for i in range(len(e)):
                d.append(self.read_memory(self.test_memory,address/4+i))
                pass
            self.compare_expected_list(reason+":"+str(a)+":"+str(address), e, d)
            pass
        pass
    #f run_start
    def run_start(self):
        pass
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.run_start()
        delay = self.run_time-self.global_cycle()/2 - 10
        if delay<0: delay=1
        print "%d: Waiting for test for %d cycles (run time is %d)"%(self.global_cycle(),delay,self.run_time)
        self.bfm_wait(delay)
        #self.ios.b.drive(1)
        self.check_memory("Check memory after run complete (%d)"%self.global_cycle())
        self.finishtest(0,"")
        pass

#c c_riscv_minimal_test_dump
class c_riscv_minimal_test_dump(c_riscv_minimal_test_base):
    dump_filename = riscv_regression_dir+"rv32ui-p-or.dump"
    base_address = 0x0000000
    memory_expectation = { "tohost":(1,),
                           }
    #f jtag_dm_write
    def jtag_dm_write(self, address, data, write_ir=False):
        """
        Requires the JTAG state machine to be in reset or idle.

        Writes the IR to be 'access' if required, then does the appropriate write access.
        """
        if write_ir:
            self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (dm_access)
            pass
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,((address&0xffff)<<34)|((data&0xffffffff)<<2)|(2)))
        return data

    #f jtag_dm_read_slow
    def jtag_dm_read_slow(self, address, write_ir=False):
        """
        Requires the JTAG state machine to be in reset or idle.

        Writes the IR to be 'access' if required, then does the appropriate read access; it then waits and does another operation to get the data back
        """
        if write_ir:
            self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (dm_access)
            pass
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,((address&0xffff)<<34)|(0<<2)|(1)))
        self.bfm_wait(100)
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,0))
        return int_of_bits(data)

    #f jtag_dm_read_pipelined
    def jtag_dm_read_pipelined(self, address):
        """
        Requires the JTAG state machine to be in reset or idle.

        Peforms the appropriate read access and returns the last data
        """
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,((address&0xffff)<<34)|(0<<2)|(1)))
        return int_of_bits(data)
    #f jtag_resume_riscv
    def jtag_resume_riscv(self, n=0):
        self.jtag_dm_write(0x10, 0x40000001) # Resume request (halt request removed)
        status = ((self.jtag_dm_read_slow(0x11)>>2)&0xffffffff) # Read status
        print "%d:%d: Status bit 17 resume_ack and bit 11 running_all should be set %08x"%(self.global_cycle(), n, status)
        self.jtag_dm_write(0x10, 0x00000001) # Resume request (halt request removed)
        status = ((self.jtag_dm_read_slow(0x11)>>2)&0xffffffff) # Read status
        print "%d:%d: Status bit 17 resume_ack should now be clear %08x"%(self.global_cycle(), n, status)
        pass
    #f jtag_halt_riscv
    def jtag_halt_riscv(self, n=0):
        self.jtag_dm_write(0x10, 0x80000001) # Halt request (resume request removed)
        status = ((self.jtag_dm_read_slow(0x11)>>2)&0xffffffff) # Read status
        print "%d:%d: Status bit 9 is halted_all and should be set %08x"%(self.global_cycle(), n, status)
        pass
    #f jtag_init
    def jtag_init(self):
        print "Start using JTAG"
        self.jtag_module = jtag_support.jtag_module(self.bfm_wait, self.tck_enable, self.jtag__tms, self.jtag__tdi, self.tdo, self)
        self.jtag_reset()
        self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (apb_access)
        self.jtag_dm_write(0x10, 1) # Enable
        pass
    #f jtag_start_riscv
    def jtag_start_riscv(self):
        self.jtag_dm_write(0x04, 0) # data0 = Initial PC
        self.jtag_dm_write(0x17, 0x002307b1) # Abstract command to Write data0 to DEPC
        self.jtag_resume_riscv()
        pass
    #f __init__
    def __init__(self, dump_filename, hw_cls=None, test_memory="dmem", num_cycles=1000, options={}, **kwargs):
        self.needs_jtag_startup = False
        if hasattr(hw_cls,"needs_jtag_startup") and hw_cls.needs_jtag_startup:
            self.needs_jtag_startup = True
            num_cycles += 2000
            pass
        self.dump_filename = dump_filename
        self.test_memory = test_memory
        self.num_cycles = num_cycles
        self.options = options
        c_riscv_minimal_test_base.__init__(self, **kwargs)
        pass
    #f run_start
    def run_start(self):
        if self.needs_jtag_startup:
            self.jtag_init()
            self.jtag_start_riscv()
            pass
        pass
    pass

#c c_riscv_minimal_test_dump_with_pauses
class c_riscv_minimal_test_dump_with_pauses(c_riscv_minimal_test_dump):
    num_pauses = 10
    #f __init__
    def __init__(self, num_cycles=1000, **kwargs):
        c_riscv_minimal_test_dump.__init__(self, num_cycles=num_cycles+self.num_pauses*2000, **kwargs)
        pass
    #f run_start
    def run_start(self):
        self.jtag_init()
        self.jtag_start_riscv()
        for i in range(self.num_pauses):
            delay = (i+1)*self.run_time/(self.num_pauses+1)-10-self.global_cycle()/2
            if delay<0: delay=1
            self.bfm_wait(delay)
            self.jtag_halt_riscv(i)
            self.jtag_resume_riscv(i)
            pass
        print "%d: Halt/resume completed"%(self.global_cycle())
        pass
    #f All done
    pass

#c c_riscv_minimal_test_jtag_server
class c_riscv_minimal_test_jtag_server(c_riscv_minimal_test_base):
    #f __init__
    def __init__(self, num_cycles=1000, **kwargs):
        self.num_cycles = num_cycles
        self.options = {}
        self.spawned_threads = {}
        c_riscv_minimal_test_base.__init__(self, **kwargs)
        pass
    def get_image(self):
        return ""
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        self.jtag_module = jtag_support.jtag_module(self.bfm_wait, self.tck_enable, self.jtag__tms, self.jtag__tdi, self.tdo, self)
        simple_tb.base_th.run_start(self)
        openocd = jtag_support.openocd_server(server=self, port=9999)
        openocd.start_nonpy()
        rxq = openocd.queue_recvd
        txq = openocd.queue_to_send
        self.running = True
        self.had_client = False
        def x(client_skt):
            print "RV Poll", client_skt, self.had_client, self.running
            if client_skt is None and self.had_client:
                self.running = False
            if client_skt is not None:
                self.had_client = True
            return not self.running
        openocd.run_poll = x

        while self.running:
            self.bfm_wait(100)
            if not rxq.empty():
                print "Rxq not empty"
                reply = ""
                data = rxq.get()
                print "Handling",data
                for c in data:
                    if c=='B': print "LED ON"
                    elif c=='b': print "LED OFF"
                    elif c in "rstu" : print "Do some reset thing '%s'"%c
                    elif c in "01234567":
                        c = int(c)
                        self.jtag__tdi.drive((c>>0)&1)
                        self.jtag__tms.drive((c>>1)&1)
                        self.tck_enable.drive((c>>2)&1)
                        self.bfm_wait(1)
                        self.tck_enable.drive(0)
                        self.bfm_wait(100)
                        pass
                    elif c=='R':
                        self.bfm_wait(100)
                        self.tck_enable.drive(0)
                        self.bfm_wait(1)
                        self.tck_enable.drive(0)
                        reply += "01"[self.tdo.value()]
                        pass
                    pass
                if reply!="": txq.put(reply)
                pass
            pass

        self.finishtest(0,"")
    #f All done
    pass

#c c_riscv_minimal_test_jtag_prog
class c_riscv_minimal_test_jtag_prog(c_riscv_minimal_test_dump):
    num_pauses = 10
    #f __init__
    def __init__(self, num_cycles=1000, **kwargs):
        c_riscv_minimal_test_dump.__init__(self, num_cycles=num_cycles+self.num_pauses*1800, **kwargs)
        pass
    #f run_start
    def run_start(self):
        print "Start using JTAG"
        self.jtag_module = jtag_support.jtag_module(self.bfm_wait, self.tck_enable, self.jtag__tms, self.jtag__tdi, self.tdo, self)
        self.jtag_reset()
        self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (apb_access)
        self.jtag_dm_write(0x10, 1) # Enable
        self.jtag_dm_write(0x04, 0) # data0 = Initial PC
        self.jtag_dm_write(0x17, 0x002307b1) # Abstract command to Write data0 to DEPC
        #self.jtag_dm_write(0x20, 0x12345678) # progbuf0
        self.jtag_dm_write(0x20, 0x00000133) # progbuf0
        self.jtag_dm_write(0x17, 0x00240000) # execute progbuf0
        status = ((self.jtag_dm_read_slow(0x11)>>2)&0xffffffff) # Read status
        self.jtag_dm_write(0x20, 0x00002103) # progbuf0
        self.jtag_dm_write(0x17, 0x00240000) # execute progbuf0
        pass
    #f All done
    pass

#c c_riscv_minimal_test_dump_with_debug
class c_riscv_minimal_test_dump_with_debug(c_riscv_minimal_test_dump):
    num_pauses = 10
    #f __init__
    def __init__(self, num_cycles=1000, **kwargs):
        c_riscv_minimal_test_dump.__init__(self, num_cycles=num_cycles+self.num_pauses*1830, **kwargs)
        pass
    #f run_start
    def run_start(self):
        print "Start using JTAG"
        self.jtag_module = jtag_support.jtag_module(self.bfm_wait, self.tck_enable, self.jtag__tms, self.jtag__tdi, self.tdo, self)
        self.jtag_reset()
        self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (apb_access)
        self.dm_write(0x10, 1) # Enable
        #self.dm_write(0x04, 0x1245678) # data0 = Initial PC
        #self.dm_write(0x17, 0x002307b1) # Abstract command to Write data0 to r1
        #while True:
        #    abstractcs = ((self.dm_read_slow(0x16)>>2)&0xffffffff)
        #    print "AbstractCS %08x"%abstractcs
        #    if (abstractcs & 0x1000)==0: break
        #    pass
        #self.dm_write(0x17, 0x00221001) # Abstract command to Read data0 to r1
        #while True:
        #    abstractcs = ((self.dm_read_slow(0x16)>>2)&0xffffffff)
        #    print "AbstractCS %08x"%abstractcs
        #    if (abstractcs & 0x1000)==0: break
        #    pass
        #print "Data0 %08x"%((self.dm_read_slow(0x04)>>2)&0xffffffff)
        #self.dm_write(0x17, 0x002207b1) # Abstract command to Read data0 to r1
        #while True:
        #    abstractcs = ((self.dm_read_slow(0x16)>>2)&0xffffffff)
        #    print "AbstractCS %08x"%abstractcs
        #    if (abstractcs & 0x1000)==0: break
        #    pass
        #print "Data0 %08x"%((self.dm_read_slow(0x04)>>2)&0xffffffff)

        self.dm_write(0x04, 0) # data0 = Initial PC
        self.dm_write(0x17, 0x002307b1) # Abstract command to Write data0 to DEPC
        self.resume_riscv()
        for i in range(self.num_pauses):
            delay = (i+1)*self.run_time/(self.num_pauses+1)-10-self.global_cycle()/2
            if delay<0: delay=1
            self.bfm_wait(delay)
            self.jtag_halt_riscv(i)
            self.jtag_resume_riscv(i)
            pass
        print "%d: Halt/resume completed"%(self.global_cycle())
        #self.dm_write(0x20, 0x12345678) # progbuf0
        #self.dm_write(0x17, 0x00240000) # execute progbuf0
        pass
    #f All done
    pass

#c c_riscv_minimal_test_one
class c_riscv_minimal_test_one(c_riscv_minimal_test_base):
    dump_filename = riscv_regression_dir+"rv32ui-p-or.dump"
    base_address = 0x0000000
    memory_expectation = { "tohost":(1,),
                           }
    pass

#c c_riscv_jtag_debug_base
class c_riscv_jtag_debug_base(simple_tb.base_th):
    """
    Base methods for JTAG interaction, really
    """
    #f run_start
    def run_start(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        self.jtag_module = jtag_support.jtag_module(self.bfm_wait, self.tck_enable, self.jtag__tms, self.jtag__tdi, self.tdo, self)
        simple_tb.base_th.run_start(self)
        pass
    #f dm_write
    def dm_write(self, address, data, write_ir=False):
        """
        Requires the JTAG state machine to be in reset or idle.

        Writes the IR to be 'access' if required, then does the appropriate write access.
        """
        if write_ir:
            self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (dm_access)
            pass
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,((address&0xffff)<<34)|((data&0xffffffff)<<2)|(2)))
        return data

    #f dm_read_slow
    def dm_read_slow(self, address, write_ir=False):
        """
        Requires the JTAG state machine to be in reset or idle.

        Writes the IR to be 'access' if required, then does the appropriate read access; it then waits and does another operation to get the data back
        """
        if write_ir:
            self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (dm_access)
            pass
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,((address&0xffff)<<34)|(0<<2)|(1)))
        self.bfm_wait(100)
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,0))
        return int_of_bits(data)

    #f dm_read_pipelined
    def dm_read_pipelined(self, address):
        """
        Requires the JTAG state machine to be in reset or idle.

        Peforms the appropriate read access and returns the last data
        """
        data = self.jtag_write_drs(dr_bits = bits_of_n(50,((address&0xffff)<<34)|(0<<2)|(1)))
        return int_of_bits(data)

    #f run
    def run(self):
        self.run_start()
        self.finishtest(0,"")
        pass
#c c_riscv_jtag_debug_simple
class c_riscv_jtag_debug_simple(c_riscv_jtag_debug_base):
    """
    """
    #f run
    def run(self):
        self.run_start()
        self.jtag_reset()
        self.jtag_write_irs(ir_bits = bits_of_n(5,0x11)) # Send in 0x11 (apb_access)
        print "DM control %08x"%((self.dm_read_slow(0x10)>>2)&0xffffffff)
        self.dm_write(0x10, 1) # Enable
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM control %08x"%((self.dm_read_slow(0x10)>>2)&0xffffffff)
        self.dm_write(0x10, 0x80000000) # Halt request
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        self.dm_write(0x10, 0x40000000) # Resume request (halt request removed)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        self.dm_write(0x10, 0x00000000) # Resume request removal
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        self.dm_write(0x10, 0x80010000) # Halt request for HART 1
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        self.dm_write(0x10, 0x40010000) # Resume request (halt request removed)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        self.dm_write(0x10, 0x00010000) # Resume request removal
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        print "DM status %08x"%((self.dm_read_slow(0x11)>>2)&0xffffffff)
        self.finishtest(0,"")
        pass

#a Hardware classes
#c riscv_i32_minimal_test_hw
class riscv_i32_minimal_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("a"),
                  "th.outputs":("b"),
                  }
    module_name = "tb_riscv_i32_minimal"
    #f __init__
    def __init__(self, test):
        self.num_cycles = test.num_cycles
        self.options    = test.options
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["dut.mem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c riscv_i32c_minimal_test_hw
class riscv_i32c_minimal_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("a"),
                  "th.outputs":("b"),
                  }
    module_name = "tb_riscv_i32c_minimal"
    #f __init__
    def __init__(self, test):
        self.num_cycles = test.num_cycles
        self.options    = test.options
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["dut.mem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c riscv_i32c_pipeline3_test_hw
class riscv_i32c_pipeline3_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("a"),
                  "th.outputs":("b"),
                  }
    module_name = "tb_riscv_i32c_pipeline3"
    #f __init__
    def __init__(self, test):
        self.num_cycles = test.num_cycles
        self.options    = test.options
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["imem.filename"] = mif_filename
        self.th_forces["dmem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c riscv_i32mc_pipeline3_test_hw
class riscv_i32mc_pipeline3_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench for i32mc pipeline3
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("tdo"),
                  "th.outputs":("jtag__ntrst jtag__tms jtag__tdi tck_enable" ),
                  }
    clocks = {"jtag_tck":(0,1,1),
              "clk":(0,1,1),
              }
    module_name = "tb_riscv_i32mc_pipeline3"
    #f __init__
    def __init__(self, test):
        self.num_cycles = test.num_cycles
        self.options    = test.options
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["imem.filename"] = mif_filename
        self.th_forces["dmem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c OLD riscv_minimal_single_memory_test_hw
class old_riscv_minimal_single_memory_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":("a"),
                  "th.outputs":("b"),
                  }
    module_name = "tb_riscv_minimal_single_memory"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        mif_filename = test.get_image()
        self.th_forces["mem.filename"] = mif_filename
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c riscv_jtag_debug_hw
class riscv_jtag_debug_hw(simple_tb.cdl_test_hw):
    """
    
    """
    loggers = {}
    th_forces = { "th.clock":"clk",
                  "th.inputs":("tdo"),
                  "th.outputs":("jtag__ntrst jtag__tms jtag__tdi tck_enable" ),
                  }
    module_name = "tb_riscv_jtag_debug"
    clocks = {"jtag_tck":(0,3,3),
              "apb_clock":(0,1,1),
              }
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c riscv_jtag_debug
class riscv_jtag_debug(simple_tb.base_test):
    def test_0(self):
        test = c_riscv_jtag_debug_simple()
        hw = riscv_jtag_debug_hw(test)
        self.do_test_run(hw, 100*1000)
    pass

#c riscv_base
class riscv_base(simple_tb.base_test):
    supports = []
    hw = None
    cycles_scale = 1.0
    test_memory = None
    default_test_class = c_riscv_minimal_test_dump
    @classmethod
    def add_test_fn(cls, name, dump_file, num_cycles, options):
        num_cycles = int(num_cycles * cls.cycles_scale)
        def test_fn(c):
            test_class = cls.default_test_class
            test = test_class(hw_cls        = cls,
                              dump_filename = dump_file,
                              test_memory   = cls.test_memory,
                              num_cycles    = num_cycles,
                              options       = options)
            hw = cls.hw(test)
            c.do_test_run(hw, hw.num_cycles)
            pass
        setattr(cls, "test_"+name, test_fn)
        pass

#c riscv_i32_minimal
class riscv_i32_minimal(riscv_base):
    supports = ["rv_timer"]
    hw = riscv_i32_minimal_test_hw
    test_memory = "dut.mem"
    cycles_scale = 1.0
    pass

#c riscv_i32c_minimal
class riscv_i32c_minimal(riscv_base):
    supports = ["compressed"]
    hw = riscv_i32c_minimal_test_hw
    cycles_scale = 1.3
    test_memory = "dut.mem"
    pass

#c riscv_i32c_pipeline3
class riscv_i32c_pipeline3(riscv_base):
    supports = ["compressed"]
    hw = riscv_i32c_pipeline3_test_hw
    test_memory = "dmem"
    cycles_scale = 1.5
    pass

#c riscv_i32mc_pipeline3
class riscv_i32mc_pipeline3(riscv_base):
    supports = ["compressed", "muldiv", "jtag"]
    hw = riscv_i32mc_pipeline3_test_hw
    test_memory = "dmem"
    cycles_scale = 1.5
    needs_jtag_startup = True
    default_test_class = c_riscv_minimal_test_dump_with_pauses
    #default_test_class = c_riscv_minimal_test_jtag_prog
    def openocd(self):
        test = c_riscv_minimal_test_jtag_server(100*1000*1000) #0*1000*1000)
        hw = self.hw(test)
        self.do_test_run(hw, hw.num_cycles)
    pass

#c OLD riscv_minimal_single_memory
class old_riscv_minimal_single_memory(riscv_base):
    pass

#c Add tests to riscv_i32_minimal, riscv_i32c_minimal, riscv_i32c_pipeline3, riscv_i32mc_pipeline3
riscv_atcf_zephyr = {#"zephyr":("zephyr.dump",250*1000,[]),
}
riscv_jtag_regression_tests = {#"jtag_simple":("",10*1000,["jtag"],{}),
                               }
riscv_atcf_regression_tests = {"logic":("logic.dump",50*1000,[],{}),
                               "traps":("traps.dump",10*1000,[],{}),
                               "timer_irqs":("timer_irqs.dump",40*1000,["rv_timer"],{}),
                               #"data_access":("data_access.dump",10*1000,["apb_timer"],{}),
                               "data":("data.dump",10*1000,[],{}),
                               "c_dprintf":("c_dprintf.dump",10*1000,["compressed"],{}),
                               "c_arith":("c_arith.dump",2*1000,["compressed"],{}),
                               "c_stack":("c_stack.dump",2*1000,["compressed"],{}),
                               "c_jump":("c_jump.dump",2*1000,["compressed"],{}),
                               "c_branch":("c_branch.dump",2*1000,["compressed"],{}),
                               "c_mv":("c_mv.dump",5*1000,["compressed"],{}),
                               "c_logic":("c_logic.dump",50*1000,["compressed"],{}),
                               #                               "c_temp":("c_temp.dump",5*1000,["compressed"],{}),
}
riscv_regression_tests = {"or":("rv32ui-p-or.dump",3*1000,[],{}),
         "simple":("rv32ui-p-simple.dump",3*1000,[],{}),
         "jalr":("rv32ui-p-jalr.dump",3*1000,[],{}),
         "jal":("rv32ui-p-jal.dump",3*1000,[],{}),
         "fence_i":("rv32ui-p-fence_i.dump",3*1000,["ifence"],{}), #Note that Fence does not work on the riscv_minimal as that does not have writable instruction memory
         "bne":("rv32ui-p-bne.dump",3*1000,[],{}),
         "bltu":("rv32ui-p-bltu.dump",3*1000,[],{}),
         "blt":("rv32ui-p-blt.dump",3*1000,[],{}),
         "bgeu":("rv32ui-p-bgeu.dump",3*1000,[],{}),
         "bge":("rv32ui-p-bge.dump",3*1000,[],{}),
         "beq":("rv32ui-p-beq.dump",3*1000,[],{}),
         "auipc":("rv32ui-p-auipc.dump",3*1000,[],{}),
         "andi":("rv32ui-p-andi.dump",3*1000,[],{}),
         "and":("rv32ui-p-and.dump",3*1000,[],{}),
         "addi":("rv32ui-p-addi.dump",3*1000,[],{}),
         "add":("rv32ui-p-add.dump",3*1000,[],{}),
         "sw":("rv32ui-p-sw.dump",3*1000,[],{}),
         "sltiu":("rv32ui-p-sltiu.dump",3*1000,[],{}),
         "slti":("rv32ui-p-slti.dump",3*1000,[],{}),
         "slt":("rv32ui-p-slt.dump",3*1000,[],{}),
         "slli":("rv32ui-p-slli.dump",3*1000,[],{}),
         "sll":("rv32ui-p-sll.dump",3*1000,[],{}),
         "sh":("rv32ui-p-sh.dump",3*1000,[],{}),
         "sb":("rv32ui-p-sb.dump",3*1000,[],{}),
         "ori":("rv32ui-p-ori.dump",3*1000,[],{}),
         "or":("rv32ui-p-or.dump",3*1000,[],{}),
         "lw":("rv32ui-p-lw.dump",3*1000,[],{}),
         "lui":("rv32ui-p-lui.dump",3*1000,[],{}),
         "lhu":("rv32ui-p-lhu.dump",3*1000,[],{}),
         "lh":("rv32ui-p-lh.dump",3*1000,[],{}),
         "lbu":("rv32ui-p-lbu.dump",3*1000,[],{}),
         "lb":("rv32ui-p-lb.dump",3*1000,[],{}),
         "xori":("rv32ui-p-xori.dump",3*1000,[],{}),
         "xor":("rv32ui-p-xor.dump",3*1000,[],{}),
         "sub":("rv32ui-p-sub.dump",3*1000,[],{}),
         "srli":("rv32ui-p-srli.dump",3*1000,[],{}),
         "srl":("rv32ui-p-srl.dump",3*1000,[],{}),
         "srai":("rv32ui-p-srai.dump",3*1000,[],{}),
         "sra":("rv32ui-p-sra.dump",3*1000,[],{}),
         "sltu":("rv32ui-p-sltu.dump",3*1000,[],{}),

         "div":("rv32um-p-div.dump",3*1000,["muldiv"],{}),
         "divu":("rv32um-p-divu.dump",3*1000,["muldiv"],{}),
         "rem":("rv32um-p-rem.dump",3*1000,["muldiv"],{}),
         "remu":("rv32um-p-remu.dump",3*1000,["muldiv"],{}),
         "mul":("rv32um-p-mul.dump",4*1000,["muldiv"],{}),
         "mulh":("rv32um-p-mulh.dump",3*3000,["muldiv"],{}),
         "mulhu":("rv32um-p-mulhu.dump",3*3000,["muldiv"],{}),
         "mulhsu":("rv32um-p-mulhsu.dump",3*3000,["muldiv"],{}),
           }
for (test_dir,tests) in [(riscv_zephyr_dir,riscv_atcf_zephyr),
                         (riscv_regression_dir,riscv_regression_tests),
                         (riscv_atcf_regression_dir,riscv_atcf_regression_tests),
                         (riscv_atcf_regression_dir,riscv_jtag_regression_tests)]:
    for tc in tests:
        (dump_file,num_cycles,tags,options) = tests[tc]
        dump_file = test_dir+dump_file
        for test_class in [ riscv_i32_minimal,                  
                                  riscv_i32c_minimal,             
                                  riscv_i32c_pipeline3,           
                                  riscv_i32mc_pipeline3,          
                                  ]:
            can_do = True
            for t in tags:
                if t not in test_class.supports: can_do = False
                pass
            if can_do:
                test_class.add_test_fn(name=tc, dump_file=dump_file, num_cycles=num_cycles, options=options)
                pass
        pass
    pass
