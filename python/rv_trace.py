#!/usr/bin/env python

from pycdl import c_logs
import csv

#timestamp,id,dut.dut.trace,1="PC",3,"pc","branch_taken","branch_target"
#timestamp,id,dut.dut.trace,1="PC",10,"pc","branch_taken","branch_target","op","subop","valids","rs1","rs2","rd","imm"

#a Rv instructions
riscv_ops = [
    "branch",
    "jal",
    "jalr",
    "system",
    "csr",
    "misc_mem",
    "load",
    "store",
    "alu",
    "muldiv",
    "auipc",
    "lui",
    "illegal",
]
def bits (s,e,v):
    l = (e+1-s)
    m = (1<<l)-1
    return (v>>s) & m

#c rv_instr
class rv_instr:
    inst_from_opcode = []
    rd = None
    rs1 = None
    rs2 = None
    immediate = None
    @classmethod
    def add_instr_class(rv,cls):
        def mk_inst(pc,x): return cls(pc).from_binary(x)
        rv.inst_from_opcode.append((cls.bin_mask,cls.bin_value,mk_inst))
    @classmethod
    def from_binary(cls, pc, x):
        for (mask,value,mk_inst) in cls.inst_from_opcode:
            if (x & mask)==value: return mk_inst(pc, x)
            pass
        return cls(pc).set_from_binary(pc,x)
    def __init__(self, pc):
        self.pc = pc
        pass
    def set_rs1(self,rs1): self.rs1=rs1
    def set_rs2(self,rs2): self.rs2=rs2
    def set_rd(self,rd): self.rd=rd
    def str_rd(self):
        if self.rd==0: return "--"
        return "r%d" % self.rd
    def str_rs(self, rs):
        if rs==0: return "0"
        return "r%d" % rs
    def str_rs1(self): return self.str_rs(self.rs1)
    def str_rs2(self): return self.str_rs(self.rs2)
    def set_imm(self,imm): self.immediate = imm
    def set_imm_sext(self,imm,b):
        if (imm>>b)&1: imm |= (0xffffffff<<b) & 0xffffffff
        if (imm>>31) & 1: imm= (-1<<31) | imm
        self.set_imm(imm)
        pass
    def set_from_binary(self,pc,x):
        self.instr_data = x
        return self
    def disassemble(self):
        return "?%08x?"%self.instr_data

