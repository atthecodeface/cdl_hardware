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
import structs
import math
from clock_timer import clock_timer_adder_bonus, clock_timer_period
#a Useful functions
def find_fractions_for(ns):
    adder_ns = int(ns*16)
    print "adder (%d,%d"%(adder_ns%16, adder_ns/16)
    for j in range(255):
        i = j+1
        d = int((ns*16-adder_ns)*i)
        print i, d, "(%d,%d)"%(i-d,i), (25+d/(i+0.))/16, "(%d,%d)"%(i-d-1,i), (25+(d+1)/(i+0.))/16
        pass
    pass
#find_fractions_for(1.6)
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

def signed32(n):
    if (n>>31)&1:
        n = (((-1) &~ 0x7fffffff) | n)
        pass
    return n

#a Globals
riscv_regression_dir      = "../riscv_tests_built/isa/"
riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"

#a Test classes
#c c_clocking_phase_measure_test_base
class c_clocking_phase_measure_test_base(simple_tb.base_th):
    verbose = False
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c c_clocking_phase_measure_test_0
class c_clocking_phase_measure_test_0(c_clocking_phase_measure_test_base):
    def wait_for_delay(self):
        toggle = 0
        if self.delay in self.stable_values:
            self.sync_value = self.stable_values[self.delay]
        else:
            toggle = 1
            pass
        while self.delay_config_cpm__op.value()!=1:
            self.sync_value = self.sync_value ^ toggle
            self.delay_response__sync_value.drive(self.sync_value)
            if self.measure_response__valid.value():
                return True
            self.bfm_wait(1)
            pass
        self.measure_request__valid.drive(0)
        self.delay_response__op_ack.drive(1)
        self.bfm_wait(1)
        self.delay_response__op_ack.drive(0)
        self.bfm_wait(4)
        self.delay = self.delay_config_cpm__value.value()
        return False
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        self.stable_values = {0:0,1:0,2:0,
                              31:1,32:1,33:1,34:1,35:1,
                              66:0,67:0,68:0,69:0,70:0,
                              101:1,102:1,103:1,104:1}
        self.delay = 0
        self.sync_value = 0
        failures = 0
        self.measure_request__valid.drive(1)
        self.wait_for_delay()
        self.measure_request__valid.drive(0)
        while True:
            if self.wait_for_delay():
                break
            pass

        result = { "initial_value":self.measure_response__initial_value.value(),
                   "initial_delay":self.measure_response__initial_delay.value(),
                   "delay":self.measure_response__delay.value(),
                   }
        self.compare_expected("initial value", 1,  result["initial_value"])
        self.compare_expected("initial delay", 31, result["initial_delay"])
        self.compare_expected("delay",         35, result["delay"])
        self.bfm_wait(10)
        self.measure_request__valid.drive(1)
        self.bfm_wait(self.run_time_remaining())
        if failures==0:
            self.passtest(self.global_cycle(),"Ran okay")
            pass
        else:
            self.failtest(self.global_cycle(),"Failed")
            pass
        self.finishtest(0,"")
        pass

#c c_clocking_eye_tracking_test_base
class c_clocking_eye_tracking_test_base(c_clocking_phase_measure_test_base):
    pass
