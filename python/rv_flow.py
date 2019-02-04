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
            if (row[3] == '0'): #timestamp,id,dut.trace,0="PC",7,"pc","branch_taken","trap","ret","jalr","branch_target","instr"

                pc = int(row[5])
                branch_taken = row[6]
                trap         = row[7]
                ret          = row[8]
                jalr         = row[9]
                print "%08x %d %d %d %d"%(pc,branch_taken,trap,ret,jalr)
                pass
            pass
        else: # rfw retirement flow
            if (row[3] == '1') and (row[5] == '1'): #timestamp,id,dut.trace,1="retire",3,"rfw","rd","data"
                rfw_rd   = row[6]
                rfw_data = row[7]
                print rfw_rd, rfw_data
                pass
            pass
        pass
    pass



        

