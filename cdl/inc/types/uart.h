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
 * @file   uart.h
 * @brief  Header for types for UARTs
 *
 * Header file for the types and CDL modules for UARTs
 *
 */

/*a Types */
/*t t_uart_tx_data */
typedef struct {
    bit txd   "Transmit data pin out";
    bit cts   "Assert low to enable rx data if other end uses handshaking";
} t_uart_tx_data;

/*t t_uart_rx_data */
typedef struct {
    bit rxd   "Receive data pin in";
    bit rts   "Asserted low if other end allows start of transmit";
} t_uart_rx_data;

/*t t_uart_status */
typedef struct {
    bit tx_empty;
    bit rx_not_empty;
    bit rx_half_full;
    bit rx_parity_error;
    bit rx_framing_error;
    bit rx_overflow;
} t_uart_status;

/*t t_uart_control */
typedef struct {
    bit clear_errors "Asserted if overflow, framing error, parity error, etc are to be cleared";
    bit rx_ack       "Asserted if any valid rx data is being taken";
    bit tx_valid     "Asserted if the tx data is valid";
    bit[8] tx_data   "Data to transmit if tx_valid is asserted";
    bit write_config "Assert to write configuration of UART (framing etc)";
    bit write_brg    "Assert to write configuration of UART brg";
    bit[32] write_data "Data to use if write_config or write_brg is asserted";
} t_uart_control;

/*t t_uart_output */
typedef struct {
    bit[32] config_data     "Current configuration, as last written (defaults to 0)";
    bit[32] brg_config_data "Current configuration of brg, as last written (defaults to 0)";
    t_uart_status status "Status for, e.g. interrupts";
    bit tx_ack       "If asserted, a tx_valid byte will be taken";
    bit rx_valid     "Asserted if rx_data is valid";
    bit[8] rx_data   "Data received if rx_valid is asserted";
} t_uart_output;
