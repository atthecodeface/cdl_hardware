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
/*m csr_master_apb
 *
 * APB target that drive a CSR master
 *
 */
extern
module csr_master_apb( clock                    clk           "Clock for the CSR interface; a superset of all targets clock",
                       input bit                reset_n       "Active low reset",
                       input t_apb_request      apb_request   "APB request from master",
                       output t_apb_response    apb_response  "APB response to master",
                       input t_csr_response     csr_response  "Pipelined csr request interface response",
                       output t_csr_request     csr_request   "Pipelined csr request interface output"
    )
{
    timing to   rising clock clk csr_response;
    timing from rising clock clk csr_request;

    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;
}

