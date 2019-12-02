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
include "cpu/riscv/riscv_config.h"

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
/*t t_riscv_opc (I32) enumeration - from inst[5;2] - see table 19.1 in RISC-V spec v2.2
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

/*t t_riscv_op - RISC-V decoded instruction operation class - no relationship to encodings */
typedef enum[4] {
    riscv_op_branch,
    riscv_op_jal,
    riscv_op_jalr,
    riscv_op_system,
    riscv_op_csr,
    riscv_op_misc_mem,
    riscv_op_mem,
    riscv_op_alu,
    riscv_op_muldiv,
    riscv_op_auipc,
    riscv_op_lui,
    riscv_op_custom_0, // for custom extensions
    riscv_op_custom_1, // for custom extensions
    riscv_op_custom_2, // for custom extensions
    riscv_op_custom_3, // for custom extensions
    riscv_op_illegal
} t_riscv_op;

/*t t_riscv_subop - RISC-V decoded instruciton operation class - mapping of f3 as much as possible */
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
    riscv_subop_sll    = 1,  // => subop shift
    riscv_subop_slt    = 2,
    riscv_subop_sltu   = 3,
    riscv_subop_xor    = 4,
    riscv_subop_srla   = 5,    // => subop shift
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
    riscv_subop_sb  = 8, // same as rvi_f3_store but with bit[3] set
    riscv_subop_sh  = 9,
    riscv_subop_sw  = 10,
    riscv_subop_atomic = 12,
    riscv_subop_ls_store     = 8,
    riscv_subop_ls_unsigned  = 4,
    riscv_subop_ls_size_mask = 3,
    riscv_subop_ls_byte      = 0,
    riscv_subop_ls_half      = 1,
    riscv_subop_ls_word      = 2,

    riscv_subop_ecall  = 0,
    riscv_subop_ebreak = 1,
    riscv_subop_mret   = 2, // possibly need uret and sret - see table 6.1 in priv spec 1.10
    riscv_subop_mwfi   = 3,

    riscv_subop_fence   = 0, // to match riscv_op_f3
    riscv_subop_fence_i = 1,

    riscv_subop_csrrw   = 1, // to match riscv_op_f3
    riscv_subop_csrrs   = 2,
    riscv_subop_csrrc   = 3,
} t_riscv_subop;

/*t t_riscv_shift_op */
typedef enum[4] {
    riscv_shift_op_left_logical_zeros  = 4b0000, // standard
    riscv_shift_op_left_logical_ones   = 4b0001,
    riscv_shift_op_left_rotate         = 4b0011,
    riscv_shift_op_right_logical_zeros = 4b0100, // standard
    riscv_shift_op_right_logical_ones  = 4b0101,
    riscv_shift_op_right_arithmetic    = 4b0110, // standard
    riscv_shift_op_right_rotate        = 4b0111,
    riscv_shift_op_bit_insert          = 4b1000, // inserts must be a 'left'
    riscv_shift_op_byte_insert         = 4b1001, // inserts must be a 'left'
    riscv_shift_op_reverse             = 4b1100, // reverse cannot be a 'left'
    riscv_shift_op_count               = 4b1010,

    riscv_shift_op_mask_right           = 4b0100 // used to determine if shift amount to  be negated
} t_riscv_shift_op;

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
    riscv_mcause_mecall                 = 11,
} t_riscv_mcause;

/*t t_riscv_trap_cause
 */
typedef enum[5] {
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
    riscv_trap_cause_mecall                 = 11,
    riscv_trap_cause_interrupt              = 16,
    riscv_trap_cause_ret_mret               = 0,
    riscv_trap_cause_ret_sret               = 1,
    riscv_trap_cause_ret_uret               = 2,
    riscv_trap_cause_ret_dret               = 3,
} t_riscv_trap_cause;

/*a CSR types */
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

    // provisional debug, used across these RISC-V implementations
    CSR_ADDR_DCSR       = 12h7B0,
    CSR_ADDR_DEPC       = 12h7B1,
    CSR_ADDR_DSCRATCH0  = 12h7B2,
    CSR_ADDR_DSCRATCH1  = 12h7B3
} t_riscv_csr_addr;

/*t t_riscv_csr_select
 *
 * RISC-V CSR addresses; the top bit indicates readable, next
 * writable; next two are the minimum privilege level to access
 * (00=user, 11=machine)
 *
 * From RISCV privileged spec v1.1
 */
