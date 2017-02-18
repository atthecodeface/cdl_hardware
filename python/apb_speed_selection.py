#!/usr/bin/env python
import apb_rom
csr_select = {}
csr_select["clock_control"] = 0
clock_control = (csr_select["clock_control"]<<16)|0
speeds = [0x020c, 0x030c, 0x040c, 0x050c, 0x060c]*10
def set_speed(speed):
    return [(apb_rom.rom.op_set("address",clock_control),["speed%d:"%speed]),
            (apb_rom.rom.op_req("write_arg",speeds[speed]),),
            (apb_rom.rom.op_finish(),),
            ] + ([ (apb_rom.rom.op_finish(),), ]*13)
program = {}
program["code"] = []
for i in range(16):
    program["code"] += set_speed(i)
    pass
compilation = apb_rom.rom.compile_program(program)

for (a,d) in compilation["object"]:
    print "%02x: %010x"%(a,d)
    pass
