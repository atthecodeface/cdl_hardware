#!/usr/bin/env python
#a Imports
from instr6502 import c65i_reset, c65am_reset, c_6502_instruction_set
import unittest

#a Register classes
#c c_6502_register
class c_6502_register(object):
    name = "BITS??"
    formats = {8:"%s:%02x"}
    width = 8
    def __init__(self):
        self.value = 0
        pass
    def set(self, value):
        self.value = value
        pass
    def get(self):
        return self.value
    def idle(self, din):
        return din
    def __str__(self):
        return self.formats[self.width] % (self.name, self.value)
    pass

#c c65r_index_x
class c65r_index_x(c_6502_register):
    name = "X"
    pass

#c c65r_index_y
class c65r_index_y(c_6502_register):
    name = "Y"
    pass

#c c65r_accumulator
class c65r_accumulator(c_6502_register):
    name = "A"
    pass

#c c65r_pcl
class c65r_pcl(c_6502_register):
    name = "PCL"
    pass

#c c65r_pch
class c65r_pch(c_6502_register):
    name = "PCH"
    pass

#c c65r_sp
class c65r_sp(c_6502_register):
    name = "SP"
    pass

#c c65r_ir
class c65r_ir(c_6502_register):
    name = "IR"
    pass

#c c65r_dl
class c65r_dl(c_6502_register):
    name = "DL"
    pass

#c c65r_adl
class c65r_adl(c_6502_register):
    name = "ADL"
    pass

#c c65r_adh
class c65r_adh(c_6502_register):
    name = "ADH"
    pass

