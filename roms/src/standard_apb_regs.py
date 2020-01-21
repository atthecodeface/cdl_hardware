# Before subsys_minimal
apb_rv_sram  = 0x00040000
apb_rv_debug = 0x000b0000
apb_uart = 0x00090000
apb_dprintf_uart = 0x000a0000

# After subsys_minimal
apb_uart         = 0x00090000
apb_dprintf_uart = 0x000a0000
apb_rv_sram      = 0x00180000
apb_rv_debug     = 0x00181000

apb_rv_sram_address       = apb_rv_sram | 0x00
apb_rv_sram_data          = apb_rv_sram | 0x04
apb_rv_sram_control       = apb_rv_sram | 0x08

apb_uart_brg    = apb_uart | 4
apb_uart_config = apb_uart | 8
apb_uart_hr     = apb_uart | 12

apb_dprintf_uart_brg    = apb_dprintf_uart | 4
apb_dprintf_uart_config = apb_dprintf_uart | 8

apb_rv_debug_data0        = apb_rv_debug | 0x10
apb_rv_debug_dmcontrol    = apb_rv_debug | 0x40
apb_rv_debug_abstract_cmd = apb_rv_debug | 0x5c

