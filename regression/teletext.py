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
               81 80 81 a0 80 a0 81 9e a0 9e a0 97 ac 93 93 96
               96 92 92 92 95 95 91 91 94 94 94 a0 a0 94 80 81
               80 81 80 81 80 81 b0 b7 fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff b0 b8
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 b0 b9 fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b0
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 b1 b1 fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b2
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 b1 b3 fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b4
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 81 80 81 80 81 80 81 80 81 80
               81 80 81 80 81 80 b1 b5 fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff fe ff
               fe ff fe ff fe ff fe ff fe ff fe ff fe ff b1 b6
               d7 e8 e9 f4 e5 83 d9 e5 ec ec ef f7 86 c3 f9 e1
               ee 82 c7 f2 e5 e5 ee 85 cd e1 e7 e5 ee f4 e1 81
               d2 e5 e4 84 c2 ec f5 e5 97 9a a1 a2 a3 93 a4 a5
               a6 a7 96 a8 a9 aa ab 92 ac ad ae af 99 b0 b1 b2
               b3 95 b4 b5 b6 b7 91 b8 b9 ba bb 94 bc bd be bf
               a0 a0 a1 a2 a3 a0 a4 a5 a6 a7 a0 a8 a9 aa ab a0
               ac ad ae af a0 b0 b1 b2 b3 a0 b4 b5 b6 b7 a0 b8
               b9 ba bb a0 bc bd be bf a0 c0 c1 c2 c3 a0 c4 c5
               c6 c7 a0 c8 c9 ca cb a0 cc cd ce cf a0 d0 d1 d2
               d3 a0 d4 d5 d6 d7 a0 d8 d9 da db a0 dc dd de df
               a0 e0 e1 e2 e3 a0 e4 e5 e6 e7 a0 e8 e9 ea eb a0
               ec ed ee ef a0 f0 f1 f2 f3 a0 f4 f5 f6 f7 a0 f8
               f9 fa fb a0 fc fd fe ff 94 e0 e1 e2 e3 91 e4 e5
               e6 e7 95 e8 e9 ea eb 92 ec ed ee ef 9a f0 f1 f2
               f3 96 f4 f5 f6 f7 93 f8 f9 fa fb 97 fc fd fe ff
               83 98 c3 ef ee e3 e5 e1 ec 88 c6 ec e1 f3 e8 83
               aa 8b 8b c2 ef f8 89 d3 f4 e5 e1 e4 f9 98 c7 ef
               ee e5 8a 8a bf 96 de ff 82 45 6e 67 69 6e 65 65
               72 69 6e 67 20 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
               00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
                die
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
            self.character_tick(0,1)
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

#c c_test_dprintf_base
class c_test_dprintf_base(simple_tb.base_th):
    writes_to_do = [
        ]
    expected_sram_ops = [
        ]
    #f bfm_tick
    def bfm_tick(self, cycles):
        for i in range(cycles):
            if (self.ios.display_sram_write__enable.value()):
                self.sram_writes.append( (self.ios.display_sram_write__address.value(),
                                          self.ios.display_sram_write__data.value(),) )
                pass
            self.bfm_wait(1)
            pass
        pass
    #f dprintf
    def dprintf(self, address, data):
        self.ios.dprintf_req__valid.drive(1)
        self.ios.dprintf_req__address.drive(address)
        self.ios.dprintf_req__data_0.drive(data[0])
        self.ios.dprintf_req__data_1.drive(data[1])
        self.bfm_tick(1)
        while self.ios.dprintf_ack.value()==0:
            self.bfm_tick(1)
            pass
        self.ios.dprintf_req__valid.drive(0)
        pass
    #f run
    def run(self):
        self.sram_writes = []
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        for (address, data) in self.writes_to_do:
            self.dprintf(address, data)
            pass
        self.bfm_tick(1000)
        if len(self.sram_writes) != len(self.expected_sram_ops):
            self.failtest(0,"Mismatch in number of SRAM writes %d/%d"%(len(self.sram_writes),len(self.expected_sram_ops)))
            for s in self.sram_writes:
                print "(0x%04x, 0x%02x),"%(s[0],s[1])
                pass
            pass
        else:
            for i in range(len(self.sram_writes)):
                if self.expected_sram_ops[i][0] != self.sram_writes[i][0]:
                    self.failtest(i,"Mismatch in SRAM %d write address %04x/%04x"%(i,self.expected_sram_ops[i][0], self.sram_writes[i][0]))
                    pass
                if self.expected_sram_ops[i][1] != self.sram_writes[i][1]:
                    self.failtest(i,"Mismatch in SRAM %d write data %02x/%02x"%(i,self.expected_sram_ops[i][1], self.sram_writes[i][1]))
                    pass
                pass
            pass
        self.finishtest(0,"")
        pass

