#!/usr/bin/env python
def bits_of_n(nbits, n):
    bits = []
    for i in range(nbits):
        bits.append(n&1)
        n >>= 1
        pass
    return bits

dec_6b5b = {"100111":(0,"-D0+"),
            "011000":(0,"+D0-"),
            "100010":(0,"+D1-"),
            "011101":(0,"-D1+"),
            "101101":(0,"-D2+"),
            "010010":(0,"+D2-"),
            "110001":(0,"D3"),
            "110101":(0,"-D4+"),
            "001010":(0,"+D4-"),
            "101001":(0,"D5"),
            "011001":(0,"D6"),
            "111000":(0,"-D7-"),
            "000111":(0,"+D7+"),
            "111001":(0,"-D8+"),
            "000110":(0,"+D8-"),
            "100101":(0,"D9"),
            "010101":(0,"D10"),
            "110100":(0,"D11"),
            "001101":(0,"D12"),
            "101100":(0,"D13"),
            "011100":(0,"D14"),
            "010111":(0,"-D15+"),
            "101000":(0,"+D15-"),
            "100100":(0,"+D16-"),
            "011011":(0,"-D16+"),
            "100011":(0,"D17"),
            "010011":(0,"D18"),
            "110010":(0,"D19"),
            "001011":(0,"D20"),
            "101010":(0,"D21"),
            "011010":(0,"D22"),
            "111010":(0,"-D.K23+"),
            "000101":(0,"+D.K23-"),
            "001100":(0,"+D24-"),
            "110011":(0,"-D24+"),
            "100110":(0,"D25"),
            "010110":(0,"D26"),
            "110110":(0,"-D.K27+"),
            "001001":(0,"+D.K27-"),
            "001110":(0,"D28"),
            "101110":(0,"-D.K29+"),
            "010001":(0,"+D.K29-"),
            "011110":(0,"-D.K30+"),
            "100001":(0,"+D.K30-"),
            "101011":(0,"-D31+"),
            "010100":(0,"+D31-"),
            "110000":(1,"+K28-"),
            "001111":(1,"-K28+"),
             }
dec_4b3b = {"1011":".-0+",
            "0100":".+0-",
            "1001":".1",
            "0101":".2",
            "1100":".-3-",
            "0011":".+3+",
            "1101":".-4+",
            "0010":".+4-",
            "1010":".5",
            "0110":".6",
            "0001":".+7-",
            "1110":".-7+",
            "0111":".-A7+",
            "1000":".+A7-",
}
dec_4b3b_k = { (0,"1011"):".-K0+",
               (1,"0100"):".+K0-",
               (0,"0110"):".-K1-",
               (1,"1001"):".+K1+",
               (0,"1010"):".-K2-",
               (1,"0101"):".+K2+",
               (0,"1100"):".-K3-",
               (1,"0011"):".+K3+",
               (0,"1101"):".-K4+",
               (1,"0010"):".+K4-",
               (0,"0101"):".-K5-",
               (1,"1010"):".+K5+",
               (0,"1001"):".-K6-",
               (1,"0110"):".+K6+",
               (1,"0111"):".-K7+",
               (1,"1000"):".+K7-",
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

# rx on Fri
data = """
a84d7a8 d7a84d7 84d7a84 7a84d7a 4d7a84d a84d7a8 d7a84d7 7a84d7a 7a84d7a 4d7a84d a84d7a8 d7a84d7 84d7a84 7a84d7a 4d7a84d d7a84d7 d7a84d7 84d7a84 7a84d7a 4d7a84d a84d7a8 d7a84d7 84d7a84 7a84d7a a84d7a8 a84d7a8 d7a84d7 84d7a84 7a84d7a 4d7a84d a84d7a8
d7a84d7
7a84d7a
7a84d7a
4d7a84d
a84d7a8
d7a84d7
84d7a84
7a84d7a
4d7a84d
d7a84d7
"""

# tx on Fri
data = """
419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 3499af41 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 19af4191 19af4191 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 7499af41 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 19af4191 19af4191 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 7499af41 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 19af4191 19af4191 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 7499af41 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 19af4191 19af4191 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 7499af41 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 19af4191 19af4191 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 7499af41 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 19af4191 19af4191 f419af41 9af419a1 419af411 af419af1 19af4191 f419af41 419af411 419af411 af419af1 19af4191 f419af41 9af419a1 419af411 af419af1 7499af41
"""
# Monday
data = """
419af41
af419af
9de75ab
101f415
19af419
f419af4
f419af4
9af419a
9af419a
419af41
419af41
af419af
af419af
19af419
19af419
f419af4
f419af4
9af419a
9af419a
419af41
af419af
19af419
af419af
19af419
19af419
f419af4
f419af4
9af419a
9af419a
419af41
419af41
af419af
af419af
19af419
19af419
f419af4
9af419a
419af41
9af419a
419af41
419af41
af419af
af419af
19af419
19af419
f419af4
f419af4
9af419a
9af419a
419af41
419af41
af419af
9de75bb
101b475
19af419
f419af4
f419af4
9af419a
9af419a
419af41
419af41
af419af
af419af
19af419
19af419
"""


def decode_hex(serial_hex, n=64):
    bits = bits_of_n(n,serial_hex)
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
            k28 = False
            if s in dec_6b5b:
                (k28,s)=dec_6b5b[s]
                pass
            r+=s
            s = ""
            if ones>3:disp=1
            if ones<3:disp=0
            ones = 0
            pass
        if n==10:
            if k28:
                if (disp,s) in dec_4b3b_k:
                    s=dec_4b3b_k[(disp,s)]
                    pass
                pass
            elif s in dec_4b3b:
                if s in dec_4b3b:
                    s=dec_4b3b[s]
                    pass
                pass
            r+=s+" "
            s = ""
            if ones>2:disp=1
            if ones<2:disp=0
            ones = 0
            pass
        n = n % 10
        pass
    print r
    print
    print bits_string[alignment:]
    print
    pass
rev_of = {0:0, 1:8, 2:4, 3:12, 4:2, 5:10, 6:6, 7:14,
          8:1, 9:9, 10:5, 11:13, 12:3, 13:11, 14:7, 15:15}
for i in range(16):
    if rev_of[rev_of[i]]!=i:
        print i
        die
def reverse_nybbles(x):
    i = 0
    y = 0
    while (x>>i) != 0:
        y |= rev_of[(x>>i)&0xf] << i
        i += 4
        pass
    return y

import sys, re
if len(sys.argv)>1:
    serial_hex = 0
    shf = 0
    for d in sys.argv[1:]:
        d = d[:-1]
        i = int(d,16)
        serial_hex = serial_hex + (i<<shf)
        shf += 4*len(d)
        pass
    serial_hex = reverse_nybbles(serial_hex)
    decode_hex(serial_hex, n=shf)
    pass
else:
    m = re.compile(r"DIV:[0-9a-fA-F]* ([0-9a-fA-F]+) ([0-9a-fA-F]+)")
    for l in data.split("\n"):
        l=l.strip()
        k = m.search(l)
        if k is not None:
            serial_hex = int(k.group(2)+k.group(1),16)
            decode_hex(serial_hex)
            pass
        pass
    pass