#a CPU
#c c_6502
class c_6502(object):
    #f __init__
    def __init__(self):
        self.pcl = c65r_pcl()
        self.pch = c65r_pch()
        self.ir  = c65r_ir()
        self.sp  = c65r_sp()
        self.acc = c65r_accumulator()
        self.x   = c65r_index_x()
        self.y   = c65r_index_y()
        self.dl  = c65r_dl()
        self.adl = c65r_adl()
        self.adh = c65r_adh()
        self.psr = {"c":0, "n":0, "z":0, "v":0, "i":0, "d":0, "b":0}
        self.reset_ack = 0
        self.instr = (c65i_reset, c65am_reset)
        self.instr_cycle = 0
        self.instruction_set = c_6502_instruction_set()
        pass
    #f reset
    def reset(self):
        self.instr = (c65i_reset, c65am_reset)
        self.instr_cycle = 0
        pass
    #f get_internal_data_bus
    def get_internal_data_bus(self, instr_am_cycle, alu=0, data_in=0):
        (instr, am, cycle) = instr_am_cycle
        if cycle.idb is None: return (None,None,None) #(0xff,0xff)
        a = 0xff
        b = 0xff
        c = 0xff
        # cycle.idb[0] should be None, "zero", "index", "src"
        # "index" is only compatible with idb[1] being "dl"
        # Hence a 'src' bus could be determined with (drive_A?A) & (drive_X?X) & (drive_Y?Y) & (drive_SP?SP)
        if cycle.idb[0] in ["zero"]:  a = 0
        elif cycle.idb[0] in ["index"]:
            if am.index=="x": a = self.x.get()
            if am.index=="y": a = self.y.get()
            pass
        elif cycle.idb[0] in ["src"]:
            if instr.src=="acc": a = self.acc.get()
            elif instr.src=="s": a = self.sp.get()
            elif instr.src=="x": a = self.x.get()
            elif instr.src=="y": a = self.y.get()
            elif instr.src=="flags": a = ( (self.psr["n"]<<7)  |
                                           (self.psr["v"]<<6)  |
                                           #(self.psr["-"]<<5) |
                                           (self.psr["b"]<<4) |
                                           (self.psr["d"]<<3) |
                                           (self.psr["i"]<<2) |
                                           (self.psr["z"]<<1)  |
                                           (self.psr["c"]<<0) )
            elif instr.src=="zero": a=0    # Used for CLx
            elif instr.src=="ones": a=0xff # Used for SEx
            else: raise Exception("Bad source '%s'"%instr.src)
            pass
        elif cycle.idb[0] in ["pcl"]:
            a = self.pcl.get()
            pass
        elif cycle.idb[0] is None:
            pass
        else: raise Exception("Bad idb[0] source %s"%cycle.idb[0])
        # cycle.idb[1] should be None, "dl", ("dl+1"?)
        if cycle.idb[1] in ["dl"]:
            b = self.dl.get()
        elif cycle.idb[1] in ["pch"]:
            b = self.pch.get()
        elif cycle.idb[1] in ["sp"]:
            b = self.sp.get()
        elif cycle.idb[1] in ["src"]:
            if instr.src=="acc": b = self.acc.get() # Used in ASL A etc
            elif instr.src=="x": b = self.x.get()
            elif instr.src=="y": b = self.y.get()
            else: raise Exception("Bad source %s"%instr.src)
            pass
        elif cycle.idb[1] is None:
            pass
        else: raise Exception("Bad idb[1] source %s"%cycle.idb[1])
        # cycle.idb[2] should be None, "data", "alu"
        if cycle.idb[2] in ["alu"]:    c = alu
        elif cycle.idb[2] in ["data"]: c = data_in
        elif cycle.idb[2] in ["pcl"]:  c = self.pcl.get()
        elif cycle.idb[2] in ["pch"]:  c = self.pch.get()
        elif cycle.idb[2] is None: pass
        else: raise Exception("Bad idb[2] %s"%str(cycle.idb))
        return (a,b,c)
    #f check_condition
    def check_condition(self, instr_am_cycle):
        (instr, am, cycle) = instr_am_cycle
        condition = instr.condition
        if condition is None: return None
        return self.psr[condition[0]] == condition[1]
    #f check_skip_if
    def check_skip_if(self, instr_am_cycle, idb, alu):
        (instr, am, cycle) = instr_am_cycle
        skip_if = am.skip_if
        if skip_if is None: return None
        elif (skip_if[0]=="cc") :
            if (alu[3]==0): return skip_if[1]
            return None
        elif (skip_if[0]=="bcc"):
            if self.instr_cycle != skip_if[1]-1: return None
            if ((idb[1]&128)!=0) and (alu[3]==1): return skip_if[1]
            if ((idb[1]&128)==0) and (alu[3]==0): return skip_if[1]
            return None
        raise Exception("Unexpected skip_if")
    #f alu_logical
    def alu_logical(self, value, carry):
        value = value & 0xff
        zero = 0
        negative = 0
        if (value==0): zero = 1 
        if (value&0x80)!=0: negative=1
        overflow = self.psr["v"]
        return (value, zero, negative, carry, overflow)
    #f alu_add
    def alu_add(self, a, b, carry):
        carry_in = carry
        value = a+b + carry
        carry = 0
        zero = 0
        negative = 0
        overflow = 0
        if (value&0x100): carry = 1
        value = value &0xff
        if (value==0): zero = 1 
        if (value&0x80)!=0: negative=1
        if (a&0x80): a = - (256-(a&0xff))
        if (b&0x80): b = - (256-(b&0xff))
        value = a+b + carry_in
        if ((value<-128) or (value>127)): overflow=1
        value = value &0xff
        return (value, zero, negative, carry, overflow)
    #f alu_add_orig
    def alu_add_orig(self, a, b, carry):
        value = a+b + carry
        carry_in_to_bit_7 = (((a&0x7f)+(b&0x7f)+carry)>>7)&1
        carry = 0
        zero = 0
        negative = 0
        overflow = 0
        if (value>=256): carry = 1
        value = value &0xff
        if carry_in_to_bit_7 != carry: overflow=1
        if (value==0): zero = 1 
        if (value&0x80)!=0: negative=1
        return (value, zero, negative, carry, overflow)
    #f alu
    def alu(self, instr_am_cycle, idb, dl_bit_7):
        (instr, am, cycle) = instr_am_cycle
        shift_inc_op = None
        alu_op = None
        carry_in = self.psr["c"]
        if cycle.alu is not None:
            (alu_op, shift_inc_op) = cycle.alu
            carry_in = 0
            pass
        elif instr.alu is not None:
            (shift_inc_op, alu_op, carry_in) = instr.alu
            if carry_in is None: carry_in=self.psr["c"]
            pass
        if ((shift_inc_op is not None) or
            (alu_op is not None)):
            if idb is None: raise Exception("ALU/shift op is not None but IDB is None")
            if idb[0] is None: raise Exception("ALU/shift op is not None but IDB[0] is None")
            if idb[1] is None: raise Exception("ALU/shift op is not None but IDB[1] is None")
            pass
        if shift_inc_op == "incdec":
            shift_inc_op="inc"
            if dl_bit_7: shift_inc_op="dec"
            pass
        alu_a = idb[0]
        alu_b = idb[1]
        if alu_a is None: alu_a = 0xff
        if alu_b is None: alu_b = 0xff
        shift_carry = carry_in
        if shift_inc_op is None:
            pass
        elif shift_inc_op in ["inc"]:
            alu_b = (idb[1]+1)&0xff
            pass
        elif shift_inc_op in ["dec"]:
            alu_b = (idb[1]-1)&0xff
            pass
        elif shift_inc_op in ["lsr"]:
            shift_carry = idb[1]&1
            alu_b = idb[1]>>1
            pass
        elif shift_inc_op in ["ror"]:
            shift_carry = idb[1]&1
            alu_b = (idb[1]>>1) | (carry_in<<7)
            pass
        elif shift_inc_op in ["asl"]:
            shift_carry = (idb[1]>>7)&1
            alu_b = idb[1]<<1
            pass
        elif shift_inc_op in ["rol"]:
            shift_carry = (idb[1]>>7)&1
            alu_b = (idb[1]<<1) | (carry_in<<0)
            pass
        else:
            raise Exception("Unknown shift_inc_op %s"%(shift_inc_op))
        if alu_op is None:
            alu_result = self.alu_logical(alu_b, shift_carry)
            pass
        elif alu_op in ["src"]:
            alu_result = self.alu_logical(alu_a, shift_carry)
            pass
        elif alu_op in ["adc"]:
            alu_result = self.alu_add(alu_a, alu_b, carry_in)
            pass
        elif alu_op in ["add"]:
            alu_result = self.alu_add(alu_a, alu_b, 0)
            pass
        elif alu_op in ["sbc"]:
            alu_result = self.alu_add(alu_a, 0xff ^ alu_b, carry_in)
            pass
        elif alu_op in ["cmp"]:
            alu_result = self.alu_add(alu_a, 0xff ^ alu_b, carry_in)
            alu_result = (alu_result[0], alu_result[1], alu_result[2], alu_result[3], self.psr["v"])
            pass
        elif alu_op in ["and"]:
            alu_result = self.alu_logical(alu_a&alu_b, shift_carry)
            pass
        elif alu_op in ["or"]:
            alu_result = self.alu_logical(alu_a|alu_b, shift_carry)
            pass
        elif alu_op in ["eor"]:
            alu_result = self.alu_logical(alu_a^alu_b, shift_carry)
            pass
        elif alu_op in ["bit"]:
            alu_result = (alu_a, 0 or ((alu_b&alu_a)==0), 0 or ((alu_b&128)!=0), shift_carry, 0 or ((alu_b&64)!=0) )
            pass
        else:
            raise Exception("Unknown alu_op %s"%(alu_op))
        alu_result = tuple(list(alu_result)+[alu_b])
        #print shift_inc_op, alu_op, idb, "dl7", dl_bit_7, "ci", carry_in, "sc", shift_carry, self.psr, alu_result
        return alu_result
    #f get_instr_am_cycle
    def get_instr_am_cycle(self):
        if self.instr is None:
            raise Exception("No instruction in hand to find cycle from")
        (instr, am) = self.instr
        if am is None:
            raise Exception("Instruction %s has no addressing mode"%(str(self.instr)))
        return (instr, am, am.cycle(self.instr_cycle))
    #f get_memory_operation
    def get_memory_operation(self, instr_am_cycle, idb_out):
        (instr, am, cycle) = instr_am_cycle
        if cycle is None: return None
        mem = cycle.get_mem()
        if mem is None: return None
        mem = [mem[0], mem[1], mem[2]]
        if mem[1] in ["pcl"]:    mem[1] = self.pcl.get()
        elif mem[1] in ["adl"]:  mem[1] = self.adl.get()
        elif mem[1] in ["dl"]:   mem[1] = self.dl.get()
        elif mem[1] in ["sp"]:   mem[1] = self.sp.get()
        if mem[2] in ["pch"]:    mem[2] = self.pch.get()
        elif mem[2] in ["adh"]:  mem[2] = self.adh.get()
        elif mem[2] in ["dl"]:   mem[2] = self.dl.get()
        elif mem[2] in ["zero"]: mem[2] = 0
        elif mem[2] in ["one"]:  mem[2] = 1
        mem = [mem[0], (mem[1]&0xff) | ((mem[2]&0xff)<<8)]
        if mem[0] in ["write"]:
            mem.append(idb_out)
            pass
        return tuple(mem)
    #f sp_op
    def sp_op(self, sp_op, idb, alu):
        if sp_op in ["shift"]:
            self.sp.set(alu[5])
        else:
            raise Exception("Unimplemented SP op %s"%sp_op)
        pass
    #f pc_op
    def pc_op(self, pc_op, idb, alu):
        if pc_op in ["reset"]:
            self.pcl.set(0xfc)
            self.pch.set(0xff)
            pass
        elif pc_op in ["pc_dl_data"]:
            self.pcl.set(self.dl.get()) # From idb[1]?
            self.pch.set(idb[2]) 
            pass
        elif pc_op in ["pcl_data"]:
            self.pcl.set(idb[2])
            pass
        elif pc_op in ["pch_data"]:
            self.pch.set(idb[2])
            pass
        elif pc_op in ["inc"]:
            pcl_max = (self.pcl.get() == 0xff)
            pcl_carry = 0 or (1 and pcl_max)
            self.pcl.set((self.pcl.get()+1)&0xff)
            self.pch.set((self.pch.get()+pcl_carry)&0xff)
            pass
        else:
            raise Exception("Unimplemented PC op %s"%pc_op)
        pass
    #f dl_op
    def dl_op(self, dl_op, idb, alu):
        if dl_op in ["idb"]:
            self.dl.set(idb[2])
            pass
        else:
            raise Exception("Unimplemented DL op %s"%dl_op)
        pass
    #f adl_op
    def adl_op(self, adl_op, idb, alu):
        if adl_op in ["dl"]:
            self.adl.set(self.dl.get())
            pass
        elif adl_op in ["pcl"]:
            self.adl.set(self.pcl.get())
            pass
        elif adl_op in ["alu"]:
            self.adl.set(alu[0])
            pass
        else:
            raise Exception("Unimplemented ADL op %s"%adl_op)
        pass
    #f adh_op
    def adh_op(self, adh_op, idb, alu):
        if adh_op in ["dl"]:
            self.adh.set(self.dl.get())
            pass
        elif adh_op in ["pch"]:
            self.adh.set(self.pch.get())
            pass
        else:
            raise Exception("Unimplemented DL op %s"%dl_op)
        pass
    #f tick_start
    def tick_start(self):
        instr_am_cycle = self.get_instr_am_cycle()
        (instr, am, cycle) = instr_am_cycle
        idb = (None,None,None)
        if cycle is not None:
            idb = self.get_internal_data_bus(instr_am_cycle, alu=0, data_in=0)
            alu = self.alu(instr_am_cycle, idb, (self.dl.get()>>7)&1)
            idb = self.get_internal_data_bus(instr_am_cycle, alu=alu[0], data_in=0)
            pass
        mem = self.get_memory_operation(instr_am_cycle, idb[2])
        return {"instr":instr.mnemonic,"cycle":cycle,"mem":mem}
    #f tick_end
    def tick_end(self, reset=0, data_in=0, irq=0, nmi=0, rdy=1):
        instr_am_cycle = self.get_instr_am_cycle()
        (instr, am, cycle) = instr_am_cycle
        idb = self.get_internal_data_bus(instr_am_cycle, alu=0, data_in=data_in)
        alu = self.alu(instr_am_cycle, idb, (self.dl.get()>>7)&1)
        idb = self.get_internal_data_bus(instr_am_cycle, alu=alu[0], data_in=data_in)
        condition = self.check_condition(instr_am_cycle)
        skip_if = self.check_skip_if(instr_am_cycle, idb, alu)
        mem = self.get_memory_operation(instr_am_cycle, idb[2])
        if False:
            if cycle.adl is not None: self.adl_op(cycle.adl, idb, alu) # alu, dl, pcl
            if cycle.adh is not None: self.adh_op(cycle.adh, idb, alu) # dl, pch
            pass
        else:
            if mem is not None:
                new_adl = mem[1]&0xff
                new_adh = (mem[1]>>8)&0xff
                if cycle.adl is "dl":  new_adl = self.dl.get()
                if cycle.adl is "alu": new_adl = alu[0]
                self.adl.set(new_adl)
                self.adh.set(new_adh)
                pass
            if False:
                if cycle.adl is not None:
                    self.adl_op(cycle.adl, idb, alu) # alu, dl, pcl
                    if self.adl.get() != new_adl:
                        print am
                        print cycle
                        raise Exception("Mismatch in adl %02x %02x"%(self.adl.get(),new_adl))
                    pass
                if cycle.adh is not None:
                    self.adh_op(cycle.adh, idb, alu) # dl, pch
                    if self.adh.get() != new_adh:
                        raise Exception("Mismatch in adh %02x %02x"%(self.adh.get(),new_adh))
                    pass
                pass
            pass
        if cycle.pc is not None:  self.pc_op(cycle.pc, idb, alu) # inc, pc_dl_data (alu or dl?)
        if cycle.sp is not None:  self.sp_op(cycle.sp, idb, alu) # shift
        if cycle.dl is not None:  self.dl_op(cycle.dl, idb, alu) # idb
        if cycle.write_dest:
            dest = instr.dest
            if am.dest is not None:
                dest=am.dest # To allow for ASL A etc
            if dest in ["setclrflag"]:
                self.psr[instr.flag] = alu[0]&1
                pass
            elif instr.flag is not False:
                self.psr["z"] = alu[1]
                self.psr["n"] = alu[2]
                self.psr["c"] = alu[3]
                self.psr["v"] = alu[4]
                pass
            if dest in ["acc"]:  self.acc.set(idb[2])
            elif dest in ["x"]:  self.x.set(idb[2])
            elif dest in ["y"]:  self.y.set(idb[2])
            elif dest in ["sp"]: self.sp.set(idb[2])
            elif dest in ["cmp"]: pass
            elif dest in ["flags"]: # for PLP or CLC, CLD, CLV, CLI, SEC, SED, SEI (and RTI?)
                self.psr["n"] = (idb[2]>>7)&1
                self.psr["v"] = (idb[2]>>6)&1
                self.psr["b"] = (idb[2]>>4)&1
                self.psr["d"] = (idb[2]>>3)&1
                self.psr["i"] = (idb[2]>>2)&1
                self.psr["z"] = (idb[2]>>1)&1
                self.psr["c"] = (idb[2]>>0)&1
                pass
            elif dest in ["setclrflag"]:
                pass
            elif dest is None: # Used for RW ops
                pass
            else: raise Exception("Bad dest %s at writing"%dest)
            pass
        if not cycle.last:
            if (condition is not None) and (not condition) and (self.instr_cycle==0):
                self.instr_cycle = am.condition_fail
                pass
            else:
                self.instr_cycle += 1
                if (skip_if is not None) and (skip_if==self.instr_cycle):
                    self.instr_cycle += 1
                    pass
                pass
            pass
        else:
            self.instr_cycle = 0
            self.ir.set(data_in)
            #print ">> %04x : %02x"%((self.pcl.get()|(self.pch.get()<<8))-1, self.ir.get())
            self.instr = self.instruction_set.decode(data_in)
            pass
        return idb, alu
    #f __str__
    def __str__(self):
        r = ""
        r += str(self.acc)+"\n"
        r += str(self.pcl)+"\n"
        r += str(self.pch)+"\n"
        r += str(self.x)+"\n"
        r += str(self.y)+"\n"
        r += str(self.dl)+"\n"
        r += str(self.adl)+"\n"
        r += str(self.adh)+"\n"
        r += str(self.sp)+"\n"
        r += str(self.ir)+"\n"
        r += str(self.psr)+"\n"
        return r


