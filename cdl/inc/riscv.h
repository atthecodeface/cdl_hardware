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
 * @file   riscv.h
 * @brief  Header file for RISC-V implementations
 *
 */

/*a Includes */
include "jtag.h"

/*a Constants
 *
 * Constants for the RISC-V implementation; can be overridden in CDL
 * builds with a dc: option in the model_list
 */
constant integer RISCV_DATA_ADDR_WIDTH = 14;
constant integer RISCV_INSTR_ADDR_WIDTH = 14;

/*a Basic types
 */
/*t t_riscv_mem_access_req
 */
typedef struct {
    bit[32]  address;
    bit[4]   byte_enable;
    bit      write_enable;
    bit      read_enable;
    bit[32]  write_data;
} t_riscv_mem_access_req;

/*t t_riscv_mem_access_resp */
typedef struct {
    bit                  wait;
    bit[32]              read_data;
} t_riscv_mem_access_resp;

/*t t_riscv_word
 */
typedef bit[32] t_riscv_word;

/*t t_riscv_fetch_req
 */
typedef struct {
    bit      valid;
    bit[32]  address;
    bit      sequential;
    // Needs mode
    // Flush indication
    // will_take?
} t_riscv_fetch_req;

/*t t_riscv_fetch_resp
 */
typedef struct {
    bit      valid;
    bit      debug  "Needs to permit register read/write encoding, break after execution, break before execution, execution mode, breakpoint-in-hardware-not-software; force-debug-subroutine-trap-before-execution";
    bit[32]  data;
    // Needs mode and error
    // Needs tag
} t_riscv_fetch_resp;

/*t t_riscv_config
 */
typedef struct {
    bit      i32c;
    bit      e32;
    bit      i32m;
    bit      i32m_fuse;
} t_riscv_config;

/*t t_riscv_debug_op
 */
typedef enum[4] {
    rv_debug_set_requests   "Set request bits for halt, resume, step (args[0..2])",
    rv_debug_read   "Request read of a GPR/CSR",
    rv_debug_write  "Request write of a GPR/CSR",
    rv_debug_acknowledge "Acknowledge halt, breakpoint hit, status; removes attention signal",
    rv_debug_execute "Execute instruction provided resumption of execution at dpc and in mode dcsr.prv",
    rv_debug_execute_progbuf "Execute instruction at 'progbuf' address X (if it is a jump and link it will return)",
} t_riscv_debug_op;

typedef bit t_riscv_debug_resp;
/*t t_riscv_debug_mst
 *
 * Debug module (DM) communication to (many) pipeline debug modules (PDMs)
 *
 * 
 *
 */
typedef struct {
    bit valid           "Asserted if op is valid; has no effect on mask and attention";
    bit[6] select       "PDM to select";
    bit[6] mask         "PDM attention mask (mask && id)==(mask&&select) -> drive attention on next cycle";
    t_riscv_debug_op op "Operation for selected PDM to perform";
    bit[16] arg          "Argument for debug op";
    t_riscv_word data   "Data for writing or instruction execution";
} t_riscv_debug_mst;

/*t t_riscv_debug_tgt
 */
typedef struct {
    bit valid               "Asserted by a PDM if driving the bus";
    bit[6] selected         "Number of the PDM driving, or 0 if not driving the bus";
    bit halted              "Asserted by a PDM if it is selected and halted since last ack; 0 otherwise";
    bit resumed             "Asserted by a PDM if it is selected and has resumed since last ack; 0 otherwise";
    bit hit_breakpoint      "Asserted by a PDM if it is selected and has hit breakpoint since lask ack; 0 otherwise";
    bit op_was_none "Asserted if the response is not valid";
    t_riscv_debug_resp resp "Response from a requested op - only one op should be requested for each response";
    t_riscv_word data       "Data from a completed transaction; 0 otherwise";

    bit attention           "Asserted by a PDM if it has unacknowledged halt, breakpoint hit, resumption";
} t_riscv_debug_tgt;

/*t t_riscv_pipeline_debug_control
 */
typedef struct {
    bit valid;
    bit kill_fetch;
    bit halt_request;
    bit fetch_dret;
    t_riscv_word data       "Data from a completed transaction; 0 otherwise";
} t_riscv_pipeline_debug_control;

