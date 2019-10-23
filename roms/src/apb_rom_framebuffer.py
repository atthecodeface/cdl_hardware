#!/usr/bin/env python
import version_control
import display_config
import apb_rom
import sys

csr_select = {}
csr_select["lcd_tt"]   = 0x00032000 # for HPS FPGA LCD teletext frame buffer (start / bytes per line)
csr_select["lcd_fbt"]  = 0x00033000 # for HPS FPGA LCD frame buffer timing
csr_select["vga_tt"]   = 0x00034000 # for HPS FPGA VGA teletext frame buffer (start / bytes per line)
csr_select["vga_fbt"]  = 0x00035000 # for HPS FPGA VGA frame buffer timing
csr_select["dprintf"]  = 0x00020000 # for HPS FPGA dprintf
csr_dprintf_address        = csr_select["dprintf"] |  0
csr_dprintf_data           = csr_select["dprintf"] |  32
csr_dprintf_address_commit = csr_select["dprintf"] |  64
csr_dprintf_data_commit    = csr_select["dprintf"] |  96

def code_display_parameters(csr_base, display):
    h_porches    = (display["h"][0]-1) | ((display["h"][2]-1)<<16) # back porch in low, front porch in high
    v_porches    = (display["v"][0]-1) | ((display["v"][2]-1)<<16) # 
    display_size = (display["h"][1]-1) | ((display["v"][1]-1)<<16) # h size in low, v size in high

    csr_display_size    = csr_base |  0
    csr_display_h_porch = csr_base |  4
    csr_display_v_porch = csr_base |  8

    return [ (apb_rom.rom.op_set("address",csr_display_size),),
             (apb_rom.rom.op_set("increment",4),),
             (apb_rom.rom.op_req("write_arg_inc",display_size),),
             (apb_rom.rom.op_req("write_arg_inc",h_porches),),
             (apb_rom.rom.op_req("write_arg_inc",v_porches),),
             ]

# data is bigendian in dprintf
# dprintf data is 0-skip; 1->127 character; 128-143 1 to 16 hex nybbles; 192-195 1-4 byte unpadded decimal; 192+(pad<<2)+(nbytes) is 1-4 nbytes decimal with padding of field to (pad+1)

program = {}
program["code"] = []
program["code"] += code_display_parameters(csr_select["vga_fbt"],displays["vga_640x480"])
program["code"] += code_display_parameters(csr_select["lcd_fbt"],displays["vga_640x480"])
program["code"] += [ (apb_rom.rom.op_set("increment",4),),
                     (apb_rom.rom.op_set("address",csr_dprintf_data),),
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
