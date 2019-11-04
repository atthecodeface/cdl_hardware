#!/usr/bin/env python
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

class crc(object):
    init=0xffffffff
    poly=0x04C11DB7
    nbits=32
    def __init__(self, value=None):
        self.value = value
        if value is None: self.value = self.init
        self.mask=(1<<self.nbits)-1
        pass
    def clk_once(self):
        self.value = self.value<<1
        if (self.value>>self.nbits):
            self.value = self.value ^ ((1<<self.nbits) ^ self.poly)
            pass
        pass
    def clk(self,n):
        for i in range(n):
            self.clk_once()
            pass
        pass
    def do_crc(self,bits):
        for b in bits:
            self.value ^= b<<(self.nbits-1)
            self.clk_once()
            pass
        pass
    def bit_reverse(self):
        x = bits_of_n(self.nbits, self.value)
        x.reverse()
        return int_of_bits(x)
for i in range(64):#range(16):
    x=crc(1)
    #ib = bits_of_n(16,i)
    #x.do_crc(ib)
    x.clk(i+8)
    print i,  "%08x %08x"%(x.value, x.bit_reverse())
    
    
