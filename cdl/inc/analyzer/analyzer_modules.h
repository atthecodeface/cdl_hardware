/** Copyright (C) 2020,  Gavin J Stark.  All rights reserved.
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
 * @file   analyzer_modules.h
 * @brief  Modules for logic analyzer tying
 *
 * Header file for the types and CDL modules for the analyzer
 *
 */

/*a Includes */
include "types/apb.h"
include "types/analyzer.h"

/*a Modules */
/*m analyzer_mux_8 */
extern
module analyzer_mux_8( clock clk,
                       input bit reset_n,
                       input  t_analyzer_mst  analyzer_mst,
                       output t_analyzer_tgt  analyzer_tgt,

                       output  t_analyzer_mst  analyzer_mst_a,
                       input   t_analyzer_tgt  analyzer_tgt_a,

                       output  t_analyzer_mst  analyzer_mst_b,
                       input   t_analyzer_tgt  analyzer_tgt_b,

                       output  t_analyzer_mst  analyzer_mst_c,
                       input   t_analyzer_tgt  analyzer_tgt_c,

                       output  t_analyzer_mst  analyzer_mst_d,
                       input   t_analyzer_tgt  analyzer_tgt_d,

                       output  t_analyzer_mst  analyzer_mst_e,
                       input   t_analyzer_tgt  analyzer_tgt_e,

                       output  t_analyzer_mst  analyzer_mst_f,
                       input   t_analyzer_tgt  analyzer_tgt_f,

                       output  t_analyzer_mst  analyzer_mst_g,
                       input   t_analyzer_tgt  analyzer_tgt_g,

                       output  t_analyzer_mst  analyzer_mst_h,
                       input   t_analyzer_tgt  analyzer_tgt_h

    )
{
    timing to     rising clock clk analyzer_mst;
    timing from   rising clock clk analyzer_tgt;

    timing to     rising clock clk analyzer_tgt_a, analyzer_tgt_b, analyzer_tgt_c, analyzer_tgt_d;
    timing to     rising clock clk analyzer_tgt_e, analyzer_tgt_f, analyzer_tgt_g, analyzer_tgt_h;
    timing from   rising clock clk analyzer_mst_a, analyzer_mst_b, analyzer_mst_c, analyzer_mst_d;
    timing from   rising clock clk analyzer_mst_e, analyzer_mst_f, analyzer_mst_g, analyzer_mst_h;

}
/*m analyzer_mux_2 */
extern
module analyzer_mux_2( clock clk,
                       input bit reset_n,
                       input  t_analyzer_mst  analyzer_mst,
                       output t_analyzer_tgt  analyzer_tgt,

                       output  t_analyzer_mst  analyzer_mst_a,
                       input   t_analyzer_tgt  analyzer_tgt_a,

                       output  t_analyzer_mst  analyzer_mst_b,
                       input   t_analyzer_tgt  analyzer_tgt_b

    )
{
    timing to     rising clock clk analyzer_mst;
    timing from   rising clock clk analyzer_tgt;

    timing to     rising clock clk analyzer_tgt_a, analyzer_tgt_b;
    timing from   rising clock clk analyzer_mst_a, analyzer_mst_b;
}

/*m analyzer_target_stub */
extern
module analyzer_target_stub( clock clk,
                           input bit reset_n,
                           input  t_analyzer_mst  analyzer_mst,
                           output t_analyzer_tgt  analyzer_tgt
    )
{
    timing to     rising clock clk analyzer_mst;
    timing from   rising clock clk analyzer_tgt;
}

/*m analyzer_target */
extern
module analyzer_target( clock clk,
                        input bit reset_n,
                        input  t_analyzer_mst  analyzer_mst,
                        output t_analyzer_tgt  analyzer_tgt,
                        output t_analyzer_ctl analyzer_ctl,
                        input t_analyzer_data analyzer_data
    )
{
    timing to     rising clock clk analyzer_mst;
    timing from   rising clock clk analyzer_tgt;

    timing from   rising clock clk analyzer_ctl;
    timing to     rising clock clk analyzer_data;
}


/*m apb_target_analyzer */
extern module apb_target_analyzer( clock analyzer_clock,
                            clock async_trace_read_clock,
                            clock apb_clock,

                            input bit reset_n,

                            input  t_apb_request  apb_request  "APB request",
                            output t_apb_response apb_response "APB response",

                            output bit trace_ready,
                            output bit trace_done,

                            output  t_analyzer_mst  analyzer_mst,
                            input t_analyzer_tgt  analyzer_tgt,

                            input bit ext_trigger_reset,
                            input bit ext_trigger_enable,

                            input bit async_trace_read_enable,
                            output bit async_trace_valid_out,
                            output bit[32] async_trace_out )
{
    timing to   rising clock apb_clock apb_request;
    timing from rising clock apb_clock apb_response;

    timing from rising clock analyzer_clock trace_ready, trace_done;
    timing from rising clock analyzer_clock analyzer_mst;
    timing to   rising clock analyzer_clock analyzer_tgt;
    timing to   rising clock analyzer_clock ext_trigger_reset, ext_trigger_enable;

    timing to   rising clock async_trace_read_clock async_trace_read_enable;
    timing from rising clock async_trace_read_clock async_trace_valid_out, async_trace_out;
}

