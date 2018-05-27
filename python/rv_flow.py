#!/usr/bin/env python

import csv

csvfile = open("itrace.log", "rb")
trace = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in trace:
    if (row[3] == '2') and (row[2]=='dut.dut.trace'):
        flow = int(row[5]) + int(row[6])*2
        print flow



        

