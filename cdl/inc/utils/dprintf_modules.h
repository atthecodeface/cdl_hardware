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
 * @file   input_devices.h
 * @brief  Input device header file for CDL modules
 *
 * Header file for the types and CDL modules for input devices
 *
 */

/*a Includes */
include "types/dprintf.h"

/*a Modules */
/*m dprintf */
extern
module dprintf( clock clk "Clock for data in and display SRAM write out",
                input bit reset_n,
                input t_dprintf_req_4   dprintf_req  "Debug printf request",
                output bit              dprintf_ack  "Debug printf acknowledge",
                input bit               byte_blocked "If asserted, byte to output will not change",
                output t_dprintf_byte   dprintf_byte "Byte to output"
    )
{
    timing to   rising clock clk dprintf_req;
    timing from rising clock clk dprintf_ack, dprintf_byte;
}

/*m dprintf_2_mux */
extern
module dprintf_2_mux( clock clk,
                              input bit reset_n,
                              input t_dprintf_req_2 req_a,
                              input t_dprintf_req_2 req_b,
                              output bit ack_a,
                              output bit ack_b,
                              output t_dprintf_req_2 req,
                              input bit ack
    )
{
    timing to    rising clock clk req_a, req_b;
    timing from  rising clock clk ack_a, ack_b;

    timing from  rising clock clk req;
    timing to    rising clock clk ack;
}
/*m dprintf_4_mux */
extern
module dprintf_4_mux( clock clk,
                              input bit reset_n,
                              input t_dprintf_req_4 req_a,
                              input t_dprintf_req_4 req_b,
                              output bit ack_a,
                              output bit ack_b,
                              output t_dprintf_req_4 req,
                              input bit ack
    )
{
    timing to    rising clock clk req_a, req_b;
    timing from  rising clock clk ack_a, ack_b;

    timing from  rising clock clk req;
    timing to    rising clock clk ack;
}
