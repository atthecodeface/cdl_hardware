#a Imports
import re
import sys, inspect

#a Instruction cycle decodes
#c c65id_cycle - base class
class c65id_cycle(object):
    alu = None
    mem = None
    pc =  None
    sp = None
    idb = None
    dl  = None # Store what in DL?
    adl = None
    write_dest = False # Default, do not write acc/x/y etc
    #f get_mem
    @classmethod
    def get_mem(cls):
        """Return None if no memory transaction, or a 3-tuple otherwise
        A 3-tuple is ("read" or "write", address source low, address source high)
        Data from a write comes from the idb output.
        Address source low is one of 'pcl', 'dl', 'adl'
        Address source high is one of 'pch', 'dl', 'adh', 'zero'
        """
        if cls.mem is None:
            return None
        return (cls.mem[0], cls.mem[1], cls.mem[2])
    
    last = False
    pass

#c c65id_cycle_dl_inc - Increment dl - possibly could be done with ADL incrementer? Or the ALU incrementer probably (or is that DL increment)
class c65id_cycle_dl_inc(c65id_cycle):
    alu = (None, "inc")
    idb = ("zero", "dl", "alu")
    dl  = "idb"

#c c65id_cycle_pc_reset - Reset PC to 0xfffc
class c65id_cycle_pc_reset(c65id_cycle):
    pc =  "reset"

#c c65id_cycle_read_pch_keep_in_pcl - Read from PC, store in DL, keep old DL in PCL
class c65id_cycle_read_pch_keep_in_pcl(c65id_cycle):
    mem = ("read","pcl","pch",None)
    idb = (None, None, "data")
    dl  = "idb"
    pc  = "pc_dl_data"

#c c65id_cycle_read_dl_inc_pc - Read from PC, increment PC, store in DL
class c65id_cycle_read_dl_inc_pc(c65id_cycle):
    mem = ("read","pcl","pch",None)
    pc =  "inc"
    idb = (None, None, "data")
    dl  = "idb"

#c c65id_cycle_read_dl_hold_pc - Read from PC, store in DL
class c65id_cycle_read_dl_hold_pc(c65id_cycle):
    mem = ("read","pcl","pch",None)
    idb = (None, None, "data")
    dl  = "idb"

#c c65id_cycle_read_dl_keep_in_adl - Read from PC, increment PC, store in DL, keep old DL in ADL
class c65id_cycle_read_dl_keep_in_adl(c65id_cycle):
    mem = ("read","pcl","pch",None)
    pc =  "inc"
    alu = ("add", None)
    idb = ("zero", "dl", "data")
    adl = "alu"
    dl  = "idb"

#c c65id_cycle_read_dl_add_index_to_adl - Read from PC, increment PC, store in DL, add index to old DL and put in ADL
class c65id_cycle_read_dl_add_index_to_adl(c65id_cycle):
    mem = ("read","pcl","pch",None)
    pc =  "inc"
    alu = ("add", None)
    idb = ("index", "dl", "data")
    adl = "alu"
    dl  = "idb"

#c c65id_cycle_read_zero_dl - Read from (0,DL), store in DL
class c65id_cycle_read_zero_dl(c65id_cycle):
    """ Read from (0,DL) in to DL, don't touch PC"""
    mem = ("read","dl","zero",None)
    alu = ("add", None)
    idb = ("zero", "dl", "data")
    dl  = "idb"

#c c65id_cycle_read_zero_dl_inc_adl - Read from (0,DL) into DL, ADL <= old DL+1
class c65id_cycle_read_zero_dl_inc_adl(c65id_cycle):
    mem = ("read","dl","zero",None)
    alu = (None, "inc")
    idb = ("zero", "dl", "data")
    adl = "alu"
    dl  = "idb"

#c c65id_cycle_read_zero_adl_keep_in_adl - Read from (0,ADL) into DL, ADL <= DL
class c65id_cycle_read_zero_adl_keep_in_adl(c65id_cycle):
    mem = ("read","adl","zero",None)
    alu = ("add", None)
    idb = ("zero", "dl", "data")
    adl = "alu"
    dl  = "idb"

#c c65id_cycle_read_zero_dl_keep_in_adl - Read from (0,DL) into DL, ADL <= DL
class c65id_cycle_read_zero_dl_keep_in_adl(c65id_cycle):
    mem = ("read","dl","zero",None)
    idb = (None, None, "data")
    dl  = "idb"

#c c65id_cycle_read_zero_adl_calc_adl_index - Read from (0,ADL) into DL, ADL <= DL + index
class c65id_cycle_read_zero_adl_calc_adl_index(c65id_cycle):
    mem = ("read","adl","zero",None)
    idb = ("index", "dl", "data")
    alu = ("add", None)
    adl = "alu"
    dl  = "idb"

#c c65id_cycle_read_dl_adl - Read from (DL, ADL), store in DL
class c65id_cycle_read_dl_adl(c65id_cycle):
    """ Read from (DL, ADL) in to DL, don't touch PC"""
    mem = ("read","adl","dl",None)
    idb = (None, None, "data")
    dl  = "idb"

#c c65id_cycle_read_dl_adl_keep_in_adh - Read from (DL, ADL), store in DL, keep DL in ADH
class c65id_cycle_read_dl_adl_keep_in_adh(c65id_cycle):
    """ Read from (DL, ADL) in to DL, keeping DL in ADH, don't touch PC"""
    mem = ("read","adl","dl",None)
    idb = (None, None, "data")
    dl  = "idb"

#c c65id_cycle_read_sp - Read (1, SP) to DL
class c65id_cycle_read_sp(c65id_cycle):
    """Read from (1, SP) to DL, don't increment sp, don't touch PC"""
    mem = ("read","sp","one", None)
    alu = (None, "inc")
    idb = (None, "sp", "data")
    dl  = "idb"
    pass

#c c65id_cycle_read_sp_inc_sp - Read (1, SP) to DL
class c65id_cycle_read_sp_inc_sp(c65id_cycle):
    """Read from (1, SP) to DL, don't increment sp, don't touch PC"""
    mem = ("read","sp","one", None)
    alu = (None, "inc")
    idb = (None, "sp", "data")
    sp = "shift"
    dl  = "idb"
    pass

#c c65id_cycle_read_sp_to_pch_keep_pcl - Read (1, SP) to DL
class c65id_cycle_read_sp_to_pch_keep_pcl(c65id_cycle):
    """Read from (1, SP) to PCH, PCL<=DL, don't increment sp"""
    mem = ("read","sp","one", None)
    alu = (None, "inc")
    idb = (None, "sp", "data")
    pc  = "pc_dl_data"
    dl  = "idb"
    pass

#c c65id_cycle_inc_sp - Increment SP
class c65id_cycle_inc_sp(c65id_cycle):
    """Increment sp, don't touch PC"""
    alu = (None, "inc")
    sp = "shift"
    idb = (None, "sp", None)
    pass

