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
 * @file   picoriscv_submodules.h
 * @brief  Modules that make up a Pico-RISC-V microcomputer
 *
 */

/*a Includes
 */
include "picoriscv_types.h"

/*a Modules
 */
/*m picoriscv_clocking
 */
extern
module picoriscv_clocking( clock clk,
                           input bit reset_n,
                           input t_prv_clock_status      clock_status,
                           output t_prv_mem_control      mem_control,
                           output t_prv_clock_control    clock_control,
                           input t_csr_request   csr_request,
                           output t_csr_response csr_response
    )
{
    timing to   rising clock clk clock_status, csr_request;
    timing from rising clock clk clock_control, csr_response;
    timing comb input  clock_status;
    timing comb output clock_control, mem_control;
}
