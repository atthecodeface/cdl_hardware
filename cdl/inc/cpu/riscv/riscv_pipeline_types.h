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
 * @file   riscv_internal_types.cdl
 * @brief  Internal types and constants for RISC-V implementations
 *
 */

/*a Includes
 */
include "cpu/riscv/riscv.h"
include "cpu/riscv/riscv_internal_types.h"

/*a RISC-V pipeline control interaction */
/*t t_riscv_pipeline_control_fetch_action
 */
typedef enum[3] {
    rv_pc_fetch_action_idle, // Idle the pipeline by flushing anything pre-exec
    rv_pc_fetch_action_none, // execute but don't fetch
    rv_pc_fetch_action_restart_at_pc,
    rv_pc_fetch_action_retry,
    rv_pc_fetch_action_continue_fetching
} t_riscv_pipeline_control_fetch_action;

/*t t_riscv_pipeline_state - early in clock cycle to affect response
 */
typedef bit[2] t_riscv_pipeline_tag;
typedef struct {
    // add in exec_wfi_continues, and exec_take_interrupt
    bit      valid;
    t_riscv_pipeline_control_fetch_action fetch_action;
    bit[32]  fetch_pc "PC of instruction to be fetched";
    t_riscv_mode mode "Mode the pipeline is executing in";
    bit          error;
    t_riscv_pipeline_tag tag;
    bit    halt                    "Halt the CPU by 'faking' an ebreak";
    bit    ebreak_to_dbg           "Breakpoint would go to debug mode (halt CPU)";
    bit    interrupt_req;
    bit[4] interrupt_number;
    t_riscv_mode interrupt_to_mode "If interrupt then this is the mode that whose pp/pie/epc should be set from current mode's";
    t_riscv_word           instruction_data;
    t_riscv_i32_inst_debug instruction_debug;
} t_riscv_pipeline_state;

/*t t_riscv_pipeline_control - early in clock cycle to affect response
 */
typedef struct {
    // add in exec_wfi_continues, and exec_take_interrupt
    bit      valid;
    t_riscv_pipeline_control_fetch_action fetch_action;
    bit[32]  fetch_pc "PC of instruction to be fetched";
    t_riscv_mode mode "Mode the pipeline is executing in";
    bit          error;
    t_riscv_pipeline_tag tag;
    bit    halt                    "Halt the CPU by 'faking' an ebreak";
    bit    ebreak_to_dbg           "Breakpoint would go to debug mode (halt CPU)";
    bit    interrupt_req;
    bit[4] interrupt_number;
    t_riscv_mode interrupt_to_mode "If interrupt then this is the mode that whose pp/pie/epc should be set from current mode's";
    t_riscv_word           instruction_data;
    t_riscv_i32_inst_debug instruction_debug;
    bit decode_cannot_complete"Asserted if the decode has a valid instruction that either cannot be started or cannot complete";
    bit exec_committed;
    bit exec_cannot_start "Asserted if the instruction is blocked from starting; ignored unless valid and first_cycle; can be because of blocked_by_mem or coprocessor not ready";
    bit exec_cannot_complete"Asserted if the ALU has a valid instruction that either cannot be started or cannot complete";

    t_riscv_word pc_if_mispredicted "From pipeline_fetch_data associated with the decode of this instruction";
    bit async_cancel;
    bit branch_taken;
    bit jalr;
    t_riscv_i32_trap trap;
    bit flush_fetch;
    bit flush_decode;
    bit flush_exec;
} t_riscv_pipeline_control;

/*t t_riscv_pipeline_response_decode
 */
typedef struct {
    bit      valid             "Asserted if branch_target and idecode are valid";
    bit[32]  pc                "PC of instruction in decode stage";
    bit[32]  branch_target     "Used if predict_branch";
    t_riscv_i32_decode idecode "Decode of instruction (if valid)";
    bit enable_branch_prediction "Asserted if branch prediction (and hence branch_target) is to be used";
} t_riscv_pipeline_response_decode;

/*t t_riscv_pipeline_response_exec
 */
typedef struct {
    bit valid;
    bit cannot_start    "Asserted if the pipeline cannot start - not dependent on coprocessors (if any)";
    bit cannot_complete "Asserted if the pipeline cannot complet - not dependent on coprocessors (if any)";
    bit interrupt_block "In standard pipelines this must be low; it blocks interrupts";
    t_riscv_i32_inst instruction;
    t_riscv_i32_decode idecode "Decode of instruction (if valid)";
    t_riscv_word rs1;
    t_riscv_word rs2;
    bit[32]  pc              "Actual PC of execution instruction";
    bit          predicted_branch   "From pipeline_fetch_data associated with the decode of this instruction";
    t_riscv_word pc_if_mispredicted "From pipeline_fetch_data associated with the decode of this instruction";
    bit branch_condition_met;
    bit first_cycle;
    t_riscv_mem_access_req dmem_access_req;
    t_riscv_csr_access     csr_access;
    bit[32]  branch_target     "Used if predict_branch";
} t_riscv_pipeline_response_exec;

/*t t_riscv_pipeline_response_rfw
 */
typedef struct {
    bit valid;
    bit rd_written;
    bit[5] rd;
    t_riscv_word data;
} t_riscv_pipeline_response_rfw;

/*t t_riscv_pipeline_response - mid cycle (dependent on control) to effect fetch request and hence fetch data
 */
typedef struct {
    t_riscv_pipeline_response_decode decode;
    t_riscv_pipeline_response_exec   exec;
    t_riscv_pipeline_response_rfw    rfw;
    bit                              pipeline_empty;
} t_riscv_pipeline_response;

/*t t_riscv_pipeline_fetch_data
 */
typedef struct {
    bit          valid;
    t_riscv_word pc;
    t_riscv_i32_inst instruction;
    bit          dec_predicted_branch   "Not part of fetch - indicates that pipeline_control predicted a branch for the decode, so when the decode is executed this should match the execution - if not, a mispredict occurs";
    t_riscv_word dec_pc_if_mispredicted;
} t_riscv_pipeline_fetch_data;

