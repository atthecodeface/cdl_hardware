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

#a Teletext test pages
#c teletext_page
class teletext_page(object):
    hexdump = None
    def __init__(self):
        if self.hexdump:
            hexdump = ("".join(self.hexdump.split("\n"))).split()
            characters = [int(t,16) for t in hexdump]
            self.lines = [[characters[i+40*j] for i in range(40)] for j in range(25)]
            pass
        pass
    def get_mif_file(self):
        a = 0
        for l in self.lines:
            data = ["%02x"%c for c in l]
            data=" ".join(data)
            print "%02x: %s"%(a,data)
            a = a + len(l)
            pass
        pass

#c teletext_test_page_0
class teletext_test_page_0(teletext_page):
    hexdump="""94 20 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 20 84 9d 83 8d 20 20 20 20
                86 9d 84 4d 79 65 72 73 20 47 72 6f 76 65 20 4e
                65 74 77 6f 72 6b 20 20 9d 20 20 20 20 20 20 20
                84 9d 83 8d 20 20 20 20 86 9d 84 4d 79 65 72 73
                20 47 72 6f 76 65 20 4e 65 74 77 6f 72 6b 20 20
                9d 20 20 20 20 20 20 20 94 20 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 20
                84 9d 83 54 65 6c 65 74 65 78 74 20 53 79 73 74
                65 6d 20 28 43 29 31 39 39 36 20 4a 2e 47 2e 48
                61 72 73 74 6f 6e 20 20 94 20 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 20
                94 e0 70 70 70 70 70 70 70 70 70 70 70 70 70 70
                70 70 70 70 70 70 70 70 70 70 70 70 70 70 70 70
                70 70 70 70 70 70 70 b0 84 9d 86 54 68 69 73 20
                69 73 20 61 20 73 61 6d 70 6c 65 20 66 72 6f 6e
                74 20 70 61 67 65 2c 20 73 69 6d 69 6c 61 72 20
                94 9d 86 20 74 6f 20 6f 6e 65 20 69 6e 20 61 63
                74 75 61 6c 20 75 73 65 20 69 6e 20 61 20 73 63
                68 6f 6f 6c 2e 84 84 9d 94 e2 73 73 73 73 73 73
                73 73 73 73 73 73 73 73 73 73 73 73 73 73 73 73
                73 73 73 73 73 73 73 73 73 73 73 73 73 73 73 b1
                84 9d 87 31 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 20 84 9d 87 32 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 20
                84 9d 87 33 20 2e 20 2e 20 2e 20 2e 20 2e 20 50
                72 6f 67 72 61 6d 73 20 6f 6e 20 74 68 65 20 4e
                65 74 77 6f 72 6b 20 20 84 9d 87 34 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 20
                84 9d 87 35 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 43 6f 6d 70 75 74 65 72 20 4d 61
                67 61 7a 69 6e 65 20 20 84 9d 87 36 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 20
                84 9d 87 37 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 20 84 9d 87 38 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e 20 20
                84 9d 87 39 20 2e 20 2e 20 2e 20 2e 20 2e 20 2e
                20 2e 20 2e 20 2e 20 2e 20 2e 49 6e 73 74 72 75
                63 74 69 6f 6e 73 20 20 94 a2 a3 a3 a3 a3 a3 a3
                a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3
                a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a1
                94 20 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 20 84 9d 83 20 20 50 72 65
                73 73 20 45 73 63 61 70 65 20 74 6f 20 72 65 74
                75 72 6e 20 74 6f 20 6d 65 6e 75 20 20 20 20 20
                94 20 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c 2c
                2c 2c 2c 2c 2c 2c 2c 20 81 56 49 45 57 44 41 54
                41 20 20 20 20 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 01 00 00 00 02 00 00 00 2c 01 00 00
                04 00 00 00 05 00 00 00 06 00 00 00 07 00 00 00
                08 00 00 00 09 00 00 00 ff ff ff ff 09 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 70 17 00 01
            """