#c c_clocking_eye_tracking_test_0
class c_clocking_eye_tracking_test_0(c_clocking_eye_tracking_test_base):
    phase_width = 73
    eye_center  = int(phase_width*2.2)
    eye_width = phase_width/2
    #f update_random_data
    def update_random_data(self):
        self.random_data = (self.random_data>>4) | ((self.random_data*0xfedcaf81) & 0xf00000000000)
        pass
    #f find_data_quality
    def find_data_quality(self, delay):
        phases = (delay - self.eye_center + 4*self.phase_width + self.phase_width/2) / self.phase_width
        dist = (delay - self.eye_center + self.phase_width) % self.phase_width
        if dist>self.phase_width/2: # -pw/2 to +pw/2
            dist -= self.phase_width
            pass
        dist = abs(dist) # 0 to +pw/2
        err = dist - self.eye_width/2
        if err<=0:
            quality=1
            pass
        else:
            quality = math.pow(err,-0.3)
            pass
        #print delay, self.eye_center, self.phase_width, dist, err, phases, quality
        return (phases,quality)
    #f data_of_quality
    def data_of_quality(self, quality, step=17):
        (phases, quality) = quality
        data = self.random_data >> phases
        if quality>0.99:
            data = data & 0x1f
        elif (quality>0.75):
            if ((data>>step)&7)==7: data = data>>1
            pass
        elif (quality>0.5):
            if ((data>>step)&3)==3: data = data>>1
            pass
        else:
            data = data ^ (data>>step)
            pass
        return data
    #f eye_track_bfam_wait
    def eye_track_bfm_wait(self, cycles):
        for i in range(cycles):
            if self.eye_track_response__eye_data_valid.value():
                self.eye_track_measure_complete = True
                pass
            self.bfm_wait(1)
            pass
        pass
    #f feed_data_after_delay
    def feed_data_after_delay(self):
        while self.delay_config_cet__op.value()==0:
            self.bfm_wait(1)
            pass
        delay_value = self.data_delay
        if self.delay_config_cet__select.value(): delay_value = self.tracking_delay
        if self.delay_config_cet__op.value()==1:  delay_value = self.delay_config_cet__value.value()
        elif self.delay_config_cet__op.value()==3: delay_value -= 1
        elif self.delay_config_cet__op.value()==2: delay_value += 1
        if self.delay_config_cet__select.value():
            self.tracking_delay = delay_value
            pass
        else:
            self.data_delay = delay_value
            print "Set data_delay to ",delay_value
            pass
        self.bfm_wait(10)
        self.delay_response__op_ack.drive(1)
        self.bfm_wait(1)
        self.delay_response__op_ack.drive(0)
        data_quality     = self.find_data_quality(self.data_delay)
        tracking_quality = self.find_data_quality(self.tracking_delay)
        for i in range(200):
            data_p = self.data_of_quality(data_quality,     step=17)
            data_n = self.data_of_quality(tracking_quality, step=23)
            self.update_random_data()
            self.data_p_in.drive(data_p&0xf)
            self.data_n_in.drive(data_n^0xf)
            self.eye_track_bfm_wait(1)
            if self.eye_track_measure_complete:
                self.eye_track_request__measure.drive(0)
                return
            pass
        pass
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        failures = 1
        self.data_delay = 0
        self.tracking_delay = 0
        self.random_data = 0xf1723622
        print "Eye %d to %d, center %d"%(self.eye_center-self.eye_width/2, self.eye_center+self.eye_width/2, self.eye_center)
        self.bfm_wait(10)
        self.eye_track_request__enable.drive(1)
        self.eye_track_request__track_enable.drive(1)
        self.eye_track_request__seek_enable.drive(1)
        self.eye_track_request__min_eye_width.drive(16)
        self.eye_track_request__phase_width.drive(self.phase_width)
        self.bfm_wait(10)
        self.eye_track_measure_complete = False            
        self.feed_data_after_delay()
        for i in range(50):
            self.eye_track_request__measure.drive(1)
            self.eye_track_measure_complete = False            
            while not self.eye_track_measure_complete:
                self.feed_data_after_delay()
                pass
            pass
        self.bfm_wait(self.run_time_remaining())
        self.eye_track_request__enable.drive(0)
        self.bfm_wait(1)
        if failures==0:
            self.passtest(self.global_cycle(),"Ran okay")
            pass
        else:
            self.failtest(self.global_cycle(),"Failed")
            pass
        self.finishtest(0,"")
        pass

#c c_clock_timer_test_base
class c_clock_timer_test_base(simple_tb.base_th):
    """
    Find a slightly slower bonus fraction for 1.6ns
    """
    master_adder = (1,0)
    master_bonus = (0,0)
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(1.6)
    slave_lock = False
    lock_window_lsb = 6
    hw_clk = "clk"
    #f configure_master
    def configure_master(self, adder, bonus=(0,0)):
        self.master_timer_control__bonus_subfraction_sub.drive(bonus[1])
        self.master_timer_control__bonus_subfraction_add.drive(bonus[0])
        self.master_timer_control__fractional_adder.drive(adder[1])
        self.master_timer_control__integer_adder.drive(adder[0])
        self.master_timer_control__reset_counter.drive(1)
        self.master_timer_control__enable_counter.drive(0)
        print "Master configured for %fns %fMHz"%(clock_timer_period(adder, bonus),1000.0/clock_timer_period(adder, bonus))
        pass
    #f configure_slave
    def configure_slave(self, adder, bonus=(0,0), lock=False):
        self.slave_timer_control__bonus_subfraction_sub.drive(bonus[1])
        self.slave_timer_control__bonus_subfraction_add.drive(bonus[0])
        self.slave_timer_control__fractional_adder.drive(adder[1])
        self.slave_timer_control__integer_adder.drive(adder[0])
        self.slave_timer_control__reset_counter.drive(1)
        self.slave_timer_control__enable_counter.drive(0)
        print "Slave configured for %fns %fMHz"%(clock_timer_period(adder, bonus),1000.0/clock_timer_period(adder, bonus))
        if lock:
            self.master_timer_control__lock_to_master.drive(1)
            self.master_timer_control__lock_window_lsb.drive({4:0,6:1,8:2,10:3}[self.lock_window_lsb])
            pass
        else:
            self.master_timer_control__lock_to_master.drive(0)
            pass
        pass
    pass
