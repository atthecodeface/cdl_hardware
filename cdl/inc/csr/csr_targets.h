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
 * @file   csr_interface.h
 * @brief  Types and modules for the CSR interface
 *
 * Header file for the types and modules in the pipelined CSR
 * interface, including APB target to CSR master, CSR target to APB
 * master, and CSR target to simple CSR access.
 *
 */

/*a Includes */
include "types/apb.h"
include "types/csr.h"

/*a Modules */
/*m csr_target_apb
 *
 * CSR target that drives an APB
 *
 */
extern
module csr_target_apb( clock                    clk           "Clock for the CSR interface, possibly gated version of master CSR clock",
                       input bit                reset_n       "Active low reset",
                       input t_csr_request      csr_request   "Pipelined csr request interface input",
                       output t_csr_response    csr_response  "Pipelined csr request interface response",
                       output t_apb_request     apb_request   "APB request to target",
                       input t_apb_response     apb_response  "APB response from target",
                       input bit[16]            csr_select    "Hard-wired select value for the client"
    )
{
    timing to   rising clock clk csr_request, csr_select;
    timing from rising clock clk csr_response;

    timing from rising clock clk apb_request;
    timing to   rising clock clk apb_response;
}

/*m csr_target_csr
 *
 * CSR target that drives a CSR access (select, read, write, data)
 *
 */
extern
module csr_target_csr( clock                       clk           "Clock for the CSR interface, possibly gated version of master CSR clock",
                       input bit                reset_n       "Active low reset",
                       input t_csr_request      csr_request   "Pipelined csr request interface input",
                       output t_csr_response    csr_response  "Pipelined csr request interface response",
                       output t_csr_access      csr_access    "Registered CSR access request to client",
                       input  t_csr_access_data csr_access_data "Read data valid combinatorially based on csr_access",
                       input bit[16]            csr_select    "Hard-wired select value for the client"
    )
{
    timing to   rising clock clk csr_request, csr_select;
    timing from rising clock clk csr_response;

    timing from rising clock clk csr_access;
    timing to   rising clock clk csr_access_data;
}

/*m csr_target_timeout
 *
 * CSR target that implements a timeout
 *
 * One of these can be placed on a CSR bus tree to terminate transactions that never complete
 *
 */
extern
module csr_target_timeout( clock                       clk        "Clock for the CSR interface, possibly gated version of master CSR clock",
                           input bit                reset_n       "Active low reset",
                           input t_csr_request      csr_request   "Pipelined csr request interface input",
                           output t_csr_response    csr_response  "Pipelined csr request interface response",
                           input bit[16]            csr_timeout   "Number of cycles to wait for until auto-acknowledging a request"
    )
{
    timing to   rising clock clk csr_request, csr_timeout;
    timing from rising clock clk csr_response;
}