#c teletext_test_page_1
class teletext_test_page_1(teletext_page):
    hexdump="""84 9d 87 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 84 9d 82 20 20 20 20 20
                20 8d 20 20 20 53 50 4f 52 54 53 20 50 41 47 45
                53 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                84 9d 82 20 20 20 20 20 20 8d 20 20 20 53 50 4f
                52 54 53 20 50 41 47 45 53 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 84 9d 92 20 20 20 20 20
                20 20 20 20 20 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3 a3
                a3 a0 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                84 9d 87 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 84 9d 87 8d 46 72 6f 6d
                20 68 65 72 65 20 6f 6e 77 61 72 64 73 2c 20 74
                68 65 72 65 20 69 73 20 73 70 6f 72 74 73 20 20
                84 9d 87 8d 46 72 6f 6d 20 68 65 72 65 20 6f 6e
                77 61 72 64 73 2c 20 74 68 65 72 65 20 69 73 20
                73 70 6f 72 74 73 20 20 84 9d 87 20 20 20 20 20
                20 20 8d 20 20 69 6e 66 6f 72 6d 61 74 69 6f 6e
                2e 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                84 9d 87 20 20 20 20 20 20 20 8d 20 20 69 6e 66
                6f 72 6d 61 74 69 6f 6e 2e 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 84 9d 87 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                84 9d 87 81 66 32 87 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 2e 4d 61 69 6e 20 6d 65 6e 75 83
                20 20 20 20 20 20 20 20 84 9d 87 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                84 9d 87 20 31 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 52 75 67 62 79 83
                28 31 31 29 20 20 20 20 84 9d 87 20 32 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 46
                6f 6f 74 62 61 6c 6c 83 28 31 32 29 20 20 20 20
                84 9d 87 20 33 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 48 6f 63 6b 65 79 83
                28 31 33 29 20 20 20 20 84 9d 87 20 34 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 54 65 6e 6e 69 73 83 28 31 34 29 20 20 20 20
                84 9d 87 20 35 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 4e 65 74 62 61 6c 6c 83
                28 31 35 29 20 20 20 20 84 9d 87 20 36 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 53
                77 69 6d 6d 69 6e 67 83 28 31 36 29 20 20 20 20
                84 9d 87 20 37 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 53 71 75 61 73 68 83
                28 31 37 29 20 20 20 20 84 9d 87 20 38 2e 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 53 63 68 6f 6f
                6c 20 73 70 6f 72 74 83 28 31 38 29 20 20 20 20
                84 9d 87 20 39 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 53 70 6f 72 74 73 20 6e 65 77 73 83
                28 31 39 29 20 20 20 20 84 9d 87 20 30 2e 2e 2e
                2e 2e 2e 2e 2e 2e 4f 74 68 65 72 73 20 28 32 6e
                64 20 6d 65 6e 75 29 83 28 31 30 29 20 20 20 20
                84 9d 87 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 85 53 70 6f 72 74 20 20
                20 20 20 20 20 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                0a 00 00 00 0b 00 00 00 0c 00 00 00 0d 00 00 00
                0e 00 00 00 0f 00 00 00 10 00 00 00 11 00 00 00
                12 00 00 00 13 00 00 00 ff ff ff ff 00 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01
                """
    pass


#c teletext_test_page_2
class teletext_test_page_2(teletext_page):
    hexdump="""84 9d 91 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 84 9d 91 20 ea b5 ea b5
                a0 f0 f0 a0 ea f5 f0 a0 ea f5 f0 a0 a0 f2 b1 a0
                a0 f0 f0 a0 a0 f0 f0 b0 a0 20 20 20 20 20 20 20
                84 9d 91 20 ea b7 eb b5 ea b5 ea b5 ea b5 ea b5
                ea b5 ea b5 a0 ea b5 a0 ea bd ae a5 a2 ad ec b0
                a0 20 20 20 20 20 20 20 84 9d 91 20 a2 a1 a2 a1
                a0 a3 a3 a0 a2 a3 a3 a0 a2 a3 a3 a0 a0 a3 a3 a0
                a0 a3 a3 a0 a2 a3 a3 a0 a0 20 20 20 20 20 20 20
                85 9d 87 20 20 20 20 20 26 20 6f 74 68 65 72 20
                69 6e 74 65 72 65 73 74 73 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 91 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                91 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 91 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 31 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 4d 75 73 69 63 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 32 2e 2e
                2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e 53 74 61
                6d 70 20 43 6f 6c 6c 65 63 74 69 6e 67 20 20 20
                20 20 20 20 20 33 2e 2e 2e 2e 2e 2e 2e 2e 2e 2e
                2e 2e 2e 2e 2e 4d 6f 76 69 65 73 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 83 9d 84 8d 20 50 72 65
                73 73 81 66 32 84 74 6f 20 72 65 74 75 72 6e 20
                74 6f 20 6d 65 6e 75 20 68 65 61 64 20 20 20 20
                83 9d 84 8d 20 50 72 65 73 73 81 66 32 84 74 6f
                20 72 65 74 75 72 6e 20 74 6f 20 6d 65 6e 75 20
                68 65 61 64 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
                20 20 20 20 20 20 20 20 82 56 69 65 77 64 61 74
                61 20 20 20 20 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 15 00 00 00 16 00 00 00 17 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                00 00 00 00 00 00 00 00 ff ff ff ff 00 00 00 00
                00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01
    """
    pass

