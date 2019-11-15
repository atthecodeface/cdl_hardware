#!/usr/bin/env python
def bits_of_n(nbits, n):
    bits = []
    for i in range(nbits):
        bits.append(n&1)
        n >>= 1
        pass
    return bits

dec_6b5b = {"100111":"D0",
            "011000":"D0",
            "100010":"D1",
            "011101":"D1",
            "101101":"D2",
            "010010":"D2",
            "101010":"D21",
            "001100":"D24",
            "110011":"D24",
            "110000":"K28",
            "001111":"K28",
             }
dec_4b3b = {"1011":".0",
             "0100":".0",
             "1001":".1",
             "0101":".2",
             "1100":".3",
             "0011":".3",
             "1101":".4",
             "0010":".4",
             "1010":".5",
             "0110":".6",
             "0001":".7",
             "1110":".7",
             "0111":".A7",
             "1000":".A7",
}
dec_4b3b_k = { (0,"1011"):".0",
             (0,"1010"):".2",
             (1,"0101"):".2",
             (0,"0101"):".5",
             (1,"1010"):".5",
}

data = """
DIV:00036000 657524BE 72AB41B6
DIV:00036000 19A8D5B4 A8AAABE3
DIV:00036000 6657524B 572AB41B
DIV:00036000 5B41B665 BE319A8D
DIV:00036000 319A8D5B 9A8AAABE
DIV:00036000 A8AAABE3 524BE319
DIV:00036000 4BE319A8 1B665752
DIV:00036000 41B66575 B66572AB
DIV:00036000 19A8D5B4 A8AAABE3
DIV:00036000 A8AAABE3 524BE319
DIV:00036000 524BE319 B41B6657
DIV:00036000 2AB41B66 B41B6657
DIV:00036000 5B41B665 BE319A8D
DIV:00036000 AAABE319 4BE319A8
DIV:00036000 6572AB41 8D5B41B6
DIV:00036000 19A8D5B4 A8AAABE3
DIV:00036000 E319A8AA 6657524B
DIV:00036000 B41B6657 1B66572A
DIV:00036000 A8D5B41B AAABE319
DIV:00036000 319A8AAA 657524BE
DIV:00036000 319A8D5B 9A8AAABE
DIV:00036000 4BE319A8 1B665752
DIV:00036000 572AB41B D5B41B66
DIV:00036000 E319A8D5 19A8AAAB
DIV:00036000 524BE319 B41B6657
DIV:00036000 1B66572A 19A8D5B4
"""
data = """
DIV:05FC9801 3515557C 1AB683B3
VGA:00020CEF 000109F9 0777CB83
DIV:05FC9801 5683B335 7C4CCAE5
VGA:00020454 000109F9 07792C36
DIV:05FC9801 C4CCAEA4 33515557
VGA:00020454 000109F9 07792C75
DIV:05FC9801 3351AB68 AE55683B
VGA:00020CEF 000109F9 0777CBC6
DIV:05FC9801 A497C4CC 57C4CCAE
VGA:00020454 000109F8 07792C75
DIV:05FC9801 3B335155 3351AB68
VGA:00020454 000109F9 07792C75
DIV:05FC9801 CAE55683 EA497C4C

"""

def decode_hex64(serial_hex):
    bits = bits_of_n(64,serial_hex)
    bits_string = "".join([str(x) for x in bits])
    comma = bits_string.find("00000")
    if comma<0: comma = bits_string.find("11111")
    alignment = (comma+18) % 10
    n = 0
    r = ""
    s = ""
    k28=False
    disp = 0
    ones = 0
    for b in bits_string[alignment:]:
        ones += int(b)
        s += b
        n += 1
        if n==6:
            if s in dec_6b5b: s=dec_6b5b[s]
            k28=(s=="K28")
            r+=s
            s = ""
            if ones>3:disp=1
            if ones<3:disp=0
            ones = 0
            pass
        if n==10:
            if k28: s=dec_4b3b_k[disp,s]
            elif s in dec_4b3b: s=dec_4b3b[s]
            r+=s+" "
            s = ""
            if ones>2:disp=1
            if ones<2:disp=0
            ones = 0
            pass
        n = n % 10
        pass
    print r, bits_string[alignment:]
    pass

import sys, re
if len(sys.argv)>1:
    serial_hex = int(sys.argv[2]+sys.argv[1],16)
    decode_hex64(serial_hex)
    pass
else:
    m = re.compile(r"DIV:[0-9a-fA-F]* ([0-9a-fA-F]+) ([0-9a-fA-F]+)")
    for l in data.split("\n"):
        l=l.strip()
        k = m.search(l)
        if k is not None:
            serial_hex = int(k.group(2)+k.group(1),16)
            decode_hex64(serial_hex)
            pass
        pass
    pass

