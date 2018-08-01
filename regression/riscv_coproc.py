#!/usr/bin/env python
#a Copyright
#  
#  This file 'riscv_minimal.py' copyright Gavin J Stark 2017
#  
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation, version 2.0.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#  for more details.

#a Imports
import pycdl
import sys, os, unittest, tempfile
import simple_tb
import riscv_internal

#a Useful functions
def int_of_bits(bits):
    l = len(bits)
    m = 1<<(l-1)
    v = 0
    for b in bits:
        v = (v>>1) | (m*b)
        pass
    return v

def bits_of_n(nbits, n):
    bits = []
    for i in range(nbits):
        bits.append(n&1)
        n >>= 1
        pass
    return bits

def signed32(n):
    if (n>>31)&1:
        n = (((-1) &~ 0x7fffffff) | n)
        pass
    return n

#a Globals
riscv_regression_dir      = "../riscv_tests_built/isa/"
riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"

#a Test classes
#c c_riscv_coproc_test_base
class c_riscv_coproc_test_base(simple_tb.base_th):
    dump_filename = None
    base_address = 0
    test_memory = "dmem"
    memory_expectation = {}
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        simple_tb.base_th.run_start(self)
        self.bfm_wait(self.run_time-10)
        self.finishtest(0,"")
        pass

#c c_riscv_coproc_test_simple
class c_riscv_coproc_test_simple(c_riscv_coproc_test_base):
    # instruction_list types: invalid, valid, holdN, flush, hold_interrupt?
    instruction_list = [
        (5, "valid", riscv_internal.mull(1,2,3), 17, 19, 17*19),
        (5, "valid", riscv_internal.mull(4,5,6), 0x12345, 0x6789a, (0x12345 * 0x6789a) & 0xffffffff),
        ]
    illegal_inst = riscv_internal.instruction()
    op_string = "*"
    #f run
    def run(self):
        self.sim_msg = self.sim_message()
        self.bfm_wait(10)
        dec_idecode = riscv_internal.i32_drivers(self, "coproc_controls__dec_idecode__")
        alu_idecode = riscv_internal.i32_drivers(self, "coproc_controls__alu_idecode__")
        simple_tb.base_th.run_start(self)
        self.bfm_wait(10)
        decode_stage = None
        alu_stage = None
        inst_index = 0
        decode_cycle = 0
        alu_cycle = 0
        while (decode_stage is not None) or (alu_stage is not None) or (inst_index < len(self.instruction_list)):
            if (not self.coproc_response__cannot_complete.value()) and (alu_stage is not None):
                result = self.coproc_response__result.value()
                print "Result %08x : %d : %s" % (result, result, alu_stage)
                if result != alu_stage[5]:
                    self.failtest(inst_index, "Mismatch in results : 0x%08x %s 0x%08x = 0x%08x got 0x%08x" % (alu_stage[3], self.op_string, alu_stage[4], alu_stage[5], result))
                    pass
                alu_stage = None # Should check for other completion mechanism!
            if alu_stage is None and decode_stage is not None:
                if decode_cycle > decode_stage[0]:
                    alu_stage = decode_stage
                    alu_cycle = 0
                    decode_stage = None
                    pass
                pass
            if decode_stage is None:
                if inst_index < len(self.instruction_list):
                    decode_stage = self.instruction_list[inst_index]
                    decode_cycle = 0
                    inst_index = inst_index + 1
                    pass
                pass
            if (decode_stage is not None) and (decode_cycle>=decode_stage[0]):
                (delay, t, inst, rs1, rs2, result) = decode_stage
                dec_idecode.drive(inst)
                self.coproc_controls__dec_idecode_valid.drive(1)
                pass
            else:
                self.coproc_controls__dec_idecode_valid.drive(0)
                dec_idecode.drive(self.illegal_inst)
                pass
            decode_cycle = decode_cycle + 1
            if alu_stage is None:
                alu_idecode.drive(self.illegal_inst)
                self.coproc_controls__alu_idecode_valid.drive(0)
                pass
            else:
                (delay, t, inst, rs1, rs2, result) = alu_stage
                alu_idecode.drive(inst)
                self.coproc_controls__alu_idecode_valid.drive(1)
                self.coproc_controls__alu_rs1.drive(rs1)
                self.coproc_controls__alu_rs2.drive(rs2)
                pass
            alu_cycle = alu_cycle + 1
            self.bfm_wait(1)
            pass
        self.bfm_wait(10)
        self.passtest(inst_index,"Ran all coprocessor instructions")
        self.finishtest(0,"")
        pass

