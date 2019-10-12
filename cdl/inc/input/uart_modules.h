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
 * @file   input_devices.h
 * @brief  Input device header file for CDL modules
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Includes */
include "types/uart.h"

/*a Modules */
/*m uart_minimal */
extern module uart_minimal( clock clk,
                     input bit reset_n,

                     input  t_uart_control uart_control,
                     output t_uart_output uart_output,

                     input    t_uart_rx_data uart_rx,
                     output   t_uart_tx_data uart_tx
    )
{
    timing to   rising clock clk uart_control, uart_rx;
    timing from rising clock clk uart_output, uart_tx;
}

