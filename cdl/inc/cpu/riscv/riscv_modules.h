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
include "srams.h"

/*a Implementations of CPUs with memories */
/*m riscv_i32_minimal_generic  - Generic I32(CM) with pipeline length of 2+

 riscv_config should be HARDWIRED (not off registers) to force logic to be
 discarded at synthesis

 alternatively submodules may be built with appropriate force's set to
 force discard of logic.
*/
extern
module riscv_i32_minimal_generic( clock clk,
                                  input bit reset_n,
                                  input bit proc_reset_n,
                                  input t_riscv_irqs             irqs               "Interrupts in to the CPU",
                                  output t_riscv_mem_access_req  data_access_req,
                                  input  t_riscv_mem_access_resp data_access_resp,
                                  output t_apb_request           apb_request,
                                  input  t_apb_response          apb_response,
                                  input t_sram_access_req sram_access_req,
                                  output t_sram_access_resp sram_access_resp,
                                  input  t_riscv_debug_mst               debug_mst,
                                  output t_riscv_debug_tgt               debug_tgt,
                                  input  t_riscv_config          riscv_config,
                                  output t_riscv_i32_trace       trace
    )
{
    timing from rising clock clk apb_request;
    timing to   rising clock clk apb_response;
    timing from rising clock clk data_access_req;
    timing to   rising clock clk data_access_resp;
    timing to   rising clock clk sram_access_req;
    timing from rising clock clk sram_access_resp;
    timing to   rising clock clk riscv_config;
    timing to   rising clock clk debug_mst;
    timing from rising clock clk debug_tgt;
    timing to   rising clock clk irqs;
    timing from rising clock clk trace;
    timing comb input riscv_config;
    timing comb input data_access_resp;
    timing comb input apb_response;
    timing comb output trace;
    timing comb output debug_tgt;
}

/*m riscv_i32_minimal  - same as riscv_i32_minimal_generic

 riscv_config should be HARDWIRED (not off registers) to force logic to be
 discarded at synthesis

 alternatively submodules may be built with appropriate force's set to
 force discard of logic.
*/
extern
module riscv_i32_minimal( clock clk,
                                  input bit reset_n,
                                  input bit proc_reset_n,
                                  input t_riscv_irqs             irqs               "Interrupts in to the CPU",
                                  output t_riscv_mem_access_req  data_access_req,
                                  input  t_riscv_mem_access_resp data_access_resp,
                                  output t_apb_request           apb_request,
                                  input  t_apb_response          apb_response,
                                  input t_sram_access_req sram_access_req,
                                  output t_sram_access_resp sram_access_resp,
                                  input  t_riscv_debug_mst               debug_mst,
                                  output t_riscv_debug_tgt               debug_tgt,
                                  input  t_riscv_config          riscv_config,
                                  output t_riscv_i32_trace       trace
    )
{
    timing from rising clock clk apb_request;
    timing to   rising clock clk apb_response;
    timing from rising clock clk data_access_req;
    timing to   rising clock clk data_access_resp;
    timing to   rising clock clk sram_access_req;
    timing from rising clock clk sram_access_resp;
    timing to   rising clock clk riscv_config;
    timing to   rising clock clk debug_mst;
    timing from rising clock clk debug_tgt;
    timing to   rising clock clk irqs;
    timing from rising clock clk trace;
    timing comb input riscv_config;
    timing comb input data_access_resp;
    timing comb input apb_response;
    timing comb output trace;
    timing comb output debug_tgt;
}

/*m riscv_i32_minimal3 - same as riscv_i32_minimal_generic

 riscv_config should be HARDWIRED (not off registers) to force logic to be
 discarded at synthesis

 alternatively submodules may be built with appropriate force's set to
 force discard of logic.
*/
extern
module riscv_i32_minimal3( clock clk,
                                  input bit reset_n,
                                  input bit proc_reset_n,
                                  input t_riscv_irqs             irqs               "Interrupts in to the CPU",
                                  output t_riscv_mem_access_req  data_access_req,
                                  input  t_riscv_mem_access_resp data_access_resp,
                                  output t_apb_request           apb_request,
                                  input  t_apb_response          apb_response,
                                  input t_sram_access_req sram_access_req,
                                  output t_sram_access_resp sram_access_resp,
                                  input  t_riscv_debug_mst               debug_mst,
                                  output t_riscv_debug_tgt               debug_tgt,
                                  input  t_riscv_config          riscv_config,
                                  output t_riscv_i32_trace       trace
    )
{
    timing from rising clock clk apb_request;
    timing to   rising clock clk apb_response;
    timing from rising clock clk data_access_req;
    timing to   rising clock clk data_access_resp;
    timing to   rising clock clk sram_access_req;
    timing from rising clock clk sram_access_resp;
    timing to   rising clock clk riscv_config;
    timing to   rising clock clk debug_mst;
    timing from rising clock clk debug_tgt;
    timing to   rising clock clk irqs;
    timing from rising clock clk trace;
    timing comb input riscv_config;
    timing comb input data_access_resp;
    timing comb input apb_response;
    timing comb output trace;
    timing comb output debug_tgt;
}

