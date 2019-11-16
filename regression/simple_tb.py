#!/usr/bin/env python
#a Copyright
#  
#  This file 'leds.py' copyright Gavin J Stark 2017
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
import sys, os, unittest
import threading
import socket, select

#a Test classes
#c base_th
class base_th(pycdl._thfile):
    hw_clk = "clk"
    #b class thread(object):
    class thread(threading.Thread):
        name = "<give me a name>"
        def __init__(self, server):
            threading.Thread.__init__(self)
            self.server = server
            self.start_cycle = None
            self.end_cycle = None
            self.thread = None
            pass
        def start(self):
            def spawn_fn(arg_tuple):
                self.start_cycle = self.server.global_cycle()
                self.thread      = threading.current_thread()
                self.run(arg_tuple)
                self.finish()
                pass
            self.server.py.pyspawn(spawn_fn,(self,))
            pass
        def start_nonpy(self):
            self.start_cycle = self.server.global_cycle()
            self.thread      = threading.current_thread()
            threading.Thread.start(self)
            pass
        def run(self, arg_tuple):
            pass
        def finish(self):
            self.end_cycle = server.global_cycle()
            pass
        pass
    #b class tcp_server_thread
    class tcp_server_thread(thread):
        def __init__(self, server, port):
            super(base_th.tcp_server_thread, self).__init__(server)
            self.server_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_skt.bind(("localhost", port))
            self.server_skt.listen(1)
            self.server_skt.setblocking(False)
            self.client_skt = None
            self.skt_timeout = 1.0
            pass
        def update_data_to_send(self):
            return ""
        def did_send_data(self, n):
            pass
        def received_data(self, data):
            pass
        def run_poll(self, client_skt):
            print "Poll", client_skt
            return False
        def run(self, arg_tuple=None):
            done = False
            while not done:
                done = self.run_poll(self.client_skt)
                if self.client_skt is None:
                    (r,_,_) = select.select([self.server_skt],[],[],self.skt_timeout)
                    if len(r)!=0:
                        (self.client_skt, address) = self.server_skt.accept()
                        print "Accepted connection from",address
                        pass
                    pass
                else:
                    data_to_send = self.update_data_to_send()
                    w = []
                    if data_to_send!="": w=[self.client_skt]
                    (r,w,_) = select.select([self.client_skt],w,[],self.skt_timeout)
                    if len(w)>0:
                        n = self.client_skt.send(data_to_send)
                        self.did_send_data(n)
                        pass
                    if len(r)>0:
                        data = self.client_skt.recv(1024)
                        if len(data)>0:
                            self.received_data(data)
                            pass
                        else:
                            self.client_skt = None
                            pass
                        pass
                    pass
                pass
            pass

    _auto_wire_same_name = False
    #f compare_expected
    def compare_expected(self, reason, expectation, actual):
        if actual!=expectation:
            self.failtest(self.global_cycle(),"Mismatch in %s act/exp (%d/%d)"%(reason,actual,expectation))
            pass
        pass
    #f compare_expected_list
    def compare_expected_list(self, reason, expectation, actual):
        expectation = list(expectation[:])
        for t in actual:
            if len(expectation)>0:
                et = expectation.pop(0)
                if t!=et:
                    self.failtest(0,"Mismatch in %s (%d/%d)"%(reason,t,et))
                    pass
                pass
            else:
                self.failtest(0,"Unexpected %s (%d)"%(reason,t,))
                pass
            pass
        if len(expectation)>0:
            self.failtest(0,"Expected more %ss: %s"%(reason,str(expectation),))
            pass
        pass
    #f set_hw
    def set_hw(self, hw):
        self.hw = hw
        pass
    #f set_run_time
    def set_run_time(self, num_cycles):
        self.run_time = num_cycles-10
        pass
    #f run_time_remaining
    def run_time_remaining(self):
        return self.run_time-self.global_cycle()/(self.hw.clock_periods[self.hw_clk])
    #f exec_run
    def exec_run(self):
        self._th = self
        self._failtests = 0
        self.run()
        pass

    #f sim_message
    def sim_message(self):
        self.cdlsim_reg.sim_message( "sim_message_obj" )
        x = self.sim_message_obj
        #x = self._thfile.sim_message
        del self.sim_message_obj
        return x

    def bfm_wait(self, cycles):
        self.cdlsim_sim.bfm_wait(cycles)

    def spawn(self, boundfn, *args):
        self.py.pyspawn(boundfn, args)

    def global_cycle(self):
        return self.cdlsim_sim.global_cycle()

    def passtest(self, code, message):
        return self.py.pypass(code, message)

    def finishtest(self, code, message):
        if (self._failtests==0):
            return self.py.pypass(code, message)
        return

    def failtest(self, code, message):
        self._failtests = self._failtests+1
        return self.py.pyfail(code, message)

    def passed(self):
        return self.py.pypassed()

    def __init__(self, th=None):
        pycdl._thfile.__init__(self, th)
        pass
    def run_start(self):
        self.bfm_wait(1)
        self.ios = self
        pass
    pass