typedef enum[12] {
    riscv_csr_select_time_l   = 12h010,
    riscv_csr_select_time_h   = 12h011,
    riscv_csr_select_cycle_l  = 12h012,
    riscv_csr_select_cycle_h  = 12h013,
    riscv_csr_select_instret_l= 12h014,
    riscv_csr_select_instret_h= 12h015,

    riscv_csr_machine_isa     = 12h020,
    riscv_csr_machine_vendorid= 12h021,
    riscv_csr_machine_archid  = 12h022,
    riscv_csr_machine_impid   = 12h023,
    riscv_csr_machine_hartid  = 12h024,

    riscv_csr_user_status     = 12h040,
    riscv_csr_user_scratch    = 12h041,
    riscv_csr_user_ie         = 12h042,
    riscv_csr_user_ip         = 12h043,
    riscv_csr_user_tvec       = 12h044,
    riscv_csr_user_tval       = 12h045,
    riscv_csr_user_epc        = 12h046,
    riscv_csr_user_cause      = 12h047,

    riscv_csr_machine_status  = 12h080,
    riscv_csr_machine_scratch = 12h081,
    riscv_csr_machine_ie      = 12h082,
    riscv_csr_machine_ip      = 12h083,
    riscv_csr_machine_tvec    = 12h084,
    riscv_csr_machine_tval    = 12h085,
    riscv_csr_machine_epc     = 12h086,
    riscv_csr_machine_cause   = 12h087,

    riscv_csr_machine_edeleg  = 12h100,
    riscv_csr_machine_ideleg  = 12h101,

    riscv_csr_debug_pc        = 12h800,
    riscv_csr_debug_csr       = 12h801,
    riscv_csr_debug_scratch0  = 12h802,
    riscv_csr_debug_scratch1  = 12h803
} t_riscv_csr_select;

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
    t_riscv_mode            mode "Used for decode and to determine legality";
    bit                     access_cancelled;
    t_riscv_csr_access_type access;
    t_riscv_csr_access_custom custom;
    bit[12]                 address "For internal use before select generation";
    t_riscv_csr_select      select;
    t_riscv_word            write_data     "Write data for the CSR access, later in the cycle than @csr_access possibly";
} t_riscv_csr_access;

/*t t_riscv_csr_data
 */
typedef struct {
    t_riscv_word    read_data;
    bit             take_interrupt;
    t_riscv_mode    interrupt_mode  "Mode to enter if take_interrupt is asserted";
    bit[4]          interrupt_cause "From table 3.6 in RV priv space 1.10";
} t_riscv_csr_data;

/*t t_riscv_i32_trap */
typedef struct {
    bit valid;
    t_riscv_mode to_mode "If interrupt then this is the mode that whose pp/pie/epc should be set from current mode's";
    t_riscv_trap_cause cause;
    bit[32] pc;
    bit[32] value;
    bit ret;
    bit ebreak_to_dbg "Asserted if the trap is a breakpoint and pipeline_control.ebreak_to_dbg was set";
} t_riscv_i32_trap;

/*t t_riscv_csr_controls
 */
typedef struct {
    t_riscv_mode exec_mode "Mode of instruction in the execution stage";
    bit retire;
    bit[64] timer_value;
    t_riscv_i32_trap trap;
} t_riscv_csr_controls;

/*t t_riscv_csr_decode */
typedef struct {
    bit illegal_access;
    t_riscv_csr_select csr_select;
} t_riscv_csr_decode;

/*t t_riscv_csr_dcsr
 *
 * From Debug spec v?
 *
 */
typedef struct {
    bit[4] xdebug_ver "4 for conformant debug support, 0 otherwise";
    bit    ebreakm    "make ebreak instructions in machine mode enter debug mode";
    bit    ebreaks    "make ebreak instructions in system mode enter debug mode";
    bit    ebreaku    "make ebreak instructions in user mode enter debug mode";
    bit    stepie     "set to enable interrupts during stepping (may be hardwired to 0)";
    bit    stopcount  "set to stop cycle and instret incrementing on instructions executed in debug mode";
    bit    stoptime   "set to disable incrementing of hart-local timers when in debug mode";
    bit[3] cause      "1=ebreak, 2=trigger module, 3=debugger request, 4=single step as step was set";
    bit    mprven     "if clear ignore mstatus.mprv when in debug mode";
    bit    nmip       "asserted if an NMI is pending for the hart";
    bit    step       "when set enter debug mode after current instruction completes";
    bit[2] prv        "mode of execution prior to entry to debug mode, and to return to on dret";
} t_riscv_csr_dcsr;

