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
import simple_tb
import structs

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

#a PS2 data
ps2_key_map = {
0x111:"Alt (right)",
0x114:"Ctrl (right)",
0x11F:"Windows (left)",
0x127:"Windows (right)",
0x12F:"Menus",
0x14A:"KP/",
0x15A:"KPEnter",
0x169:"End",
0x16B:"Left Arrow",
0x16C:"Home",
0x170:"Insert",
0x171:"Delete",
0x172:"Down Arrow",
0x174:"Right Arrow",
0x175:"Up Arrow",
0x17A:"Page Down",
0x17D:"Page Up",

0x01:"F9",
0x03:"F5",
0x04:"F3",
0x05:"F1",
0x06:"F2",
0x07:"F12",
0x09:"F10",
0x0A:"F8",
0x0B:"F6",
0x0C:"F4",
0x0D:"Tab",
0x0E:"`",
0x11:"Alt (left)",
0x12:"Shift",
0x14:"Ctrl",
0x15:"Q",
0x16:"1",
0x1A:"Z",
0x1B:"S",
0x1C:"A",
0x1D:"W",
0x1E:"2",
0x21:"C",
0x22:"X",
0x23:"D",
0x24:"E",
0x25:"4",
0x26:"3",
0x29:"Spacebar",
0x2A:"V",
0x2B:"F",
0x2C:"T",
0x2D:"R",
0x2E:"5",
0x31:"N",
0x32:"B",
0x33:"H",
0x34:"G",
0x35:"Y",
0x36:"6",
0x3A:"M",
0x3B:"J",
0x3C:"U",
0x3D:"7",
0x3E:"8",
0x41:",",
0x42:"K",
0x43:"I",
0x44:"O",
0x45:"0",
0x46:"9",
0x49:".",
0x4A:"/",
0x4B:"L",
0x4C:";",
0x4D:"P",
0x4E:"-",
0x52:"'",
0x54:"[",
0x55:"=",
0x58:"Caps Lock",
0x59:"RtShift",
0x5A:"Enter",
0x5B:"]",
0x5D:"\\",
0x66:"Backspace",
0x69:"KP1",
0x6B:"KP4",
0x6C:"KP7",
0x70:"KP0",
0x71:"KP.",
0x72:"KP2",
0x73:"KP5",
0x74:"KP6",
0x75:"KP8",
0x76:"ESC",
0x77:"Num Lock",
0x78:"F11",
0x79:"KP+",
0x7A:"KP3",
0x7B:"KP-",
0x7C:"KP*",
0x7D:"KP9",
0x7E:"Scroll Lock",
0x83:"F7",
}
ps2_code_of_key = {}
for c,k in ps2_key_map.iteritems():
    ps2_code_of_key[k]=c
    pass

