apb_uart = 0x00090000
apb_uart_brg    = apb_uart | 4
apb_uart_config = apb_uart | 8
apb_uart_hr     = apb_uart | 12
apb_dprintf_uart = 0x000a0000
apb_dprintf_uart_brg    = apb_dprintf_uart | 4
apb_dprintf_uart_config = apb_dprintf_uart | 8

brg_config = 162
delay      = 1<<24
# 1 out of 17
# brg_config = 0x80010010
# 3 adds of 16 and 16 subs of 3 gets back again
# so cycle of 19 and 3 so 3 out of 19
#brg_config = 0x80030010
#brg_config = 1
#delay      = (brg_config+2)*6*10
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
compilation = apb_rom.rom.compile_program(program)
apb_rom.rom.mif_of_compilation(compilation)
