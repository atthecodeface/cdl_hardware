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

/*a Constants
 *
 * Constants for the RISC-V implementation; can be overridden in CDL
 * builds with a dc: option in the model_list
 */
constant integer RISCV_DATA_ADDR_WIDTH = 14;
constant integer RISCV_INSTR_ADDR_WIDTH = 14;

/*a Basic types
 */
/*t t_riscv_mode
 */
typedef enum[3] {
    rv_mode_user       = 3b000, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_supervisor = 3b001, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_machine    = 3b011, // matches the encoding in table 1.1 of v1.10 privilege spec
    rv_mode_debug      = 3b111, // all 1s so that it is a superset of machine mode
} t_riscv_mode;

/*t t_riscv_mem_access_req_type
 *
 * For an implementation that does not support atomics only 2 bits are used
 *
 */
typedef enum[5] {
    rv_mem_access_idle        = 5b00000,
    rv_mem_access_read        = 5b00001,
    rv_mem_access_write       = 5b00010,
    rv_mem_access_atomic_lr   = 5b10000,
    rv_mem_access_atomic_sc   = 5b10001,
    rv_mem_access_atomic_swap = 5b10010,
    rv_mem_access_atomic_and  = 5b10100,
    rv_mem_access_atomic_or   = 5b10101,
    rv_mem_access_atomic_xor  = 5b10110,
    rv_mem_access_atomic_add  = 5b11000,
    rv_mem_access_atomic_umin = 5b11100,
    rv_mem_access_atomic_smin = 5b11101,
    rv_mem_access_atomic_umax = 5b11110,
    rv_mem_access_atomic_smax = 5b11111,
    rv_mem_access_nonatomic_mask = 5b00011
} t_riscv_mem_access_req_type;

/*t t_riscv_mem_access_req
 *
 * add atomic_aq and atomic_rl bits for atomics
 * atomic_aq means that all memory requests *after* this atomic must only be observable after the atomic is observable
 * atomic_rl means that all memory requests *prior* to this atomic must be observable before the atomic is observable
 *
 */
typedef struct {
    bit valid              "Asserted if a valid access request";
    t_riscv_mode mode      "Mode of the access - usually the same as the pipeline execution, but not necessarily";
    t_riscv_mem_access_req_type req_type "Type of request";
    bit[32]  address       "Address of transaction - aligned to a word for atomics";
    bit      sequential    "Asserted if the transaction is guaranteed to be to the next word after the last access - this is a hint only";
    bit[4]   byte_enable   "Byte enables for writes, should be ignored by atomics";
    bit[32]  write_data    "Data for writing, or to be used in the atomic";
} t_riscv_mem_access_req;

/*t t_riscv_mem_access_resp
 *
 * This structure contains the response to a memory request, and memory return data
 *
 * Each request must be acknowledged
 * In the cycle following an acknowledged request an abort may be raised, which will force a data trap
 *
 * Responses can include an error indication?
 * Responses for atomics are the original read data, or the result of an 'store conditional'
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
    bit                  ack_if_seq        "Asserted if a sequential access request (if valid) would be taken";
    bit                  ack               "Asserted if an access request (if valid) would be taken; if this is asserted, ack_if_seq should be asserted too";
    bit                  abort_req         "If asserted (in the cycle after an acked request) then the data transaction must abort. Can be configured to work until access_complete, in conjunction with may_still_abort";
    bit                  may_still_abort   "If asserted (starting in the cycle after an acked request) then the data transaction may yet assert abort_req in a subsequent cycle (this blocks the starting of the exec stage of the following instruction). If pipeline is configured to not support late aborts then this signal is ignored.";
    bit                  access_complete   "Valid in the same cycle as read_data; must be set on writes as well as reads, as it completes an access";
    bit[32]              read_data         "Data returned from reading the requested address";
} t_riscv_mem_access_resp;

/*t t_riscv_word
 */
typedef bit[32] t_riscv_word;

/*t t_riscv_irqs
 *
 * Note that USIP and SSIP are local to the RISC-V hart
 *
 * Note that meip, seip and ueip are effectively three separate interrupt pins to the RISC-V
 *
 */
typedef struct {
    bit nmi;
    bit meip          "External interrupt pending 'for machine mode'";
    bit seip          "External interrupt pending 'for supervisor mode' - actually, it goes to machine mode";
    bit ueip          "External interrupt pending 'for user mode' - actually, it goes to machine mode";
    bit mtip          "Timer interrupt, set by memory-mapped timer";
    bit msip          "Read-write in a memory-mapped register";
    bit[64] time      "Global time concept; may be tied low if user time CSR is not required";
} t_riscv_irqs;

/*t t_riscv_fetch_req_type
 *
 *
 *
 */
typedef enum[3] {
    rv_fetch_none           = 3b000, // address is invalid - next non-none request MUST be nonsequential
    rv_fetch_nonsequential  = 3b001, // address is anything, and will be valid late in the cycle
    rv_fetch_sequential_32  = 3b010, // address=+4 from last cycle
    rv_fetch_repeat         = 3b011, // address will be same as last cycle
    rv_fetch_sequential_16  = 3b110, // address=+2 from last cycle
} t_riscv_fetch_req_type;

/*t t_riscv_fetch_req
 *
 * Fetch request comes from the start of pipeline control and
 * is delivered to the pipeline fetch data through any prefetch
 * mechanism.
 * The fetch request type indicates what data is needed next in
 * conjunction with the address
 *
 */
typedef struct {
    bit      flush_pipeline         "Asserted if prefetch should flush any pipeline";
    t_riscv_fetch_req_type req_type "Request type - none, nonseq, seq, repeat; if flush only none, nonseq";
    bit[32]  address;
    t_riscv_mode mode;
} t_riscv_fetch_req;

