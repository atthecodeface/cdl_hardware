#a APB
#t apb_request
apb_request = {
    "paddr":32,
    "penable":1,
    "psel":1,
    "pwrite":1,
    "pwdata":32,
}

#t apb_response
apb_response = {
    "prdata":32,
    "pready":1,
    "perr":1,
}

#t apb_processor_response
apb_processor_response = {
    "acknowledge":1,
    "rom_busy":1,
}

#t apb_processor_request
apb_processor_request = {
    "valid":1,
    "address":16,
}

#t apb_rom_request
apb_rom_request = {
    "enable":1,
    "address":16,
}

#a Timer
#t timer_control
timer_control = {"reset_counter":1,
                 "enable_counter":1,
                 "block_writes":1,
                 "bonus_subfraction_numer":8,
                 "bonus_subfraction_denom":8,
                 "fractional_adder":4,
                 "integer_adder":8,
}

#t timer_value
timer_value = {"irq":1,
               "value":64,
}

#a I/O
#t uart_rx
uart_rx = {"rxd":1, "rts":1}

#t uart_tx
uart_tx = {"txd":1, "cts":1}

#t mdio
mdio = {"mdc":1, "mdio":1, "mdio_enable":1}

#t i2c
i2c = {"scl":1, "sda":1}

#t i2c_master_request
i2c_master_request = {"valid":1,
                      "cont":1,
                      "data":32,
                      "num_in":3,
                      "num_out":3,
}

#t i2c_master_response
i2c_master_response = {"ack":1,
                       "in_progress":1,
                       "response_valid":1,
                       "response_type":3,
                       "data":32,
}

#t i2c_conf
i2c_conf = {"divider":8, "period":8}

#a clocking - bit_delay and phase_measure
#t t_bit_delay_config 
bit_delay_config = { "load":1, "value":9}

#t t_bit_delay_response
bit_delay_response = { "load_ack":1, "value":9, "sync_value":1}

#t phase_measure_request
phase_measure_request = {"valid":1}

#t phase_measure_response
phase_measure_response = {"ack":1, "abort":1, "valid":1, "delay":9, "initial_delay":9, "initial_value":1}
#a dprintf
#t dprintf_byte
dprintf_byte = {"address":16,
                "data":8,
                "last":1,
                "valid":1,
}

#t dprintf_req_4
dprintf_req_4 = {
    "valid":1,
    "address":16,
    "data_0":64,
    "data_1":64,
    "data_2":64,
    "data_3":64,
    }

#t dprintf_req_2
dprintf_req_2 = {
    "valid":1,
    "address":16,
    "data_0":64,
    "data_1":64,
    }

#t vcu108_inputs
vcu108_inputs = {
    "i2c":i2c,
    "eth_int_n":1,
    "mdio":1,
    "uart_rx":uart_rx,
    "switches":4,
    "buttons":5}

#t vcu108_outputs
vcu108_outputs = {
    "i2c":i2c,
    "i2c_reset_mux_n":1,
    "eth_reset_n":1,
    "mdio":mdio,
    "uart_tx":uart_tx,
    "leds":8,
}

#t adv7511
adv7511 = {"spdif":1,
           "hsync":1,
           "vsync":1,
           "de":1,
           "data":16,
}
#t mem_flash_in
#t mem_flash_out
