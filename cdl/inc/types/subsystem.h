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
 * @file   subsystem.h
 * @brief  CDL header file for subsystem types used in subsystem modules
 *
 * Header file for the types and CDL modules for subsystems
 *
 */

/*a Includes */
include "types/i2c.h"
include "types/uart.h"

/*a Types */
/*t t_subsys_inputs */
typedef struct {
    bit[8] switches;
    bit[8] buttons;
    t_uart_rx_data uart_rx;
    t_i2c          i2c;
    bit[8] gpio_input;
} t_subsys_inputs;

/*t t_subsys_outputs */
typedef struct {
    bit reset_request;
    t_uart_tx_data uart_tx;
    t_i2c          i2c;
    bit[8] gpio_output;
    bit[8] gpio_output_enable;
} t_subsys_outputs;

