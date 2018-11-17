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
 * @file   apb_peripherals.h
 * @brief  Modules of various simple APB peripherals
 *
 * Header file for the modules for some very simple APB peripherals
 *
 */

/*a Includes */
include "types/apb.h"
include "boards/de1_cl/de1_cl_types.h"

/*a Modules - see also csr_target_apb, csr_master_apb in csr_interface.h */
/*m apb_target_de1_cl_inputs */
extern
module apb_target_de1_cl_inputs( clock clk         "System clock",
                                 input bit reset_n "Active low reset",

                                 input  t_apb_request  apb_request  "APB request",
                                 output t_apb_response apb_response "APB response",

                                 input t_de1_cl_user_inputs    user_inputs
    )
{
    timing to   rising clock clk apb_request;
    timing from rising clock clk apb_response;

    timing to   rising clock clk user_inputs;
    
}

/*a Editor preferences and notes
mode: c ***
c-basic-offset: 4 ***
c-default-style: (quote ((c-mode . "k&r") (c++-mode . "k&r"))) ***
outline-regexp: "/\\\*a\\\|[\t ]*\/\\\*[b-z][\t ]" ***
*/