#c teletext_test_page
class teletext_test_page(teletext_page):
    hexdump="""81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 b0 b1
               97 9e 8f f3 93 9a 96 9e 9f 98 84 8d 9d 83 c5 ce c7 c9 ce c5 c5 d2 c9 ce c7 a0 92 9c 8c 9e f3 95 8e 91 8f 94 8f 87 b0 b2
               97 9e 8f f3 93 9a 96 9e 9f 98 84 8d 9d 83 c5 ce c7 c9 ce c5 c5 d2 c9 ce c7 a0 92 9c 8c 9e f3 95 8e 91 8f 94 8f 87 b0 b2
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff b0 b4
               94 9a 9e f3 91 99 95 80 95 81 8d a0 85 9d 82 d4 e5 f3 f4 a0 d0 e1 e7 e5 a0 a0 9c 8c 9e 92 f3 96 98 93 80 97 98 81 b0 b5
               94 9a 9e f3 91 99 95 80 95 81 8d a0 85 9d 82 d4 e5 f3 f4 a0 d0 e1 e7 e5 a0 a0 9c 8c 9e 92 f3 96 98 93 80 97 98 81 b0 b5
               81 80 81 a0 80 a0 81 9e a0 9e a0 97 ac 93 93 96 96 92 92 92 95 95 91 91 94 94 94 a0 a0 94 80 81 80 81 80 81 80 81 b0 b7
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff b0 b8
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 b0 b9
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b0
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 b1 b1
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b2
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 b1 b3
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b4
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80 b1 b5
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b6
               d7 e8 e9 f4 e5 83 d9 e5 ec ec ef f7 86 c3 f9 e1 ee 82 c7 f2 e5 e5 ee 85 cd e1 e7 e5 ee f4 e1 81 d2 e5 e4 84 c2 ec f5 e5
               97 9a a1 a2 a3 93 a4 a5 a6 a7 96 a8 a9 aa ab 92 ac ad ae af 99 b0 b1 b2 b3 95 b4 b5 b6 b7 91 b8 b9 ba bb 94 bc bd be bf
               a0 a0 a1 a2 a3 a0 a4 a5 a6 a7 a0 a8 a9 aa ab a0 ac ad ae af a0 b0 b1 b2 b3 a0 b4 b5 b6 b7 a0 b8 b9 ba bb a0 bc bd be bf
               a0 c0 c1 c2 c3 a0 c4 c5 c6 c7 a0 c8 c9 ca cb a0 cc cd ce cf a0 d0 d1 d2 d3 a0 d4 d5 d6 d7 a0 d8 d9 da db a0 dc dd de df
               a0 e0 e1 e2 e3 a0 e4 e5 e6 e7 a0 e8 e9 ea eb a0 ec ed ee ef a0 f0 f1 f2 f3 a0 f4 f5 f6 f7 a0 f8 f9 fa fb a0 fc fd fe ff
               94 e0 e1 e2 e3 91 e4 e5 e6 e7 95 e8 e9 ea eb 92 ec ed ee ef 9a f0 f1 f2 f3 96 f4 f5 f6 f7 93 f8 f9 fa fb 97 fc fd fe ff
               83 98 c3 ef ee e3 e5 e1 ec 88 c6 ec e1 f3 e8 83 aa 8b 8b c2 ef f8 89 d3 f4 e5 e1 e4 f9 98 c7 ef ee e5 8a 8a bf 96 de ff
               82 45 6e 67 69 6e 65 65 72 69 6e 67 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               """
    pass

