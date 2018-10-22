#a Enumerations etc
#v rv32_opc
rv32_opc = {
    "riscv_opc_load":       0,# // rv32i (lb, lh, lw, lbu, lhu); rv64i (lwu, ld)
    "riscv_opc_load_fp":    1,# // rv32f (flw)
    "riscv_opc_custom_0":   2,#
    "riscv_opc_misc_mem":   3,# // rv32i (fence, fence.i)
    "riscv_opc_op_imm":     4,# // rv32i (addi, slti, sltiu, xori, ori, andi); rv64i (slli, srli, srai)
    "riscv_opc_auipc":      5,# // rv32i (auipc)
    "riscv_opc_op_imm32":   6,# // rv64i (addiw, slliw, srliw, sraiw)
    "riscv_opc_store":      8,# // rv32i (sb, sh, sw); rv64i (sd)
    "riscv_opc_store_fp":   9,# // rv32f (fsw)
    "riscv_opc_custom_1":  10,#
    "riscv_opc_amo":       11,# // rv32a (lr.w, sc.w, amoswap.w, amoadd.w, amoxor.w, amoand.w, amoor.w, amomin.w, amomax.w, amomaxu.w) (+rv64a)
    "riscv_opc_op":        12,# // rv32i (add, sub, sll, slt, sltu, xor, srl, sra, or, and); rv32m (mul, mulh, mulhsu, mulhu, div, divu, rem, remu)
    "riscv_opc_lui":       13,# // rv32i
    "riscv_opc_op32":      14,# // rv64i (addw, subw, sllw, srlw, sraw)
    "riscv_opc_madd":      16,# // rv32f (fmadd.s)
    "riscv_opc_msub":      17,# // rv32f (fmsub.s)
    "riscv_opc_nmsub":     18,# // rv32f (fnmsub.s)
    "riscv_opc_nmadd":     19,# // rv32f (fnmadd.s)
    "riscv_opc_op_fp":     20,# // rv32f (fadd.s, fsub.s, fmul.s, fdiv.s, fsqrt.s, fsgnj.s, fsgnjn.s, fsgnjx.s, fmin.s, ... fmv.s.x)
    "riscv_opc_resvd_0":   21,#
    "riscv_opc_custom_2":  22,#
    "riscv_opc_branch":    24,# // rv32i (beq, bne, blt, bge, bltu, bgeu)
    "riscv_opc_jalr":      25,# // rv32i (jalr)
    "riscv_opc_resvd_1":   26,#
    "riscv_opc_jal":       27,# // rv32i (jal)
    "riscv_opc_system":    28,# // rv32i (ecall, ebreak, csrrw, csrrs, csrrc, csrrwi, csrrsi, csrrci)
    "riscv_opc_resvd_2":   29,#
    "riscv_opc_custom_3":  30, #
}

#v i32_op - decode for 32-bit RISC-V implementation
i32_op = [
    "riscv_op_branch",
    "riscv_op_jal",
    "riscv_op_jalr",
    "riscv_op_system",
    "riscv_op_csr",
    "riscv_op_misc_mem",
    "riscv_op_load",
    "riscv_op_store",
    "riscv_op_alu",
    "riscv_op_muldiv",
    "riscv_op_auipc",
    "riscv_op_lui",
    "riscv_op_illegal",
    ]

#v i32_subop - decode for 32-bit RISC-V implementation
i32_subop = {
    "riscv_subop_valid":0, # // for op==illegal, really - means op==invalid is sufficient for illegal op
    "riscv_subop_illegal": 0xf, # // for many of the ops...

    "riscv_subop_beq":0, # // same as rvi_branch_f3
    "riscv_subop_bne":1, # 
    "riscv_subop_blt":2, # 
    "riscv_subop_bge":3, # 
    "riscv_subop_bltu":4, # 
    "riscv_subop_bgeu":5, # 

    "riscv_subop_add": 0, # // same as riscv_op_f3, with bit[3] as the 'extra' ops
    "riscv_subop_sub": 0+8, #
    "riscv_subop_sll": 1, #
    "riscv_subop_slt": 2, #
    "riscv_subop_sltu": 3, #
    "riscv_subop_xor": 4, #
    "riscv_subop_srl": 5, #
    "riscv_subop_sra": 5+8, #
    "riscv_subop_or": 6, #
    "riscv_subop_and": 7, #

    "riscv_subop_mull": 0, # // same as riscv_op_f3
    "riscv_subop_mulhss": 1, #
    "riscv_subop_mulhsu": 2, #
    "riscv_subop_mulhu":  3, #
    "riscv_subop_divs": 4, #
    "riscv_subop_divu": 5, #
    "riscv_subop_rems": 6, #
    "riscv_subop_remu": 7, #

    "riscv_subop_lb": 0, # // same as rvi_f3_load
    "riscv_subop_lh": 1, #
    "riscv_subop_lw": 2, #
    "riscv_subop_lbu": 4, #
    "riscv_subop_lhu": 5, #

    "riscv_subop_sb": 0, # // same as rvi_f3_store
    "riscv_subop_sh": 1, #
    "riscv_subop_sw": 2, #

    "riscv_subop_ecall": 0, #
    "riscv_subop_ebreak": 1, #
    "riscv_subop_mret": 2, #
    "riscv_subop_mwfi": 3, #

    "riscv_subop_fence": 0, # // to match riscv_op_f3
    "riscv_subop_fence_i": 1, #

    "riscv_subop_csrrw": 1, # // to match riscv_op_f3
    "riscv_subop_csrrs": 2, #
    "riscv_subop_csrrc": 3, #
}