#c c65id_cycle_write_zero_adl - Write DL to (0,ADL)
class c65id_cycle_write_zero_adl(c65id_cycle):
    """ Write to (0,ADL) with data from dl, don't touch PC"""
    mem = ("write","adl","zero","idb")
    alu = (None, None)
    idb = ("src", "dl", "alu")
    pass

#c c65id_cycle_write_zero_dl - Read from (0,DL), store in DL
class c65id_cycle_write_zero_dl(c65id_cycle):
    """ Write to (0,DL) with data from src, don't touch PC"""
    mem = ("write","dl","zero","idb")
    alu = ("src", None)
    idb = ("src", None, "alu")
    pass

#c c65id_cycle_write_adh_adl - Write DL to (ADH,ADL)
class c65id_cycle_write_adh_adl(c65id_cycle):
    """ Write to (ADH,ADL) with data from dl, don't touch PC"""
    mem = ("write","adl","adh","idb")
    #idb = (None, "dl", "alu")
    alu = (None, None)
    idb = ("src", "dl", "alu")
    pass

#c c65id_cycle_write_dl_adl - Write src to (DL, ADL)
class c65id_cycle_write_dl_adl(c65id_cycle):
    """ Write to (DL, ADL) with data from src, don't touch PC"""
    mem = ("write","adl","dl", "idb")
    alu = ("src", None)
    idb = ("src", None, "alu")
    pass

#c c65id_cycle_push_src - Write src to (1, SP), decrement sp
class c65id_cycle_push_src(c65id_cycle):
    """ Write to (1, SP) with data from src, decrement sp, don't touch PC"""
    mem = ("write","sp","one", "idb")
    alu = ("src", "dec")
    sp = "shift"
    idb = ("src", "sp", "alu")
    pass

#c c65id_cycle_push_pcl - Write src to (1, SP), decrement sp
class c65id_cycle_push_pcl(c65id_cycle):
    """ Write to (1, SP) with data from src, decrement sp, don't touch PC"""
    mem = ("write","sp","one", "idb")
    alu = (None, "dec")
    sp = "shift"
    idb = (None, "sp", "pcl")
    pass

#c c65id_cycle_push_pch - Write src to (1, SP), decrement sp
class c65id_cycle_push_pch(c65id_cycle):
    """ Write to (1, SP) with data from src, decrement sp, don't touch PC"""
    mem = ("write","sp","one", "idb")
    alu = (None, "dec")
    sp = "shift"
    idb = (None, "sp", "pch")
    pass

#c c65id_cycle_calc_dl_index - Calculate DL + index (x or y), don't touch PC
class c65id_cycle_calc_dl_index(c65id_cycle):
    alu = ("add", None)
    idb = ("index", "dl", "alu")
    dl  = "idb"

#c c65id_cycle_dl_alu - Perform ALU operation (src op dl) and store in dl, keep old DL in ADL
class c65id_cycle_dl_alu(c65id_cycle):
    idb = ("src", "dl", "alu")
    dl  = "idb"
    write_dest = True

#c c65id_cycle_bcc_pcl - Pcl += dl (if carry and dl[7] OR no carry and !dl[7] then skip next) (MUST store PCL); don't touch dl
class c65id_cycle_bcc_pcl(c65id_cycle):
    alu = ("add", None)
    idb = ("pcl", "dl", "alu")
    pc  = "pcl_data"

#c c65id_cycle_bcc_pch - Pch ++ (dl[7]==0) or -- (dl[7]==1) (MUST store PCH)
class c65id_cycle_bcc_pch(c65id_cycle):
    alu = (None, "incdec")
    idb = (None, "pch", "alu")
    pc  = "pch_data"

#c c65id_cycle_fetch_next - Read PC, increment PC, last cycle of instruction
class c65id_cycle_fetch_next(c65id_cycle):
    mem = ("read","pcl","pch",None)
    pc =   "inc"
    last = True # Forces store of IR (if not taking interrupt...)
    alu = (None,None)
    pass

#c c65id_cycle_complete_alu_src_dl - Complete ALU (and read PC, increment PC, last cycle of instruction)
class c65id_cycle_complete_alu_src_dl(c65id_cycle_fetch_next):
    idb = ("src", "dl", "alu")
    write_dest = True
    alu = None # No special ALU for the cycle
    pass

#c c65id_cycle_complete_alu_src_src - Complete ALU (and read PC, increment PC, last cycle of instruction)
class c65id_cycle_complete_alu_src_src(c65id_cycle_fetch_next):
    idb = ("src", "src", "alu")
    write_dest = True
    alu = None # No special ALU for the cycle
    pass

#a Instruction addressing mode classes - instructions are subclass of these, and these consist of lists of cycles
#c c_6502_addressing_mode
class c_6502_addressing_mode(object):
    index = "x"
    assembler_re = None
    assembler_res = {"imp":"^$",
                     "a":"^[aA]$",
                     "imm":"^# *(.*)$",
                     "zp":"^([^(#,]*)$",
                     "abs":"^([^(#,]*)$",
                     "zx":"^([^(#]*) *, *[xX]$", # this will match abs,x too
                     "zy":"^([^(#]*) *, *[yY]$", # this will match abs,y too
                     "absx":"^([^(#]*) *, *[xX]$", # this will match zp,x too
                     "absy":"^([^(#]*) *, *[yY]$", # this will match zp,y too
                     "indx":"^\((.*) *, *[xX] *\)$",
                     "indy":"^\((.*)\) *, *[yY]$",
                     "ind":"^\((.*)\)$",
                     }
    bytes = None
    operand_relative = False
    skip_if = None
    dest = None # Usually this is in the instr, but for ASL A etc this is 'acc' to take precedence over other ams
    @classmethod
    def cycle(cls, n):
        if (n<0) or (n>=len(cls.cycles)):
            return None
        return cls.cycles[n]
    @classmethod
    def op(cls, cpu, instr):
        raise Exception("Unimplemented addressing mode operation")

#c c65am_reset - Reset - effectively a JMPI(0xfffc)
class c65am_reset(c_6502_addressing_mode):
    """
    Reset is a bit of a hack - not trying to be compatible with 6502 (yet)
    0 - Set pcl/pch to fffc
    1 - read (pc) to dl, pc+1,
    2 - read (pc) to dl, pcl <= dl
    3 - read (adl,adh) to dl, pch <= dl
    5 - fetch next - read (pc), pc+1, IR <= data
    """
    cycles = ( c65id_cycle_pc_reset,
               c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_pch_keep_in_pcl,
               c65id_cycle_fetch_next )
    @classmethod
    def op(cls, cpu, instr):
        pc = cpu.read(0xfffc)
        pc = pc | cpu.read(0xfffd)
        cpu.set({"pc":pc})
        pass
    pass

