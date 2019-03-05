/** @copyright (C) 2016-2018,  Gavin J Stark.  All rights reserved.
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
 * @file   riscv_modules.h
 * @brief  Header file for RISC-V implementations
 *
 */

/*a Includes */
include "types/apb.h"
include "types/jtag.h"
include "utils/jtag_modules.h"
include "cpu/riscv/riscv.h"
include "cpu/riscv/riscv_internal_types.h"

/*a Implementations */
/*m riscv_i32_pipeline_control
 */
extern module riscv_i32_pipeline_control( clock clk,
                                          input bit reset_n,
                                          input bit riscv_clk_enable,
                                          input t_riscv_csrs_minimal         csrs,
                                          output t_riscv_pipeline_state      pipeline_state,
                                          input t_riscv_pipeline_response    pipeline_response,
                                          input t_riscv_pipeline_fetch_data  pipeline_fetch_data,
                                          input t_riscv_pipeline_control     pipeline_control,
                                          input  t_riscv_config              riscv_config,
                                          input t_riscv_i32_trace            trace,
                                          input  t_riscv_debug_mst               debug_mst,
                                          output t_riscv_debug_tgt               debug_tgt,

                                          input bit[6] rv_select
)
{
    timing to   rising clock clk riscv_clk_enable;
    timing to   rising clock clk csrs, pipeline_response, pipeline_fetch_data;
    timing to   rising clock clk riscv_config, trace;
    timing to   rising clock clk debug_mst;
    timing from rising clock clk pipeline_state;
    timing from rising clock clk debug_tgt;
    timing comb input riscv_config, csrs;
    timing comb output pipeline_state, debug_tgt;
}

/*m riscv_i32_pipeline_control_fetch_req
 */
extern module riscv_i32_pipeline_control_fetch_req( input t_riscv_pipeline_state     pipeline_state,
                                                    input t_riscv_pipeline_response  pipeline_response,
                                                    output t_riscv_fetch_req           ifetch_req
)
{
    timing comb input pipeline_state, pipeline_response;
    timing comb output ifetch_req;
}

/*m riscv_i32_pipeline_control_fetch_data
 */
extern module riscv_i32_pipeline_control_fetch_data( input t_riscv_pipeline_state   pipeline_state,
                                                     input t_riscv_fetch_req          ifetch_req,
                                                     input t_riscv_fetch_resp         ifetch_resp,
                                                    input t_riscv_pipeline_response  pipeline_response,
                                                     output t_riscv_pipeline_fetch_data pipeline_fetch_data
)
{
    timing comb input pipeline_state, pipeline_response, ifetch_req, ifetch_resp;
    timing comb output pipeline_fetch_data;
}

/*m riscv_i32_pipeline_control_csr_trace
 */
extern module riscv_i32_pipeline_control_csr_trace( input t_riscv_pipeline_state    pipeline_state,
                                                    input t_riscv_pipeline_response   pipeline_response,
                                                    input t_riscv_pipeline_fetch_data pipeline_fetch_data,
                                                    input  t_riscv_config             riscv_config,
                                                    input t_riscv_i32_coproc_response   coproc_response,
                                                    output t_riscv_i32_coproc_controls  coproc_controls,
                                                    output t_riscv_csr_controls       csr_controls,
                                                    output t_riscv_i32_trace          trace
    )
{
    timing comb input  pipeline_state, pipeline_response, pipeline_fetch_data, riscv_config, coproc_response;
    timing comb output coproc_controls, csr_controls, trace;
}

/*m riscv_i32_pipeline_control_flow
 */
extern module riscv_i32_pipeline_control_flow( input t_riscv_pipeline_state       pipeline_state,
                                               input t_riscv_pipeline_response    pipeline_response,
                                               output t_riscv_pipeline_control    pipeline_control
)
{
    timing comb input pipeline_state, pipeline_response;
    timing comb output pipeline_control;
}

/*m riscv_i32c_pipeline
 */
extern
module riscv_i32c_pipeline( clock clk,
                            input bit reset_n,
                            output t_riscv_mem_access_req      dmem_access_req,
                            input  t_riscv_mem_access_resp     dmem_access_resp,
                            input t_riscv_pipeline_state     pipeline_state,
                            output t_riscv_pipeline_response   pipeline_response,
                            input t_riscv_pipeline_fetch_data  pipeline_fetch_data,
                            input t_riscv_i32_coproc_response  coproc_response,
                            output t_riscv_csr_access          csr_access,
                            input t_riscv_word                 csr_read_data,
                            input  t_riscv_config              riscv_config
)
{
    timing from rising clock clk dmem_access_req, pipeline_response, csr_access;
    timing to   rising clock clk dmem_access_resp, pipeline_state, coproc_response, csr_read_data;
    timing to   rising clock clk riscv_config;
    timing comb input riscv_config, pipeline_state;
    timing comb output dmem_access_req, pipeline_response, csr_access;
}

/*m riscv_i32c_pipeline3
 */
extern
module riscv_i32c_pipeline3( clock clk,
                             input bit reset_n,
                             input t_riscv_pipeline_state     pipeline_state,
                             input t_riscv_pipeline_control     pipeline_control,
                             output t_riscv_pipeline_response   pipeline_response,
                             input t_riscv_pipeline_fetch_data  pipeline_fetch_data,
                             output t_riscv_mem_access_req  dmem_access_req,
                             input  t_riscv_mem_access_resp dmem_access_resp,
                             input t_riscv_i32_coproc_response   coproc_response,
                             output t_riscv_csr_access          csr_access,
                             input t_riscv_word                 csr_read_data,
                             input  t_riscv_config          riscv_config
)
{
    timing from rising clock clk dmem_access_req, pipeline_response, csr_access;
    timing to   rising clock clk dmem_access_resp, pipeline_state, pipeline_control, pipeline_fetch_data, coproc_response, csr_read_data;
    timing to   rising clock clk riscv_config;
    timing comb input riscv_config, pipeline_state, coproc_response;
    timing comb output pipeline_response, dmem_access_req, csr_access;
}