#a PS2 test classes
#c c_ps2_test_one
class c_ps2_test_one(simple_tb.base_th):
    keys_to_test = ( ("Q", True),
                     ("Alt (right)", False),
                     ("Q", False),
                     ("Q", True),
                     ("Q", False),
                     ("KP1", False),
                     (None, (0,0,0),),
                     (None, (0,1,1,1,1,0,0,0,0,1,1,1),),
                     (None, (0, 0,0,0,0, 0,0,1,1, 1,1),),
                     ("Page Up", True),
                     ("F9", True),
                     ("F9", False),
                     ("Spacebar", False),
                     ("Page Up", True),
                     ("F9", True),
                     ("F9", False),
                     ("Spacebar", False),
                     ("Page Up", True),
                     (None, (0,0,0),),
                     (None, 1600),
                     ("F9", True),
                     ("F9", False),
                     (None, 100),
                     ("Alt (left)", True),
                     (None, 10),
                     ("Alt (left)", False),
                     (None, 300),
                     ("Alt (left)", True),
                     (None, 510),
                     ("Alt (left)", False),
                     )
    #f drive
    def drive(self, clk, data=None):
        if data is not None:
            self.ios.ps2_out__data.drive(data)
            pass
        self.ios.ps2_out__clk.drive(clk)
        pass
    #f parity
    def parity(self,data):
        if data==0: return 1 # odd parity
        return self.parity(data>>1) ^ (data&1)
    #f ps2_data_bits
    def ps2_data_bits(self, data, delay_fn):
        self.drive(1,1)
        delay_fn()
        while len(data)>0:
            self.drive(1,data.pop(0))
            delay_fn()
            self.drive(0)
            delay_fn()
            delay_fn()
            self.drive(1)
            delay_fn()
            pass
        pass
    #f ps2_data
    def ps2_data(self, data, delay_fn, parity=0):
        data = [0] + [(data>>i)&1 for i in range(8)] + [parity ^ self.parity(data)] + [1]
        self.ps2_data_bits(data=data, delay_fn=delay_fn)
        pass
    #f ps2_key
    def ps2_key(self, key, delay_fn, down=True):
        code = ps2_code_of_key[key]
        if code&0x100:
            self.ps2_data(0xe0,delay_fn)
            pass
        if not down:
            self.ps2_data(0xf0,delay_fn)
            pass
        self.ps2_data(code & 0xff,delay_fn)
        pass
    #f run
    def run(self):
        self.cfg_divider = 3
        simple_tb.base_th.run_start(self)
        self.drive(1,1)
        self.bfm_wait(25)
        self.ios.divider.drive(self.cfg_divider)
        keys_pressed = []
        def delay(cycles=self.cfg_divider*3):
            for i in range(cycles):
                if self.ios.ps2_key__valid.value()==1:
                    code = (self.ios.ps2_key__extended.value(),
                            self.ios.ps2_key__key_number.value(),
                            self.ios.ps2_key__release.value())
                    #print >>sys.stderr, "Key valid %d %02x %d"%code
                    s = code[1]
                    if code[0]: s=s+0x100
                    if s not in ps2_key_map:
                        self.failtest(0,"Key not found in ps2_key_map"+str(s))
                        pass
                    else:
                        print >>sys.stderr, "Added key %s"%(str((not code[2],s,ps2_key_map[s]),))
                        keys_pressed.append((not code[2],s,ps2_key_map[s]))
                        pass
                    pass
                self.bfm_wait(1)
                pass
            pass
        keys_tested = []
        for (k,down) in self.keys_to_test:
            #print >>sys.stderr, "Test input",k,down
            if k is None:
                if type(down)==int:
                    delay(down*self.cfg_divider)
                    pass
                else:
                    self.ps2_data_bits(data=list(down), delay_fn=delay)
                    pass
                pass
            else:
                self.ps2_key(k, delay, down=down)
                keys_tested.append( (k,down) )
                pass
            pass
        delay()
        if (len(keys_tested) != len(keys_pressed)):
            self.failtest(0,"Mismatch in length of keys to test and keys pressed"+str((len(keys_tested),len(keys_pressed))))
        else:
            for i in range(len(keys_tested)):
                (ek,edown)  = keys_tested[i]
                (ddown,_,dk) = keys_pressed[i]
                print ek,dk,edown,ddown
                if (ek!=dk) or (edown!=ddown):
                    self.failtest(0,"Mismatch in keys tested and pressed "+str((ek,dk,edown,ddown)))
                pass
            pass
        self.finishtest(0,"")
        pass

