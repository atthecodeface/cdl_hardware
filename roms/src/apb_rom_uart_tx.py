import apb_rom
import clock_divider
from standard_apb_regs import *

# 1 out of 17
# brg_config = 0x80010010
# 3 adds of 16 and 16 subs of 3 gets back again
# so cycle of 19 and 3 so 3 out of 19
#brg_config = 0x80030010
#brg_config = 1
#delay      = (brg_config+2)*6*10

def program(defines):
    clk = apb_rom.get_define_int(defines,"clk",100)
    brg_config = clock_divider.config_for_frequency(f=0.1152*16, clk=clk, accuracy=0.005)
    ns_per_clk = 1000. / clk
    delay      = int(1000. * 1000. * 1000. / ns_per_clk)

    program = {}
    program["code"] = []
    program["code"] += [ (apb_rom.rom.op_set("increment",4),),
                         (apb_rom.rom.op_set("address",apb_uart_brg),),
                         (apb_rom.rom.op_req("write_arg",brg_config),),
                         (apb_rom.rom.op_set("address",apb_dprintf_uart_brg),),
                         (apb_rom.rom.op_req("write_arg",brg_config),),
                         (apb_rom.rom.op_set("address",apb_uart_hr),),
                         (apb_rom.rom.op_set("accumulator",64),),
                         (apb_rom.rom.op_req("write_acc",brg_config),("loop:",)),
                         (apb_rom.rom.op_wait(delay),),
                         (apb_rom.rom.op_req("read",brg_config),),
                         (apb_rom.rom.op_alu("add",1),),
                         (apb_rom.rom.op_branch("branch",0),("loop",)),
    ]
    program["code"] += [
        (apb_rom.rom.op_finish(),),
    ]
    return program
