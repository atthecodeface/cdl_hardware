#a Imports
import re
import sys, inspect
from model6502 import c_6502

#a Memory
#c c_memory
class c_memory(object):
    def __init__(self):
        self.data = bytearray(65536)
        self.data[0xfffc] = 0
        self.data[0xfffd] = 0
        n = 0
        n = self.add_code(n, (0xa9, 0x54) )
        n = self.add_code(n, (0xa0, 0x18) )
        n = self.add_code(n, (0xa2, 0x82) )
        n = self.add_code(n, (0x69, 0x01) )
        n = self.add_code(n, (0x8d, 0x12, 0x34) )
        self.data[n] = 0x4c
        n+=1
        self.data[n] = 0x06
        n+=1
        self.data[n] = 0x00
        n+=1
        pass
    def load_binary(self, base_address, f):
        address = base_address
        while True:
            d = f.read(4096)
            if len(d)==0: break
            address = self.add_code(address, d)
            pass
        pass
    def add_code(self, address, data):
        for i in data:
            self.write(address,i)
            address += 1
            pass
        return address
    def read(self, address):
        return self.data[address]
    def write(self, address, data):
        self.data[address] = data
        pass
    def dump(self, address, length=256):
        while length>0:
            r = "%04x :"%address
            for i in range(min(length,16)):
                r += " %02x"%self.read(address+i)
                pass
            address += 16
            length -= 16
            print r
            pass
        pass
    
#a System
#c c_system
class c_system(object):
    #f __init__
    def __init__(self):
        self. cpu = c_6502()
        self.memory = c_memory()
        if False:
            self.memory.load_binary(0xc000, file("../../BeebEm3/BeebFile/BBCINT/OS12.ROM","r"))
            self.memory.load_binary(0x8000, file("../../BeebEm3/BeebFile/BBCINT/BASIC2.ROM","r"))
            pass
        self.cpu.reset()
        pass
    #f tick
    def tick(self, verbose=False):
        ts = self.cpu.tick_start()
        if verbose:
            print ts
            pass
        data_in = 0xff
        if ts["mem"] is not None:
            if ts["mem"][0] in ["read"]:
                data_in = self.memory.read(ts["mem"][1])
                pass
            elif ts["mem"][0] in ["write"]:
                self.memory.write(ts["mem"][1], ts["mem"][2])
                pass
            pass
        te = self.cpu.tick_end(data_in=data_in)
        if verbose:
            print "%02x"%data_in, te
            print self.cpu
            pass
        pass
        