/*t t_riscv_pipeline_debug_response
 */
typedef struct {
    bit exec_valid;
    bit exec_halting;
    bit exec_dret;
} t_riscv_pipeline_debug_response;

/*t t_riscv_i32_trace
 */
typedef struct {
    bit                instr_valid;
    bit[32]            instr_pc   "Program counter of the instruction";
    t_riscv_word       instr_data "Instruction word being decoded";
    bit                rfw_retire "Asserted if an instruction is being retired";
    bit                rfw_data_valid;
    bit[5]             rfw_rd;
    t_riscv_word       rfw_data   "Result of ALU/memory operation for the instruction";
    bit                branch_taken "Asserted if a branch is being taken";
    bit[32]            branch_target "Target of branch if being taken";
    bit                trap;
    // Needs tag
} t_riscv_i32_trace;

/*a Implementations */
/*m riscv_minimal

 riscv_config should be HARDWIRED (not off registers) to force logic to be
 discarded at synthesis

 alternatively submodules may be built with appropriate force's set to
 force discard of logic.

 */
extern
module riscv_minimal( clock clk,
                      input bit reset_n,
                      output t_riscv_mem_access_req  dmem_access_req,
                      input  t_riscv_mem_access_resp dmem_access_resp,
                      output t_riscv_mem_access_req  imem_access_req,
                      input  t_riscv_mem_access_resp imem_access_resp,
                      input  t_riscv_config          riscv_config,
                      output t_riscv_i32_trace       trace
)
{
    timing from rising clock clk dmem_access_req, imem_access_req;
    timing to   rising clock clk dmem_access_resp, imem_access_resp;
    timing to   rising clock clk riscv_config;
    timing from rising clock clk trace;
    timing comb input riscv_config;
    timing comb output dmem_access_req, imem_access_req;
    timing comb input dmem_access_resp;
    timing comb output trace;
}

/*m riscv_i32c_pipeline
 */
extern
module riscv_i32c_pipeline( clock clk,
                            input bit reset_n,
                            output t_riscv_fetch_req       ifetch_req,
                            input  t_riscv_fetch_resp      ifetch_resp,
                            output t_riscv_mem_access_req  dmem_access_req,
                            input  t_riscv_mem_access_resp dmem_access_resp,
                            input  t_riscv_config          riscv_config,
                            output t_riscv_i32_trace       trace
)
{
    timing from rising clock clk dmem_access_req, ifetch_req;
    timing to   rising clock clk dmem_access_resp, ifetch_resp;
    timing to   rising clock clk riscv_config;
    timing from rising clock clk trace;
    timing comb input riscv_config;
    timing comb output dmem_access_req, ifetch_req;
    timing comb input dmem_access_resp;
    timing comb output trace;
}

/*m riscv_i32c_pipeline3
 */
extern
module riscv_i32c_pipeline3( clock clk,
                             input bit reset_n,
                             output t_riscv_fetch_req       ifetch_req,
                             input  t_riscv_fetch_resp      ifetch_resp,
                             output t_riscv_mem_access_req  dmem_access_req,
                             input  t_riscv_mem_access_resp dmem_access_resp,
                             input  t_riscv_config          riscv_config,
                             output t_riscv_i32_trace       trace
)
{
    timing from rising clock clk dmem_access_req, ifetch_req;
    timing to   rising clock clk dmem_access_resp, ifetch_resp;
    timing to   rising clock clk riscv_config;
    timing comb input riscv_config;
    timing comb output ifetch_req;
    timing from rising clock clk trace;
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

/*m riscv_i32_pipeline_debug */
extern module riscv_i32_pipeline_debug( clock clk,
                                 input bit reset_n,
                                 input  t_riscv_debug_mst debug_mst,
                                 output t_riscv_debug_tgt debug_tgt,
                                 output t_riscv_pipeline_debug_control debug_control,
                                 input  t_riscv_pipeline_debug_response debug_response,

                                 input bit[6] rv_select
)
{
    timing to rising clock clk debug_mst, debug_response, rv_select;
    timing from rising clock clk debug_control, debug_tgt;
    timing comb input rv_select;
    timing comb output debug_tgt;
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
                        input t_riscv_i32_trace trace "Trace signals"
)
{
    timing to rising clock clk trace;
}

