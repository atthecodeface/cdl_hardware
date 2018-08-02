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
include "riscv.h"

/*a Constants
 */

/*v RISC-V 32-bit instruction decoding - see fig 2.3 RISC-V specification v2.1
 *
 * Constants for the RISC-V 32-bit instruction decoding
 */
constant integer riscv_i32_ones = 0  "Two bits of 1 for 32-bit encoded instructions";
constant integer riscv_i32_opc  = 2  "Five bit field of opcode, for all types";
constant integer riscv_i32_rd   = 7  "Five bit field of destination register for r/i/u/uj, imm for s/sb type";
constant integer riscv_i32_f3   = 12 "Three bit function field for r/i/s/sb, imm for u/uj type";
constant integer riscv_i32_rs1  = 15 "Five bit source register 1 field for r/i/s/sb, imm for u/uj type";
constant integer riscv_i32_rs2  = 20 "Five bit source register 2 field for r/s/sb, imm for i/u/uj type";
constant integer riscv_i32_f7   = 25 "Seven bit function field for r, imm for i/s/sb/u/uj type";
constant integer riscv_i32_f12  = 20 "Twelve bit function/immediage field for i type";

/*a RISC-V ABI register names */
typedef enum[5] {
    riscv_abi_zero = 0,
    riscv_abi_link = 1,
    riscv_abi_sp   = 2
} t_riscv_abi;

/*a RISC-V instruction decode types */
/*t t_riscv_opc (I32) enumeration
 */
typedef enum[5] {
    riscv_opc_load     =  0, // rv32i (lb, lh, lw, lbu, lhu); rv64i (lwu, ld)
    riscv_opc_load_fp  =  1, // rv32f (flw)
    riscv_opc_custom_0 =  2,
    riscv_opc_misc_mem =  3, // rv32i (fence, fence.i)
    riscv_opc_op_imm   =  4, // rv32i (addi, slti, sltiu, xori, ori, andi); rv64i (slli, srli, srai)
    riscv_opc_auipc    =  5, // rv32i (auipc)
    riscv_opc_op_imm32 =  6, // rv64i (addiw, slliw, srliw, sraiw)
    riscv_opc_store    =  8, // rv32i (sb, sh, sw); rv64i (sd)
    riscv_opc_store_fp =  9, // rv32f (fsw)
    riscv_opc_custom_1 = 10,
    riscv_opc_amo      = 11, // rv32a (lr.w, sc.w, amoswap.w, amoadd.w, amoxor.w, amoand.w, amoor.w, amomin.w, amomax.w, amomaxu.w) (+rv64a)
    riscv_opc_op       = 12, // rv32i (add, sub, sll, slt, sltu, xor, srl, sra, or, and); rv32m (mul, mulh, mulhsu, mulhu, div, divu, rem, remu)
    riscv_opc_lui      = 13, // rv32i
    riscv_opc_op32     = 14, // rv64i (addw, subw, sllw, srlw, sraw)
    riscv_opc_madd     = 16, // rv32f (fmadd.s)
    riscv_opc_msub     = 17, // rv32f (fmsub.s)
    riscv_opc_nmsub    = 18, // rv32f (fnmsub.s)
    riscv_opc_nmadd    = 19, // rv32f (fnmadd.s)
    riscv_opc_op_fp    = 20, // rv32f (fadd.s, fsub.s, fmul.s, fdiv.s, fsqrt.s, fsgnj.s, fsgnjn.s, fsgnjx.s, fmin.s, ... fmv.s.x)
    riscv_opc_resvd_0  = 21,
    riscv_opc_custom_2 = 22,
    riscv_opc_branch   = 24, // rv32i (beq, bne, blt, bge, bltu, bgeu)
    riscv_opc_jalr     = 25, // rv32i (jalr)
    riscv_opc_resvd_1  = 26,
    riscv_opc_jal      = 27, // rv32i (jal)
    riscv_opc_system   = 28, // rv32i (ecall, ebreak, csrrw, csrrs, csrrc, csrrwi, csrrsi, csrrci)
    riscv_opc_resvd_2  = 29,
    riscv_opc_custom_3 = 30
} t_riscv_opc_rv32;

