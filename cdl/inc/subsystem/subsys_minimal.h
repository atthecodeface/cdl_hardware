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
 * @file   subsys_minimal.h
 * @brief  Subsys_minimal CDL module
 *
 */

/*a Includes */
include "types/apb.h"
include "types/video.h"
include "types/csr.h"
include "types/dprintf.h"
include "types/timer.h"
include "types/subsystem.h"

/*a Modules */
extern module subsys_minimal( clock clk,
                       input bit reset_n,

                       input  t_apb_request     master_apb_request "APB request from main system",
                       output t_apb_response    master_apb_response "APB request from main system",
                       input  t_dprintf_req_4   master_dprintf_req "Dprintf request from board (sync to clk)",
                       output bit               master_dprintf_ack "Ack for dprintf request",
                       output t_csr_request     master_csr_request,
                       input  t_csr_response    master_csr_response,

                       input  t_subsys_inputs   subsys_inputs,
                       output t_subsys_outputs  subsys_outputs,

                       clock video_clk,
                       input bit video_reset_n,
                       output t_video_bus video_bus,
                       input bit        tx_axi4s_tready,
                       output t_axi4s32 tx_axi4s,
                       input t_axi4s32  rx_axi4s,
                       output bit       rx_axi4s_tready,
                       output t_timer_control timer_control,
                       output bit[32] analyzer_mux_control,
                       input bit[32] analyzer_trace
    )
{
    timing to   rising clock clk master_apb_request, master_dprintf_req;
    timing from rising clock clk master_apb_response, master_dprintf_ack;

    timing from rising clock clk master_csr_request;
    timing to   rising clock clk master_csr_response;

    timing to   rising clock clk tx_axi4s_tready, rx_axi4s;
    timing from rising clock clk rx_axi4s_tready, tx_axi4s;

    timing to   rising clock clk subsys_inputs, analyzer_trace;
    timing from rising clock clk subsys_outputs, timer_control;

    timing from rising clock video_clk video_bus;
}