/*a Interfaces */
/*m riscv_i32_minimal_apb */
extern
module riscv_i32_minimal_apb( clock clk,
                              input bit reset_n,
                              input  t_riscv_mem_access_req  data_access_req,
                              output t_riscv_mem_access_resp data_access_resp,
                              output t_apb_request apb_request,
                              input  t_apb_response apb_response
)
{
    timing comb input  apb_response; //, data_access_req;
    timing comb output data_access_resp;
    timing to   rising clock clk data_access_req, apb_response;
    timing from rising clock clk data_access_resp, apb_request;
}

/*a Trace, debug */
/*m riscv_jtag_apb_dm */
extern module riscv_jtag_apb_dm( clock jtag_tck                "JTAG TCK signal, used as a clock",
                                 input bit reset_n             "Reset that drives all the logic",

                                 input bit[5] ir               "JTAG IR which is to be matched against t_jtag_addr",
                                 input t_jtag_action dr_action "Action to perform with DR (capture or update, else ignore)",
                                 input  bit[50]dr_in           "Data register in; used in update, replaced by dr_out in capture, shift",
                                 output bit[50]dr_tdi_mask     "One-hot mask indicating which DR bit TDI should replace (depends on IR)",
                                 output bit[50]dr_out          "Data register out; same as data register in, except during capture when it is replaced by correct data dependent on IR, or shift when it goes right by one",

                                 clock apb_clock                   "APB clock signal, asynchronous to JTAG TCK",
                                 output t_apb_request apb_request  "APB request out",
                                 input t_apb_response apb_response "APB response"
    )
{
    timing to rising clock jtag_tck ir, dr_action, dr_in;
    timing from rising clock jtag_tck dr_tdi_mask, dr_out;
    timing from rising clock apb_clock apb_request;
    timing to rising clock apb_clock apb_response;
    timing comb input dr_in, dr_action, ir;
    timing comb output dr_out, dr_tdi_mask;
}

/*m riscv_i32_debug */
extern module riscv_i32_debug( clock clk         "System clock",
                         input bit reset_n "Active low reset",

                         input  t_apb_request  apb_request  "APB request",
                         output t_apb_response apb_response "APB response",

                        output t_riscv_debug_mst debug_mst "Debug master to PDMs",
                        input t_riscv_debug_tgt debug_tgt "Debug target from PDMs"
    )
{
    timing to   rising clock clk apb_request, debug_tgt;
    timing from rising clock clk apb_response, debug_mst;
}

/*m riscv_i32_ifetch_debug */
extern module riscv_i32_ifetch_debug( input t_riscv_fetch_req pipeline_ifetch_req,
                                      output t_riscv_fetch_resp pipeline_ifetch_resp,
                                      input t_riscv_i32_trace pipeline_trace,
                                      input t_riscv_pipeline_debug_control debug_control,
                                      output t_riscv_pipeline_debug_response debug_response,
                                      output t_riscv_fetch_req ifetch_req,
                                      input t_riscv_fetch_resp ifetch_resp
)
{
    timing comb input pipeline_ifetch_req, pipeline_trace, debug_control, ifetch_resp;
    timing comb output pipeline_ifetch_resp, debug_response, ifetch_req;
}

/*m riscv_i32_trace  */
extern
module riscv_i32_trace( clock clk            "Clock for the CPU",
                        input bit reset_n     "Active low reset",
                        input bit riscv_clk_enable,
                        input t_riscv_i32_trace trace "Trace signals"
)
{
    timing to   rising clock clk riscv_clk_enable;
    timing to rising clock clk trace;
}

/*m riscv_i32_trace_pack */
extern module riscv_i32_trace_pack( clock clk            "Free-running clock",
                                           input bit reset_n     "Active low reset",
                                           input t_riscv_packed_trace_control trace_control      "Control of trace",
                                           input t_riscv_i32_trace trace "Trace signals",
                                           output t_riscv_i32_packed_trace packed_trace "Packed trace"
)
{
    timing to   rising clock clk trace_control, trace;
    timing from rising clock clk packed_trace;
}

/*m riscv_i32_trace_compression */
extern module riscv_i32_trace_compression( input t_riscv_i32_packed_trace packed_trace      "Control of trace",
                                           output t_riscv_i32_compressed_trace compressed_trace "Compressed trace"
)
{
    timing comb input packed_trace;
    timing comb output compressed_trace;
}

/*m riscv_i32_trace_decompression */
extern module riscv_i32_trace_decompression( input bit[64] compressed_nybbles "Nybbles from compressed trace",
                                             output t_riscv_i32_decompressed_trace decompressed_trace "Decompressed trace",
                                             output bit[5] nybbles_consumed "number of nybbles (from bit 0) consumed by current decompression"
)
{
    timing comb input compressed_nybbles;
    timing comb output decompressed_trace, nybbles_consumed;
}