#c c_riscv_coproc_test_multiply
class c_riscv_coproc_test_multiply(c_riscv_coproc_test_simple):
    # instruction_list types: invalid, valid, holdN, flush, hold_interrupt?
    instruction_list = [
        (5, "valid", riscv_internal.mull(1,2,3), 17, 19, 17*19),
        (5, "valid", riscv_internal.mull(4,5,6), 0x12345, 0x6789a, (0x12345 * 0x6789a) & 0xffffffff),
        ]
    for (rs1,rs2) in [(0xfedcba98, 0),
                      (0, 0xfedcba98),
                      (0, 0),
                      (0, 1),
                      (1, 0),
                      (0xfedcba98, 0x76543210),
                      (0x76543210, 0xfedcba98),
                      (0x210, (-0x210)&0xffffffff),
                      ((-0x210)&0xffffffff, 0x210),
                      ]:
        result = rs1 * rs2
        instruction_list.append( (5, "valid", riscv_internal.mulhu(4,5,6), rs1, rs2, (result>>32) & 0xffffffff) )
        instruction_list.append( (5, "valid", riscv_internal.mull(4,5,6),  rs1, rs2, (result>> 0) & 0xffffffff) )

        result = signed32(rs1) * signed32(rs2)
        instruction_list.append( (5, "valid", riscv_internal.mulh(4,5,6), rs1, rs2, (result>>32) & 0xffffffff) )
        instruction_list.append( (5, "valid", riscv_internal.mull(4,5,6), rs1, rs2, (result>> 0) & 0xffffffff) )

        result = signed32(rs1) * rs2
        instruction_list.append( (5, "valid", riscv_internal.mulhsu(4,5,6), rs1, rs2, (result>>32) & 0xffffffff) )
        instruction_list.append( (5, "valid", riscv_internal.mull(4,5,6),   rs1, rs2, (result>>0) & 0xffffffff) )

        pass

#c c_riscv_coproc_test_divide
class c_riscv_coproc_test_divide(c_riscv_coproc_test_simple):
    op_string = "/" # should be part of instruction_list
    instruction_list = [
        (5, "valid", riscv_internal.div(1,2,3), 17, 4, 17/4),
        (5, "valid", riscv_internal.div(1,2,3), 16, 4, 16/4),
        (5, "valid", riscv_internal.div(4,5,6), 0x6789a, 0x123, 0x6789a / 0x123 ),
        (5, "valid", riscv_internal.divu(1,2,3), 17, 4, 17/4),
        (5, "valid", riscv_internal.divu(1,2,3), 16, 4, 16/4),
        (5, "valid", riscv_internal.divu(4,5,6), 0x6789a, 0x123, 0x6789a / 0x123 ),
        (5, "valid", riscv_internal.rem(1,2,3), 17, 4, 17%4),
        (5, "valid", riscv_internal.rem(1,2,3), 16, 4, 16%4),
        (5, "valid", riscv_internal.rem(4,5,6), 0x6789a, 0x123, 0x6789a % 0x123 ),
        (5, "valid", riscv_internal.remu(1,2,3), 17, 4, 17%4),
        (5, "valid", riscv_internal.remu(1,2,3), 16, 4, 16%4),
        (5, "valid", riscv_internal.remu(4,5,6), 0x6789a, 0x123, 0x6789a % 0x123 ),
        (5, "valid", riscv_internal.div(1,2,3), 17, (-4)&0xffffffff, (-(17/4)) & 0xffffffff),
        (5, "valid", riscv_internal.rem(1,2,3), 17, (-4)&0xffffffff, (17 - (-4)*(-(17/4)))&0xffffffff),
        (5, "valid", riscv_internal.divu(1,2,3), 17, (-4)&0xffffffff, (17/((-4) & 0xffffffff))),
        (5, "valid", riscv_internal.remu(1,2,3), 17, (-4)&0xffffffff, (17%((-4) & 0xffffffff))),

        (5, "valid", riscv_internal.div(1,2,3),  (-17)&0xffffffff, 4, (-(17/4)) & 0xffffffff),
        (5, "valid", riscv_internal.rem(1,2,3),  (-17)&0xffffffff, 4, ((-17) - 4*(-(17/4)) & 0xffffffff)),
        (5, "valid", riscv_internal.divu(1,2,3), (-17)&0xffffffff, 4, (((-17) & 0xffffffff)/4)),
        (5, "valid", riscv_internal.remu(1,2,3), (-17)&0xffffffff, 4, (((-17) & 0xffffffff)%4)),

        ]

#a Hardware classes
#c riscv_coproc_test_hw
class riscv_coproc_test_hw(simple_tb.cdl_test_hw):
    """
    Simple instantiation of RISCV minimal testbench
    """
    loggers = {#"itrace": {"verbose":0, "filename":"itrace.log", "modules":("dut.trace "),},
               }
    coproc_response = pycdl.wirebundle(riscv_internal.i32_coproc_response)
    coproc_controls = pycdl.wirebundle(riscv_internal.i32_coproc_controls)
    th_forces = { "th.clock":"clk",
                  "th.inputs":" ".join(coproc_response._name_list("coproc_response")),
                  "th.outputs":" ".join(coproc_controls._name_list("coproc_controls")),
                  }
    module_name = "tb_riscv_i32_muldiv"
    #f __init__
    def __init__(self, test):
        self.th_forces = self.th_forces.copy()
        simple_tb.cdl_test_hw.__init__(self,test)
        pass
    pass

#a Simulation test classes
#c riscv_coproc
class riscv_coproc(simple_tb.base_test):
    def test_simple(self):
        self.do_test_run(riscv_coproc_test_hw(c_riscv_coproc_test_simple()), num_cycles=5000)
        pass
    def test_multiply(self):
        self.do_test_run(riscv_coproc_test_hw(c_riscv_coproc_test_multiply()), num_cycles=5000)
        pass
    def test_divide(self):
        self.do_test_run(riscv_coproc_test_hw(c_riscv_coproc_test_divide()), num_cycles=5000)
        pass
    pass

