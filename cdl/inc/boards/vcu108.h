/** Copyright (C) 2019,  Gavin J Stark.  All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @file   vcu108.h
 * @brief  Header file for Xilinx VCU108 board
 *
 * Header file for the types and CDL modules
 *
 */

/*a Includes */
include "types/i2c.h"
include "types/mdio.h"
include "types/uart.h"

/*a Types */
/*t t_vcu108_inputs - low speed inputs */
typedef struct {
    bit[4]  switches;
    bit[5]  buttons; // N S W E C
    t_uart_rx_data uart_rx;
    bit     mdio; // L3, M1
    bit     eth_int_n; // L1
    t_i2c   i2c;
} t_vcu108_inputs;

/*t t_vcu108_outputs - low speed outputs */
typedef struct {
    bit[8]     leds;
    t_uart_tx_data uart_tx;
    t_mdio_out mdio; // L3, M1
    bit        eth_reset_n; // K3
    bit        i2c_reset_mux_n;
    t_i2c      i2c;
} t_vcu108_outputs;

/*t t_vcu108_bpi_flash - the actual I/O for record */
typedef struct {
    bit[16] d;
    bit[26] a;
    bit fwe_b;
    bit oe_b;
    bit adv;
} t_vcu_bpi_flash;