/*t t_riscv_opcc (I32C) enumeration
 */
typedef enum[3] {
    riscv_opcc0_addi4spn =  0,
    riscv_opcc0_lw       =  2,
    riscv_opcc0_sw       =  6,
    riscv_opcc1_addi     =  0,
    riscv_opcc1_jal      =  1,
    riscv_opcc1_li       =  2,
    riscv_opcc1_lui      =  3,
    riscv_opcc1_arith    =  4,
    riscv_opcc1_j        =  5,
    riscv_opcc1_beqz     =  6,
    riscv_opcc1_bnez     =  7,
    riscv_opcc2_slli     =  0,
    riscv_opcc2_lwsp     =  2,
    riscv_opcc2_misc_alu =  4,
    riscv_opcc2_swsp     =  6,

} t_riscv_opc_rv32c;

/*t t_riscv_f12- see RISC-V spec 2.1 table 9.2
 */
typedef enum[12] {
    riscv_f12_ecall   = 12h0, // originally scall
    riscv_f12_ebreak  = 12h1, // originally sbreak

    riscv_f12_mret  = 12h302, // from RISC-V privileged spec
    riscv_f12_mwfi  = 12h105, // from RISC-V privileged spec

} t_riscv_system_f12;

/*t t_riscv_f3_alu
 */
typedef enum[3] {
    riscv_f3_addsub = 0, // sub has f7[5] set, add has it clear
    riscv_f3_sll    = 1,
    riscv_f3_slt    = 2,
    riscv_f3_sltu   = 3,
    riscv_f3_xor    = 4,
    riscv_f3_srlsra = 5, // sra has f7[5] set, srl has it clear
    riscv_f3_or     = 6,
    riscv_f3_and    = 7,
} t_riscv_f3_alu;

/*t t_riscv_f3_muldiv
 */
typedef enum[3] {
    riscv_f3_mul    = 0,
    riscv_f3_mulh   = 1,
    riscv_f3_mulhsu = 2,
    riscv_f3_mulhu  = 3,
    riscv_f3_div    = 4,
    riscv_f3_divu   = 5,
    riscv_f3_rem    = 6,
    riscv_f3_remu   = 7
} t_riscv_f3_muldiv;

/*t t_riscv_f3_branch
 */
typedef enum[3] {
    riscv_f3_beq  = 0,
    riscv_f3_bne  = 1,
    riscv_f3_blt  = 4,
    riscv_f3_bge  = 5,
    riscv_f3_bltu = 6,
    riscv_f3_bgeu = 7
} t_riscv_f3_branch;

/*t t_riscv_f3_load
 */
typedef enum[3] {
    riscv_f3_lb  = 0,
    riscv_f3_lh  = 1,
    riscv_f3_lw  = 2,
    riscv_f3_lbu = 4,
    riscv_f3_lhu = 5,
} t_riscv_f3_load;

/*t t_riscv_f3_store
 */
typedef enum[3] {
    riscv_f3_sb  = 0,
    riscv_f3_sh  = 1,
    riscv_f3_sw  = 2,
} t_riscv_f3_store;

/*t t_riscv_f3_misc_mem
 */
typedef enum[3] {
    riscv_f3_fence   = 0,
    riscv_f3_fence_i = 1,
} t_riscv_f3_misc_mem;

/*t t_riscv_f3_system
 */
typedef enum[3] {
    riscv_f3_privileged = 0,
    riscv_f3_csrrw = 1,
    riscv_f3_csrrs = 2,
    riscv_f3_csrrc = 3,
    riscv_f3_csrrwi = 5,
    riscv_f3_csrrsi = 6,
    riscv_f3_csrrci = 7,
} t_riscv_f3_system;

/*t t_riscv_mem_width */
typedef enum[2] {
    mw_byte,
    mw_half,
    mw_word
} t_riscv_mem_width;

/*t t_riscv_op - RISC-V decoded instruction operation class */
typedef enum[4] {
    riscv_op_branch,
    riscv_op_jal,
    riscv_op_jalr,
    riscv_op_system,
    riscv_op_csr,
    riscv_op_misc_mem,
    riscv_op_load,
    riscv_op_store,
    riscv_op_alu,
    riscv_op_muldiv,
    riscv_op_auipc,
    riscv_op_lui,
    riscv_op_illegal
} t_riscv_op;

