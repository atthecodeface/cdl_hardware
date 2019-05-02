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

/*a Constants
 */
constant integer RV32I_EBREAK=0x00100073;

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

/*t t_riscv_pipeline_control_decode - late in clock cycle to affect clocking
 */
typedef struct {
    bit completing     "Asserted if decode is valid AND will pass on to exec; if low, decode cannot progress: flushing decode empties it though";
    bit blocked        "Asserted if decode is valid AND cannot pass on to exec; if low, decode can take from fetch (unless flushing fetch)";

    bit cannot_complete"Asserted if the decode has a valid instruction that either cannot be started or cannot complete";
} t_riscv_pipeline_control_decode;

/*t t_riscv_pipeline_control_exec - late in clock cycle to affect clocking
 */
typedef struct {
    bit completing_cycle  "Asserted if exec is valid AND will complete a cycle; if low, exec cannot progress: flushing exec empties it though";
    bit completing        "Asserted if exec is valid AND will complete its last cycle AND hence passes it on to mem";
    bit blocked_start     "Asserted if exec is valid and blocked from starting; can be because of exec or coprocessor are blocked from starting";
    bit blocked           "Asserted if exec is valid AND cannot pass on to mem; if low, exec can take from decode (unless flushing decode)";

//    bit ret "Asserted for RET instructions - presumably needs an indication as to which mode to return to";
    bit mispredicted_branch         "Used internally inside control_flow - should remove? Asserted if the exec has a mispredicted branch - could be a JALR, or conditional branch that was not predicted to be taken";
    t_riscv_word pc_if_mispredicted "Target for a mispredicted branch - used in the state";
} t_riscv_pipeline_control_exec;

/*t t_riscv_pipeline_control_exec - late in clock cycle to affect clocking
 */
typedef struct {
    bit blocked           "Asserted if mem stage is valid AND is not completing; if low, mem can take from exec (unless flushing exec)";
} t_riscv_pipeline_control_mem;

/*t t_riscv_pipeline_control_flush - late in clock cycle to affect clocking
 */
typedef struct {
    bit fetch;
    bit decode;
    bit exec  "If asserted then exec stage completes without comitting";
    bit mem   "If asserted, mem stage is completing anyway, but does not write any RF";
} t_riscv_pipeline_control_flush;

/*t t_riscv_pipeline_control - late in clock cycle to affect clocking
 */
typedef struct {
    t_riscv_i32_trap trap;
    t_riscv_pipeline_control_flush   flush;
    t_riscv_pipeline_control_decode  decode;
    t_riscv_pipeline_control_exec    exec;
    t_riscv_pipeline_control_mem     mem;
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
    bit first_cycle     "Asserted if first clock cycles of exec stage; not changed if pipeline control indicates a cycle cannot complete";
    bit last_cycle      "Asserted if no more clock cycles after this (if not blocked) are required to complete the exec stage";
    bit interrupt_block "In standard pipelines this must be low; it blocks interrupts";
    t_riscv_i32_inst instruction;
    t_riscv_i32_decode idecode "Decode of instruction (if valid)";
    t_riscv_word rs1;
    t_riscv_word rs2;
    bit[32]  pc              "Actual PC of execution instruction";
    bit          predicted_branch   "From pipeline_fetch_data associated with the decode of this instruction";
    t_riscv_word pc_if_mispredicted "From pipeline_fetch_data associated with the decode of this instruction";
    bit branch_condition_met;
    t_riscv_mem_access_req dmem_access_req;
    t_riscv_csr_access     csr_access;
} t_riscv_pipeline_response_exec;

/*t t_riscv_pipeline_response_mem
 */
typedef struct {
    bit valid;
    bit access_in_progress;
    bit[32]  pc              "Actual PC of memory instruction";
    bit[32]  addr            "Address being accessed";
} t_riscv_pipeline_response_mem;

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
    t_riscv_pipeline_response_mem    mem;
    t_riscv_pipeline_response_rfw    rfw;
    bit                              pipeline_empty;
} t_riscv_pipeline_response;

/*t t_riscv_pipeline_trap_request
  From the trap interposer
 */
typedef struct {
    bit valid_from_mem;
    bit valid_from_int;
    bit valid_from_exec;
    bit flushes_exec     "Asserted if the exec stage gets flushed (e.g. for interrupts, illegal instruction, mem abort";
    t_riscv_mode to_mode "If interrupt then this is the mode that whose pp/pie/epc should be set from current mode's";
    t_riscv_trap_cause cause;
    bit[32] pc;
    bit[32] value;
    bit ret;
    bit ebreak_to_dbg "Asserted if the trap is a breakpoint and pipeline_control.ebreak_to_dbg was set";
} t_riscv_pipeline_trap_request;

/*t t_riscv_pipeline_fetch_req
 */
typedef struct {
    bit      debug_fetch            "Asserted if fetch of a debug location (data0 or ebreak)";
    bit     predicted_branch   "Only used if branch prediction is supported - so not for single cycle pipeline; for internal use really";
    bit[32] pc_if_mispredicted "Only used if branch prediction is supported - so not for single cycle pipeline for internal use really";
} t_riscv_pipeline_fetch_req;

/*t t_riscv_pipeline_fetch_data
 */
typedef struct {
    bit          valid;
    t_riscv_mode mode "Mode the pipeline is executing in";
    t_riscv_word pc;
    t_riscv_i32_inst instruction;
    bit          dec_predicted_branch   "Not part of fetch - indicates that pipeline_control predicted a branch for the decode, so when the decode is executed this should match the execution - if not, a mispredict occurs";
    t_riscv_word dec_pc_if_mispredicted;
} t_riscv_pipeline_fetch_data;