#a I2C test classes
#c c_i2c_test_base
class c_i2c_test_base(simple_tb.base_th):
    #f i2c_wait
    def i2c_wait(self, n):
        self.bfm_wait(self.cfg_divider*n*5)
    #f i2c_idle - leaves clock high
    def i2c_idle(self):
        self.ios.i2c_out__scl.drive(1)
        self.ios.i2c_out__sda.drive(1)
        self.i2c_wait(3)
        pass
    #f i2c_start - leaves clock low
    def i2c_start(self):
        self.ios.i2c_out__sda.drive(1)
        self.ios.i2c_out__scl.drive(1)
        self.i2c_wait(1)
        self.ios.i2c_out__sda.drive(0)
        self.i2c_wait(1)
        self.ios.i2c_out__scl.drive(0)
        self.i2c_wait(1)
        pass
    #f i2c_stop - leaves bus quiescent (both high)
    def i2c_stop(self):
        self.ios.i2c_out__sda.drive(0)
        self.ios.i2c_out__scl.drive(1)
        self.i2c_wait(1)
        self.ios.i2c_out__sda.drive(1)
        self.i2c_wait(1)
        pass
    #f i2c_cont - expects clock low, leaves bus quiescent
    def i2c_cont(self):
        self.ios.i2c_out__sda.drive(1)
        self.ios.i2c_out__scl.drive(0)
        self.i2c_wait(1)
        self.ios.i2c_out__scl.drive(1)
        self.i2c_wait(1)
        pass
    #f i2c_bit_start - requires clock low, leaves clock high
    def i2c_bit_start(self, d=None):
        if d is not None:
            self.ios.i2c_out__sda.drive(d)
            self.i2c_wait(1)
            pass
        else:
            pass
        self.ios.i2c_out__scl.drive(1)
        d = self.ios.i2c_in__sda.value()
        self.i2c_wait(1)
        return d
    #f i2c_bit_stop - requires clock high, leaves clock low
    def i2c_bit_stop(self):
        self.ios.i2c_out__scl.drive(0)
        self.i2c_wait(1)
        pass
    #f i2c_ack - requires clock low, leaves clock low
    def i2c_ack(self):
        self.i2c_bit_start(0)
        self.i2c_bit_stop()
        self.ios.i2c_out__sda.drive(1)
        self.i2c_wait(1)
        pass
    #f i2c_out_byte
    def i2c_out_byte(self, data):
        bits = bits_of_n(8, data)
        bits.reverse()
        for d in bits:
            self.i2c_bit_start(d)
            self.i2c_bit_stop()
            pass
        ack = self.i2c_bit_start(None)
        self.i2c_bit_stop()
        return ack==0
    #f i2c_read_byte
    def i2c_read_byte(self, do_ack=False):
        d = []
        for i in range(8):
            d.append(self.i2c_bit_start())
            self.i2c_bit_stop()
            pass
        d.reverse()
        data = int_of_bits(d)
        if do_ack:
            self.i2c_ack()
            pass
        return data
    #f i2c_write
    def i2c_write(self, data, cont=False):
        self.i2c_start()
        for d in data:
            ack = self.i2c_out_byte(d)
            if not ack: self.failtest(self.global_cycle(),"Expected an ack")
        if cont:
            self.i2c_cont()
        else:
            self.i2c_stop()
            pass
        return
    #f i2c_read
    def i2c_read(self, data, num, cont=False):
        self.i2c_start()
        for d in data:
            ack = self.i2c_out_byte(d)
            if not ack: self.failtest(self.global_cycle(),"Expected an ack")
        data = []
        for i in range(num):
            data.append(self.i2c_read_byte(do_ack=(i<num-1)))
        if cont:
            self.i2c_cont()
        else:
            self.i2c_stop()
            pass
        return data
    #f i2c_apb_device_write
    def i2c_apb_device_write(self, address, reg, data):
        self.i2c_write(cont=False, data=[(address<<1) | 0, reg, data])
        pass
    #f i2c_apb_device_read
    def i2c_apb_device_read(self, address, reg):
        self.i2c_write(cont=True, data=[(address<<1) | 0, reg])
        return self.i2c_read(cont=False, data=[(address<<1) | 1], num=1)[0]
#c c_i2c_test_one
class c_i2c_test_one(c_i2c_test_base):
    #f run
    def run(self):
        self.cfg_divider = 3
        self.cfg_period = 2
        simple_tb.base_th.run_start(self)
        self.bfm_wait(25)
        self.i2c_idle()
        self.ios.i2c_conf_0__divider.drive(self.cfg_divider)
        self.ios.i2c_conf_0__period.drive(self.cfg_period)
        self.bfm_wait(100)
        self.i2c_write(cont=False, data=[(0x1<<1) | 0, 0x12, 0x34, 0x56, 0x78])
        self.i2c_apb_device_write(0x1b, 0, 0xf0)
        if self.i2c_apb_device_read(0x1b, 0)!=0xf0:
            self.failtest(self.global_cycle(),"Read back of GPIO did not get 0xf0 when expected")
            pass
        if self.ios.gpio_output.value()!=0xc:
            self.failtest(self.global_cycle(),"Expected GPIOs to be 0xc")
            pass
        self.i2c_apb_device_write(0x1b, 0, 0x0f)
        if self.i2c_apb_device_read(0x1b, 0)!=0x0f:
            self.failtest(self.global_cycle(),"Read back of GPIO did not get 0x0f when expected")
            pass
        if self.ios.gpio_output.value()!=0x3:
            self.failtest(self.global_cycle(),"Expected GPIOs to be 0x3")
            pass
        self.finishtest(0,"")
        pass

