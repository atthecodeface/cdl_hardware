#!/usr/bin/env python
import apb_rom
csr_select = {}
csr_select["clock_control"] = 0
csr_select["bbc_display"] = 1
clock_control = (csr_select["clock_control"]<<16)|0
display_porches = (csr_select["bbc_display"]<<16)|2
speeds = [0x000b, 0x010b, 0x020b, 0x040b, 0x060b, 0x080b, 0x0a0b,
          0x031c, 0x011c]
porches = [(65536-280-12) | (((65536-70)<<16)),
           (65536-280-8) | (((65536-70)<<16)),
           (65536-280-6) | (((65536-70)<<16)),
    ]
           
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
for i in range(len(porches)):
    program["code"] += set_porch(i)
    pass
compilation = apb_rom.rom.compile_program(program)

for (a,d) in compilation["object"]:
    print "%02x: %010x"%(a,d)
    pass