#c c65am_acc - Accumulator addressing mode A = op A
class c65am_acc(c_6502_addressing_mode):
    """
    Immediates have 2 cycles:
    0 - read to dl   - read (pc), DL <= data
    1 - repeat fetch - read (pc), IR <= data, A <= ALU op A
    """
    dest = "acc"
    assembler_re = c_6502_addressing_mode.assembler_res["a"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_complete_alu_src_src )
    pass

#c c65am_imm - Immediate addressing mode <dest> = <dest> op #imm
class c65am_imm(c_6502_addressing_mode):
    """
    Immediates have 2 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - complete ALU - read (pc), pc+1, IR <= data, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imm"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_zp_in - Zero page op/load addressing mode <dest> = <dest> op mem[zero page]
class c65am_zp_in(c_6502_addressing_mode):
    """
    Zero page in have 3 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - read (0,DL), DL <= data
    2 - complete ALU - read (pc), pc+1, IR <= data, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["zp"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_zero_dl,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_zp_out - Zero page store addressing mode mem[zero page] = <src>
class c65am_zp_out(c_6502_addressing_mode):
    """
    Zero page store have 3 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - write (0,DL,src)
    2 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["zp"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_write_zero_dl,
               c65id_cycle_fetch_next )
    pass

#c c65am_zp_rw - Zero page load+op+store addressing mode mem[zero page] = op mem[zero page] (e.g. inc/dec)
class c65am_zp_rw(c_6502_addressing_mode):
    """
    Zero page rw have 5 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - read (0,DL), DL <= data, ADL <= dl
    2 - DL <=  ALU
    3 - write (0,ADL,dl)
    4 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["zp"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_zero_dl_keep_in_adl,
               c65id_cycle_dl_alu,
               c65id_cycle_write_zero_adl,
               c65id_cycle_fetch_next )
    pass

#c c65am_zx_in - Zero page + index op/load addressing mode <dest> = <dest> op mem[zero page+index]
class c65am_zx_in(c_6502_addressing_mode):
    """
    Zero page indexed by X have 4 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - calculate dl + index - DL <= index + DL
    2 - read (0,DL), DL <= data
    3 - complete ALU - read (pc), pc+1, IR <= data, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["zx"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_calc_dl_index,
               c65id_cycle_read_zero_dl,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_zx_out - Zero page + index store addressing mode mem[zero page+index] = <src>
class c65am_zx_out(c_6502_addressing_mode):
    """
    Zero page indexed by X have 4 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - calculate dl + index - DL <= index + DL
    2 - write (0,DL,src)
    3 - fetch next
    """
    assembler_re = c_6502_addressing_mode.assembler_res["zx"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_calc_dl_index,
               c65id_cycle_write_zero_dl,
               c65id_cycle_fetch_next )
    pass

#c c65am_zx_rw - Zero page + index load+op+store addressing mode mem[zero page+index] = op mem[zero page+index] (e.g. inc/dec)
class c65am_zx_rw(c_6502_addressing_mode):
    """
    Zero page indexed by X have 4 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - calculate dl + index - DL <= index + DL
    1 - read (0,DL), DL <= data, ADL <= dl
    2 - DL <=  ALU
    3 - write (0,ADL,dl)
    4 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["zx"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_calc_dl_index,
               c65id_cycle_read_zero_dl_keep_in_adl,
               c65id_cycle_dl_alu,
               c65id_cycle_write_zero_adl,
               c65id_cycle_fetch_next )
    pass

#c c65am_zy_in - Absolute + index op/load addressing mode <dest> = <dest> op  mem[address+index]
class c65am_zy_in(c65am_zx_in):
    index="y"
    assembler_re = c_6502_addressing_mode.assembler_res["zy"]

#c c65am_zy_out- Absolute + index op/load addressing mode <dest> = <dest> op  mem[address+index]
class c65am_zy_out(c65am_zx_out):
    index="y"
    assembler_re = c_6502_addressing_mode.assembler_res["zy"]

#c c65am_abs_in - Absolute op/load addressing mode <dest> = <dest> op mem[address]
class c65am_abs_in(c_6502_addressing_mode):
    """
    Absolute in have 3 cycles:
    0 - read, DL <= data
    1 - read, ADL<=DL, DL <= data
    2 - read (DL,ADL), DL <= data
    3 - fetch next, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["abs"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_dl_keep_in_adl,
               c65id_cycle_read_dl_adl,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_abs_out - Absolute store addressing mode mem[address] = <src>
class c65am_abs_out(c_6502_addressing_mode):
    """
    Absolute in have 3 cycles:
    0 - read, DL <= data
    1 - read, ADL<=DL, DL <= data
    2 - write (DL,ADL,src)
    3 - fetch next
    """
    assembler_re = c_6502_addressing_mode.assembler_res["abs"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_dl_keep_in_adl,
               c65id_cycle_write_dl_adl,
               c65id_cycle_fetch_next )
    pass

#c c65am_abs_rw - Absolute load+op+store addressing mode mem[address] = op mem[address] (e.g. inc/dec)
class c65am_abs_rw(c_6502_addressing_mode):
    """
    Absolute rw have 3 cycles:
    0 - read, DL <= data
    1 - read, ADL<=DL, DL <= data
    2 - read (DL,ADL), DL <= data, ADH <= DL
    3 - DL <=  ALU
    4 - write (ADH,ADL,src)
    5 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["abs"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_dl_keep_in_adl,
               c65id_cycle_read_dl_adl_keep_in_adh,
               c65id_cycle_dl_alu,
               c65id_cycle_write_adh_adl,
               c65id_cycle_fetch_next )
    pass

#c c65am_absx_in - Absolute + index op/load addressing mode <dest> = <dest> op  mem[address+index]
class c65am_absx_in(c_6502_addressing_mode):
    """
    Absolute + index in have 4/5 cycles:
    0 - read, DL <= data
    1 - read, ADL<=DL+index, DL <= data (CC -> skip 2)
    2 - DL <= DL+1
    3 - read (DL,ADL), DL <= data
    4 - fetch next, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["absx"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_dl_add_index_to_adl,
               c65id_cycle_dl_inc,
               c65id_cycle_read_dl_adl,
               c65id_cycle_complete_alu_src_dl )
    skip_if = ("cc", 2)
    pass

#c c65am_absx_out - Absolute + index store addressing mode mem[address+index] = <src>
class c65am_absx_out(c_6502_addressing_mode):
    """
    Absolute + index out have 4/5 cycles:
    0 - read, DL <= data
    1 - read, ADL<=DL+index, DL <= data (CC -> skip 2)
    2 - DL <= DL+1
    3 - write (DL,ADL,src)
    4 - fetch next
    """
    assembler_re = c_6502_addressing_mode.assembler_res["absx"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_dl_add_index_to_adl,
               c65id_cycle_dl_inc,
               c65id_cycle_write_dl_adl,
               c65id_cycle_fetch_next )
    skip_if = ("cc", 2)
    pass

#c c65am_absx_rw - Absolute + index load+op+store addressing mode mem[address+index] = op mem[address+index] (e.g. inc/dec)
class c65am_absx_rw(c_6502_addressing_mode):
    """
    Absolute + index in have 4/5 cycles:
    0 - read, DL <= data
    1 - read, ADL<=DL+index, DL <= data (CC -> skip 2)
    2 - DL <= DL+1
    3 - read (DL,ADL), DL <= data, ADH <= DL
    4 - DL <=  ALU
    5 - write (ADH,ADL,src)
    6 - fetch next
    """
    assembler_re = c_6502_addressing_mode.assembler_res["absx"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_dl_add_index_to_adl,
               c65id_cycle_dl_inc,
               c65id_cycle_read_dl_adl_keep_in_adh,
               c65id_cycle_dl_alu,
               c65id_cycle_write_adh_adl,
               c65id_cycle_fetch_next )
    skip_if = ("cc", 2)
    pass

#c c65am_absy_in - Absolute + index op/load addressing mode <dest> = <dest> op  mem[address+index]
class c65am_absy_in(c65am_absx_in):
    index="y"
    assembler_re = c_6502_addressing_mode.assembler_res["absy"]

#c c65am_absy_out - Absolute + index op/load addressing mode <dest> = <dest> op  mem[address+index]
class c65am_absy_out(c65am_absx_out):
    index="y"
    assembler_re = c_6502_addressing_mode.assembler_res["absy"]

#c c65am_indx_in - Indirect + X op/load addressing mode <dest> = <dest> op  mem[mem[zero_page+index]]
class c65am_indx_in(c_6502_addressing_mode):
    """
    Indirect + index in have 6 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - calculate dl + index - DL <= index + DL
    2 - read zero,dl and inc dl into adl
    3 - read zero,adl into dl, adl <= dl
    4 - read (DL,ADL), DL <= data
    5 - fetch next, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["indx"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_calc_dl_index,
               c65id_cycle_read_zero_dl_inc_adl,
               c65id_cycle_read_zero_adl_keep_in_adl,
               c65id_cycle_read_dl_adl,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_indx_out - Indirect + X store addressing mode mem[mem[zero_page+index]] = <src>
class c65am_indx_out(c_6502_addressing_mode):
    """
    Indirect + index in have 6 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - calculate dl + index - DL <= index + DL
    2 - read zero,dl and inc dl into adl
    3 - read zero,adl into dl, adl <= dl
    4 - read (DL,ADL), DL <= data
    5 - fetch next, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["indx"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_calc_dl_index,
               c65id_cycle_read_zero_dl_inc_adl,
               c65id_cycle_read_zero_adl_keep_in_adl,
               c65id_cycle_write_dl_adl,
               c65id_cycle_fetch_next )
    pass

#c c65am_indx_rw - Indirect + X load+op+store addressing mode mem[mem[zero_page+index]] = op mem[mem[zero_page+index]] (e.g. inc/dec)
class c65am_indx_rw(c_6502_addressing_mode):
    """
    Indirect + index in have 8 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - calculate dl + index - DL <= index + DL
    2 - read zero,dl and inc dl into adl
    3 - read zero,adl into dl, adl <= dl
    4 - read (DL,ADL), DL <= data, ADH <= DL
    5 - DL <=  ALU
    6 - write (ADH,ADL,src)
    7 - fetch next
    """
    assembler_re = c_6502_addressing_mode.assembler_res["indx"]
    bytes = 2
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_calc_dl_index,
               c65id_cycle_read_zero_dl_inc_adl,
               c65id_cycle_read_zero_adl_keep_in_adl,
               c65id_cycle_read_dl_adl_keep_in_adh,
               c65id_cycle_dl_alu,
               c65id_cycle_write_adh_adl,
               c65id_cycle_fetch_next )
    pass

#c c65am_indy_in - Indirect + Y op/load addressing mode <dest> = <dest> op  mem[mem[zero_page]+index]
class c65am_indy_in(c_6502_addressing_mode):
    """
    Indirect + index in have 5/6 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - read zero,dl and inc dl into adl
    2 - read zero,adl into dl, adl <= dl + index, skip 3 if cc
    3 - DL <= DL+1
    4 - read (DL,ADL), DL <= data
    5 - fetch next, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["indy"]
    bytes = 2
    index="y"
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_zero_dl_inc_adl,
               c65id_cycle_read_zero_adl_calc_adl_index,
               c65id_cycle_dl_inc,
               c65id_cycle_read_dl_adl,
               c65id_cycle_complete_alu_src_dl )
    skip_if = ("cc", 3)
    pass

#c c65am_indy_out - Indirect + Y store addressing mode mem[mem[zero_page]+index] = <src>
class c65am_indy_out(c_6502_addressing_mode):
    """
    Indirect + index in have 5/6 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - read zero,dl and inc dl into adl
    2 - read zero,adl into dl, adl <= dl + index, skip 3 if cc
    3 - DL <= DL+1
    4 - read (DL,ADL), DL <= data
    5 - fetch next, dest <= ALU op A/X/Y, DL
    """
    assembler_re = c_6502_addressing_mode.assembler_res["indy"]
    bytes = 2
    index="y"
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_zero_dl_inc_adl,
               c65id_cycle_read_zero_adl_calc_adl_index,
               c65id_cycle_dl_inc,
               c65id_cycle_write_dl_adl,
               c65id_cycle_fetch_next )
    skip_if = ("cc", 3)
    pass