#c c_i2c_test_two
class c_i2c_test_two(c_i2c_test_base):
    #f i2c_do_transaction
    def i2c_do_transaction(self, i2c_data, num_out=1, num_in=0, cont=0, master=0 ):
        self.ios.master_request_0__valid.drive(1)
        self.ios.master_request_0__cont.drive(cont)
        self.ios.master_request_0__num_in.drive(num_in)
        self.ios.master_request_0__num_out.drive(num_out)
        self.ios.master_request_0__data.drive(i2c_data)
        self.bfm_wait(1)
        while self.ios.master_response_0__ack.value()==0:
            self.bfm_wait(1)
            pass
        self.ios.master_request_0__valid.drive(0)
        while self.ios.master_response_0__response_valid.value()==0:
            self.bfm_wait(1)
            pass
        response_data = self.ios.master_response_0__data.value()
        response_type = self.ios.master_response_0__response_type.value()
        return (response_type, response_data)
    #f i2c_apb_slave_write
    def i2c_apb_slave_write(self, address, data):
        i2c_data = (data<<16) | (address<<8) | (0x1b<<1) | 0
        return self.i2c_do_transaction( i2c_data, num_out=3, num_in=0, cont=0 ) 
    #f i2c_apb_slave_read
    def i2c_apb_slave_read(self, address):
        i2c_data = (address<<8) | (0x1b<<1) | 0
        (response_type, response_data) = self.i2c_do_transaction( i2c_data, num_out=2, num_in=0, cont=1 )
        if response_type==0:
            i2c_data = (0x1b<<1) | 1
            (response_type, response_data) = self.i2c_do_transaction( i2c_data, num_out=1, num_in=1, cont=0 )
            pass
        return (response_type, response_data)
    #f run
    def run(self):
        self.cfg_divider = 3
        self.cfg_period = 2
        simple_tb.base_th.run_start(self)
        self.bfm_wait(25)
        self.i2c_idle()
        self.ios.i2c_conf_0__divider.drive(self.cfg_divider)
        self.ios.i2c_conf_0__period.drive(self.cfg_period)
        self.bfm_wait(100)
        (rt, rd)=self.i2c_apb_slave_write(0, 0xf0)
        self.compare_expected("APB write of GPIO response",rt, 0)
        (rt, rd)=self.i2c_apb_slave_read(0)
        self.compare_expected("APB read of GPIO response",rt, 0)
        self.compare_expected("APB read of GPIO response",rd, 0xf0)
        (rt, rd)=self.i2c_apb_slave_write(0, 0x0f)
        self.compare_expected("APB write of GPIO response",rt, 0)
        (rt, rd)=self.i2c_apb_slave_read(0)
        self.compare_expected("APB read of GPIO response",rt, 0)
        self.compare_expected("APB read of GPIO response",rd, 0x0f)
        self.finishtest(0,"")
        pass

#a Hardware classes
#c ps2_test_hw
class ps2_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of LED chain
    """
    th_forces = { "th.clock":"clk",
                  "th.inputs":("ps2_in__data "+
                               "ps2_in__clk "+
                               "ps2_rx_data__valid "+
                               "ps2_rx_data__data[8] "+
                               "ps2_rx_data__parity_error "+
                               "ps2_rx_data__protocol_error "+
                               "ps2_rx_data__timeout "+
                               "ps2_key__valid "+
                               "ps2_key__extended "+
                               "ps2_key__key_number[8] "+
                               "ps2_key__release "+
                               ""),
                  "th.outputs":("ps2_out__data "+
                                "ps2_out__clk "+
                                "divider[16] "+
                               ""),
                  }
    module_name = "tb_input_devices"
    pass

#c i2c_test_hw
class i2c_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of LED chain
    """
    i2c                  = pycdl.wirebundle(structs.i2c)
    i2c_conf             = pycdl.wirebundle(structs.i2c_conf)
    i2c_master_request   = pycdl.wirebundle(structs.i2c_master_request)
    i2c_master_response  = pycdl.wirebundle(structs.i2c_master_response)
    loggers = {"i2c_slave": {"verbose":0, "filename":"i2c_slave.log", "modules":("dut.slave dut.i2c_apb dut.i2c_apb.apb_log ")},
               "i2c_master_0": {"verbose":0, "filename":"i2c_master.log", "modules":("dut.master___0 ")},
               }
    th_forces = { "th.clock":"clk",
                  "th.inputs":" ".join(i2c._name_list("i2c_in")+
                                        i2c_master_response._name_list("master_response_0")+
                                        i2c_master_response._name_list("master_response_1")+
                                       ["gpio_output[16]"]
                                       ),
                  "th.outputs":" ".join(i2c._name_list("i2c_out") +
                                        i2c_conf._name_list("i2c_conf_0") +
                                        i2c_conf._name_list("i2c_conf_1") +
                                        i2c_master_request._name_list("master_request_0")+
                                        i2c_master_request._name_list("master_request_1")
                  ),
                  }
    module_name = "tb_i2c"
    pass

#a Simulation test classes
#c ps2
class ps2(simple_tb.base_test):
    def test_one(self):
        test = c_ps2_test_one()
        hw = ps2_test_hw(test=test)
        self.do_test_run(hw, num_cycles=1000*1000)
        pass
    pass

#c i2c
class i2c(simple_tb.base_test):
    def test_one(self):
        test = c_i2c_test_one()
        hw = i2c_test_hw(test=test)
        self.do_test_run(hw, num_cycles=20*1000)
        pass
    def test_two(self):
        test = c_i2c_test_two()
        hw = i2c_test_hw(test=test)
        self.do_test_run(hw, num_cycles=100*1000)
        pass
    pass
