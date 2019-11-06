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
    pass

"""
Some notes on 64-bit number modulo 10^9

10^9 = 2^9 * 5^9

So we need a 64-9=55-bit number modulo 5^9 (i.e. bottom 9 bits are passed through)
5^9 is 21 bits long (0x1dcd65)
Hence the next 21 bits we can pass through stage one - and we need ((N&(0x3ffffffff<<30))>>9) mod 0x1dxd65

Hence we could do with knowing 1<<21 through 1<<54 modulo (5^9)
 for i in range(64): print i, "%08x"%((1<<i) % (5**9))
...
21 0002329b
22 00046536
23 0008ca6c
24 001194d8
25 00055c4b
26 000ab896
27 0015712c
28 000d14f3
29 001a29e6
30 00168667
31 000f3f69
32 0000b16d
33 000162da
34 0002c5b4
35 00058b68
36 000b16d0
37 00162da0
38 000e8ddb
39 001d1bb6
40 001c6a07
41 001b06a9
42 00183fed
43 0012b275
44 00079785
45 000f2f0a
46 000090af
47 0001215e
48 000242bc
49 00048578
50 00090af0
51 001215e0
52 00065e5b
53 000cbcb6
54 0019796c
55 00152573
56 000c7d81
57 0018fb02
58 0014289f
59 000a83d9
60 001507b2
61 000c41ff
62 001883fe
63 00133a97

Clearly this can be handled with a 21 bit added in 34 cycles (possibly 2 adders)
A method would be to have an accumulator.
In each step take bit N and if set add 0x2329b
Then double the accumulator and move to bit N-1
Stop when N=21
Note that the accumulator will reach or exceed 1<<21. When it does so add in 0x2329b on top of the current value.
Eventually one will reach a stable point.
If accumulator is > 5**9 then subtract 5**9
Possibly this can be done instead of the 'exceed 1<<21 means add a further 0x2329b'
"""


    