#c c_test_dprintf_one
class c_test_dprintf_one(c_test_dprintf_base):
    writes_to_do = [ (0x1234, ((0x4142434445464748,0xff00ff00ff00ff00)) ),
                     (0xfedc, ((0x4100420043004400,0x0045460047000048)) ),
                     (0xf00f, ((0x80feffffffffffff,0)) ),
                     (0xf00f, ((0x80fe81dcffffffff,0)) ),
                     (0xf00f, ((0x80fe81dc0082a9bc,0x87deadbeefff0000)) ),
                     ]
    expected_sram_ops = [(0x1234, 0x41),
                         (0x1235, 0x42),
                         (0x1236, 0x43),
                         (0x1237, 0x44),
                         (0x1238, 0x45),
                         (0x1239, 0x46),
                         (0x123a, 0x47),
                         (0x123b, 0x48),
                         (0xfedc, 0x41),
                         (0xfedd, 0x42),
                         (0xfede, 0x43),
                         (0xfedf, 0x44),
                         (0xfee0, 0x45),
                         (0xfee1, 0x46),
                         (0xfee2, 0x47),
                         (0xfee3, 0x48),

                         (0xf00f, 0x45),

                         (0xf00f, 0x45),
                         (0xf010, 0x44),
                         (0xf011, 0x43),

                         (0xf00f, 0x45),
                         (0xf010, 0x44),
                         (0xf011, 0x43),
                         (0xf012, 0x39),
                         (0xf013, 0x42),
                         (0xf014, 0x43),
                         (0xf015, 0x44),
                         (0xf016, 0x45),
                         (0xf017, 0x41),
                         (0xf018, 0x44),
                         (0xf019, 0x42),
                         (0xf01a, 0x45),
                         (0xf01b, 0x45),
                         (0xf01c, 0x46),
        ]
#c c_test_dprintf_two
class c_test_dprintf_two(c_test_dprintf_base):
    writes_to_do = [ (0x1234, ((0xc041c00041424344,0xc3ffffffff00ffff)) ),
                     ]
    expected_sram_ops = [(0x1234, 0x36),
                         (0x1235, 0x35),
                         (0x1236, 0x30),
                         (0x1237, 0x41),
                         (0x1238, 0x42),
                         (0x1239, 0x43),
                         (0x123a, 0x44),
                         (0x123b, 0x34),
                         (0x123c, 0x32),
                         (0x123d, 0x39),
                         (0x123e, 0x34),
                         (0x123f, 0x39),
                         (0x1240, 0x36),
                         (0x1241, 0x37),
                         (0x1242, 0x32),
                         (0x1243, 0x39),
                         (0x1244, 0x35),
        ]