/*t t_riscv_subop - RISC-V decoded instruciton operation class */
typedef enum[4] {
    riscv_subop_valid=0, // for op==illegal, really - means op==invalid is sufficient for illegal op
    riscv_subop_illegal = 0xf, // for many of the ops...

    riscv_subop_beq=0, // same as rvi_branch_f3
    riscv_subop_bne=1, 
    riscv_subop_blt=2, 
    riscv_subop_bge=3, 
    riscv_subop_bltu=4, 
    riscv_subop_bgeu=5, 

    riscv_subop_add    = 0, // same as riscv_op_f3, with bit[3] as the 'extra' ops
    riscv_subop_sub    = 0+8,
    riscv_subop_sll    = 1,
    riscv_subop_slt    = 2,
    riscv_subop_sltu   = 3,
    riscv_subop_xor    = 4,
    riscv_subop_srl    = 5,
    riscv_subop_sra    = 5+8,
    riscv_subop_or     = 6,
    riscv_subop_and    = 7,

    riscv_subop_mull     = 0, // same as riscv_op_f3
    riscv_subop_mulhss   = 1,
    riscv_subop_mulhsu   = 2,
    riscv_subop_mulhu    = 3,
    riscv_subop_divs     = 4,
    riscv_subop_divu     = 5,
    riscv_subop_rems     = 6,
    riscv_subop_remu     = 7,

    riscv_subop_lb  = 0, // same as rvi_f3_load
    riscv_subop_lh  = 1,
    riscv_subop_lw  = 2,
    riscv_subop_lbu = 4,
    riscv_subop_lhu = 5,

    riscv_subop_sb  = 0, // same as rvi_f3_store
    riscv_subop_sh  = 1,
    riscv_subop_sw  = 2,

    riscv_subop_ecall  = 0,
    riscv_subop_ebreak = 1,
    riscv_subop_mret   = 2,
    riscv_subop_mwfi   = 3,

    riscv_subop_fence   = 0, // to match riscv_op_f3
    riscv_subop_fence_i = 1,

    riscv_subop_csrrw   = 1, // to match riscv_op_f3
    riscv_subop_csrrs   = 2,
    riscv_subop_csrrc   = 3,
} t_riscv_subop;

/*t t_riscv_mcause
 * Non-interrupt MCAUSE reasons, from the spec
 */
typedef enum[8] {
    riscv_mcause_instruction_misaligned = 0,
    riscv_mcause_instruction_fault      = 1,
    riscv_mcause_illegal_instruction    = 2,
    riscv_mcause_breakpoint             = 3,
    riscv_mcause_load_misaligned        = 4,
    riscv_mcause_load_fault             = 5,
    riscv_mcause_store_misaligned       = 6,
    riscv_mcause_store_fault            = 7,
    riscv_mcause_uecall                 = 8,
    riscv_mcause_secall                 = 9,
    riscv_mcause_hecall                 = 10,
    riscv_mcause_mecall                 = 11,
} t_riscv_mcause;

/*t t_riscv_trap_cause
 */
typedef enum[4] {
    riscv_trap_cause_instruction_misaligned = 0,
    riscv_trap_cause_instruction_fault      = 1,
    riscv_trap_cause_illegal_instruction    = 2,
    riscv_trap_cause_breakpoint             = 3,
    riscv_trap_cause_load_misaligned        = 4,
    riscv_trap_cause_load_fault             = 5,
    riscv_trap_cause_store_misaligned       = 6,
    riscv_trap_cause_store_fault            = 7,
    riscv_trap_cause_uecall                 = 8,
    riscv_trap_cause_secall                 = 9,
    riscv_trap_cause_hecall                 = 10,
    riscv_trap_cause_mecall                 = 11,
} t_riscv_trap_cause;

/*a CSR types */
/*t t_riscv_csr_access_type
 */