#a Hardware classes
#c cdl_test_hw
class cdl_test_hw(pycdl.hw):
    """
    Simple instantiation of a module with just clock and reset, and some specified th ports
    """
    wave_hierarchies = []
    th_forces = {}
    module_name = ""
    system_clock_half_period = 1
    loggers = []
    clocks = { "clk":(0,None,None)}
    #f __init__
    def __init__(self, test):
        test.set_hw(self)
        self.test = test
        self.wave_file = self.__class__.__module__+".vcd"

        self.cdl_clocks = {}
        self.clock_periods = {}
        for clk_pin in self.clocks:
            (delay, low, high) = self.clocks[clk_pin]
            if low  is None: low  = self.system_clock_half_period
            if high is None: high = self.system_clock_half_period
            self.cdl_clocks[clk_pin] = pycdl.clock(delay, low, high)
            self.clock_periods[clk_pin] = low + high
            pass

        reset_n        = pycdl.wire()

        self.drivers = [pycdl.timed_assign( signal=reset_n, init_value=0, wait=33, later_value=1),
                        ]

        hw_forces = dict(self.th_forces.items())
        hw_forces["th.object"] = test
        self.dut = pycdl.module( self.module_name,
                                 clocks = self.cdl_clocks,
                                 inputs = {"reset_n":reset_n},
                                 forces = hw_forces,
                                 )
        children = [self.dut] + self.drivers
        for clk_pin in self.cdl_clocks:
            children.append(self.cdl_clocks[clk_pin])
            pass
        for l in self.loggers:
            log_module = pycdl.module( "se_logger", options=self.loggers[l] )
            children.append(log_module)
            pass
        pycdl.hw.__init__(self,
                          thread_mapping=None,
                          children=children,
                          )
        self.wave_hierarchies = [self.dut]
        pass
    #f passed
    def passed(self):
        return self.test.passed()
    #f set_run_time
    def set_run_time(self, num_cycles):
        self.test.set_run_time(num_cycles/2/self.system_clock_half_period)
        pass

#a Simulation test classes
#c base_test
class base_test(unittest.TestCase):
    #f do_test_run
    def do_test_run(self, hw, num_cycles, num_cycles_with_waves=None):
        print >>sys.stderr, "Running %s"%(self.id(),)
        if num_cycles_with_waves is None:
            num_cycles_with_waves = num_cycles
            pass
        waves_delay = None
        if ("WAVES" in os.environ.keys()):
            waves_delay = int(os.environ["WAVES"])
            pass
        do_waves = waves_delay is not None
        if do_waves:
            waves = hw.waves()
            waves.reset()
            waves.open(hw.wave_file)
            waves.add_hierarchy(hw.wave_hierarchies)
            pass
        hw.reset()
        hw.set_run_time(num_cycles)
        if not do_waves:
            hw.step(num_cycles)
            pass
        else:
            hw.step(waves_delay)
            print "Waves enabled - running for ",num_cycles_with_waves
            waves.enable()
            hw.step(num_cycles_with_waves)
            print "Waves stopped"
            pass
        self.assertTrue(hw.passed())
        pass
    pass