/*t t_riscv_fetch_resp
 */
typedef struct {
    bit      valid;
    bit[32]  data;
    bit[2]   error "One bit per 16-bits of the data";
} t_riscv_fetch_resp;

/*t t_riscv_config
 */
typedef struct {
    bit      i32c;
    bit      e32;
    bit      i32m;
    bit      i32m_fuse;
    bit      debug_enable;
    bit      coproc_disable;
    bit      unaligned_mem;   // if clear, trap on unaligned memory loads/stores
    bit      mem_abort_late;  // if clear memory aborts must occur in the first cycle
} t_riscv_config;

/*t t_riscv_debug_op
 */
typedef enum[4] {
    rv_debug_acknowledge "Acknowledge halt, breakpoint hit, status; removes attention signal",
    rv_debug_set_requests   "Set request bits for halt, resume, step (args[0..2])",
    rv_debug_read   "Request read of a GPR/CSR",
    rv_debug_write  "Request write of a GPR/CSR",
    rv_debug_execute "Execute instruction provided resumption of execution at dpc and in mode dcsr.prv",
    rv_debug_execute_progbuf "Execute instruction at 'progbuf' address X (if it is a jump and link it will return)",
} t_riscv_debug_op;

/*t t_riscv_debug_resp
 */
typedef enum[2] {
    rv_debug_resp_acknowledge,
    rv_debug_resp_read_write_complete
} t_riscv_debug_resp;

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
    bit[6] mask             "Mask received by PDM that matches the acknowledge - all PDMs will drive the same value";
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
    // Following are valid at commit stage of pipeline
    bit                instr_valid;
    t_riscv_mode       mode          "Mode of instruction";
    bit[32]            instr_pc      "Program counter of the instruction";
    bit[32]            instruction   "Instruction word being decoded - without debug";
    bit                branch_taken  "Asserted if a branch is being taken";
    bit[32]            branch_target "Target of branch if being taken";
    bit                trap          "Asserted if a trap is taken (including interrupt) - nonseq";
    bit                ret           "Asserted if an [m]ret instruction is taken - nonseq";
    bit                jalr          "Asserted if a jalr instruction is taken - nonseq";
    // Following are valid at rfw stage of pipeline
    bit                rfw_retire "Asserted if an instruction is being retired";
    bit                rfw_data_valid;
    bit[5]             rfw_rd;
    t_riscv_word       rfw_data   "Result of ALU/memory operation for the instruction";
    // Following are anywhere
    bit                bkpt_valid;
    bit[4]             bkpt_reason;
    // Needs tag?
} t_riscv_i32_trace;

/*t t_riscv_packed_trace_control
 */
typedef struct {
    bit enable     "Global enable";
    bit enable_control;
    bit enable_pc;
    bit enable_rfd;
    bit enable_breakpoint;
    bit valid;
} t_riscv_packed_trace_control;

/*t t_riscv_i32_packed_trace
  The packed trace takes an i32 trace
*/
typedef struct {
    bit                seq_valid;
    bit[3]             seq;

    bit                nonseq_valid;
    bit[2]             nonseq;

    bit                bkpt_valid;
    bit[4]             bkpt;

    bit                data_valid;
    bit                data_reason;
    bit[40]            data;

    bit[3]             compressed_data_nybble "Nybble at which data nybbles will start in compressed stream, if required";
    bit[4]             compressed_data_num_bytes "Extra";
} t_riscv_i32_packed_trace;

/*t t_riscv_i32_compressed_trace
  The compressed trace is designed to come out as a sequence of nybbles.

  The nybbles are:

  0000   => skip
  0SSS   => SSS (1 to 7 sequential executions)
  10RR   => RR non-sequential reason (trap, ret, jalr, other branch); PC should come next
  1100 RNNN {DDDD}2N => Reason R 2N nybbles of data DDDD+
    R => PC, rfw + data [future? , data mem address, access, data]
  1101 NNNN  => breakpoint
  111x       => reserved

  The actual trace from the compression currently comes out as four separate fields

  sequential - three bits plus a valid bit

  nonsequential reason - two bits plus a valid bit

  breakpoint reason - four bits plus a valid bit

  eiter address or data - two reason bits, 4 bits of # bytes, and 64 bits of data, plus a valid bit


  A nybble stream should be constructed from:
    a valid 0SSS sequential nybble (if necessary)
    a valid 10RR nonsequential reason (if necessary)
    a valid 1101 NNNN breakpoint reason (if necessary)
    a valid data starting with 1100, then RNNN, then the required number of nybbles

  In a single clock tick one may need 1 seq nybble, 1 nonseq nybble, 2 breakpoint nybbles, and 12 data nybbles
  Total is 16 nybbles or 64 bits (for 40-bit data)

  A decompressor can take a nybble stream and produce a corresponding
  trace - but the timing is lost in this process.
 */
typedef struct {
    bit[5]  valid;
    bit[64] data;
} t_riscv_i32_compressed_trace;

/*t t_riscv_i32_decompressed_trace
  The decompressed trace undoes the trace compression
 */
typedef struct {
    bit                seq_valid;
    bit[3]             seq;
    
    bit                branch_taken "Asserted if a branch is being taken";
    bit                trap          "Asserted if a trap is taken (including interrupt) - nonseq";
    bit                ret           "Asserted if an [m]ret instruction is taken - nonseq";
    bit                jalr          "Asserted if a jalr instruction is taken - nonseq";

    bit                pc_valid;
    bit[32]            pc            "PC if pc_valid";

    bit                rfw_data_valid;
    bit[5]             rfw_rd;
    bit[32]            rfw_data   "Result of ALU/memory operation for the instruction";

    bit                bkpt_valid;
    bit[4]             bkpt_reason;
} t_riscv_i32_decompressed_trace;