#c c65am_indy_rw - Indirect + Y load+op+store addressing mode mem[mem[zero_page]+index] = op mem[mem[zero_page]+index] (e.g. inc/dec)
class c65am_indy_rw(c_6502_addressing_mode):
    """
    Indirect + index in have 7/8 cycles:
    0 - read to dl   - read (pc), pc+1, DL <= data
    1 - read zero,dl and inc dl into adl
    2 - read zero,adl into dl, adl <= dl + index, skip 3 if cc
    3 - DL <= DL+1
    4 - read (DL,ADL), DL <= data, ADH <= DL
    5 - DL <=  ALU
    6 - write (ADH,ADL,src)
    7 - fetch next
    """
    assembler_re = c_6502_addressing_mode.assembler_res["indy"]
    bytes = 2
    index="y"
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_zero_dl_inc_adl,
               c65id_cycle_read_zero_adl_calc_adl_index,
               c65id_cycle_dl_inc,
               c65id_cycle_read_dl_adl_keep_in_adh,
               c65id_cycle_dl_alu,
               c65id_cycle_write_adh_adl,
               c65id_cycle_fetch_next )
    skip_if = ("cc", 3)
    pass

#c c65am_abs_jmp - Absolute jump
class c65am_abs_jmp(c_6502_addressing_mode):
    """
    Jump
    0 - read (pc) to dl, pc+1,
    1 - read (pc) to pch, pcl <= dl
    3 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["abs"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_pch_keep_in_pcl,
               c65id_cycle_fetch_next )
    pass

#c c65am_ind_jmp - Indirect jump
class c65am_ind_jmp(c_6502_addressing_mode):
    """
    Jump indirect 
    0 - read (pc) to dl, pc+1,
    1 - read (pc) to pch, pcl <= dl
    3 - read (pc) to dl, pc+1,
    4 - read (pc) to pch, pcl <= dl
    5 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["ind"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_pch_keep_in_pcl,
               c65id_cycle_read_dl_inc_pc,
               c65id_cycle_read_pch_keep_in_pcl,
               c65id_cycle_fetch_next )
    pass