typedef enum[3] {
    riscv_csr_access_none = 0,
    riscv_csr_access_write = 1,
    riscv_csr_access_read  = 2,
    riscv_csr_access_rw    = 3,
    riscv_csr_access_rs    = 6,
    riscv_csr_access_rc   =  7,
} t_riscv_csr_access_type;

/*t t_riscv_csr_access
 */
typedef struct {
    t_riscv_csr_access_type access;
    bit[12]                 address;
} t_riscv_csr_access;

/*t t_riscv_csr_data
 */
typedef struct {
    t_riscv_word            read_data;
    bit                     illegal_access;
} t_riscv_csr_data;

/*t t_riscv_csr_controls
 */
typedef struct {
    bit retire;
    bit timer_inc;
    bit timer_clear;
    bit timer_load;
    bit[64] timer_value;
    bit trap;
    t_riscv_trap_cause trap_cause;
    bit[32] trap_pc;
    bit[32] trap_value;
} t_riscv_csr_controls;

/*t t_riscv_csr_addr
 *
 * RISC-V CSR addresses; the top bit indicates readable, next
 * writable; next two are the minimum privilege level to access
 * (00=user, 11=machine)
 *
 * From RISCV privileged spec v1.1
 */
typedef enum[12] {
    CSR_ADDR_READWRITE_MASK  = 12hc00,
    CSR_ADDR_READ_WRITE_A    = 12h000,
    CSR_ADDR_READ_WRITE_B    = 12h400,
    CSR_ADDR_READ_WRITE_C    = 12h800,
    CSR_ADDR_READ_ONLY       = 12hC00,

    CSR_ADDR_MODE_MASK       = 12h300,
    CSR_ADDR_USER_MODE       = 12h000,
    CSR_ADDR_SUPERVISOR_MODE = 12h100,
    CSR_ADDR_HYPERVISOR_MODE = 12h200,
    CSR_ADDR_MACHINE_MODE    = 12h300,

    // Read-write registers accessible from user mode (if provided)
    CSR_ADDR_USTATUS   = 12h000  "User status register, optional",
    // 1, 2, 3 are floating point (fflags, frm, fcsr)
    CSR_ADDR_UIE       = 12h004  "User interrupt enable register, optional",
    CSR_ADDR_UTVEC     = 12h005  "User trap handler base register, optional",

    CSR_ADDR_USCRATCH  = 12h040  "Scratch register for user trap handlers, only if user mode provided",
    CSR_ADDR_UEPC      = 12h041  "User exception program counter, only if user mode provided",
    CSR_ADDR_UCAUSE    = 12h042  "User trap cause register, only if user mode provided",
    CSR_ADDR_UTVAL     = 12h043  "User trap value register, only if user mode provided",
    CSR_ADDR_UIP       = 12h044  "User interrupt pending register, only if user mode interrupts provided",

    // Read-only registers accessible from user mode
    CSR_ADDR_CYCLE     = 12hC00  "Required register for RV32I, low 32-bits of cycle counter",
    CSR_ADDR_TIME      = 12hC01  "Required register for RV32I, low 32-bits of wall-clock timer",
    CSR_ADDR_INSTRET   = 12hC02  "Required register for RV32I, low 32-bits of instructions retired counter",
    // c03 to c1f are more high performance counters if required
    CSR_ADDR_CYCLEH    = 12hC80  "Required register for RV32I, high 32-bits of cycle counter - may be implemented in software with a trap",
    CSR_ADDR_TIMEH     = 12hC81  "Required register for RV32I, high 32-bits of wall-clock timer - may be implemented in software with a trap",
    CSR_ADDR_INSTRETH  = 12hC82  "Required register for RV32I, high 32-bits of instructions retired counter - may be implemented in software with a trap",
    // c83 to c9f are more high performance counters high 32 bits if required

    // Read-write registers accessible from system mode (if provided)
    CSR_ADDR_SSTATUS   = 12h100  "Supervisor status register, optional",
    CSR_ADDR_SEDELEG   = 12h102  "Supervisor exception delegation register, optional",
    CSR_ADDR_SIDELEG   = 12h103  "Supervisor interrupt delegation register, optional",
    CSR_ADDR_SIE       = 12h104  "Supervisor interrupt enable register, optional",
    CSR_ADDR_STVEC     = 12h105  "Supervisor trap handler base register, optional",
    CSR_ADDR_SCOUNTEREN = 12h106  "Supervisor counter enable, optional",
    CSR_ADDR_SSCRATCH  = 12h140  "Scratch register for supervisor trap handlers",
    CSR_ADDR_SEPC      = 12h141  "Supervisor exception program counter, optional",
    CSR_ADDR_SCAUSE    = 12h142  "Supervisor trap cause register, optional",
    CSR_ADDR_SBADADDR  = 12h143  "Supervisor trap value register, optional",
    CSR_ADDR_SIP       = 12h144  "Supervisor interrupt pending register, optional",
    CSR_ADDR_SPTBR     = 12h180  "Supervisor page-table base register, optional",

    // Read-write registers accessible from machine mode (if provided)
    CSR_ADDR_MSTATUS   = 12h300  "Machine status register, required",
    CSR_ADDR_MISA      = 12h301  "ISA and extensions, required - but may be hardwire to zero",
    CSR_ADDR_MEDELEG   = 12h302  "Machine exception delegation register, optional - tests require this to not be illegal",
    CSR_ADDR_MIDELEG   = 12h303  "Machine interrupt delegation register, optional - tests require this to not be illegal",
    CSR_ADDR_MIE       = 12h304  "Machine interrupt enable register, optional - tests require this to not be illegal",
    CSR_ADDR_MTVEC     = 12h305  "Machine trap handler base register, optional - tests require this to not be illegal",
    CSR_ADDR_MCOUNTEREN = 12h306  "Machine counter enable, optional",
    CSR_ADDR_MSCRATCH  = 12h340  "Scratch register for machine trap handlers",
    CSR_ADDR_MEPC      = 12h341  "Machine exception program counter",
    CSR_ADDR_MCAUSE    = 12h342  "Machine trap cause register",
    CSR_ADDR_MTVAL     = 12h343  "Machine trap value register",
    CSR_ADDR_MIP       = 12h344  "Machine interrupt pending register, optional",

    // Machine-mode only read-write registers that shadow other registers (read-only elsewhere)
    // Clarvi maps the following to Fxx, rather than the specs Bxx - hence the spec has them read/write
    CSR_ADDR_MCYCLE    = 12hB00  "Required register for RV32I, low 32-bits of cycle counter",
    CSR_ADDR_MINSTRET  = 12hB02  "Required register for RV32I, low 32-bits of instructions retired counter",
    CSR_ADDR_MCYCLEH   = 12hB80  "Required register for RV32I, high 32-bits of cycle counter - may be implemented in software with a trap",
    CSR_ADDR_MINSTRETH = 12hB82  "Required register for RV32I, high 32-bits of instructions retired counter - may be implemented in software with a trap",

    // Read-only registers, accesible from machine mode only
    CSR_ADDR_MVENDORID = 12hF11  "Vendor ID, required - but may be hardwired to zero for not implemented or non-commercial",
    CSR_ADDR_MARCHID   = 12hF12  "Architecture ID, required - but may be hardwired to zero for not implemented",
    CSR_ADDR_MIMPID    = 12hF13  "Implementation ID, required - but may be hardwired to zero for not implemented",
    CSR_ADDR_MHARTID   = 12hF14  "Hardware thread ID, required - but may be hardwired to zero (if only one thread in system)",

    // CLARVI does not memory-map mtime and mtime_cmp, but the spec says it should - these are clarvi-specific, then
    // Rumor has it that MTIME has now been removed entirely; the spec does not say so. This is a sadness of open source hardware - architecture by github...
    //CSR_ADDR_MTIME     = 12hF01,
    //CSR_ADDR_MTIMEH    = 12hF81,
    //CSR_ADDR_MTIMECMP  = 12h7C1,
    //CSR_ADDR_MTIMECMPH = 12h7C2,

    // provisional debug, used across these RISC-V implementations
    CSR_ADDR_DSCRATCH  = 12h7B2
} t_riscv_csr_addr;