#v rv32_f3 - RV32I decode of f3 = instruction[3;12]
rv32_f3 = {
    "riscv_f3_addsub":  0,# alu // sub has f7[5] set, add has it clear
    "riscv_f3_sll":     1,#
    "riscv_f3_slt":     2,#
    "riscv_f3_sltu":    3,#
    "riscv_f3_xor":     4,#
    "riscv_f3_srlsra":  5,# // sra has f7[5] set, srl has it clear
    "riscv_f3_or":      6,#
    "riscv_f3_and":     7,#

    "riscv_f3_mul":     0,# muldiv
    "riscv_f3_mulh":    1,#
    "riscv_f3_mulhsu":  2,#
    "riscv_f3_mulhu":   3,#
    "riscv_f3_div":     4,#
    "riscv_f3_divu":    5,#
    "riscv_f3_rem":     6,#
    "riscv_f3_remu":    7,#

    "riscv_f3_beq":   0,# branch
    "riscv_f3_bne":   1,#
    "riscv_f3_blt":   4,#
    "riscv_f3_bge":   5,#
    "riscv_f3_bltu":  6,#
    "riscv_f3_bgeu":  7,#

    "riscv_f3_lb":   0,# load
    "riscv_f3_lh":   1,#
    "riscv_f3_lw":   2,#
    "riscv_f3_lbu":  4,#
    "riscv_f3_lhu":  5,#

    "riscv_f3_sb":   0,# store
    "riscv_f3_sh":   1,#
    "riscv_f3_sw":   2,#

    "riscv_f3_fence":    0,# misc_mem
    "riscv_f3_fence_i":  1,#

    "riscv_f3_privileged":  0,# system
    "riscv_f3_csrrw":  1,#
    "riscv_f3_csrrs":  2,#
    "riscv_f3_csrrc":  3,#
    "riscv_f3_csrrwi":  5,#
    "riscv_f3_csrrsi":  6,#
    "riscv_f3_csrrci":  7,#
}

#a Dictionaries for wirebundles
#v riscv_config - signal widths for pycdl.wirebundle - must match implementation
riscv_config = {"i32c":1,
                "e32":1,
                "i32m":1,
                "i32m_fuse":1,
                "coproc_disable":1,
                "unaligned_mem":1,
}

#v i32_csr_access - signal widths for pycdl.wirebundle - must match implementation
i32_csr_access = {"access":3, "address":12, "access_cancelled":1}

#v i32_decode - signal widths for pycdl.wirebundle - must match implementation
i32_decode = {"rs1":5,
              "rs1_valid":1,
              "rs2":5,
              "rs2_valid":1,
              "rd":5,
              "rd_written":1,
              "immediate":32,
              "immediate_shift":5,
              "immediate_valid":1,
              "op":4,
              "subop":4,
              "memory_read_unsigned":1,
              "memory_width":2,
              "csr_access":i32_csr_access,
              "illegal":1,
              "illegal_pc":1,
              "requires_machine_mode":1,
              "is_compressed":1,
              "ext__dummy":1,
              }

#v i32_coproc_response - signal widths for pycdl.wirebundle - must match implementation
i32_coproc_response = {"result":32,
                       "result_valid":1,
                       "cannot_complete":1,
                       "cannot_start":1}
#v i32_coproc_controls - signal widths for pycdl.wirebundle - must match implementation
i32_coproc_controls = {"dec_idecode_valid":1,
                       "dec_idecode":i32_decode,
                       "dec_to_alu_blocked":1,
                       "alu_cannot_complete":1,
                       "alu_flush_pipeline":1,
                       "alu_cannot_start":1,
                       "alu_rs1":32,
                       "alu_rs2":32,
                       }

#a Class i32_drivers
class i32_drivers:
    def __init__(self, o, s):
        """o is a pycdl object with signals, s is a signal base such as coproc_controls__alu_idecode__, so o.<s> is the base for the i32_decode"""
        self.drivers = {}
        for k in i32_decode:
            if hasattr(o,s+k):
                self.drivers[k] = getattr(o,s+k)
                pass
            else:
                self.drivers[k] = None
                pass
            pass
        pass
    pass
    def drive(self, inst):
        """inst is an instruction"""
        r = inst.i32_decode()
        for k in r:
            if self.drivers[k]:
                self.drivers[k].drive(r[k])
            pass
        pass
    pass