#c c_test_dprintf_three
class c_test_dprintf_three(c_test_dprintf_base):
    writes_to_do = [ (0x1234, ((0xc001c401c801cc01,0xc000c400c800cc00)) ),
                     (0x2000, ((0xc0ffc4ffc8ffccff,0xff00c400c800cc00)) ),
                     (0x3000, ((0xc1ffff00c5ffff00,0xc9ffff00cdffffff)) ),
                     (0x3100, ((0xd1ffff00d5ffff00,0xd9ffff00ddffffff)) ),
                     (0x4000, ((0xc3ffffffffff0000,0)) ),
                     (0x4100, ((0xe7ffffffffff0000,0)) ),
                     (0x5000, ((0xc300000000ff0000,0)) ),
                     (0x5100, ((0xe700000000ff0000,0)) ),
                     ]
    expected_sram_ops = [(0x1234, 0x31),
                         (0x1235, 0x20),
                         (0x1236, 0x31),
                         (0x1237, 0x20),
                         (0x1238, 0x20),
                         (0x1239, 0x31),
                         (0x123a, 0x20),
                         (0x123b, 0x20),
                         (0x123c, 0x20),
                         (0x123d, 0x31),
                         (0x123e, 0x30),
                         (0x123f, 0x20),
                         (0x1240, 0x30),
                         (0x1241, 0x20),
                         (0x1242, 0x20),
                         (0x1243, 0x30),
                         (0x1244, 0x20),
                         (0x1245, 0x20),
                         (0x1246, 0x20),
                         (0x1247, 0x30),

                         (0x2000, 0x32),
                         (0x2001, 0x35),
                         (0x2002, 0x35),
                         (0x2003, 0x32),
                         (0x2004, 0x35),
                         (0x2005, 0x35),
                         (0x2006, 0x32),
                         (0x2007, 0x35),
                         (0x2008, 0x35),
                         (0x2009, 0x20),
                         (0x200a, 0x32),
                         (0x200b, 0x35),
                         (0x200c, 0x35),

                         (0x3000, 0x36),
                         (0x3001, 0x35),
                         (0x3002, 0x35),
                         (0x3003, 0x33),
                         (0x3004, 0x35),
                         (0x3005, 0x36),
                         (0x3006, 0x35),
                         (0x3007, 0x35),
                         (0x3008, 0x33),
                         (0x3009, 0x35),
                         (0x300a, 0x36),
                         (0x300b, 0x35),
                         (0x300c, 0x35),
                         (0x300d, 0x33),
                         (0x300e, 0x35),
                         (0x300f, 0x36),
                         (0x3010, 0x35),
                         (0x3011, 0x35),
                         (0x3012, 0x33),
                         (0x3013, 0x35),

                         (0x3100, 0x36),
                         (0x3101, 0x35),
                         (0x3102, 0x35),
                         (0x3103, 0x33),
                         (0x3104, 0x35),
                         (0x3105, 0x20),
                         (0x3106, 0x36),
                         (0x3107, 0x35),
                         (0x3108, 0x35),
                         (0x3109, 0x33),
                         (0x310a, 0x35),
                         (0x310b, 0x20),
                         (0x310c, 0x20),
                         (0x310d, 0x36),
                         (0x310e, 0x35),
                         (0x310f, 0x35),
                         (0x3110, 0x33),
                         (0x3111, 0x35),
                         (0x3112, 0x20),
                         (0x3113, 0x20),
                         (0x3114, 0x20),
                         (0x3115, 0x36),
                         (0x3116, 0x35),
                         (0x3117, 0x35),
                         (0x3118, 0x33),
                         (0x3119, 0x35),

                         (0x4000, 0x34),
                         (0x4001, 0x32),
                         (0x4002, 0x39),
                         (0x4003, 0x34),
                         (0x4004, 0x39),
                         (0x4005, 0x36),
                         (0x4006, 0x37),
                         (0x4007, 0x32),
                         (0x4008, 0x39),
                         (0x4009, 0x35),

                         (0x4100, 0x34),
                         (0x4101, 0x32),
                         (0x4102, 0x39),
                         (0x4103, 0x34),
                         (0x4104, 0x39),
                         (0x4105, 0x36),
                         (0x4106, 0x37),
                         (0x4107, 0x32),
                         (0x4108, 0x39),
                         (0x4109, 0x35),

                         (0x5000, 0x30),
                         (0x5100, 0x20),
                         (0x5101, 0x20),
                         (0x5102, 0x20),
                         (0x5103, 0x20),
                         (0x5104, 0x20),
                         (0x5105, 0x20),
                         (0x5106, 0x20),
                         (0x5107, 0x20),
                         (0x5108, 0x20),
                         (0x5109, 0x30),

        ]
