#!/usr/bin/env python

import csv

import argparse

parser = argparse.ArgumentParser(description='Display execution trace of RV simulation')
parser.add_argument('--logfile', type=str, default='itrace.log',
                    help='logfile to parse')
parser.add_argument('--module', type=str, default="dut.trace",
                    help='module to show trace of')

args = parser.parse_args()

csvfile = open("itrace.log", "rb")
trace = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in trace:
    if (row[2]==args.module):
        if False: # branch + trap flow
            if (row[3] == '1'):
                flow = int(row[5]) + int(row[6])*2
                print flow
                pass
            pass
        else: # rfw retirement flow
            if (row[3] == '2') and (row[5] == '1'):
                print row[6], row[7] # rd, data
                pass
            pass
        pass
    pass



        