#a Test classes
#c c_test_one
class c_test_one(simple_tb.base_th):
    blah = {"tvi_all_scanlines":0,
            "tvi_even_scanlines":1,
            "tvi_odd_scanlines":2}
    lines = teletext_test_page().lines
    lines = ("abcdefghijklmnop",
             (129,"a",130,"b",131,"c",132,"d",133,"e",134,"f",135,"g",32,32),
             )
    lines = ( (17,30,"a",18,"b",19,20,21),
              (17,30,"a",18,"b",19,20,21),
             )
    lines = teletext_test_page().lines
    #f new_pixel
    def new_pixel(self,r,g,b):
        rgb=[0,0,0]
        if r!=0: rgb[0]=255
        if g!=0: rgb[1]=255
        if b!=0: rgb[2]=255
        self.ppm_row +="%d %d %d "%tuple(rgb)
        pass
    #f bfm_tick
    def bfm_tick(self):
        self.ch_valid_pipeline.append(self.ch_valid)
        self.bfm_wait(1)
        if self.ch_valid_pipeline.pop(0):
            if (self.ios.pixels__valid.value()==0):
                self.failtest(0,"Expected a valid pixel out of teletext pipeline, but did not get one")
                #return
            rgb = (self.ios.pixels__red.value(),
                   self.ios.pixels__green.value(),
                   self.ios.pixels__blue.value())
            for i in [1<<(11-x) for x in range(12)]:
                self.new_pixel(rgb[0]&i,rgb[1]&i,rgb[2]&i)
                pass
            pass
        pass
    #f character_tick
    def character_tick(self, valid=0, ticks=1):
        self.ios.character__valid.drive(valid)
        self.ch_valid = valid
        for i in range(ticks):
            self.bfm_tick()
            pass
        pass
    #f drive_line
    def drive_line(self, text):
        self.ppm_row = ""
        self.ios.timings__end_of_scanline.drive(0)
        self.character_tick(0,10)
        for i in range(len(text)):
            d = text[i]
            if type(d)==str: d=ord(d)
            self.ios.character__character.drive(d)
            self.character_tick(1,1)
            if True:
                self.character_tick(0,1)
                pass
            pass
        self.character_tick(0,10)
        self.ios.timings__end_of_scanline.drive(1)
        self.bfm_wait(1)
        print >>self.ppm_file, self.ppm_row
    #f run
    def run(self):
        self.ppm_file = open("a.ppm","w")
        print >> self.ppm_file, "P3\n%d %d\n255\n"%(len(self.lines[0])*12,len(self.lines)*20)
        self.cfg_divider = 3
        self.ch_valid_pipeline = [0,0,0]
        simple_tb.base_th.run_start(self)
        self.bfm_wait(25)
        self.ios.timings__interpolate_vertical.drive(self.blah["tvi_all_scanlines"])
        self.ios.timings__smoothe.drive(1)
        self.ios.timings__restart_frame.drive(1)
        self.bfm_wait(10)
        self.ios.timings__restart_frame.drive(0)
        self.bfm_wait(10)
        self.ios.timings__end_of_scanline.drive(1)
        self.bfm_wait(10)
        self.ios.timings__end_of_scanline.drive(0)
        self.bfm_wait(10)
        for l in self.lines:
            for i in range(20):
                self.drive_line(l)
                pass
            pass
        self.ppm_file.close()
        self.finishtest(0,"")
        pass


#c c_scanline
class c_scanline(object):
    def __init__(self):
        self.back_porch=0
        self.front_porch=0
        self.pixels = []
        pass
    def add_pixel(self, r, g, b):
        self.pixels.append((r&255) | ((g&255)<<8) | ((b&255)<<16))
        pass
    def ppm_line(self):
        row = ""
        for p in self.pixels:
            row +="%d %d %d "%( ((p>> 0)&255),
                                ((p>> 8)&255),
                                ((p>>16)&255),
                                )
            pass
        return row
    pass

#c c_frame
class c_frame(object):
    def __init__(self):
        self.num_hsyncs = 0
        self.scanlines = []
        self.back_porch = 0
        self.front_porch = 0
        pass
    def new_scanline(self):
        self.scanlines.append(c_scanline())
        return self.scanlines[-1]
    def validate(self):
        p = []
        in_back_porch = True
        for i in range(len(self.scanlines)):
            if len(self.scanlines[i].pixels)==0:
                if in_back_porch:
                    self.back_porch = self.back_porch + 1
                else:
                    self.front_porch = self.front_porch + 1
                pass
            else:
                p.append(self.scanlines[i])
                in_back_porch = False
                pass
            pass
        self.scanlines=p
        pass
    def write_ppm(self, ppm_file):
        self.validate()
        print >> ppm_file, "P3\n%d %d\n255\n"%(len(self.scanlines[0].pixels),len(self.scanlines))
        for l in self.scanlines:
            print >>ppm_file, l.ppm_line()
            pass
        pass
    pass