/*a CSR modules */
/*m riscv_csrs - generic, may not be built  */
extern
module riscv_csrs( clock clk                                   "RISC-V clock",
                   clock riscv_clk                             "Clk gated by riscv_clk_enable - provide for single clock gate outside the module",
                   input bit reset_n                           "Active low reset",
                   input bit riscv_clk_enable,
                   input t_riscv_irqs       irqs               "Interrupts in to the CPU",
                   input t_riscv_csr_access csr_access         "RISC-V CSR access, combinatorially decoded",
                   output t_riscv_csr_data csr_data            "CSR response (including take interrupt and read data), from the current @a csr_access",
                   input t_riscv_csr_controls csr_controls     "Control signals to update the CSRs",
                   output t_riscv_csrs        csrs            "CSR values"
    )
{
    timing to   rising clock clk riscv_clk_enable;
    timing to   rising clock riscv_clk csr_access, csr_controls, irqs;
    timing from rising clock riscv_clk csr_data, csrs;
    timing comb input csr_access;
    timing comb output csr_data;
}

/*m riscv_csrs_machine_only  */
extern
module riscv_csrs_machine_only( clock clk                                   "RISC-V clock",
                   clock riscv_clk                             "Clk gated by riscv_clk_enable - provide for single clock gate outside the module",
                   input bit reset_n                           "Active low reset",
                   input bit riscv_clk_enable,
                   input t_riscv_irqs       irqs               "Interrupts in to the CPU",
                   input t_riscv_csr_access csr_access         "RISC-V CSR access, combinatorially decoded",
                   output t_riscv_csr_data csr_data            "CSR response (including take interrupt and read data), from the current @a csr_access",
                   input t_riscv_csr_controls csr_controls     "Control signals to update the CSRs",
                   output t_riscv_csrs        csrs            "CSR values"
    )
{
    timing to   rising clock clk riscv_clk_enable;
    timing to   rising clock riscv_clk csr_access, csr_controls, irqs;
    timing from rising clock riscv_clk csr_data, csrs;
    timing comb input csr_access;
    timing comb output csr_data;
}

/*m riscv_csrs_machine_debug  */
extern
module riscv_csrs_machine_debug( clock clk                                   "RISC-V clock",
                   clock riscv_clk                             "Clk gated by riscv_clk_enable - provide for single clock gate outside the module",
                   input bit reset_n                           "Active low reset",
                   input bit riscv_clk_enable,
                   input t_riscv_irqs       irqs               "Interrupts in to the CPU",
                   input t_riscv_csr_access csr_access         "RISC-V CSR access, combinatorially decoded",
                   output t_riscv_csr_data csr_data            "CSR response (including take interrupt and read data), from the current @a csr_access",
                   input t_riscv_csr_controls csr_controls     "Control signals to update the CSRs",
                   output t_riscv_csrs        csrs            "CSR values"
    )
{
    timing to   rising clock clk riscv_clk_enable;
    timing to   rising clock riscv_clk csr_access, csr_controls, irqs;
    timing from rising clock riscv_clk csr_data, csrs;
    timing comb input csr_access;
    timing comb output csr_data;
}

/*m riscv_csrs_machine_debug_user  */
extern
module riscv_csrs_machine_debug_user( clock clk                                   "RISC-V clock",
                   clock riscv_clk                             "Clk gated by riscv_clk_enable - provide for single clock gate outside the module",
                   input bit reset_n                           "Active low reset",
                   input bit riscv_clk_enable,
                   input t_riscv_irqs       irqs               "Interrupts in to the CPU",
                   input t_riscv_csr_access csr_access         "RISC-V CSR access, combinatorially decoded",
                   output t_riscv_csr_data csr_data            "CSR response (including take interrupt and read data), from the current @a csr_access",
                   input t_riscv_csr_controls csr_controls     "Control signals to update the CSRs",
                   output t_riscv_csrs        csrs            "CSR values"
    )
{
    timing to   rising clock clk riscv_clk_enable;
    timing to   rising clock riscv_clk csr_access, csr_controls, irqs;
    timing from rising clock riscv_clk csr_data, csrs;
    timing comb input csr_access;
    timing comb output csr_data;
}

/*m riscv_csrs_machine_debug_user_irq  */
extern
module riscv_csrs_machine_debug_user_irq( clock clk                                   "RISC-V clock",
                   clock riscv_clk                             "Clk gated by riscv_clk_enable - provide for single clock gate outside the module",
                   input bit reset_n                           "Active low reset",
                   input bit riscv_clk_enable,
                   input t_riscv_irqs       irqs               "Interrupts in to the CPU",
                   input t_riscv_csr_access csr_access         "RISC-V CSR access, combinatorially decoded",
                   output t_riscv_csr_data csr_data            "CSR response (including take interrupt and read data), from the current @a csr_access",
                   input t_riscv_csr_controls csr_controls     "Control signals to update the CSRs",
                   output t_riscv_csrs        csrs            "CSR values"
    )
{
    timing to   rising clock clk riscv_clk_enable;
    timing to   rising clock riscv_clk csr_access, csr_controls, irqs;
    timing from rising clock riscv_clk csr_data, csrs;
    timing comb input csr_access;
    timing comb output csr_data;
}