#c c_clock_timer_test_master_0
class c_clock_timer_test_master_0(c_clock_timer_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        self.configure_master( adder=self.master_adder )
        self.bfm_wait(40)
        self.master_timer_control__reset_counter.drive(0)
        self.bfm_wait(40)
        self.master_timer_control__enable_counter.drive(1)
        self.bfm_wait(1000)
        master = self.master_timer_value__value.value()
        if (master<990) or (master>1010):
            self.failtest(0,"Master clock %d out of range 990 to 1010"%master)
        self.finishtest(0,"")
        pass
    pass

#c c_clock_timer_test_master_sync_0
class c_clock_timer_test_master_sync_0(c_clock_timer_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        self.configure_master( adder=self.master_adder )
        self.bfm_wait(40)
        self.master_timer_control__reset_counter.drive(0)
        self.bfm_wait(40)
        self.master_timer_control__enable_counter.drive(1)
        self.bfm_wait(100)
        self.master_timer_control__synchronize.drive(3)
        self.master_timer_control__synchronize_value.drive(0x123456789abcdef0)
        self.bfm_wait(1)
        self.master_timer_control__synchronize.drive(0)
        self.bfm_wait(1000)
        master = self.master_timer_value__value.value() - 0x123456789abcdef0
        if (master<990) or (master>1010):
            self.failtest(0,"Master clock %d out of range 990 to 1010"%master)
        self.finishtest(0,"")
        pass
    pass

#c c_clock_timer_test_master_sync_1
class c_clock_timer_test_master_sync_1(c_clock_timer_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        self.configure_master( adder=self.master_adder )
        self.bfm_wait(40)
        self.master_timer_control__reset_counter.drive(0)
        self.bfm_wait(40)
        self.master_timer_control__enable_counter.drive(1)
        self.bfm_wait(100)
        self.master_timer_control__synchronize.drive(1)
        self.master_timer_control__synchronize_value.drive(0x123456789abcdef0)
        self.bfm_wait(1)
        self.master_timer_control__synchronize.drive(0)
        self.bfm_wait(1000)
        master = self.master_timer_value__value.value() - 0x9abcdef0
        if (master<990) or (master>1010):
            self.failtest(0,"Master clock %d out of range 990 to 1010"%master)
        self.finishtest(0,"")
        pass
    pass

#c c_clock_timer_test_master_sync_2
class c_clock_timer_test_master_sync_2(c_clock_timer_test_base):
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)
        self.configure_master( adder=self.master_adder )
        self.bfm_wait(40)
        self.master_timer_control__reset_counter.drive(0)
        self.bfm_wait(40)
        self.master_timer_control__enable_counter.drive(1)
        self.bfm_wait(100)
        self.master_timer_control__synchronize.drive(2)
        self.master_timer_control__synchronize_value.drive(0x123456789abcdef0)
        self.bfm_wait(1)
        self.master_timer_control__synchronize.drive(0)
        self.bfm_wait(1000)
        master = self.master_timer_value__value.value() - 0x1234567800000000
        if (master<1090) or (master>1110):
            self.failtest(0,"Master clock %d out of range 1090 to 1110"%master)
        self.finishtest(0,"")
        pass
    pass

#c c_clock_timer_test_master_slave_base
class c_clock_timer_test_master_slave_base(c_clock_timer_test_base):
    max_diff = 8
    master_sync = None
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(100)
        simple_tb.base_th.run_start(self)

        self.configure_master( adder=self.master_adder, bonus=self.master_bonus )
        self.configure_slave( adder=self.slave_adder, bonus=self.slave_bonus, lock=self.slave_lock )
        self.bfm_wait(200)
        self.slave_timer_control__reset_counter.drive(0)
        self.master_timer_control__reset_counter.drive(0)
        self.bfm_wait(200) # For a slow clock period
        self.slave_timer_control__enable_counter.drive(1)
        self.master_timer_control__enable_counter.drive(1)
        if self.master_sync is not None:
            self.bfm_wait(500)
            self.master_timer_control__synchronize.drive(3)
            self.master_timer_control__synchronize_value.drive(self.master_sync)
            self.bfm_wait(1)
            self.master_timer_control__synchronize.drive(0)
            pass
        self.bfm_wait(self.run_time_remaining())
        master = self.master_timer_value__value.value()
        slave = self.slave_timer_value__value.value()
        diff = abs(master-slave)
        print "Difference in master/slave clocks is %d"%diff
        if diff>self.max_diff:
            self.failtest(0,"Difference in times is more than %d (%d) (%08x to %08x) - should have locked"%
                          (self.max_diff, diff, master, slave))
        master_sec  = self.master_timer_sec_nsec__sec.value()
        master_nsec = self.master_timer_sec_nsec__nsec.value()
        master_sec_nsec = master_sec*(10**9)+master_nsec
        if master_nsec>10**9:
            self.failtest(0,"Master_nsec should be less than 1000,000,000 (%d)"%
                          (master_nsec))
        diff = master - master_sec_nsec
        if diff>2:
            self.failtest(0,"Difference in sec/nsec and actual timer is more than 2 (%d) (%08x to %08x)"%
                          (diff, master, master_sec_nsec))
        slave_sec  = self.slave_timer_sec_nsec__sec.value()
        slave_nsec = self.slave_timer_sec_nsec__nsec.value()
        slave_sec_nsec = slave_sec*(10**9)+slave_nsec
        if slave_nsec>10**9:
            self.failtest(0,"Slave_nsec should be less than 1000,000,000 (%d)"%
                          (slave_nsec))
        diff = slave - slave_sec_nsec
        if diff>self.slave_adder[0]+1:
            self.failtest(0,"Difference in sec/nsec and actual timer is more than %d (%d) (%08x to %08x)"%
                          (self.slave_adder[0]+1, diff, slave, slave_sec_nsec))
        self.finishtest(0,"")
        pass
    pass

#c c_clock_timer_test_master_slave_0
class c_clock_timer_test_master_slave_0(c_clock_timer_test_master_slave_base):
    pass
    
#c c_clock_timer_test_master_slave_1
class c_clock_timer_test_master_slave_1(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(1.6002)
    slave_lock=True
    lock_window_lsb = 4
    max_diff = 2  # 600MHz
    pass

#c c_clock_timer_test_master_slave_2
class c_clock_timer_test_master_slave_2(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(1.5998)
    slave_lock=True
    lock_window_lsb = 4
    max_diff = 2  # 600MHz
    pass

#c c_clock_timer_test_master_slave_3
class c_clock_timer_test_master_slave_3(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(1.599)
    slave_lock = True
    lock_window_lsb = 4
    max_diff = 2 # 600MHz
    pass

#c c_clock_timer_test_master_slave_4
class c_clock_timer_test_master_slave_4(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(1.599)
    slave_lock = True
    master_sync = ((10**9)*0xfeedbeef) - 1000
    lock_window_lsb = 4
    max_diff = 2 # 600MHz
    pass

#c c_clock_timer_test_master_slave_5
class c_clock_timer_test_master_slave_5(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(10.0)
    slave_lock = True
    master_sync = ((10**9)*0xfeedbeee) - 1000
    lock_window_lsb = 6
    max_diff = 10 # 100MHz
    pass

#c c_clock_timer_test_master_slave_6
class c_clock_timer_test_master_slave_6(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(100.1)
    slave_lock = True
    master_sync = 0xdeadbeefcafef00d
    lock_window_lsb = 8
    max_diff = 100 # 10MHz
    # In theory this may not work - as the edge detection is too frequent
    # And indeed it does not, except that we have oversped the clock by 1/1600
    # and this helps catch up with the initial delay in synchronization
    pass

#c c_clock_timer_test_master_slave_7
class c_clock_timer_test_master_slave_7(c_clock_timer_test_master_slave_base):
    (slave_adder, slave_bonus) = clock_timer_adder_bonus(100.0)
    slave_lock = True
    master_sync = 0xdeadbeefcafef00d
    lock_window_lsb = 10
    max_diff = 100 # 10MHz
    pass

#a Hardware classes
#c clocking_test_hw
class clocking_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of clocking testbench
    """
    loggers = {#"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    bit_delay_config        = pycdl.wirebundle(structs.bit_delay_config)
    bit_delay_response      = pycdl.wirebundle(structs.bit_delay_response)
    phase_measure_request   = pycdl.wirebundle(structs.phase_measure_request)
    phase_measure_response  = pycdl.wirebundle(structs.phase_measure_response)
    eye_track_request   = pycdl.wirebundle(structs.eye_track_request)
    eye_track_response  = pycdl.wirebundle(structs.eye_track_response)

    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(phase_measure_request._name_list("measure_request")) + " " +
                                " ".join(bit_delay_response._name_list("delay_response")) + " " +
                                " ".join(eye_track_request._name_list("eye_track_request")) + " " +
                                " data_p_in[4]"+
                                " data_n_in[4]"+
                                " "),
                  "th.inputs":(" ".join(phase_measure_response._name_list("measure_response")) + " " +
                                " ".join(eye_track_response._name_list("eye_track_response")) + " " +
                               " ".join(bit_delay_config._name_list("delay_config_cpm")) + " " +
                               " ".join(bit_delay_config._name_list("delay_config_cet")) + " " +
                               " "),
                  }
    module_name = "tb_clocking"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#c clock_timer_test_hw
class clock_timer_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of clock_timer testbench
    """
    system_clock_half_period = 5
    loggers = {"async": {"verbose":0, "filename":"ckts.log", "modules":("dut.ckts "),},
               }
    timer_control      = pycdl.wirebundle(structs.timer_control)
    timer_value        = pycdl.wirebundle(structs.timer_value)
    timer_sec_nsec     = pycdl.wirebundle(structs.timer_sec_nsec)

    th_forces = { "th.clock":"clk",
                  "th.outputs":(" ".join(timer_control._name_list("master_timer_control")) + " " +
                                " ".join(timer_control._name_list("slave_timer_control")) + " " +
                                " "),
                  "th.inputs":(" ".join(timer_value._name_list("master_timer_value")) + " " +
                               " ".join(timer_value._name_list("slave_timer_value")) + " " +
                               " ".join(timer_sec_nsec._name_list("master_timer_sec_nsec")) + " " +
                               " ".join(timer_sec_nsec._name_list("slave_timer_sec_nsec")) + " " +
                               " "),
                  }
    module_name = "tb_clock_timer"
    clocks = { "clk":(0,5,5),
               "slave_clk":(3,8,8),
               }
    #f __init__
    def __init__(self, test, slave_period=None):
        if slave_period is not None:
            self.clocks = { "clk":(0,5,5), "slave_clk":(3,slave_period/2,slave_period/2),
               }
            pass
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c clocking_phase_measure
class clocking_phase_measure(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(clocking_test_hw(c_clocking_phase_measure_test_0()), num_cycles=10000)
        pass
    pass

#c clocking_eye_tracking
class clocking_eye_tracking(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(clocking_test_hw(c_clocking_eye_tracking_test_0()), num_cycles=400000)
        pass
    pass
#c clock_timer
class clock_timer(simple_tb.base_test):
    def test_master_0(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_0()), num_cycles=12000)
        pass
    def test_master_sync_0(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_sync_0()), num_cycles=20000)
        pass
    def test_master_sync_1(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_sync_1()), num_cycles=20000)
        pass
    def test_master_sync_2(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_sync_2()), num_cycles=20000)
        pass
    def test_master_slave_0(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_0()), num_cycles=200000)
        pass
    def test_master_slave_1(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_1()), num_cycles=5*1000*1000)
        pass
    def test_master_slave_2(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_2()), num_cycles=5*1000*1000)
        pass
    def test_master_slave_3(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_3()), num_cycles=5*1000*1000)
        pass
    def test_master_slave_4(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_4()), num_cycles=1*1000*1000)
        pass
    def test_master_slave_5(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_5(), slave_period=100), num_cycles=5*1000*1000)
        pass
    def test_master_slave_6(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_6(), slave_period=1000), num_cycles=25*1000*1000)
        pass
    def test_master_slave_7(self):
        self.do_test_run(clock_timer_test_hw(c_clock_timer_test_master_slave_7(), slave_period=1000), num_cycles=25*1000*1000)
        pass
    pass

