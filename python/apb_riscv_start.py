#!/usr/bin/env python
import apb_rom

apb_rv_sram  = 0x00040000
apb_rv_sram_address       = apb_rv_sram | 0x00
apb_rv_sram_data          = apb_rv_sram | 0x04
apb_rv_sram_control       = apb_rv_sram | 0x08

apb_rv_debug = 0x000b0000
apb_rv_debug_data0        = apb_rv_debug | 0x10
apb_rv_debug_dmcontrol    = apb_rv_debug | 0x40
apb_rv_debug_abstract_cmd = apb_rv_debug | 0x5c

apb_uart = 0x00090000
apb_uart_brg    = apb_uart | 4
apb_uart_config = apb_uart | 8
apb_uart_hr     = apb_uart | 12
apb_dprintf_uart = 0x000a0000
apb_dprintf_uart_brg    = apb_dprintf_uart | 4
apb_dprintf_uart_config = apb_dprintf_uart | 8

brg_config = 162

program = {}
program["code"] = []
program["code"] += [
                     (apb_rom.rom.op_set("address",apb_dprintf_uart_brg),),
                     (apb_rom.rom.op_req("write_arg",brg_config),),
    ]
program["code"] += [ (apb_rom.rom.op_set("address",apb_rv_sram_control),),
                     (apb_rom.rom.op_req("write_arg",1),), # Enable clock on RISC-V
                     (apb_rom.rom.op_set("address",apb_rv_debug_dmcontrol),),
                     (apb_rom.rom.op_req("write_arg",1),), # select HART 0 enable debug
                     (apb_rom.rom.op_set("address",apb_rv_debug_data0),),
                     (apb_rom.rom.op_req("write_arg",0),), # Set data0 to 0
                     (apb_rom.rom.op_set("address",apb_rv_debug_abstract_cmd),),
                     (apb_rom.rom.op_req("write_arg",0),), # set program counter to data0
                     (apb_rom.rom.op_set("address",apb_rv_debug_dmcontrol),),
                     (apb_rom.rom.op_req("write_arg",(1<<30)|1),), # Resume hart
                     ]
program["code"] += [
    (apb_rom.rom.op_finish(),),
    ]
compilation = apb_rom.rom.compile_program(program)
apb_rom.rom.mif_of_compilation(compilation)