#a Tests
#c Test6502_Internal
class Test6502_Internal(unittest.TestCase):
    alu_test_data = [0,1,2,3,4,6,8,12,15,16,17,31,32,33,63,64,65,127,128,129,254,255]
    #alu_test_data = range(129)
    def check_alu_add(self, a, b, c, alu_r):
        (alu_sum, alu_z, alu_n, alu_c, alu_v) = alu_r
        r = " %02x %02x %d :  %03x %d %d %d %d"%(a,b,c,alu_sum, alu_z, alu_n, alu_c, alu_v)
        value = a + b + c
        self.assertEqual(value&0xff,alu_sum,"Mismatch on sum in alu op"+r)
        self.assertEqual((value>>7)&1,alu_n,"Mismatch on negative flag in alu op"+r)
        self.assertEqual((value>>8)&1,alu_c,"Mismatch on carry in alu op"+r)
        z = 0
        if (value&0xff)==0: z=1
        self.assertEqual(z,alu_z,"Mismatch on zero in alu op"+r)
        if a>=128: a=-256+a
        if b>=128: b=-256+b
        value = a + b + c
        if (a>=0) and (b>=0) and alu_n: self.assertEqual(1,alu_v,"Check that V set if both A and B non-negative and result is negative failed"+r)
        elif (a<0) and (b<0) and (not alu_n): self.assertEqual(1,alu_v,"Check that V set if both A and B negative and result is non-negative failed"+r)
        else:
            if (alu_v!=0): print "Check that V clear 'otherwise' failed"+r
            #self.assertEqual(0,alu_v,"Check that V clear 'otherwise' failed"+r)
            pass
        if value>=128:
            self.assertEqual(1,alu_v,"Mismatch on overflow when a and b are both positive without overflow"+r)
        elif value<-128:
            self.assertEqual(1,alu_v,"Mismatch on overflow when a and b are both negative without overflow"+r)
        else:
            self.assertEqual(0,alu_v,"Mismatch on overflow when a and b are both negative with overflow"+r)
        pass
    def test_alu_add(self):
        cpu = c_6502()
        for a in self.alu_test_data:
            for b in self.alu_test_data:
                for carry_in in (0,1):
                    alu_r = cpu.alu_add(a,b,carry_in)
                    self.check_alu_add(a,b,carry_in,alu_r)
                    alu_r = cpu.alu_add(a^0xff,b,carry_in)
                    self.check_alu_add(a^0xff,b,carry_in,alu_r)
                    alu_r = cpu.alu_add(a^0xff,b^0xff,carry_in)
                    self.check_alu_add(a^0xff,b^0xff,carry_in,alu_r)
                    pass
                pass
            pass
        pass
#a Toplevel
if __name__=="__main__":
    unittest.main()
