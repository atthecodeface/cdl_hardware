#!/usr/bin/env python
import subprocess
import apb_rom
import sys

displays = {}
displays["lcd_480x272"] = {"h":(40,480,5),
                           "v":(8,272,8)
                           }

display = displays["lcd_480x272"]

csr_select = {}
csr_select["vga_rom"] = 0x00034000 # for HPS FPGA frame buffer OR framebuffer_teletext
csr_select["dprintf"] = 0x00020000 # for HPS FPGA dprintf
csr_display_size    = csr_select["vga_rom"] |  0
csr_display_h_porch = csr_select["vga_rom"] |  4
csr_display_v_porch = csr_select["vga_rom"] |  8
csr_dprintf_address        = csr_select["dprintf"] |  0
csr_dprintf_data           = csr_select["dprintf"] |  32
csr_dprintf_address_commit = csr_select["dprintf"] |  64
csr_dprintf_data_commit    = csr_select["dprintf"] | 128

h_porches    = (display["h"][0]-1) | ((display["h"][2]-1)<<16) # back porch in low, front porch in high
v_porches    = (display["v"][0]-1) | ((display["v"][2]-1)<<16) # 
display_size = (display["h"][1]-1) | ((display["v"][1]-1)<<16) # h size in low, v size in high

porches = [(65536-170+16-3*i) | (((65536-68)<<16)) for i in range(16)]

# data is bigendian in dprintf
# dprintf data is 0-skip; 1->127 character; 128-143 1 to 16 hex nybbles; 192-195 1-4 byte unpadded decimal; 192+(pad<<2)+(nbytes) is 1-4 nbytes decimal with padding of field to (pad+1)

cs_string = subprocess.check_output(["git","rev-parse","HEAD"]).strip()
cs = int(cs_string[:16],16)
print >> sys.stderr, "VGA rom - CS from GIT is ",cs_string
print >> sys.stderr, "%016x"%cs
dprintf_data = [0]*8
dprintf_data[0] = 0x48505320
dprintf_data[1] = 0x46504741
dprintf_data[2] = 0x0343533a # 03 -> green (teletext)
dprintf_data[3] = 0x8f000000 | ((cs>>40)&0xffffff)
dprintf_data[4] = (cs>> 8)&0xffffffff
dprintf_data[5] = (((cs>> 0)&0xff) << 24) | 0xffffff
dprintf_data[6] = 0xffffffff
program = {}
program["code"] = []
#program["code"] += [ (apb_rom.rom.op_set("address",csr_display_size),),
#                     (apb_rom.rom.op_req("write_arg_inc",display_size),),
#                     (apb_rom.rom.op_req("write_arg_inc",h_porches),),
#                     (apb_rom.rom.op_req("write_arg_inc",v_porches),),
#                     ]
program["code"] += [ (apb_rom.rom.op_set("address",csr_dprintf_data),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[0]),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[1]),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[2]),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[3]),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[4]),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[5]),),
                     (apb_rom.rom.op_req("write_arg_inc",dprintf_data[6]),),
                     (apb_rom.rom.op_set("address",csr_dprintf_address_commit),),
                     (apb_rom.rom.op_req("write_arg",40*0),),
                     ]
program["code"] += [
    (apb_rom.rom.op_finish(),),
    ]
compilation = apb_rom.rom.compile_program(program)
apb_rom.rom.mif_of_compilation(compilation)