#c c65am_abs_jsr - Absolute jump to subroutine
class c65am_abs_jsr(c_6502_addressing_mode):
    """
    Jump to subroutine
    0 - read (pc) to dl, pc+1
    1 - write pcl to (stack,sp), sp-=1
    2 - write pch to (stack,sp), sp-=1
    3 - read (pc) to pch, pcl <= dl
    4 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["abs"]
    bytes = 3
    cycles = ( c65id_cycle_read_dl_inc_pc, # Inc PC so that we push PC+2
               c65id_cycle_push_pch,
               c65id_cycle_push_pcl,
               c65id_cycle_read_pch_keep_in_pcl,
               c65id_cycle_fetch_next )
    pass

#c c65am_bcc - Conditional branch
class c65am_bcc(c_6502_addressing_mode):
    """
    Conditional branch
    0 - read (pc) to dl, pc+1; if condition code fails, become simple implied no effect?
    1 - read (pc), pcl += dl, skip 2 if cc (+ve) or cs (-vs)
    2 - read (?), pch += 0
    3 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["abs"]
    bytes = 2
    operand_relative = True
    cycles = ( c65id_cycle_read_dl_inc_pc,
               c65id_cycle_bcc_pcl,
               c65id_cycle_bcc_pch,
               c65id_cycle_fetch_next )
    condition_fail = 3
    skip_if = ("bcc", 2)
    pass

#c c65am_imp_rts - RTS - implied
class c65am_imp_rts(c_6502_addressing_mode):
    """
    RTS has 6 cycles
    0 - read next
    1 - inc sp
    1 - read (1, sp) to dl, sp++
    2 - read (1, sp) to pch, pcl <= dl
    3 - fetch ignore - read (pc), pc+1
    4 - fetch next - read (pc), pc+1, IR <= data
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imp"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_inc_sp,
               c65id_cycle_read_sp_inc_sp,
               c65id_cycle_read_sp_to_pch_keep_pcl,
               c65id_cycle_read_dl_inc_pc, # Inc PC so that we move to JSR PC +3
               c65id_cycle_fetch_next )
    pass

#c c65am_imp_flag - CLC, SEC, CLV, CLD, SRD, CLI, SEI
class c65am_imp_flag(c_6502_addressing_mode):
    """
    implicit flag
    0 - read next, 
    1 - fetch repeat - read (pc), pc, IR <= data, complete flag
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imp"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_imp_transfer - TAX, TXA, TSX, TXS, TAY, TYA
class c65am_imp_transfer(c_6502_addressing_mode):
    """
    implicit transfer
    0 - read next, 
    1 - fetch repeat - read (pc), pc, IR <= data, complete flag
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imp"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_complete_alu_src_dl )
    pass

#c c65am_imp_incdec - INX, DEX, INY, DEY
class c65am_imp_incdec(c_6502_addressing_mode):
    """
    implicit transfer
    0 - read next, 
    1 - fetch repeat - read (pc), pc, IR <= data, complete flag
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imp"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_complete_alu_src_src )
    pass

