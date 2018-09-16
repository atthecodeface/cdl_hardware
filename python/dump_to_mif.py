#!/usr/bin/env python
import sys
import dump
dump_filename = sys.argv[1]
base_address = int(sys.argv[2],0)
if (len(sys.argv)>3):
    format = sys.argv[3]
    pass
d = dump.c_dump()
f = open(dump_filename)
d.load(f, base_address)
f.close()
if format=="C":
    d.write_c_data(sys.stdout)
else:    
    d.write_mif(sys.stdout)
