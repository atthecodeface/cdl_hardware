/** Copyright (C) 2016-2018,  Gavin J Stark.  All rights reserved.
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
 * @file   axi4s_modules.h
 * @brief  AXI4s modules header file for CDL modules
 *
 * Header file for the types and CDL modules for AXI4S modules
 *
 */

/*a Includes */
include "types/axi.h"

/*m axi4s32_fifo_4 */
extern
module axi4s32_fifo_4( clock clk                      "Clock for the FIFO",
                       input bit reset_n              "Asynchronous reset",
                       input t_axi4s32 req_in         "AXI4S input side master data",
                       output bit ack_in              "AXI4S input side slave 'tready' signal",
                       output t_axi4s32 req_out       "AXI4S output side master data",
                       input bit ack_out              "AXI4S output side slave 'tready' signal"
    )
{
    timing to    rising clock clk req_in;
    timing from  rising clock clk ack_in;

    timing from  rising clock clk req_out;
    timing to    rising clock clk ack_out;
}

