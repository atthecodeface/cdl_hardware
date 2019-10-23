#!/usr/bin/env python
import subprocess
import sys

def git_cs(verbose = True):
    cs_string = subprocess.check_output(["git","rev-parse","HEAD"]).strip()
    if verbose:
        print >> sys.stderr, "CS from GIT is ",cs_string
        pass
    return int(cs_string[:16],16)

def dprintf_cs(cs):
    dprintf_data = [0]*8
    dprintf_data[0] = 0x48505320
    dprintf_data[1] = 0x46504741
    dprintf_data[2] = 0x0343533a # 03 -> green (teletext)
    dprintf_data[3] = 0x8f000000 | ((cs>>40)&0xffffff)
    dprintf_data[4] = (cs>> 8)&0xffffffff
    dprintf_data[5] = (((cs>> 0)&0xff) << 24) | 0xffffff
    dprintf_data[6] = 0xffffffff
    return dprintf_data
    
