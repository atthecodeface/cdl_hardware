#!/usr/bin/env python
import sys
disk_filename = sys.argv[1]
a = open(disk_filename)
num_tracks = 40
sectors_per_track = 10
address = 0
r = "%04x: "%address    
while True:
    ch = a.read(4)
    if len(ch)==0: break
    r += "%02x%02x%02x%02x "%(ord(ch[3]),ord(ch[2]),ord(ch[1]),ord(ch[0]))
    address = address+1
    if (address%16)==0:
        print r
        r = "%04x: "%address    
        pass
    pass
address = 0xf000
for track in range(num_tracks):
    for sector in range(sectors_per_track):
        r = "%04x: "%address    
        r += "%08x" % ((track<<0) | (sector<<8) | (1<<16) | (0<<24)) # head 0, no errors etc
        print r
        address = address + 1
        pass
    pass
