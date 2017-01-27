#!/usr/bin/env python
#a Imports
import unittest

data_in
data_out
chip_select
read_not_write
register_select[4]
reset_n
chip_select_n
irq_n

port.control[2]
port.data_out[8]
port.data_in[8]

registers = {
0: "orb_irb",
1: "ora_ira",
2: "ddr_b",
3: "ddr_a",
4: "t1c_l",
5: "t1c_h",
6: "t1l_l",
7: "t1l_h",
8: "t2c_l",
9: "t2c_h",
10: "sr",
11: "acr",
12: "pcr",
13: "ifr",
14: "ier",
15: "ora_ira_nhs",
}
#a Register classes
#c c_6522_register
class c_6522_register(object):
    name = "BITS??"
    formats = {8:"%s:%02x"}
    width = 8
    def __init__(self):
        self.value = 0
        pass
    def set(self, value):
        self.value = value
        pass
    def get(self):
        return self.value
    def idle(self, din):
        return din
    def __str__(self):
        return self.formats[self.width] % (self.name, self.value)
    pass

#a c_6522
class c_6522(object):
    def __init__(self):
        self.pcr = c_6522_register()
        self.acr = c_6522_register()
        self.ifr = c_6522_register()
        self.ier = c_6522_register()

        self.t1l_l = c_6522_register()
        self.t1l_h = c_6522_register()
        self.t1c_l = c_6522_register()
        self.t1c_h = c_6522_register()

        self.t2l_l = c_6522_register()
        self.t2c_l = c_6522_register()
        self.t2c_h = c_6522_register()

        self.ira = c_6522_register()
        self.ora = c_6522_register()
        self.ddr_a = c_6522_register()

        self.irb = c_6522_register()
        self.orb = c_6522_register()
        self.ddr_b = c_6522_register()

        self.sr = c_6522_register()
        pass
    def get_outputs(self):
        pa_data_out = 0xff
        pa_nondriven_bits = (self.ddr_a.get()^0xff)
        pa_driven_bits    = (self.ddr_a.get()&0xff)
        pa_data_out = pa_nondriven_bits | (pa_driven_bits & self.ora.get())

        pb_data_out = 0xff
        pb_nondriven_bits = (self.ddr_b.get()^0xff)
        pb_driven_bits    = (self.ddr_b.get()&0xff)
        pb_data_out = pb_nondriven_bits | (pb_driven_bits & self.orb.get())
        return {"pa":pa_data_out, "pb":pb_data_out}
    def clock_inputs(self, pa_data_in, pb_data_in):
        if (!latched or ca1_latch):
            self.ira.set(pa_data_in)
            pass
        pb_driven_bits    = (self.ddr_b.get()&0xff)
        pb_driven_out     = pb_driven_bits & self.orb.get()
        pb_data_in = pb_data_in & (pb_driven_bits^0xff)
        pb_data_in |= pb_driven_out
        self.irb.set(pb_data_in)
    def pcr(self):
        
    
