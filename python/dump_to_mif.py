#!/usr/bin/env python
import sys
import dump
dump_filename = sys.argv[1]
base_address = int(sys.argv[2],0)
d = dump.c_dump()
f = open(dump_filename)
d.load(f, base_address)
f.close()
d.write_mif(sys.stdout)