#c c_test_dprintf_mux_one
class c_test_dprintf_mux_one(simple_tb.base_th):
    sram_reqs = {0:[(0x1010, 0x41),
                    (0x1011, 0x42),
                    (0x1012, 0x43),
                    (0x1013, 0x44),
                    (0x1014, 0x45),
                    (0x1015, 0x46),
                    (0x1016, 0x47),
                    (0x1017, 0x48),
                    (0x1018, 0x44),
                    (0x1019, 0x45),
                    (0x101a, 0x41),
                    (0x101b, 0x44),
                    (0x101c, 0x42),
                    (0x101d, 0x45),
                    (0x101e, 0x45),
                    (0x101f, 0x46),
                    ],
                 1:[(0x2010, 0x20),],
                 2:[(0x3010, 0x22),],
                 3:[(0x4010, 0x33),],
                 }
    requests = {50:(1,),
                52:(0,),
                80:(0,1,),
                90:(0,1,2,3),
                150:(0,1,2,3),
                200:(3,),
                250:(0,1),
                251:(2,),
                252:(3,),
                }
    responses = [1,0,1,0,3,2,1,0,
                 3,2,1,0,
                 3,
                 2,3,1,0,]
    expected_sram_ops = []
    for i in responses:
        expected_sram_ops.extend(sram_reqs[i])
        pass
    #f bfm_tick
    def bfm_tick(self, cycles):
        for i in range(cycles):
            acks = self.ios.acks.value()
            if acks!=0:
                if (acks &~ self.current_reqs)!=0:
                    self.failtest(0,"Ack of unrequested data %d/%d"%(acks, self.current_reqs))
                    pass
                self.current_reqs = self.current_reqs &~ acks
                self.ios.reqs.drive(self.current_reqs)
                pass
            if self.tick in self.requests:
                for j in self.requests[self.tick]:
                    self.current_reqs = self.current_reqs | (1<<j)
                    pass
                self.ios.reqs.drive(self.current_reqs)
                pass
            self.tick = self.tick + 1
            if (self.ios.display_sram_write__enable.value()):
                self.sram_writes.append( (self.ios.display_sram_write__address.value(),
                                          self.ios.display_sram_write__data.value(),) )
                pass
            self.bfm_wait(1)
            pass
        pass
    #f run
    def run(self):
        self.sram_writes = []
        self.tick = 0
        self.current_reqs = 0
        simple_tb.base_th.run_start(self)
        self.ios.reqs.drive(0)
        self.bfm_wait(10)
        self.bfm_tick(10000)
        if len(self.sram_writes) != len(self.expected_sram_ops):
            self.failtest(0,"Mismatch in number of SRAM writes %d/%d"%(len(self.sram_writes),len(self.expected_sram_ops)))
            for s in self.sram_writes:
                print "(0x%04x, 0x%02x),"%(s[0],s[1])
                pass
            pass
        else:
            for i in range(len(self.sram_writes)):
                if self.expected_sram_ops[i][0] != self.sram_writes[i][0]:
                    self.failtest(i,"Mismatch in SRAM %d write address %04x/%04x"%(i,self.expected_sram_ops[i][0], self.sram_writes[i][0]))
                    pass
                if self.expected_sram_ops[i][1] != self.sram_writes[i][1]:
                    self.failtest(i,"Mismatch in SRAM %d write data %02x/%02x"%(i,self.expected_sram_ops[i][1], self.sram_writes[i][1]))
                    pass
                pass
            pass
        self.finishtest(0,"")
        pass

#a Hardware classes
#c teletext_dprintf_hw
class teletext_dprintf_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of the teletext dprintf module
    """
    th_forces = { "th.clock":"clk",
                  "th.inputs":("" +
                               "display_sram_write__address[16] " +
                               "display_sram_write__data[48] " +
                               "display_sram_write__enable " +
                               "dprintf_ack " +
                               ""),
                  "th.outputs":("" +
                                "dprintf_req__data_1[64] " +
                                "dprintf_req__data_0[64] " +
                                "dprintf_req__address[16] " +
                                "dprintf_req__valid " +
                                ""),
                  }
    module_name = "tb_teletext_dprintf"
    pass

#c teletext_dprintf_mux_hw
class teletext_dprintf_mux_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of the teletext dprintf mux module
    """
    th_forces = { "th.clock":"clk",
                  "th.inputs":("" +
                               "display_sram_write__address[16] " +
                               "display_sram_write__data[48] " +
                               "display_sram_write__enable " +
                               "acks[4] " +
                               ""),
                  "th.outputs":("" +
                                "reqs[4] "+
                                ""),
                  }
    module_name = "tb_teletext_dprintf_mux"
    pass

#c cdl_test_hw
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
                               "csr_response__ack "+
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
                               "display_sram_write__address[16] "+
                               "display_sram_write__data[48] "+
                               "display_sram_write__enable "+
                                ""),
                  }


    module_name = "tb_framebuffer_teletext"
    pass

#a Simulation test classes
#c c_Test_LedChain
class c_Test_LedChain(simple_tb.base_test):
    def test_one(self):
        test = c_test_one()
        hw = cdl_test_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=1000*1000)
        pass
    pass

#c dprintf
class dprintf(simple_tb.base_test):
    def test_one(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_one()), num_cycles=100*1000)
    def test_two(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_two()), num_cycles=1000*1000)
    def test_three(self): self.do_test_run(teletext_dprintf_hw(test=c_test_dprintf_three()), num_cycles=1000*1000)
    pass
#c dprintf_mux
class dprintf_mux(simple_tb.base_test):
    def test_one(self):
        test = c_test_dprintf_mux_one()
        hw = teletext_dprintf_mux_hw(test=test)
        self.do_test_run(hw,
                         num_cycles=100*1000)
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