#c c_test_fb_one
class c_test_fb_one(simple_tb.base_th):
    blah = {"tvi_all_scanlines":0,
            "tvi_even_scanlines":1,
            "tvi_odd_scanlines":2}
    lines = teletext_test_page().lines
    lines = ("abcdefghijklmnop",
             (129,"a",130,"b",131,"c",132,"d",133,"e",134,"f",135,"g",32,32),
             )
    lines = ( (17,30,"a",18,"b",19,20,21),
              (17,30,"a",18,"b",19,20,21),
             )
    #teletext_test_page().get_mif_file()
    #f wait_for_vsync
    def wait_for_vsync(self):
        while self.ios.video_bus__vsync.value()==0:
            self.bfm_wait(100) # vsync is one line long
            pass
        pass
    #f wait_for_hsync
    def wait_for_hsync(self):
        while self.ios.video_bus__hsync.value()==0:
            self.bfm_wait(1)
            pass
        pass
    #f capture_scanline
    def capture_scanline(self, frame):
        pixels = []
        scanline = frame.new_scanline()
        while self.ios.video_bus__display_enable.value()==0:
            scanline.back_porch = scanline.back_porch+1
            self.bfm_wait(1)
            if self.ios.video_bus__hsync.value()==1:
                return 
            pass
        while self.ios.video_bus__display_enable.value()==1:
            scanline.add_pixel( self.ios.video_bus__red.value(),
                                self.ios.video_bus__green.value(),
                                self.ios.video_bus__blue.value() )
            self.bfm_wait(1)
            if self.ios.video_bus__hsync.value()==1:
                return 
            pass
        while self.ios.video_bus__hsync.value()==0:
            scanline.front_porch = scanline.front_porch+1
            self.bfm_wait(1)
        pass
    #f capture_frame
    def capture_frame(self):
        frame = c_frame()
        self.wait_for_vsync()
        while True:
            self.wait_for_hsync()
            if self.ios.video_bus__vsync.value()==1:
                return frame
            frame.num_hsyncs = frame.num_hsyncs + 1
            self.capture_scanline(frame)
            pass
        pass
    #f run
    def run(self):
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        f = self.capture_frame()
        ppm_file = open("a.ppm","w")
        f.write_ppm(ppm_file)
        ppm_file.close()
        self.finishtest(0,"")
        pass

#a Hardware classes
#c cdl_test_hw - teletext
class cdl_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of teletext module
    """
    th_forces = { "character_rom.filename":"roms/teletext.mif",
                  "th.clock":"clk",
                  "th.inputs":("pixels__valid "+
                               "pixels__blue[12] "+
                               "pixels__green[12] "+
                               "pixels__red[12] "+
                               "pixels__last_scanline "+
                               ""),
                  "th.outputs":("timings__interpolate_vertical[2] "+
                                "timings__smoothe "+
                                "timings__first_scanline_of_row "+
                                "timings__end_of_scanline "+
                                "timings__restart_frame "+
                                "character__character[7] "+
                                "character__valid "+
                                ""),
                  }
    module_name = "tb_teletext"
    pass

#c framebuffer_teletext_hw
class framebuffer_teletext_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of teletext framebuffer module
    """
    th_forces = { "fb.character_rom.filename":"roms/teletext.mif",
                  "fb.display.filename":"a.mif",
                  "th.clock":"clk",
                  "th.inputs":("csr_response__read_data[32] "+
                               "csr_response__read_data_valid "+
                               "csr_response__read_data_error "+
                               "csr_response__acknowledge "+
                               "video_bus__blue[8] "+
                               "video_bus__green[8] "+
                               "video_bus__red[8] "+
                               "video_bus__display_enable "+
                               "video_bus__hsync "+
                               "video_bus__vsync "+
                               "" ),
                  "th.outputs":("csr_request__data[32] "+
                               "csr_request__address[16] "+
                               "csr_request__select[16] "+
                               "csr_request__read_not_write "+
                               "csr_request__valid "+
                               "display_sram_write__address[32] "+
                               "display_sram_write__write_data[64] "+
                               "display_sram_write__valid "+
                               "display_sram_write__read_not_write "+
                               "display_sram_write__byte_enable[8] "+
                               "display_sram_write__id[4] "+
                                ""),
                  }


    module_name = "tb_framebuffer_teletext"
    pass

#a Simulation test classes
#c teletext
class teletext(simple_tb.base_test):
    def test_one(self):
        test = c_test_one()
        hw = cdl_test_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=1000*1000)
        pass
    pass

#c framebuffer
class framebuffer(simple_tb.base_test):
    def test_one(self):
        test = c_test_fb_one()
        hw = framebuffer_teletext_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=1000*1000)
        pass
    pass
