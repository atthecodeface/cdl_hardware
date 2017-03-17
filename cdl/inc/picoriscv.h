/** @copyright (C) 2016-2017,  Gavin J Stark.  All rights reserved.
 *
 * @copyright
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0.
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *
 * @file   picoriscv.h
 * @brief  Module that makes up a Pico-RISC-V microcomputer
 *
 */

/*a Includes
 */
include "framebuffer.h"
include "csr_interface.h"
include "picoriscv_types.h"

/*a Modules
 */
/*m picoriscv_clocking
 */
extern
module picoriscv( clock clk                   "Clock, divided down for CPU",
                  input bit reset_n           "Active low reset",
                  clock video_clk             "Video clock, independent of CPU clock",
                  input bit video_reset_n     "Active low reset",
                  output t_video_bus video_bus,
                  input t_prv_keyboard keyboard,
                  input t_csr_request   csr_request,
                  output t_csr_response csr_response

                  //,
                  //output t_bbc_floppy_op floppy_op,
                  //input t_bbc_floppy_response floppy_response,
                  //input t_bbc_micro_sram_request   host_sram_request,
                  //output t_bbc_micro_sram_response host_sram_response
)
{
    timing to   rising clock clk keyboard, csr_request;
    timing from rising clock clk csr_response;
    timing from rising clock video_clk video_bus;
}