/*t t_riscv_csr_mstatus
 *
 * From Priv spec v1.10
 *
 */
typedef struct {
    bit sd;
    bit tsr;
    bit tw;
    bit tvm;
    bit mxr;
    bit sum;
    bit mprv;
    bit[2] xs;
    bit[2] fs;
    bit[2] mpp;
    bit spp;
    bit mpie;
    bit spie;
    bit upie;
    bit mie;
    bit sie;
    bit uie;
} t_riscv_csr_mstatus;

/*t t_riscv_csr_mip
 *
 * From Priv spec v1.10
 *
 */
typedef struct {
    bit meip "Machine-external interrupt pending, mirroring the input pin";
    bit seip "System-external interrupt pending, mirroring the input pin";
    bit ueip "User-external interrupt pending, mirroring the input pin";
    bit seip_sw "System-external interrupt pending, mirroring the input pin";
    bit ueip_sw "User-external interrupt pending, mirroring the input pin";
    bit mtip "Machine timer interrupt pending, set by memory-mapped machine timer comparator meeting mtime";
    bit stip "System timer interrupt pending, set by software";
    bit utip "User timer interrupt pending, set by software";
    bit msip "Machine system interrupt pending, set by memory-mapped register if supported";
    bit ssip "System software interrupt pending, set by software";
    bit usip "User software interrupt pending, set by software";
} t_riscv_csr_mip;

/*t t_riscv_csr_mie
 *
 * From Priv spec v1.10
 *
 */
typedef struct {
    bit meip "Enable for machine-external interrupt pending";
    bit seip "Enable for system-external interrupt pending";
    bit ueip "Enable for user-external interrupt pending";
    bit mtip "Enable for machine timer interrupt pending";
    bit stip "Enable for system timer interrupt pending";
    bit utip "Enable for user timer interrupt pending";
    bit msip "Enable for machine system interrupt pending";
    bit ssip "Enable for system software interrupt pending";
    bit usip "Enable for user software interrupt pending";
} t_riscv_csr_mie;

/*t t_riscv_csr_tvec
 */
typedef struct {
    bit[30] base;
    bit     vectored;
} t_riscv_csr_tvec;

/*t t_riscv_csrs
 *
 * Minimal set of RISC-V CSRs - actually not minimal... but some are hardwired 0 if minimal
 *
 * mstatus    - see above
 * medeleg    - sync exceptions delegation - must be 0 if machine mode only
 * mideleg    - interrupt delegation       - must be 0 if machine mode only
 * mie        - interrupt enable           - meie, mtie, msie as a minimum
 * mtvec      - can be hardwired to 0
 * mcounteren - counter permissions     - should be 0 if machine mode only
 * mcause     - cause of interrupt/trap    - top bit set if interrupt, bottom bits indicate trap/irq
 * mscratch
 * mepc
 * mtval
 * mip        - interrupt pending          - meip, mtip, msip as a minimum
 *
 * dcsr       - see above
 * dpc        - address of ebreak, or of instruction to be executed after (single step or halt)
 * dscratch
 *
 */
typedef struct {
    bit[64] cycles    "Number of cycles since reset";
    bit[64] instret   "Number of instructions retired";
    bit[64] time      "Mirror of irqs.time - may be tied to 0 if only machine mode is supported";

    bit[32] mscratch  "Scratch register for exception routines";
    bit[32] mepc      "PC at last exception";
    bit[32] mcause    "Cause of last exception";
    bit[32] mtval     "Value associated with last exception";
    t_riscv_csr_tvec    mtvec     "Trap vector, can be hardwired or writable";
    t_riscv_csr_mstatus mstatus     "";
    t_riscv_csr_mip     mip         "";
    t_riscv_csr_mie     mie         "";

    // for N (User mode IRQs)
    bit[32] uscratch  "Scratch register for exception routines";
    bit[32] uepc      "PC at last exception";
    bit[32] ucause    "Cause of last exception";
    bit[32] utval     "Value associated with last exception";
    t_riscv_csr_tvec   utvec     "Trap vector, can be hardwired or writable";
    //  ustatus is a User-mode view on mstatus bits
    //  uip     is a User-mode view on mstatus bits
    //  uie     is a User-mode view on mstatus bits

    t_riscv_csr_dcsr    dcsr        "Debug control/status, if debug enabled (otherwise 0)";
    bit[32] depc;
    bit[32] dscratch0;
    bit[32] dscratch1;
} t_riscv_csrs;