#c rv_instr_lui
class rv_instr_lui(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x37
    def from_binary(self, x):
        self.set_rd(bits(7,11,x))
        self.set_imm(bits(12,31,x)<<12)
        return self
    def disassemble(self):
        return "lui r%d, 0x%08x"%(self.rd, self.immediate)

#c rv_instr_auipc
class rv_instr_auipc(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x17
    def from_binary(self, x):
        self.set_rd(bits(7,11,x))
        self.set_imm(bits(12,31,x)<<12)
        return self
    def disassemble(self):
        return "auipc r%d, 0x%08x"%(self.rd, self.immediate)

#c rv_instr_jal
class rv_instr_jal(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x6f
    def from_binary(self, x):
        self.set_rd(bits(7,11,x))
        self.set_imm_sext( (bits(12,19,x)<<12) |
                           (bits(20,20,x)<<11) |
                           (bits(21,30,x)<<1) |
                           (bits(31,31,x)<<20), 20 )
        return self
    def disassemble(self):
        link = ""
        if self.rd!=0: link = "al %s,"%self.str_rd()
        return "j %s0x%08x"%(link, self.pc + self.immediate)

#c rv_instr_bcc
class rv_instr_bcc(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x63
    cc_str = ["eq", "ne", "??", "??", "lt", "ge", "ltu", "geu"]
    def from_binary(self, x):
        self.set_rs1(bits(15,19,x))
        self.set_rs2(bits(20,24,x))
        self.set_imm_sext( (bits(8,11,x)<<1) |
                           (bits(25,30,x)<<5) |
                           (bits(7,7,x)<<11) |
                           (bits(31,31,x)<<12), 12 )
        self.cc = bits(12,14,x)
        return self
    def disassemble(self):
        return "b%s %s, %s, 0x%08x"%(self.cc_str[self.cc], self.str_rs1(), self.str_rs2(), self.pc+self.immediate)

#c rv_instr_alui
class rv_instr_alui(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x13
    subop_str = ["add", "sll", "slt", "sltiu", "xor", "srl", "or", "and", "sra"]
    def from_binary(self, x):
        self.set_rd(bits(7,11,x))
        self.set_rs1(bits(15,19,x))
        self.set_imm_sext( (bits(20,31,x)<<0), 11 )
        self.subop = bits(12,14,x)
        if (self.subop==1) or (self.subop==5): self.immediate = self.immediate & 31
        if (self.subop==5) and (bits(30,30,x)): self.subop=8 # srai
        return self
    def disassemble(self):
        return "%si %s, %s, %d"%(self.subop_str[self.subop], self.str_rd(), self.str_rs1(), self.immediate)

#c rv_instr_alu
class rv_instr_alu(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x33
    subop_str = ["add", "sll", "slt", "sltu", "xor", "srl", "or", "and", "sra", "sub"]
    def from_binary(self, x):
        self.set_rd(bits(7,11,x))
        self.set_rs1(bits(15,19,x))
        self.set_rs2(bits(20,24,x))
        self.subop = bits(12,14,x)
        if (self.subop==0) and (bits(30,30,x)): self.subop=9 # sub
        if (self.subop==5) and (bits(30,30,x)): self.subop=8 # sra
        return self
    def disassemble(self):
        return "%s %s, %s, %s"%(self.subop_str[self.subop], self.str_rd(), self.str_rs1(), self.str_rs2())

#c rv_instr_system
class rv_instr_system(rv_instr):
    bin_mask  = 0xfffff
    bin_value = 0x73
    syscalls = {0:"ecall", 1:"ebreak", 0x302:"mret"}
    def from_binary(self, x):
        self.sys   = bits(20,31,x)
        return self
    def disassemble(self):
        if self.sys not in self.syscalls: return "sys? %x ?"%self.sys
        return "%s"%(self.syscalls[self.sys])

#c rv_instr_csr
class rv_instr_csr(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x73
    csr_str = ["??", "csrrw", "csrrs", "csrrc", "??", "csrrwi", "csrrsi", "csrrci"]
    def from_binary(self, x):
        self.csrop = bits(12,14,x)
        self.set_rs1(bits(15,19,x))
        self.set_rd(bits(7,11,x))
        self.csr   = bits(20,31,x)
        return self
    def disassemble(self):
        if self.csrop>=4:
            if self.rd==0: return "csrwi %d, 0x%03x"%(self.rs1, self.csr)
            return "%s %s, %s, 0x%03x"%(self.csr_str[self.csrop], self.str_rd(), self.rs1, self.csr)
        if self.rd==0: return "csrw %s, 0x%03x"%(self.str_rs1(), self.csr)
        if (self.csrop==2) and (self.rs1==0):return "csrr %s, 0x%03x"%(self.str_rd(), self.csr)
        return "%s %s, %s, 0x%03x"%(self.csr_str[self.csrop], self.str_rd(), self.str_rs1(), self.csr)

#c rv_instr_store
class rv_instr_store(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x23
    subop_str = ["sb", "sh", "sw", "??"]
    def from_binary(self, x):
        self.set_rs1(bits(15,19,x))
        self.set_rs2(bits(20,24,x))
        self.subop = bits(12,14,x)
        self.set_imm_sext( (bits(25,31,x)<<5)|
                           (bits(7,11,x)<<0), 11 )
        return self
    def disassemble(self):
        return "%s %s, %d(%s)"%(self.subop_str[self.subop], self.str_rs2(), self.immediate, self.str_rs1())

#c rv_instr_load
class rv_instr_load(rv_instr):
    bin_mask  = 0x7f
    bin_value = 0x03
    subop_str = ["lb", "lh", "lw", "??", "lbu", "lsu", "??", "??"]
    def from_binary(self, x):
        self.set_rs1(bits(15,19,x))
        self.set_rd(bits(7,11,x))
        self.subop = bits(12,14,x)
        self.set_imm_sext( (bits(20,31,x)<<0), 11 )
        return self
    def disassemble(self):
        return "%s %s, %d(%s)"%(self.subop_str[self.subop], self.str_rd(), self.immediate, self.str_rs1())

#f add instruction classes
rv_instr.add_instr_class(rv_instr_lui)
rv_instr.add_instr_class(rv_instr_auipc)
rv_instr.add_instr_class(rv_instr_jal)
rv_instr.add_instr_class(rv_instr_bcc)
rv_instr.add_instr_class(rv_instr_alui)
rv_instr.add_instr_class(rv_instr_alu)
rv_instr.add_instr_class(rv_instr_system)
rv_instr.add_instr_class(rv_instr_csr)
rv_instr.add_instr_class(rv_instr_store)
rv_instr.add_instr_class(rv_instr_load)

#a Toplevel
module_aliases = {}
itrace = c_logs.c_log_file(module_aliases)
itrace.open("itrace.log")

retire_filter = c_logs.c_log_filter()
retire_filter.add_match({"field":"reason", "type":"streq", "string":"retire"})
itrace.add_filter("retire",retire_filter)

pc_filter = c_logs.c_log_filter()
pc_filter.add_match({"field":"reason", "type":"streq", "string":"PC"})
itrace.add_filter("pc",pc_filter)

# print itrace.matching_events(["retire"])
retire_events = itrace.matching_event_occurrences(module="dut.trace", filter_name_list=["retire"])

pc_events = itrace.matching_event_occurrences(module="dut.trace", filter_name_list=["pc"])

rfw_events = {}
for (k,o) in retire_events:
    (timestamp,n,args) = o
    rfw = args[0]
    rd = args[1]
    data = args[2]
    if rfw:
        rfw_events[n] = "r%d <= %08x"%(rd, data)
        pass
    pass

for (k,o) in pc_events:
    (timestamp,n,args) = o
    pc = args[0]
    branch_taken  = args[1]
    branch_nonpredicted = args[2]
    instr_data   = args[3]
    c = rv_instr.from_binary(pc, instr_data)
    rfw_str = ""
    if n in rfw_events: rfw_str = rfw_events[n]
    timestamp_str = ""
    if False:
        timestamp_str = "%7d : "%timestamp
    print "%s%08x : %30s : %15s"%(timestamp_str,pc,c.disassemble(), rfw_str)



        