/*t t_riscv_csrs_minimal
 *
 * Minimal set of RISC-V CSRs
 */
typedef struct {
    bit[64] cycles    "Number of cycles since reset";
    bit[64] instret   "Number of instructions retired";
    bit[64] time      "Global time concept, synchronized through the timer control interface";
    bit[32] mscratch  "Scratch register for exception routines";
    bit[32] mepc      "PC at last exception";
    bit[32] mcause    "Cause of last exception";
    bit[32] mtval     "Value associated with last exception";
    bit[32] mtvec     "Trap vector, can be hardwired or writable";
} t_riscv_csrs_minimal;

/*a I32 types */
/*t t_riscv_i32_decode
 * Decoded i32 instruction, used throughout a pipeline (decode onwards)
 */
typedef struct {
    bit[5]       rs1                   "Source register 1 that is required by the instruction";
    bit          rs1_valid             "Asserted if rs1 is valid; if deasserted then rs1 is not used";
    bit[5]       rs2                   "Source register 2 that is required by the instruction";
    bit          rs2_valid             "Asserted if rs2 is valid; if deasserted then rs2 is not used";
    bit[5]       rd                    "Destination register that is written by the instruction";
    bit          rd_written            "Asserted if Rd is written to (hence also Rd will be non-zero)";
    t_riscv_csr_access     csr_access  "CSR access if valid and legal";
    bit[32]      immediate             "Immediate value decoded from the instruction";
    bit[5]       immediate_shift       "Immediate shift value decoded from the instruction";
    bit          immediate_valid       "Asserted if immediate data is valid (generally used instead of source register 2)";
    t_riscv_op     op                  "Operation class of the instruction";
    t_riscv_subop  subop               "Subclass of the operation class";
    bit          requires_machine_mode "Indicates that in non-machine-mode the instruction is illlegal";
    bit          memory_read_unsigned  "if a memory read (op is riscv_opc_load), this indicates an unsigned read; otherwise ignored";
    t_riscv_mem_width  memory_width    "ignored unless @a memory_read or @a memory_write; indicates size of memory transfer";
    bit           illegal              "asserted if an illegal opcode";
    bit           is_compressed        "asserted if from an i32-c decode, clear otherwise (effects link register)";
} t_riscv_i32_decode;