#c c65am_imp_push - PHA, PHP
class c65am_imp_push(c_6502_addressing_mode):
    """
    implicit transfer
    0 - read next
    1 - push (1,sp,src)
    2 - fetch repeat - read (pc), pc, IR <= data, complete flag
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imp"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_push_src,
               c65id_cycle_fetch_next )
    pass

#c c65am_imp_pull - PLA, PLP
class c65am_imp_pull(c_6502_addressing_mode):
    """
    implicit transfer
    0 - read next
    1 - sp <= sp+1
    2 - dl <= read (1,sp)
    3 - fetch repeat - read (pc), pc, IR <= data, complete flag (dest <= dl)
    """
    assembler_re = c_6502_addressing_mode.assembler_res["imp"]
    bytes = 1
    cycles = ( c65id_cycle_read_dl_hold_pc,
               c65id_cycle_inc_sp,
               c65id_cycle_read_sp,
               c65id_cycle_complete_alu_src_dl )
    pass

#a Instructions
#c c_instruction
class c_instruction(object):
    ops_and_srcs = {}
    alu = None
    mem = None
    src = "acc"
    flag = None
    dest = None
    mnemonic = None
    condition = None
    pass

#c c65i_ora
class c65i_ora(c_instruction):
    mnemonic = "ora"
    alu = (None, "or", None)
    dest = "acc"
    pass

#c c65i_and
class c65i_and(c_instruction):
    mnemonic = "and"
    alu = (None, "and", None)
    dest = "acc"
    pass

#c c65i_eor
class c65i_eor(c_instruction):
    mnemonic = "eor"
    alu = (None, "eor", None)
    dest = "acc"
    pass

#c c65i_adc
class c65i_adc(c_instruction):
    mnemonic = "adc"
    alu = (None, "adc", None)
    dest = "acc"
    pass

#c c65i_sbc
class c65i_sbc(c_instruction):
    mnemonic = "sbc"
    alu = (None, "sbc", None)
    dest = "acc"
    pass

#c c65i_cmp
class c65i_cmp(c_instruction):
    mnemonic = "cmp"
    alu = (None, "cmp", 1)
    dest = "cmp"
    pass

#c c65i_bit
class c65i_bit(c_instruction):
    mnemonic = "bit"
    alu = (None, "bit", None)
    dest = "acc"
    pass

#c c65i_asl
class c65i_asl(c_instruction):
    mnemonic = "asl"
    alu = ("asl", None, None)
    pass

#c c65i_lsr
class c65i_lsr(c_instruction):
    mnemonic = "lsr"
    alu = ("lsr", None, None)
    pass

#c c65i_rol
class c65i_rol(c_instruction):
    mnemonic = "rol"
    alu = ("rol", None, None)
    pass

#c c65i_ror
class c65i_ror(c_instruction):
    mnemonic = "ror"
    alu = ("ror", None, None)
    pass

#c c65i_inc
class c65i_inc(c_instruction):
    mnemonic = "inc"
    alu = ("inc", None, None)
    pass

#c c65i_dec
class c65i_dec(c_instruction):
    mnemonic = "dec"
    alu = ("dec", None, None)
    pass

#c c65i_cpx
class c65i_cpx(c_instruction):
    mnemonic = "cpx"
    alu = (None, "cmp", 1)
    src = "x"
    dest = "cmp"
    pass

#c c65i_cpy
class c65i_cpy(c_instruction):
    mnemonic = "cpy"
    alu = (None, "cmp", 1)
    src = "y"
    dest = "cmp"
    pass

#c c65i_lda
class c65i_lda(c_instruction):
    mnemonic = "lda"
    dest = "acc"
    pass

#c c65i_ldx
class c65i_ldx(c_instruction):
    mnemonic = "ldx"
    dest = "x"
    pass

#c c65i_ldy
class c65i_ldy(c_instruction):
    mnemonic = "ldy"
    dest = "y"
    pass

#c c65i_sta
class c65i_sta(c_instruction):
    mnemonic = "sta"
    src = "acc"
    flag = False
    pass

#c c65i_stx
class c65i_stx(c_instruction):
    mnemonic = "stx"
    src = "x"
    flag = False
    pass

#c c65i_sty
class c65i_sty(c_instruction):
    mnemonic = "sty"
    src = "y"
    flag = False
    pass

#c c65i_reset
class c65i_reset(c_instruction):
    pass

#c c65i_jmp
class c65i_jmp(c_instruction):
    mnemonic = "jmp"
    pass

#c c65i_jsr
class c65i_jsr(c_instruction):
    mnemonic = "jsr"
    pass

#c c65i_rts
class c65i_rts(c_instruction):
    mnemonic = "rts"
    pass

#c c65i_flag
class c65i_flag(c_instruction):
    dest = "setclrflag"
    src = "ones"
    alu = (None, "src", None)
    def __init__(self, mnemonic):
        self.mnemonic = mnemonic
        if mnemonic[0] == 'c': self.src = "zero"
        self.flag = mnemonic[-1]
        pass
    pass

#c c65i_transfer
class c65i_transfer(c_instruction):
    def __init__(self, mnemonic, src, dest, do_not_set_flags=False):
        self.mnemonic = mnemonic
        self.src = src
        self.dest = dest
        self.alu = (None, "src", None)
        if do_not_set_flags:
            self.flag = False
            pass
    pass

#c c65i_pushpull
class c65i_pushpull(c_instruction):
    def __init__(self, mnemonic, dir, src):
        self.mnemonic = mnemonic
        if dir == "push":
            self.src = src
            #self.alu = (None, "src", None)
            pass
        else:
            self.dest = src
            pass
    pass

#c c65i_incdec_index
class c65i_incdec_index(c_instruction):
    def __init__(self, mnemonic, index, op):
        self.mnemonic = mnemonic
        self.src = index
        self.dest = index
        self.alu=("inc", None, None)
        if op=="dec": self.alu=("dec", None, None)
    pass

#c c65i_branch
class c65i_branch(c_instruction):
    def __init__(self, mnemonic, condition):
        self.mnemonic = mnemonic
        self.condition = condition
    pass

#a Instruction encodings
#c c_instruction_encodings
class c_instruction_encodings(object):
    instruction = None
    encodings = None
    @staticmethod
    def std_acc(base_op): # For ORA, AND, EOR, ADC, LDA, CMP, SBC
        return ( (base_op+0x01,c65am_indx_in),
                  (base_op+0x05,c65am_zp_in),
                  (base_op+0x09,c65am_imm),
                  (base_op+0x0d,c65am_abs_in),
                  (base_op+0x11,c65am_indy_in),
                  (base_op+0x15,c65am_zx_in),
                  (base_op+0x19,c65am_absy_in),
                  (base_op+0x1d,c65am_absx_in),
                  )
    @staticmethod
    def sta(base_op): # For STA
        return ( (base_op+0x01,c65am_indx_out),
                  (base_op+0x05,c65am_zp_out),
                  #(base_op+0x09,c65am_imm),
                  (base_op+0x0d,c65am_abs_out),
                  (base_op+0x11,c65am_indy_out),
                  (base_op+0x15,c65am_zx_out),
                  (base_op+0x19,c65am_absy_out),
                  (base_op+0x1d,c65am_absx_out),
                  )
    @staticmethod
    def acc_shift(base_op): # For ASL, ROL, LSR, ROR
        return (  (base_op+0x06,c65am_zp_rw),
                  (base_op+0x0a,c65am_acc),
                  (base_op+0x0e,c65am_abs_rw),
                  (base_op+0x16,c65am_zx_rw),
                  (base_op+0x1e,c65am_absx_rw),
                  )
    @staticmethod
    def incdec(base_op): # For INC, DEC
        return (  (base_op+0x06,c65am_zp_rw),
                  (base_op+0x0e,c65am_abs_rw),
                  (base_op+0x16,c65am_zx_rw),
                  (base_op+0x1e,c65am_absx_rw),
                  )
    pass
#c c65ie_ora
class c65ie_ora(c_instruction_encodings):
    instruction = c65i_ora
    encodings = c_instruction_encodings.std_acc(0x00)
#c c65ie_and
class c65ie_and(c_instruction_encodings):
    instruction = c65i_and
    encodings = c_instruction_encodings.std_acc(0x20)
#c c65ie_eor
class c65ie_eor(c_instruction_encodings):
    instruction = c65i_eor
    encodings = c_instruction_encodings.std_acc(0x40)
#c c65ie_adc
class c65ie_adc(c_instruction_encodings):
    instruction = c65i_adc
    encodings = c_instruction_encodings.std_acc(0x60)
#c c65ie_sta
class c65ie_sta(c_instruction_encodings):
    instruction = c65i_sta
    encodings = c_instruction_encodings.sta(0x80)
#c c65ie_lda
class c65ie_lda(c_instruction_encodings):
    instruction = c65i_lda
    encodings = c_instruction_encodings.std_acc(0xa0)
#c c65ie_inc
class c65ie_inc(c_instruction_encodings):
    instruction = c65i_inc
    encodings = c_instruction_encodings.incdec(0xe0)
#c c65ie_dec
class c65ie_dec(c_instruction_encodings):
    instruction = c65i_dec
    encodings = c_instruction_encodings.incdec(0xc0)
#c c65ie_cmp
class c65ie_cmp(c_instruction_encodings):
    instruction = c65i_cmp
    encodings = c_instruction_encodings.std_acc(0xc0)
#c c65ie_sbc
class c65ie_sbc(c_instruction_encodings):
    instruction = c65i_sbc
    encodings = c_instruction_encodings.std_acc(0xe0)

#c c65ie_bit
class c65ie_bit(c_instruction_encodings):
    instruction = c65i_bit
    encodings = ( (0x24, c65am_zp_in),
                  (0x2c, c65am_abs_in) )

#c c65ie_nop
class c65ie_nop(c_instruction_encodings):
    instruction = c65i_transfer("nop", src="acc", dest=None, do_not_set_flags=True)
    encodings = ( (0xea, c65am_imp_transfer), )

#c c65ie_asl
class c65ie_asl(c_instruction_encodings):
    instruction = c65i_asl
    encodings = c_instruction_encodings.acc_shift(0x00)
#c c65ie_rol
class c65ie_rol(c_instruction_encodings):
    instruction = c65i_rol
    encodings = c_instruction_encodings.acc_shift(0x20)
#c c65ie_lsr
class c65ie_lsr(c_instruction_encodings):
    instruction = c65i_lsr
    encodings = c_instruction_encodings.acc_shift(0x40)
#c c65ie_ror
class c65ie_ror(c_instruction_encodings):
    instruction = c65i_ror
    encodings = c_instruction_encodings.acc_shift(0x60)

#c c65ie_stx
class c65ie_stx(c_instruction_encodings):
    instruction = c65i_stx
    encodings = ( (0x86,c65am_zp_out),
                  (0x8e,c65am_abs_out),
                  (0x96,c65am_zy_out),
                  )
#c c65ie_sty
class c65ie_sty(c_instruction_encodings):
    instruction = c65i_sty
    encodings = ( (0x84,c65am_zp_out),
                  (0x8c,c65am_abs_out),
                  (0x94,c65am_zx_out),
                  )
#c c65ie_cpx
class c65ie_cpx(c_instruction_encodings):
    instruction = c65i_cpx
    encodings = ( (0xe0,c65am_imm),
                  (0xe4,c65am_zp_in),
                  (0xec,c65am_abs_in),
                  )
#c c65ie_cpy
class c65ie_cpy(c_instruction_encodings):
    instruction = c65i_cpy
    encodings = ( (0xc0,c65am_imm),
                  (0xc4,c65am_zp_in),
                  (0xcc,c65am_abs_in),
                  )
#c c65ie_ldx
class c65ie_ldx(c_instruction_encodings):
    instruction = c65i_ldx
    encodings = ( (0xa2,c65am_imm),
                  (0xa6,c65am_zp_in),
                  (0xb6,c65am_zy_in),
                  (0xae,c65am_abs_in),
                  (0xbe,c65am_absy_in),
                  )
#c c65ie_ldy
class c65ie_ldy(c_instruction_encodings):
    instruction = c65i_ldy
    encodings = ( (0xa0,c65am_imm),
                  (0xa4,c65am_zp_in),
                  (0xac,c65am_abs_in),
                  (0xb4,c65am_zx_in),
                  (0xbc,c65am_absx_in),
                  )
#c c65ie_jmp
class c65ie_jmp(c_instruction_encodings):
    instruction = c65i_jmp
    encodings = ( (0x4c,c65am_abs_jmp),
                  (0x6c,c65am_ind_jmp),
                  )
#c c65ie_jsr
class c65ie_jsr(c_instruction_encodings):
    instruction = c65i_jsr
    encodings = ( (0x20,c65am_abs_jsr),
                  )

#c c65ie_rts
class c65ie_rts(c_instruction_encodings):
    instruction = c65i_rts
    encodings = ( (0x60,c65am_imp_rts),
                  )

#c c65ie_clc
class c65ie_clc(c_instruction_encodings):
    instruction = c65i_flag("clc")
    encodings = ( (0x18,c65am_imp_flag),)

#c c65ie_sec
class c65ie_sec(c_instruction_encodings):
    instruction = c65i_flag("sec")
    encodings = ( (0x38,c65am_imp_flag), )

#c c65ie_cli
class c65ie_cli(c_instruction_encodings):
    instruction = c65i_flag("cli")
    encodings = ( (0x58,c65am_imp_flag),)

#c c65ie_clv
class c65ie_clv(c_instruction_encodings):
    instruction = c65i_flag("clv")
    encodings = ( (0xb8,c65am_imp_flag),)

#c c65ie_sei
class c65ie_sei(c_instruction_encodings):
    instruction = c65i_flag("sei")
    encodings = ( (0x78,c65am_imp_flag), )

#c c65ie_cld
class c65ie_cld(c_instruction_encodings):
    instruction = c65i_flag("cld")
    encodings = ( (0xd8,c65am_imp_flag),)

#c c65ie_sed
class c65ie_sed(c_instruction_encodings):
    instruction = c65i_flag("sed")
    encodings = ( (0xf8,c65am_imp_flag), )

#c c65ie_tax
class c65ie_tax(c_instruction_encodings):
    instruction = c65i_transfer("tax", src="acc", dest="x")
    encodings = ( (0xaa,c65am_imp_transfer), )

#c c65ie_txa
class c65ie_txa(c_instruction_encodings):
    instruction = c65i_transfer("txa", src="x", dest="acc")
    encodings = ( (0x8a,c65am_imp_transfer), )

#c c65ie_tay
class c65ie_tay(c_instruction_encodings):
    instruction = c65i_transfer("tay", src="acc", dest="y")
    encodings = ( (0xa8,c65am_imp_transfer), )

#c c65ie_tya
class c65ie_tya(c_instruction_encodings):
    instruction = c65i_transfer("tya", src="y", dest="acc")
    encodings = ( (0x98,c65am_imp_transfer), )

#c c65ie_tsx
class c65ie_tsx(c_instruction_encodings):
    instruction = c65i_transfer("sp", src="acc", dest="x")
    encodings = ( (0xba,c65am_imp_transfer), )

#c c65ie_txs
class c65ie_txs(c_instruction_encodings):
    instruction = c65i_transfer("txs", src="x", dest="sp", do_not_set_flags=True)
    encodings = ( (0x9a,c65am_imp_transfer), )

#c c65ie_dex
class c65ie_dex(c_instruction_encodings):
    instruction = c65i_incdec_index("dex", op="dec", index="x")
    encodings = ( (0xca,c65am_imp_incdec), )

#c c65ie_inx
class c65ie_inx(c_instruction_encodings):
    instruction = c65i_incdec_index("inx", op="inc", index="x")
    encodings = ( (0xe8,c65am_imp_incdec), )

#c c65ie_dey
class c65ie_dey(c_instruction_encodings):
    instruction = c65i_incdec_index("dey", op="dec", index="y")
    encodings = ( (0x88,c65am_imp_incdec), )

#c c65ie_iny
class c65ie_iny(c_instruction_encodings):
    instruction = c65i_incdec_index("iny", op="inc", index="y")
    encodings = ( (0xc8,c65am_imp_incdec), )

#c c65ie_bpl
class c65ie_bpl(c_instruction_encodings):
    instruction = c65i_branch("bpl", ("n",0))
    encodings = ( (0x10,c65am_bcc), )

#c c65ie_bmi
class c65ie_bmi(c_instruction_encodings):
    instruction = c65i_branch("bmi", ("n",1))
    encodings = ( (0x30,c65am_bcc), )

#c c65ie_bvc
class c65ie_bvc(c_instruction_encodings):
    instruction = c65i_branch("bvc", ("v",0))
    encodings = ( (0x50,c65am_bcc), )

#c c65ie_bvs
class c65ie_bvs(c_instruction_encodings):
    instruction = c65i_branch("bvs", ("v",1))
    encodings = ( (0x70,c65am_bcc), )

#c c65ie_bcc
class c65ie_bcc(c_instruction_encodings):
    instruction = c65i_branch("bcc", ("c",0))
    encodings = ( (0x90,c65am_bcc), )

#c c65ie_bcs
class c65ie_bcs(c_instruction_encodings):
    instruction = c65i_branch("bcs", ("c",1))
    encodings = ( (0xb0,c65am_bcc), )

#c c65ie_bne
class c65ie_bne(c_instruction_encodings):
    instruction = c65i_branch("bne", ("z",0))
    encodings = ( (0xd0,c65am_bcc), )

#c c65ie_beq
class c65ie_beq(c_instruction_encodings):
    instruction = c65i_branch("beq", ("z",1))
    encodings = ( (0xf0,c65am_bcc), )

#c c65ie_pha
class c65ie_pha(c_instruction_encodings):
    instruction = c65i_pushpull("pha", dir="push", src="acc")
    encodings = ( (0x48,c65am_imp_push), )

#c c65ie_php
class c65ie_php(c_instruction_encodings):
    instruction = c65i_pushpull("php", dir="push", src="flags")
    encodings = ( (0x08,c65am_imp_push), )

#c c65ie_pla
class c65ie_pla(c_instruction_encodings):
    instruction = c65i_pushpull("pla", dir="pull", src="acc")
    encodings = ( (0x68,c65am_imp_pull), )

#c c65ie_plp
class c65ie_plp(c_instruction_encodings):
    instruction = c65i_pushpull("plp", dir="pull", src="flags")
    encodings = ( (0x28,c65am_imp_pull), )

#a Instruction set
#c c_instruction_set
class c_instruction_set(object):
    def __init__(self):
        self.decodings = {}
        self.mnemonics = {}
        for ie in self.encodings:
            self.mnemonics[ie.instruction.mnemonic.lower()] = ie
            for (e,am) in ie.encodings:
                if e in self.decodings: raise Exception("Duplicate instruction encoding %s"%(str((e,ie,ie.instruction,am))))
                self.decodings[e] = (ie.instruction, am)
                pass
            pass
        pass
    def decode(self, encoding):
        if encoding in self.decodings:
            return  self.decodings[encoding]
        print "Could not find encoding for %02x"%encoding
        return (None, None)
    def find_ie_of_mnemonic(self, mnemonic, addressing):
        mnemonic = mnemonic.lower()
        addressing = addressing.strip()
        if mnemonic not in self.mnemonics: return None
        ie = self.mnemonics[mnemonic]
        ams = []
        for (e,am) in ie.encodings:
            m = re.match(am.assembler_re, addressing)
            if m is not None:
                ams.insert(0,am)
                pass
            pass
        if len(ams)==0:
            return None
        return (ie, ams)
    def encoding_of(self, ie, am):
        for enc in ie.encodings:
            if enc[1]==am: return enc[0]
            pass
        return None
    def assemble(self, addressing, ie, scope, asm_pass):
        """Return tuple of Nones or opcodes
        """
        (ie, ams) = ie
        assembly_options = []
        for am in ams:
            opcode = self.encoding_of(ie,am)
            addressing = addressing.strip()
            m = re.match(am.assembler_re, addressing)
            if m is None: raise Exception("Bug - matching twice with same data got two different answers")
            operand = None
            if am.bytes>1:
                operand = scope.evaluate(m.group(1), am.operand_relative)
                pass
            if am.bytes==1:
                assembly_options = (((opcode,),))
                break
            elif am.bytes==2:
                if operand is None:
                    assembly_options.append((opcode,None))
                    pass
                elif (operand>=0) and (operand<=255):
                    assembly_options.append((opcode,operand))
                    pass
                pass
            elif am.bytes==3:
                if operand is None:
                    assembly_options.append((opcode,None,None))
                    pass
                else:
                    assembly_options.append((opcode,operand&0xff,(operand>>8)&0xff))
                    pass
                pass
            pass
        if len(assembly_options)==0:
            raise Exception("Failed to assemble %s %s"%(ie.instruction.mnemonic, addressing))
        assembly = None
        for ao in assembly_options:
            #print assembly_options
            if (asm_pass>=1) or (None not in ao):
                if None in ao: raise Exception("Failed to resolve addressing %s %s"%(ie.instruction.mnemonic, addressing))
                if assembly is None:
                    assembly=ao
                    pass
                elif len(assembly)>len(ao):
                    assembly=ao
                    pass
                pass
            else:
                if assembly is None:
                    assembly=ao
                    pass
                elif len(assembly)<len(ao):
                    assembly=ao
                    pass
                pass
            pass
        return assembly
    pass

#c c_6502_instruction_set
class c_6502_instruction_set(c_instruction_set):
    """
    Missing:
    rti
    bit abs, bit zpg,
    """
    encodings = (c65ie_ora,
                 c65ie_and,
                 c65ie_eor,
                 c65ie_adc,
                 c65ie_cmp,
                 c65ie_sbc,
                 c65ie_inc,
                 c65ie_dec,
                 c65ie_bit,
                 c65ie_nop,

                 c65ie_sta,
                 c65ie_stx,
                 c65ie_sty,

                 c65ie_lda,
                 c65ie_ldx,
                 c65ie_ldy,

                 c65ie_cpx,
                 c65ie_cpy,

                 c65ie_jmp,
                 c65ie_jsr,
                 c65ie_rts,

                 c65ie_clc,
                 c65ie_sec,
                 c65ie_cld,
                 c65ie_sed,
                 c65ie_cli,
                 c65ie_sei,
                 c65ie_clv,

                 c65ie_txa,
                 c65ie_tax,
                 c65ie_tya,
                 c65ie_tay,
                 c65ie_txs,
                 c65ie_tsx,

                 c65ie_dex,
                 c65ie_inx,
                 c65ie_dey,
                 c65ie_iny,

                 c65ie_php,
                 c65ie_plp,
                 c65ie_pha,
                 c65ie_pla,

                 c65ie_bpl,
                 c65ie_bmi,
                 c65ie_bvc,
                 c65ie_bvs,
                 c65ie_bcc,
                 c65ie_bcs,
                 c65ie_bne,
                 c65ie_beq,

                 c65ie_asl,
                 c65ie_rol,
                 c65ie_lsr,
                 c65ie_ror,
                 )
    pass


