#!/usr/bin/env python
import apb_rom
csr_select = {}
csr_select["clock_control"] = 0
csr_select["bbc_display"] = 1
clock_control = (csr_select["clock_control"]<<16)|0
display_porches = (csr_select["bbc_display"]<<16)|2
speeds = [0x0015, 0x0215, 0x0415, 0x0615, 0x0815, 0x0a15, 0x0c15, 0x0e15, 0x1015, 0x1215, 0x1415, 0x1515]

porches = [(65536-170+16-3*i) | (((65536-68)<<16)) for i in range(12)]
           
def set_speed(speed):
    return [(apb_rom.rom.op_set("address",clock_control),["speed%d:"%speed]),
            (apb_rom.rom.op_req("write_arg",speeds[speed]),),
            (apb_rom.rom.op_finish(),),
            ] + ([ (apb_rom.rom.op_finish(),), ]*13)
def set_porch(porch):
    return [(apb_rom.rom.op_set("address",display_porches),["porches%d:"%porch]),
            (apb_rom.rom.op_req("write_arg",porches[porch]),),
            (apb_rom.rom.op_finish(),),
            ] + ([ (apb_rom.rom.op_finish(),), ]*13)
program = {}
program["code"] = []
for i in range(len(speeds)):
    program["code"] += set_speed(i)
    pass
program["code"] += ([ (apb_rom.rom.op_finish(),), ]*64)
for i in range(len(porches)):
    program["code"] += set_porch(i)
    pass
compilation = apb_rom.rom.compile_program(program)

for (a,d) in compilation["object"]:
    print "%02x: %010x"%(a,d)
    pass