/*t t_riscv_i32_alu_result
 *
 * Result of i32 ALU operation
 */
typedef struct {
    t_riscv_word result       "Result of ALU operation, dependent on subop";
    t_riscv_word arith_result "Use for mem_address";
    bit          branch_condition_met;
    t_riscv_word branch_target;
    t_riscv_csr_access csr_access;
} t_riscv_i32_alu_result;


/*t t_riscv_i32_coproc_controls
 */
typedef struct {
    bit                     dec_idecode_valid "Mid-cycle: validates dec_idecode";
    t_riscv_i32_decode      dec_idecode "Mid-cycle: Idecode for the next cycle";
    bit                     dec_to_alu_blocked "Late in the cycle: if set, ALU will not take decode; note that ALU flush overpowers this";
    t_riscv_word            alu_rs1     "Early in cycle (after some muxes)";
    t_riscv_word            alu_rs2     "Early in cycle (after some muxes)";
    bit                     alu_flush_pipeline "Late in cycle: If asserted, flush everything prior to alu; will only be asserted during a cycle if first cycle if ALU instruction - or if alu_cannot_start";
    bit                     alu_cannot_start "Late in cycle: If asserted, alu_idecode may be valid but rs1/rs2 are not; once deasserted it remains deasserted until a new ALU instruction starts";
    bit                     alu_cannot_complete "Late in cycle: If asserted, alu cannot complete because it is still working on its operation";
} t_riscv_i32_coproc_controls;

/*t t_riscv_i32_coproc_response
 */
typedef struct {
    bit          cannot_start "If asserted, block start of the ALU stage - the instruction is then tried again in the next cycle, but can be interrupted";
    t_riscv_word result;
    bit          cannot_complete "Early in cycle: if deasserted the module is performing a calculation that has not produced a valid result yet (feeds back in to controls alu_cannot_complete)";
} t_riscv_i32_coproc_response;