/*a I32 types */
/*t t_riscv_i32_inst_debug_op
 */
typedef enum[2] {
    rv_inst_debug_op_read_reg,
    rv_inst_debug_op_write_reg
} t_riscv_i32_inst_debug_op;

/*t t_riscv_i32_inst_debug
 */
typedef struct {
    bit valid;
    t_riscv_i32_inst_debug_op debug_op;
    bit[16]                   data     "For reading/writing a register, this is the register number";
} t_riscv_i32_inst_debug;

/*t t_riscv_i32_inst
 */
typedef struct {
    t_riscv_mode mode;
    bit[32]      data;
    t_riscv_i32_inst_debug debug;
} t_riscv_i32_inst;

/*t t_riscv_i32_decode_ext
 *
 * A type that can be used to create an extended RISC-V, returned as part of the decode
 *
 */
typedef struct {
    bit dummy; // not used, but the struct must not be empty
} t_riscv_i32_decode_ext;

/*t t_riscv_i32_decode
 * Decoded i32 instruction, used throughout a pipeline (decode onwards)
 */
typedef struct {
    bit[5]       rs1                   "Source register 1 that is required by the instruction";
    bit          rs1_valid             "Asserted if rs1 is valid; if deasserted then rs1 is not used - only used for blocking in pipelines";
    bit[5]       rs2                   "Source register 2 that is required by the instruction";
    bit          rs2_valid             "Asserted if rs2 is valid; if deasserted then rs2 is not used - only used for blocking in pipelines";
    bit[5]       rd                    "Destination register that is written by the instruction";
    bit          rd_written            "Asserted if Rd is written to (hence also Rd will be non-zero)";
    t_riscv_csr_access     csr_access  "CSR access if valid and legal";
    bit[32]      immediate             "Immediate value decoded from the instruction";
    bit[5]       immediate_shift       "Immediate shift value decoded from the instruction";
    bit          immediate_valid       "Asserted if immediate data is valid and therefore to be used instead of source register 2";
    t_riscv_op     op                  "Operation class of the instruction";
    t_riscv_subop  subop               "Subclass of the operation class";
    t_riscv_shift_op shift_op          "Only valid for shift operations (i.e. ignored if op is not alu and subop is not a shift)";
    bit[7]         funct7              "Options for subop only to be used by custom instructions (so it can be optimized out)";
    bit           illegal              "asserted if an illegal opcode";
    bit           is_compressed        "asserted if from an i32-c decode, clear otherwise (effects link register)";
    t_riscv_i32_decode_ext ext         "extended decode, not used by the main pipeline";
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
    bit                     alu_data_not_ready   "Early in cycle (independent of coprocessors): If asserted, alu_idecode may be valid but rs1/rs2 are not; once deasserted it remains deasserted until a new ALU instruction starts";
    bit                     alu_cannot_complete "Late in cycle: If asserted, alu cannot complete because it is still working on its operation";
} t_riscv_i32_coproc_controls;

/*t t_riscv_i32_coproc_response
 */
typedef struct {
    bit          cannot_start "If asserted, block start of the ALU stage - the instruction is then tried again in the next cycle, but can be interrupted";
    t_riscv_word result;
    bit          result_valid "Early in cycle, if asserted then coproc overcomes the ALU result";
    bit          cannot_complete "Early in cycle: if deasserted the module is performing a calculation that has not produced a valid result yet (feeds back in to controls alu_cannot_complete)";
} t_riscv_i32_coproc_response;

/*a Dmem access */
/*t t_riscv_i32_dmem_exec */
typedef struct {
    bit                     valid;
    t_riscv_mode            mode;
    t_riscv_i32_decode      idecode "Exec stage idecode";
    t_riscv_word            arith_result;
    t_riscv_word            rs2;
    bit                     first_cycle;
} t_riscv_i32_dmem_exec;

/*t t_riscv_i32_dmem_request */
typedef struct {
    t_riscv_mem_access_req access;
    bit load_address_misaligned  "Asserted only for valid instructions, for loads not aligned to the alignment of the access";
    bit store_address_misaligned "Asserted only for valid instructions, for stores not aligned to the alignment of the access";
    bit    reading;
    bit[2] read_data_rotation;
    bit[4] read_data_byte_clear;
    bit[4] read_data_byte_enable;
    bit    sign_extend_byte;
    bit    sign_extend_half;
    bit    multicycle;
} t_riscv_i32_dmem_request;


