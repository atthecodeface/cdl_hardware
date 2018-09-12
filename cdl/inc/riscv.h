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

/*t t_riscv_mem_access_resp
 *
 * Note that the response in some circumstances is defined to be valid in the same cycle as the request.
 * In other circumstances it is defined to be valid in the cycle following a request.
 *
 * The signals do not change.
 *
 * For example, a very simple fetch/execute RISC-V implementation
 * requires the read response in the same cycle as a data memory
 * request, since execute (which includes the full memory access) is a
 * single cycle.
 *
 * However, a deeper pipeline RISC-V implementation such as pipeline3
 * issues a request in the ALU cycle and provides a whole cycle for an
 * SRAM access to satisfy any data memory read. Here, then, the
 * response is valid one cycle after the request.
 *
 * Note that the wait signal is valid with the data; but it also
 * applies to a memory cycle that is a write; that is, a write memory
 * cycle cannot complete if wait is asserted. The next request is
 * already being presented when the wait is given in response to the
 * previous request, though.
 *
 */
typedef struct {
    bit                  wait       "Valid in the same cycle as read_data";
    bit[32]              read_data  "Data returned from reading the requested address";
} t_riscv_mem_access_resp;

/*t t_riscv_word
 */
typedef bit[32] t_riscv_word;

/*t t_riscv_irqs
 */
typedef struct {
    bit nmi;
    bit meip;
    bit seip;
    bit ueip;
    bit mtip;
    bit msip;
} t_riscv_irqs;

/*t t_riscv_mode
 */
typedef enum[3] {
    rv_mode_user       = 3b000, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_supervisor = 3b001, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_machine    = 3b011, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_debug      = 3b111, // all 1s so that it is a superset of machine mode
} t_riscv_mode;

/*t t_riscv_fetch_req
 */
typedef struct {
    bit      valid;
    bit[32]  address;
    bit      sequential;
    t_riscv_mode mode;
    bit          flush;
    // will_take?
} t_riscv_fetch_req;

/*t t_riscv_fetch_resp
 */
typedef bit[2] t_riscv_fetch_tag;
typedef struct {
    bit      valid;
    bit      debug  "Needs to permit register read/write encoding, break after execution, break before execution, execution mode, breakpoint-in-hardware-not-software; force-debug-subroutine-trap-before-execution";
    bit[32]  data;
    t_riscv_mode mode;
    bit          error;
    t_riscv_fetch_tag tag;
} t_riscv_fetch_resp;

/*t t_riscv_config
 */
typedef struct {
    bit      i32c;
    bit      e32;
    bit      i32m;
    bit      i32m_fuse;
    bit      coproc_disable;
    bit      unaligned_mem; // if clear, trap on unaligned memory loads/stores
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

