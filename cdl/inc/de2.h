/** Copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
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
 * @file   de2.h
 * @brief  Header file for Altera DE2 board
 *
 * Header file for the types and CDL modules
 *
 */

/*a Includes */
include "csr_interface.h"
include "input_devices.h"

/*a Types */
/*t t_de2_inputs */
typedef struct {
    bit[4]  keys;
    bit[18] switches;
    bit     irda_rxd;
} t_de2_inputs;

/*t t_de2_audio */
typedef struct {
    bit data;
    bit lrc;
} t_de2_audio;

/*t t_i2c */
typedef struct {
    bit sclk   "Open collector output";
    bit sdat   "Open collector output";
} t_i2c;

/*t t_de2_lcd */
typedef struct {
    bit backlight;
    bit on;
    bit rs;
    bit read_write;
    bit enable;
    bit[8] data;
} t_de2_lcd;

/*t t_uart_in */
typedef struct {
    bit rxd;
    bit rts;
} t_uart_in;

/*t t_uart_out */
typedef struct {
    bit txd;
    bit cts;
} t_uart_out;

/*t t_de2_leds */
typedef struct {
    bit[10] ledg;
    bit[18] ledr;
    bit[7] h0;
    bit[7] h1;
    bit[7] h2;
    bit[7] h3;
    bit[7] h4;
    bit[7] h5;
    bit[7] h6;
    bit[7] h7;
} t_de2_leds;

/*t t_adv7180 */
typedef struct {
    bit hs;
    bit vs;
    bit[8] data;
} t_adv7180;

/*t t_de2_gpio */
typedef struct {
    bit[18] gpio_0;
    bit[18] gpio_1;
} t_de2_gpio;

/*t t_sdram_16_12_2_out */
typedef struct {
    bit cke;
    bit cs_n;
    bit ras_n;
    bit cas_n;
    bit we_n;
    bit[2]  ba;
    bit[12] addr;
    bit[16] dq;
    bit[2]  dqm;
    bit dqe "Assert to drive dq out";
} t_sdram_16_12_2_out;

/*t t_sdram_16_12_2_in */
typedef struct {
    bit[16] dq;
} t_sdram_16_12_2_in;

/*t t_asram_16_18_out */
typedef struct {
    bit ce_n;
    bit oe_n;
    bit we_n;
    bit[2] be_n;
    bit[12] addr;
    bit[16] dq;
    bit dqe "Assert to drive dq out";
} t_asram_16_18_out;

/*t t_asram_16_18_in */
typedef struct {
    bit[16] dq;
} t_asram_16_18_in;

/*t t_flash_8_22_out */
typedef struct {
    bit reset_n;
    bit ce_n;
    bit oe_n;
    bit we_n;
    bit[22] addr;
    bit[8] dq;
    bit dqe "Assert to drive dq out";
} t_flash_8_22_out;

/*t t_flash_8_22_in */
typedef struct {
    bit[8] dq;
} t_flash_8_22_in;