#a RV32 instruction classes with i32 decode
#c instruction - the base class
class instruction:
    rs1 = None
    rs2 = None
    rd = None
    immediate = None
    immediate_shift = None
    op    = "riscv_op_illegal"
    subop = "riscv_subop_illegal"
    csr_access = None
    rv32_encode = None
    disassembly = None
    def __init__(self):
        pass
    def i32_decode(self):
        r = {}
        for k in i32_decode:
            r[k] = 0
            pass
        if self.rs1 is not None:
            r["rs1"] = self.rs1
            r["rs1_valid"] = 1
            pass
        if self.rs2 is not None:
            r["rs2"] = self.rs2
            r["rs2_valid"] = 1
            pass
        if self.rd is not None:
            r["rd"] = self.rd
            r["rd_written"] = 1
            pass
        if self.immediate is not None:
            r["immediate"]  = self.immediate
            r["immediate_valid"] = 1
            pass
        if self.immediate_shift is not None:
            r["immediate_shift"]  = self.immediate_shift
            pass
        r["op"] = i32_op.index(self.op)
        r["subop"] = i32_subop[self.subop]
        return r

#c mul base class (subclass of instruction)
class mul(instruction):
    op = "riscv_op_muldiv"
    subop = "riscv_subop_mull"
    f3_of_subop = {"riscv_subop_mull"  :rv32_f3["riscv_f3_mul"],
                   "riscv_subop_mulhss":rv32_f3["riscv_f3_mulh"],
                   "riscv_subop_mulhsu":rv32_f3["riscv_f3_mulhsu"],
                   "riscv_subop_mulhu" :rv32_f3["riscv_f3_mulhu"],
                   }
    def __init__(self, rs1, rs2, rd):
        """rs1 is the multiplicand, rs2 the multiplier"""
        self.rs1 = rs1
        self.rs2 = rs2
        self.rd = rd
        if not self.high:
            self.subop = "riscv_subop_mull"
            pass
        elif self.unsigned:
            self.subop = "riscv_subop_mulhu"
            pass
        elif self.signed_unsigned:
            self.subop = "riscv_subop_mulhsu"
            pass
        else:
            self.subop = "riscv_subop_mulhss"
            pass
        self.rv32_encode = 3 | (rv32_opc["riscv_opc_op"]<<2) | (self.rd<<7) | (self.f3_of_subop[self.subop]<<12) | (self.rs1<<15) | (self.rs2<<20) | (1<<25) # muldiv in top 7 is 0000001
        self.disassembly = ["MUL?", self.rs1, self.rs2, self.rd]
        pass
    pass

#c mull, mulh, mulhu, mulhsu RV32M instructions
class mull(mul):
    high = False
    pass
class mulh(mul):
    high = True
    unsigned = False
    signed_unsigned = False
    pass
class mulhu(mul):
    high = True
    unsigned = True
    signed_unsigned = False
    pass
class mulhsu(mul):
    high = True
    unsigned = False
    signed_unsigned = True
    pass

#c div base class (subclass of instruction)
class div(instruction):
    op = "riscv_op_muldiv"
    subop = "riscv_subop_divs"
    f3_of_subop = {"riscv_subop_divs" :rv32_f3["riscv_f3_div"],
                   "riscv_subop_divu" :rv32_f3["riscv_f3_divu"],
                   "riscv_subop_rems" :rv32_f3["riscv_f3_rem"],
                   "riscv_subop_remu" :rv32_f3["riscv_f3_remu"],
                   }
    signed = True
    remainder = False
    def __init__(self, rs1, rs2, rd):
        """rs1 is the dividend, rs2 the divisor"""
        self.rs1 = rs1
        self.rs2 = rs2
        self.rd = rd
        if self.remainder:
            if self.signed:
                self.subop = "riscv_subop_rems"
            else:
                self.subop = "riscv_subop_remu"
            pass
        else:
            if self.signed:
                self.subop = "riscv_subop_divs"
            else:
                self.subop = "riscv_subop_divu"
            pass
        self.rv32_encode = 3 | (rv32_opc["riscv_opc_op"]<<2) | (self.rd<<7) | (self.f3_of_subop[self.subop]<<12) | (self.rs1<<15) | (self.rs2<<20) | (1<<25) # muldiv in top 7 is 0000001
        self.disassembly = ["DIV?", self.rs1, self.rs2, self.rd]
        pass
    pass

#c divu, rem, remu RV32M instructions
class divu(div):
    signed = False
    remainder = False
    pass
class rem(div):
    signed = True
    remainder = True
    pass
class remu(div):
    signed = False
    remainder = True
    pass
