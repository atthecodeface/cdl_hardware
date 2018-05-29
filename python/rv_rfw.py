#!/usr/bin/env python

import csv

csvfile = open("itrace.log", "rb")
trace = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in trace:
    if (row[3] == '3') and (row[2]=='dut.dut.trace'):
        rd = int(row[5],16)
        data = int(row[6],16)
        print "r%d <= %08x"%(rd, data)




        

