#!/usr/bin/env python
#a Imports
import re
import unittest
import sys, inspect
from instr6502 import c_6502_instruction_set
from system6502 import c_system
from asm6502 import c_assembler

#a Still to test
# stop reset writing psr and pcl/pch
# stop nmi,irq from incrementing pc?
# undocumented instructions
# irq, nmi
# pha, php, txs do not set flags

#a Unit tests
#c c_6502_test
class c_6502_test(object):
    #b Default property values
    verbose = False
    src = ""
    src_args = tuple()
    #f add_op
    @staticmethod
    def add_op(a, b, c, v):
        value = a + b + c
        sum = value&0xff
        c = (value>>8)&1
        value = value & 0xff
        v = 0
        if a<128 and b<128:
            if value>=128:
                v = 1
                pass
            pass
        elif a>=128 and b>=128:
            if value<128:
                v = 1
                pass
            pass
        return (sum, c, v)
    #f get_adder_results
    @staticmethod
    def get_adder_results(a, b, c):
        a_in = a
        b_in = b
        c_in = c
        a = a&0xff
        b = b&0xff
        if (a>=128) : a = (a-256) 
        if (b>=128) : b = (b-256) 
        value = a + b + c
        v = 0
        if value>=128:
            v = 1
            pass
        elif value<-128:
            v = 1
            pass
        value = a_in + b_in + c
        sum = value&0xff
        n = (value>>7)&1
        c = (value>>8)&1
        z = 0
        if (value&0xff)==0: z=1
        #print "%02x %02x %d : %03x : %02x %d %d %d %d"%(a_in,b_in,c_in,value,sum,z,n,c,v)
        return (sum, z, n, c, v)
    #f get_adder_results_dec_14
    @staticmethod
    def get_adder_results_dec_14(a, b, c):
        value = a + b + c
        sum = value&0xff
        n = (value>>7)&1
        c = (value>>8)&1
        value = value & 0xff
        z = 0
        if value==0: z=1
        v = 0
        if a<128 and b<128:
            if value>=128:
                v = 1
                pass
            pass
        elif a>=128 and b>=128:
            if value<128:
                v = 1
                pass
            pass
        return (sum, z, n, c, v)
    #f set_v
    @staticmethod
    def set_v(v):
        r = "clv\n"
        if v:
            r = "lda #0x40 \n adc#0x40\n" # set V
            pass
        return r
    #f check_flags
    @staticmethod
    def check_flags(z,n,c,v,d,i):
        l = "%d%d%d%d%d%d"%(z,n,c,v,d,i)
        fail_label = "check_flags_fail_"+l
        next_label = "check_flags_next_"+l
        r = ""
        r += "cld \n lda #0x40 \n adc#0x40\n" # set V
        r += ["lda #1", "lda #0x0", "lda #0x80", "lda #0xc3\npha\nplp\n"][z+2*n] + "\n" # V, and N/Z set appropriately
        r += ["clv", ""][v] + "\n" # clear V if necessary
        r += ["clc", "sec"][c] + "\n" # set C approriately
        r += ["cld", "sed"][d] + "\n" # set D approriately
        r += ["cli", "sei"][i] + "\n" # set I approriately
        r += ["beq", "bne"][z] + " " + fail_label + "\n" # Check beq/bne
        r += ["bcs", "bcc"][c] + " " + fail_label + "\n" # Check bcc/bcs
        r += ["bmi", "bpl"][n] + " " + fail_label + "\n" # Check bmi/bpl
        r += ["bvs", "bvc"][v] + " " + fail_label + "\n" # Check bvc/bvs
        r += "php \n pla \n and #0xcf \n"
        r += ("cmp #$%02x \n bne " + fail_label + "\n") % ( (n<<7) | (v<<6) | (d<<3) | (i<<2) | (z<<1) | (c<<0) )
        r += "pha \n plp \n"
        r += ["beq", "bne"][z] + " " + fail_label + "\n" # Check beq/bne
        r += ["bcs", "bcc"][c] + " " + fail_label + "\n" # Check bcc/bcs
        r += ["bmi", "bpl"][n] + " " + fail_label + "\n" # Check bmi/bpl
        r += ["bvs", "bvc"][v] + " " + fail_label + "\n" # Check bvc/bvs
        r += "jmp "+next_label+"\n"
        r += (fail_label+": lda #$%02x \n sta $ff \n jmp fail \n" ) % (0xff ^ ( (n<<7) | (v<<6) | (d<<3) | (i<<2) | (z<<1) | (c<<0) ))
        r += next_label+":\n"
        return r
    pass
    #f check_shift
    @staticmethod
    def check_shift(m,v,ci,res,co):
        """
        Try a shift mnemonic with various addressing modes and carry in for a particular data
        """
        if ci is None:
            l = "%s_%02x"%(m,v)
            pass
        else:
            l = "%s_%02x_%d"%(m,v,ci)
            pass
        fail_label = "check_flags_fail_"+l
        next_label = "check_flags_next_"+l
        r = "ldx #0x1\n"
        lbl_id = 0
        for am in ("0x08", "0x7fff","0x09,x", "0x07ffd,x", "A"):
            fail_label = "check_flags_fail_%s_%d"%(l,lbl_id)
            next_label = "check_flags_next_%s_%d"%(l,lbl_id)
            for c in range(2):
                if (ci is not None) and (ci!=c): continue
                r += ["clc", "sec"][c] + "\n"
                if am =="A":
                    r += "lda #0x%02x \n %s A \n"%(v,m)
                    pass
                else:
                    r += "lda #0x%02x \n sta %s \n %s %s \n"%(v,am,m,am)
                    pass
                r += ["bcs", "bcc"][co] + " "+ fail_label + "\n"
                r += ["beq", "bne"][res==0] + " "+ fail_label + "\n"
                r += ["bmi", "bpl"][(res>>7)&1] + " "+ fail_label + "\n"
                if am =="A":
                    r += "cmp #0x%02x \n bne %s\n"%(res, fail_label)
                    pass
                else:
                    r += "cmp #0x%02x \n bne %s\n"%(v, fail_label)
                    r += "ldy %s \n cpy #0x%02x \n bne %s\n"%(am, res, fail_label)
                    pass
                pass
            r += "jmp "+next_label+"\n"
            r += (fail_label+": jmp fail \n" )
            r += next_label+":\n"
            lbl_id += 1
            pass
        return r

    #f check_logical
    @staticmethod
    def check_logical(m,d0,d1,res):
        """
        Try a shift mnemonic with various addressing modes and carry in for a particular data
        """
        l = "%s_%02x_%02x"%(m,d0,d1)
        fail_label = "check_flags_fail_"+l
        next_label = "check_flags_next_"+l
        r = "ldx #0x1\n"
        lbl_id = 0
        for am in ("0x08", "0x7fff","0x09,x", "0x07ffd,x", "#"):
            fail_label = "check_flags_fail_%s_%d"%(l,lbl_id)
            next_label = "check_flags_next_%s_%d"%(l,lbl_id)
            for c in range(2):
                r += ["clc", "sec"][c] + "\n"
                if am =="#":
                    r += "lda #0x%02x \n %s #0x%02x \n"%(d0,m,d1)
                    pass
                else:
                    r += "lda #0x%02x \n sta %s \n lda #0x%02x \n %s %s \n"%(d0,am,d1,m,am)
                    pass
                r += ["bcs", "bcc"][c] + " "+ fail_label + "\n"
                r += ["beq", "bne"][res==0] + " "+ fail_label + "\n"
                r += ["bmi", "bpl"][(res>>7)&1] + " "+ fail_label + "\n"
                r += "cmp #0x%02x \n bne %s\n"%(res, fail_label)
                if am !="#":                
                    r += "lda %s \n cmp #0x%02x \n bne %s\n"%(am, d0, fail_label)
                    pass
                pass
            r += "jmp "+next_label+"\n"
            r += (fail_label+": jmp fail \n" )
            r += next_label+":\n"
            lbl_id += 1
            pass
        return r

    #f check_addsub
    @staticmethod
    def check_addsub(m,d0,d1,op_fn):
        """
        Try an add, sub or cmp mnemonic with various addressing modes and carry in for a particular data
        """
        l = "%s_%02x_%02x"%(m,d0,d1)
        fail_label = "check_flags_fail_"+l
        next_label = "check_flags_next_"+l
        r = "ldx #0x1\n"
        lbl_id = 0
        for am in ("0x08", "0x7fff","0x09,x", "0x07ffd,x", "#"):
            fail_label = "check_flags_fail_%s_%d"%(l,lbl_id)
            next_label = "check_flags_next_%s_%d"%(l,lbl_id)
            for c in range(2):
                alu_res = c_6502_test.get_adder_results(d0,op_fn(d1),c)
                (alu_sum, alu_z, alu_n, alu_c, alu_v) = alu_res
                r += ["clc", "sec"][c] + "\n"
                if am =="#":
                    r += "lda #0x%02x \n %s #0x%02x \n"%(d0,m,d1)
                    pass
                else:
                    r += "lda #0x%02x \n sta %s \n lda #0x%02x \n %s %s \n"%(d1,am,d0,m,am)
                    pass
                r += ["bcs", "bcc"][alu_c] + " "+ fail_label + "\n"
                r += ["beq", "bne"][alu_z] + " "+ fail_label + "\n"
                r += ["bmi", "bpl"][alu_n] + " "+ fail_label + "\n"
                r += ["bvs", "bvc"][alu_v] + " "+ fail_label + "\n"
                r += "cmp #0x%02x \n bne %s\n"%(alu_sum, fail_label)
                if am !="#":                
                    r += "lda %s \n cmp #0x%02x \n bne %s\n"%(am, d1, fail_label)
                    pass
                pass
            r += "jmp "+next_label+"\n"
            r += (fail_label+": jmp fail \n" )
            r += next_label+":\n"
            lbl_id += 1
            pass
        return r

    #f cmp_check_flags
    @staticmethod
    def cmp_check_flags(d0, d1, v, fail_label):
        r = ""
        alu_res = c_6502_test.get_adder_results(d0,(d1^0xff),1)
        (alu_sum, alu_z, alu_n, alu_c, alu_v) = alu_res
        r += ["bcs", "bcc"][alu_c] + " "+ fail_label + "\n"
        r += ["beq", "bne"][alu_z] + " "+ fail_label + "\n"
        r += ["bmi", "bpl"][alu_n] + " "+ fail_label + "\n"
        r += ["bvs", "bvc"][v]     + " "+ fail_label + "\n"
        return r
    #f check_cmp
    @staticmethod
    def check_cmp(d0,d1,v):
        """
        Try a cmp mnemonic with various addressing modes and carry in for a particular data
        Checks N, Z, C set appropriately, and V is untouched
        """
        l = "cmp_%02x_%02x_%d_"%(d0,d1,v)
        fail_label = "check_flags_fail_"+l
        next_label = "check_flags_next_"+l
        r = "ldx #0x1\n"
        lbl_id = 0
        for am in ("0x08", "0x7fff","0x09,x", "0x07ffd,x", "#"):
            fail_label = "check_flags_fail_%s_%d"%(l,lbl_id)
            next_label = "check_flags_next_%s_%d"%(l,lbl_id)
            for c in range(2):
                r += ["clc", "sec"][c] + "\n"
                if am =="#":
                    r += "lda #0x%02x \n cmp #0x%02x \n"%(d0,d1)
                    pass
                else:
                    r += "lda #0x%02x \n sta %s \n lda #0x%02x \n cmp %s \n"%(d1,am,d0,am)
                    pass
                r += c_6502_test.cmp_check_flags(d0, d1, v, fail_label)
                if am !="#":                
                    r += "lda %s \n cmp #0x%02x \n bne %s\n"%(am, d1, fail_label)
                    pass
                pass
            r += "jmp "+next_label+"\n"
            r += (fail_label+": jmp fail \n" )
            r += next_label+":\n"
            lbl_id += 1
            pass
        return r

    #f check_addressing_mode
    @staticmethod
    def check_addressing_mode(op, op_fn, am, label, mem_data, change_acc, change_v):
        src = ""
        for c in range(2):
            for v in range(2):
                fail_label = "fail"+label+"%d_%d"%(c,v)
                pass_label = "pass"+label+"%d_%d"%(c,v)
                for test_data in [0,1,0x40,0x80,0xf0,0xff]:
                    alu_res = op_fn(test_data,mem_data,c,v)
                    (alu_sum, alu_c, alu_v) = alu_res
                    alu_z = 0|(alu_sum==0)
                    alu_n = 0|(alu_sum>=128)
                    src_td = """
                    lda #{0}
                    {2} {1}
                    """
                    src += c_6502_test.set_v(v)
                    src += ["clc","sec"][c]+"\n"
                    src += src_td.format(test_data,am,op)
                    src += ["bcs", "bcc"][alu_c] + " "+ fail_label + "\n"
                    src += ["beq", "bne"][alu_z] + " "+ fail_label + "\n"
                    src += ["bmi", "bpl"][alu_n] + " "+ fail_label + "\n"
                    if change_v:
                        src += ["bvs", "bvc"][alu_v] + " "+ fail_label + "\n"
                        pass
                    else:
                        src += ["bvs", "bvc"][v] + " "+ fail_label + "\n"
                        pass
                    if change_acc:
                        src += "cmp #0x%02x \n bne %s\n"%(alu_sum, fail_label)
                        pass
                    else:
                        src += "cmp #0x%02x \n bne %s\n"%(test_data, fail_label)
                        pass
                    pass
                src += """
                jmp """+pass_label+"""
                """+fail_label+""":
                jmp fail
                """+pass_label+""":
                """
                pass
            pass
        return src
    #f addressing_mode_test
    @staticmethod
    def addressing_mode_test(op, op_fn, change_acc=True, change_v=True):
        src = """. = $fffb
        jmp code_start
        . = $1400
        code_start: """
        init_data = { 0x08:0xfc,
                      0x09:0x11,
                      0x12:0xf8,
                      0x13:0x12,
                      0xfc:0xf0,
                      0xfd:0x11,
                      0x0a:0x5a,
                      0x10:0x87,
                      0xf8:0x0f,
                      0xf9:0x10,
                      0xfa:0xf0,
                      0xfe:0xa5,
                      0x100f:0x04,
                      0x11f0:0x3c,
                      0x11fc:0xc3,
                      0x1234:0x1e,
                      0x12f8:0x20,
                      0x12fa:0x02,
                      0x12fc:0xe1,
                      0x12fe:0x78,
                      0x1308:0xd2,
                      0x130a:0x2d,
                      }
        for (a,d) in init_data.iteritems():
            src_l = "lda #{1} \n sta {0} \n".format(a,d)
            src += src_l
            pass
        for (x,y) in [(0,0),
                      (4,16),
                      (16,4),
                      ]:
            src_minit = """
            ldx #{0}
            ldy #{1}
            """
            src += src_minit.format(x,y)
            n = 0
            for (am, is_address, address) in [("#12",False,12),
                                              ("0x10",True, 16),
                                              ("0x1234",True, 0x1234),
                                              ("0xfa,x",True, (0xfa+x)&0xff),
                                              ("0x12f8,x",True, 0x12f8+x),
                                              ("0x12fa,y",True, 0x12fa+y),
                                              ("(0x12),y",True, 0x12f8+y),
                                              ("(0xf8,x)",True, init_data[(0xf8+x)&0xff] | (init_data[(0xf9+x)&0xff]<<8)),
                                              ]:
                mem_data = address
                if is_address: mem_data=init_data[address]
                label = "add{0}_{1}_{2}".format(x,y,n)
                n += 1
                src += c_6502_test.check_addressing_mode(op, op_fn, am, label, mem_data, change_acc, change_v)
            pass
        src +=  """       
                jmp pass
    
        pass:
                    lda #0x12
                    sta 0x00
                    lda #0x34
                    sta 0x01
                    jmp done
        fail:
                    lda #0
                    sta 0x00
                    sta 0x01
        done: jmp done
        """
        expected_memory_data = [(0,0x12), (1,0x34)]
        for (a,d) in init_data.iteritems():
            expected_memory_data.append((a,d))
            pass
        return (src, expected_memory_data)
    #f check_incdec
    @staticmethod
    def check_incdec(m,v,res):
        """
        Try inc/dec mnemonic with various addressing modes a particular data
        """
        l = "%s_%02x"%(m,v)
        fail_label = "check_flags_fail_"+l
        next_label = "check_flags_next_"+l
        r = "ldx #0x1\n"
        lbl_id = 0
        for am in ("0x08", "0x7fff","0x09,x", "0x07ffd,x", "X", "Y"):
            fail_label = "check_flags_fail_%s_%d"%(l,lbl_id)
            next_label = "check_flags_next_%s_%d"%(l,lbl_id)
            for c in range(2):
                r += ["clc", "sec"][c] + "\n"
                if am in ["X", "Y"]:
                    r += "ld%s #0x%02x \n %s%s \n"%(am,v,m[0:2],am)
                    pass
                else:
                    r += "lda #0x%02x \n sta %s \n %s %s \n"%(v,am,m,am)
                    pass
                r += ["bcs", "bcc"][c] + " "+ fail_label + "\n"
                r += ["beq", "bne"][res==0] + " "+ fail_label + "\n"
                r += ["bmi", "bpl"][(res>>7)&1] + " "+ fail_label + "\n"
                if am in ["X", "Y"]:
                    r += "cp%s #0x%02x \n bne %s\n"%(am, res, fail_label)
                    pass
                else:
                    r += "cmp #0x%02x \n bne %s\n"%(v, fail_label)
                    r += "ldy %s \n cpy #0x%02x \n bne %s\n"%(am, res, fail_label)
                    pass
                pass
            r += "jmp "+next_label+"\n"
            r += (fail_label+": jmp fail \n" )
            r += next_label+":\n"
            lbl_id += 1
            pass
        return r

#c test_6502_simplest
class test_6502_simplest(c_6502_test):
    num_cycles = 50
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start:lda #2
               sta 0x00
               clc
               adc #1
               ldx #1
               sta 0x00, x
    done: jmp done
    """
    expected_memory_data = [(i,i+2) for i in range(2)]
    verbose = False

#c test_6502_stack
class test_6502_stack(c_6502_test):
    num_cycles = 500
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start:ldx #0xff
                txs
                lda #3
                pha
                ldy $1ff
                txa
                cmp #0xff
                bne fail
                tya
                cmp #3
                bne fail
                jmp fixed
    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    . = 0x240
    way_home:   jmp pass
    die:        jmp die
                jmp die
                jmp die
                jmp die
                jmp die
    . = 0x280
    fixed:
                jsr skipped
    skipped:
                pla
                cmp #0x82
                bne fail
                pla
                cmp #0x02
                bne fail

                lda #0x02
                pha
                lda #0x3f ; way_home-1
                pha
                rts

    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_push_pull
class test_6502_push_pull(c_6502_test):
    num_cycles = 500
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start:lda #2
                adc #1 ; VC, PL, NE, CC
                php
                pla
                and #$c3 ; NV-BDIZC, 00----00
                cmp #0 ; VC, PL, EQ, CS
                bne fail
                php
                pla
                and #$c3 ; NV-BDIZC, 00----11
                cmp #3
                bne fail
                adc #$7e ; 0x82, NV-BDIZC, 11----00
                php
                pla
                and #0xc3 ; NV-BDIZC, 11----00
                cmp #0xc0 ; NV-BDIZC, 00----11
                bne fail
                adc #0xff ; 0xc0, NV-BDIZC, 10----01
                php
                pla
                and #0xc3 ; NV-BDIZC, 10----01
                cmp #0x81 ; NV-BDIZC, 00----11
                bne fail
    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_flags
class test_6502_flags(c_6502_test):
    """
    Test every setting of C, N, V, Z, D, I, and branches for CNZV,
    and that push/pop of processor status works correctly
    """
    num_cycles = 5000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: 
    """
    for z in range(2):
        for c in range(2):
            for v in range(2):
                for n in range(2):
                    for d in range(2):
                        for i in range(2):
                            src += c_6502_test.check_flags(z,n,c,v,d,i)
                            pass
                        pass
                    pass
                pass
            pass
        pass
    src += """
    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_branches
class test_6502_branches(c_6502_test):
    num_cycles = 500
    src = """. = $fffb
    jmp code_start
    . = $2c0
    code_start:lda #2
                bne forward_across_page
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
    backward_across_page: ; should be at <$300
                jmp continue_test
                jmp fail
                jmp fail
                jmp fail
                jmp fail
    . = $300
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
    forward_across_page: ; should be at >$300
                bne backward_across_page
                jmp fail
                jmp fail
                jmp fail
                jmp fail
                jmp fail
    . = $400
    continue_test:
        lda #0
        sta 0x1cd
        lda #5
        sta 0x1ce
        jmp (0x1cd)
                jmp fail
                jmp fail
                jmp fail
                jmp fail
    . = $500
    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_adc
class test_6502_adc(c_6502_test):
    num_cycles = 50
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start:lda #2
               sta 0x00
               clc
               adc #1
               ldx #1
               sta 0x00, x
    done: jmp done
    """
    expected_memory_data = [(i,i+2) for i in range(2)]
    verbose = False

#c test_6502_adds
class test_6502_adds(c_6502_test):
    num_cycles = 500
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start:lda #2
               sta 0x00
               clc
               adc #1 ; 3
               beq fail
               bvs fail
               bcs fail
               bmi fail
               sta 0x01
               adc #0xfd ; 256 == 0 with carry, no overflow
               bne fail
               bvs fail
               bcc fail
               bmi fail
               sta 0x02
               adc #0x00 ; 1
               beq fail
               bvs fail
               bcs fail
               bmi fail
               sta 0x03
               adc #0x3f ; 0x40
               beq fail
               bvs fail
               bcs fail
               bmi fail
               sta 0x04
               adc #0x40 ; 0x80
               beq fail
               bvc fail
               bcs fail
               bpl fail
               sta 0x05
               adc #0xff ; 0x(1) 7f, overflowed
               beq fail
               bvc fail
               bcc fail
               bmi fail
               sta 0x06
               adc #0x80 ; carry in, 0x(1) 00, no overflow
               bne fail
               bvs fail
               bcc fail
               bmi fail
               sta 0x07
    done: jmp done
    fail: jmp fail
    """
    expected_memory_data = [(0,2), (1,3), (2,0), (3,1), (4,64), (5,128), (6,127), (7,0)]
    verbose = False

#c test_6502_shift
class test_6502_shift(c_6502_test):
    """
    Try all the shift types with appropriate carry in, carry out, and various data values
    """
    shift_ops = {"asl":(False, lambda v,c:(v<<1,v&0x80)),
                 "lsr":(False, lambda v,c:((v&0xff)>>1,v&0x01)),
                 "ror":(True,  lambda v,c:(v>>1,v&0x01)),
                 "rol":(True,  lambda v,c:((v<<1)|c,v&0x80)),
                 }
    shift_data = (0xff,0x80,0x40,0x0f,0xf0,0x2,0x1,0)
    num_cycles = 50000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: """
    for op in shift_ops:
        (needs_carry, op_fn) = shift_ops[op]
        for d in shift_data:
            for c in range(2):
                c_in = c
                if not needs_carry: c_in=None
                v = d | (c<<8)
                res, c_out = op_fn(v,c)
                c_out = [0,1][c_out!=0]
                src += c_6502_test.check_shift(op,d,c_in,res&0xff,c_out)
                if not needs_carry: break
                pass
            pass
        pass
    src += """
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_logical
class test_6502_logical(c_6502_test):
    """
    Try all the logical ops (and, or, eor) with some addressing modes
    Ensure that N, Z are set correctly, C, V untouched
    """
    logic_ops = {"and":lambda a,b:a&b,
                 "eor":lambda a,b:a^b,
                 "ora":lambda a,b:a|b,
                 }
    logic_data = (0xff,0x80,0x40,0xf0,0x1,0)
    num_cycles = 50000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: """
    for op in logic_ops:
        op_fn = logic_ops[op]
        for d0 in logic_data:
            for d1 in logic_data:
                res = op_fn(d0, d1)
                src += c_6502_test.check_logical(op,d0,d1,res)
                pass
            pass
        pass
    src += """
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_addsub
class test_6502_addsub(c_6502_test):
    """
    Try adc and sbc ops with some addressing modes
    Ensure that N, Z, C and V are set correctly
    """
    logic_ops = {"adc":lambda a:a,
                 "sbc":lambda a:(a^0xff),
                 }
    logic_data = (0xff,0xfe,0x80,0x40,0xf0,0x1,0)
    num_cycles = 50000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: """
    for op in logic_ops:
        op_fn = logic_ops[op]
        for d0 in logic_data:
            for d1 in logic_data:
                src += c_6502_test.check_addsub(op,d0,d1,op_fn)
                pass
            pass
        pass
    src += """
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_cmp
class test_6502_cmp(c_6502_test):
    """
    Try cmp with some addressing modes
    Ensure that N, Z, C are set correctly and V is untouched
    """
    logic_data = (0xff,0xfe,0x80,0x40,0xf0,0x1,0)
    num_cycles = 50000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: """
    for v in range(2):
        src += c_6502_test.set_v(v)
        for d0 in logic_data:
            for d1 in logic_data:
                src += c_6502_test.check_cmp(d0,d1,v)
                pass
            pass
        pass
    src += """
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_incdec
class test_6502_incdec(c_6502_test):
    """
    Try inc and dec with a suite of values in all addressing modes
    """
    incdec_ops = {"inc":+1,
                 "dec":+255}
    incdec_data = (0xff,0x80,0x40,0x0f,0xf0,0x2,0x1,0)
    num_cycles = 15000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: """
    for op in incdec_ops:
        op_delta = incdec_ops[op]
        for d in incdec_data:
            res = (d+op_delta) & 0xff
            src += c_6502_test.check_incdec(op,d,res)
            pass
        pass
    src += """
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_xy_reg
class test_6502_xy_reg(c_6502_test):
    #b Start
    """
    Test XY specific instructions
    ldy #, cpy#, tya, tay, iny, dey
    ld/sty zpgx
    ld/sty zpg, 
    sty abs, ldy abs, 
    ldy absx (note no sty absx)
    cpy zpg
    cpy abs
    """
    num_cycles = 20000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start: """
    #b Test load immediate, compare immediate, inc/dec do not change V, other regs uneffected, transfers
    for (r,i) in ( ("x","y"), ("y","x") ):
        for v in range(2):
            label = "imm_{0}{1}{2}".format(r,i,v)
            src_l = """
            lda #$20
            ld{1} #$13
            ta{0}
            lda #17
            """ + c_6502_test.set_v(v) + """
            t{0}a
            clc
            ld{0} #$56 \n""" + "cp{0} #$56\n"+c_6502_test.cmp_check_flags(0x56, 0x56, v, "fail"+label) + """
            ld{0} #$51 \n""" + "cp{0} #$42\n"+c_6502_test.cmp_check_flags(0x51, 0x42, v, "fail"+label) + """
            de{0} \n""" + "cp{0} #$4f\n"+c_6502_test.cmp_check_flags(0x50, 0x4f, v, "fail"+label) + """
            de{0} \n""" + "cp{0} #$4f\n"+c_6502_test.cmp_check_flags(0x4f, 0x4f, v, "fail"+label) + """
            de{0} \n""" + "cp{0} #$4f\n"+c_6502_test.cmp_check_flags(0x4e, 0x4f, v, "fail"+label) + """
            in{0} \n""" + "cp{0} #$4f\n"+c_6502_test.cmp_check_flags(0x4f, 0x4f, v, "fail"+label) + """
            in{0} \n""" + "cp{0} #$4f\n"+c_6502_test.cmp_check_flags(0x50, 0x4f, v, "fail"+label) + """
            cmp #$20
            bne fail"""+label+"""
            cp{1} #$13
            bne fail"""+label+"""
            jmp pass"""+label+"""
            fail"""+label+""":
            jmp fail
            pass"""+label+""":
            """
            src += src_l.format(r,i)
            pass
        pass
    #b Test inc/dec around zero
    for (r,i) in ( ("x","y"), ("y","x") ):
        for v in range(2):
            label = "incdec{0}{1}{2}".format(r,i,v)
            src_l = """
            lda #$1
            sta $07
            ld{0} $07 
            """ + c_6502_test.set_v(v) + """
            cp{0} #$1\n"""+c_6502_test.cmp_check_flags(0x1, 0x1, v, "fail"+label) + """
            clc
            de{0} \n bne fail"""+label+""" \n bmi fail"""+label+"""
            de{0} \n beq fail"""+label+""" \n bpl fail"""+label+"""
            in{0} \n bne fail"""+label+""" \n bmi fail"""+label+"""
            in{0} \n beq fail"""+label+""" \n bmi fail"""+label+"""
            bcs fail"""+label+"""

            sec
            de{0} \n bne fail"""+label+""" \n bmi fail"""+label+"""
            de{0} \n beq fail"""+label+""" \n bpl fail"""+label+"""
            in{0} \n bne fail"""+label+""" \n bmi fail"""+label+"""
            in{0} \n beq fail"""+label+""" \n bmi fail"""+label+"""
            bcc fail"""+label+"""

            jmp pass"""+label+"""
            fail"""+label+""":
            jmp fail
            pass"""+label+""":
            """
            src += src_l.format(r,i)
            pass
        pass
    #b Test ld/st zpg index
    for (r,i) in ( ("y","x"), ("x","y") ):
        label = "ldstz{0}{1}".format(r,i)
        src_l = """
        ld{1} #0
        st{1} $1234
        ld{0} $1234
        loop"""+label+""":
        st{0} $10,{1}
        in{1}
        de{0}
        bne loop"""+label+"""
        ld{0} $ff
        st{0} $0
        ld{0} $2
        t{0}a
        eor $0
        ta{0}
        st{0} $0
        ld{0} $3
        t{0}a
        eor $0
        ta{0}
        st{0} $4

        jmp pass"""+label+"""
        fail"""+label+""":
        jmp fail
        pass"""+label+""":
        """
        src += src_l.format(r,i)
        pass
    #b Test ld/st abs index
    for (r,i) in ( ("x","y"), ("y","x") ):
        label = "ldsta{0}{1}".format(r,i)
        src_l = """
        ld{0} #0
        st{0} 0x1fe
        in{0}
        st{0} 0x1ff
        in{0}
        st{0} 0x200
        in{0}
        st{0} 0x201
        in{0}
        st{0} 0x202

        st{0} 0
        sec
        ld{1} 0x202
        loop"""+label+""":
        ld{0} 0x1fe, {1}
        t{0}a
        adc 0
        sta 0
        de{1}
        bpl loop"""+label+"""

        lda 0
        sta 5

        jmp pass"""+label+"""
        fail"""+label+""":
        jmp fail
        pass"""+label+""":
        """
        src += src_l.format(r,i)
        pass
    #b Test cp abs and zp
    for (r,i) in ( ("x","y"), ("y","x") ):
        for v in range(2):
            label = "cmp{0}{1}{2}".format(r,i,v)
            src_l = """
            """ + c_6502_test.set_v(v) + """
            ld{0} #4 \n cp{0} 0x202\n"""+c_6502_test.cmp_check_flags(0x4, 0x4, v, "fail"+label) + """
            ld{0} #2 \n cp{0} 0x202\n"""+c_6502_test.cmp_check_flags(0x2, 0x4, v, "fail"+label) + """
            ld{0} #4 \n cp{0} 0x1ff\n"""+c_6502_test.cmp_check_flags(0x4, 0x1, v, "fail"+label) + """

            ld{0} #16 \n cp{0} 0x05\n"""+c_6502_test.cmp_check_flags(16, 15, v, "fail"+label) + """
            ld{0} #15 \n cp{0} 0x05\n"""+c_6502_test.cmp_check_flags(15, 15, v, "fail"+label) + """
            ld{0} #14 \n cp{0} 0x05\n"""+c_6502_test.cmp_check_flags(14, 15, v, "fail"+label) + """

            jmp pass"""+label+"""
            fail"""+label+""":
            jmp fail
            pass"""+label+""":
            """
            src += src_l.format(r,i)
            pass
        pass
    #b Trailer
    src +=  """       
            jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34), (2,0x0e), (3,0x0d), (4,0x12), (5,1+4+4+3+2+1+0), (0xff,0x11),
                            (510,0), (511,1), (512,2), (513,3), (514,4)]
    verbose = False

#c test_6502_addressing_logical_ora
class test_6502_addressing_logical_ora(c_6502_test):
    """
    Have to test:
    0: ora #12
    1: ora 0x12
    2: ora 0x1234
    3: ora (0x12),y
    4: ora (0x12,x)
    5: ora 0x12, x
    6: ora 0x1234, x
    7: ora 0x1234, y

    One possibility is to use data[n] for each of the above
    Then one needs referred_to_address[n] for the above too
    Then the test becomes
    lda #test_data[m]
    ora data[n] through referred_to_address[n]
    check logical op (no V change, no C change, N, Z and A set correctly)

    repeat for all m, n, op_type

    for n we could use memory addresses:
    #, 0x10, 0x1234, (0x12)+y, (0xf8+x), 0xfa+x, 0x12f8+x, 0x12fa+y

    With x, y causing page crosses for some times, we need two sets of x/y: x=16, y=4, and vice versa
    Hence the addresss would be:

    #, 0x10, 0x1234, (0x12)+y=0x12fc, (0xf8+x)=0x11fc, 0xfa+x=0x0a, 0x12f8+x=0x1308, 0x12fa+y=0x12fe
    #, 0x10, 0x1234, (0x12)+y=0x1308, (0xf8+x)=0x11f0, 0xfa+x=0xfe, 0x12f8+x=0x12fc, 0x12fa+y=0x130a
    This requires 0x08=0xfc, 0x09=0x11, 0x12=0xf8, 0x13=0x12, 0xfc=0xf0, 0xfd=0x11
    and data in 0x06, 0x10, 0xfe, 0x11f0, 0x11fc, 0x1234, 0x12fc, 0x12fe, 0x1308, 0x130a
    """
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:(a|b,c,v)
    op = "ora"
                # test with ora, and, eor
                # test with adc, sbc, cmp
                # test with ld/st
                # test with asl,lsr,rol,ror,inc,dec
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn)
    verbose = False

#c test_6502_addressing_logical_and
class test_6502_addressing_logical_and(c_6502_test):
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:(a&b,c,v)
    op = "and"
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn)
    verbose = False

#c test_6502_addressing_logical_eor
class test_6502_addressing_logical_eor(c_6502_test):
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:(a^b,c,v)
    op = "eor"
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn)
    verbose = False

#c test_6502_addressing_logical_adc
class test_6502_addressing_logical_adc(c_6502_test):
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:c_6502_test.add_op(a,b,c,v)
    op = "adc"
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn)
    verbose = False

#c test_6502_addressing_logical_sbc
class test_6502_addressing_logical_sbc(c_6502_test):
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:c_6502_test.add_op(a,0xff^b,c,v)
    op = "sbc"
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn)
    verbose = False

#c test_6502_addressing_logical_lda
class test_6502_addressing_logical_lda(c_6502_test):
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:(b,c,v)
    op = "lda"
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn)
    verbose = False

#c test_6502_addressing_logical_cmp
class test_6502_addressing_logical_cmp(c_6502_test):
    #b Start
    num_cycles = 80000
    op_fn = lambda a,b,c,v:c_6502_test.add_op(a,0xff^b,1,v)
    op = "cmp"
    src, expected_memory_data = c_6502_test.addressing_mode_test(op, op_fn, change_acc=False, change_v=False)
    verbose = False

#c test_6502_sta
class test_6502_sta(c_6502_test):
    num_cycles = 5000
    src = """. = $fffb
    jmp code_start
    . = $400
    code_start:
        ldx #4
        ldy #6
        lda #2
        sta 0x00
        bit 0x00 ; clear N, clear V, clear Z
        clc
        sta 0x80
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta 0x7d, x ; 0x80,0x81 = 0x0202
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta 0x100,x ; 0x104
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta 0x100,y ; 0x106
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta 0x2fe,x ; 0x302
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta 0x2ff,y ; 0x305
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta (0x80), y ; 0x0208
        bcs fail
        bvs fail
        beq fail
        bmi fail
        sta (0x7c, x) ; 0x0202
        bcs fail
        bvs fail
        beq fail
        bmi fail
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34), (0x80,2), (0x81,2), (0x104,2), (0x106,2), (0x302,2), (0x305,2), (0x202,2), (0x208,2)]
    verbose = False

#c test_6502_sta_flags_set
class test_6502_sta_flags_set(c_6502_test):
    num_cycles = 5000
    src = """. = $fffb
    jmp code_start
    . = $400
    code_start:
        ldx #4
        ldy #6
        lda #0xcc
        sta 0x00
        lda #2
        bit 0x00 ; set N, set V, set Z
        sec
        sta 0x80
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta 0x7d, x ; 0x80,0x81 = 0x0202
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta 0x100,x
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta 0x100,y
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta 0x2fe,x
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta 0x2ff,y
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta (0x80), y ; 0x0208
        bcc fail
        bvc fail
        bne fail
        bpl fail
        sta (0x7c, x) ; 0x0202
        bcc fail
        bvc fail
        bne fail
        bpl fail
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34), (0x80,2), (0x81,2), (0x104,2), (0x106,2), (0x302,2), (0x305,2), (0x202,2), (0x208,2)]
    verbose = False

#c test_6502_coverage
class test_6502_coverage(c_6502_test):
    num_cycles = 5000
    src = """. = $fffb
    jmp code_start
    . = $400
    code_start:
        ldx #0xff

        lda #0xcc
        sta 0x00
        lda #2
        bit 0x00 ; set N, set V, set Z
        sec

        txs
        bcc fail1
        bvc fail1
        bne fail1
        bpl fail1
        php
        bcc fail1
        bvc fail1
        bne fail1
        bpl fail1
        pha
        bcc fail1
        bvc fail1
        bne fail1
        bpl fail1

        lda #2
        sta 0x00
        bit 0x00 ; clear N, clear V, clear Z
        clc

        txs
        bcs fail1
        bvs fail1
        beq fail1
        bmi fail1
        php
        bcs fail1
        bvs fail1
        beq fail1
        bmi fail1
        pha
        bcs fail1
        bvs fail1
        beq fail1
        bmi fail1

        jmp cont1
    fail1: jmp fail
    cont1:

        ldy #0
        lda #2
        sta 0x00
        bit 0x00 ; clear N, clear V, clear Z
        clc
        tya ; should set Z, rest clear
        bcs fail2
        bvs fail2
        bne fail2
        bmi fail2

        ldy #0x80
        lda #2
        sta 0x00
        bit 0x00 ; clear N, clear V, clear Z
        clc
        tya ; should clear Z, set N, rest clear
        bcs fail2
        bvs fail2
        beq fail2
        bpl fail2

        ldx #0
        lda #2
        sta 0x00
        bit 0x00 ; clear N, clear V, clear Z
        clc
        txa ; should set Z, rest clear
        bcs fail2
        bvs fail2
        bne fail2
        bmi fail2

        ldx #0x80
        lda #2
        sta 0x00
        bit 0x00 ; clear N, clear V, clear Z
        clc
        txa ; should clear Z, set N, rest clear
        bcs fail2
        bvs fail2
        beq fail2
        bpl fail2


        jmp cont2
    fail2: jmp fail
    cont2:

        lda #0
        pha

        lda #0
        plp
        php ; all flags clear

        tay ; should set Z, rest clear
        bcs fail2
        bvs fail2
        bne fail2
        bmi fail2

        lda #2
        plp
        php ; all flags clear

        tay ; should clear all flags
        bcs fail2
        bvs fail2
        beq fail2
        bmi fail2

        lda #0x80
        plp
        php ; all flags clear

        tay ; should set N, clear all others
        bcs fail2
        bvs fail2
        beq fail2
        bpl fail2

        lda #0
        plp
        php ; all flags clear

        tax ; should set Z, rest clear
        bcs fail2
        bvs fail2
        bne fail2
        bmi fail2

        lda #2
        plp
        php ; all flags clear

        tax ; should clear all flags
        bcs fail2
        bvs fail2
        beq fail2
        bmi fail2

        lda #0x80
        plp
        php ; all flags clear

        tax ; should set N, clear all others
        bcs fail2
        bvs fail2
        beq fail2
        bpl fail2

        jmp cont3
    fail3: jmp fail
    cont3:

        lda #0xc3
        pha

        lda #0
        plp
        php ; all flags set

        tay ; should set Z, clear N, CV set
        bcc fail3
        bvc fail3
        bne fail3
        bmi fail3

        lda #2
        plp
        php ; all flags set

        tay ; should clear all flags, CV set
        bcc fail3
        bvc fail3
        beq fail3
        bmi fail3

        lda #0x80
        plp
        php ; all flags set

        tay ; should set N, C, V, clear Z
        bcc fail3
        bvc fail3
        beq fail3
        bpl fail3

        lda #0
        plp
        php ; all flags set

        tax ; should set Z, clear N, set VC
        bcc fail3
        bvc fail3
        bne fail3
        bmi fail3

        lda #2
        plp
        php ; all flags set

        tax ; should clear all NZ, set VC
        bcc fail3
        bvc fail3
        beq fail3
        bmi fail3

        lda #0x80
        plp
        php ; all flags set

        tax ; should set N, C, V, clear Z
        bcc fail3
        bvc fail3
        beq fail3
        bpl fail3

                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_mem_loop256
class test_6502_mem_loop256(c_6502_test):
    num_cycles = 5000
    src_args = (0x200,)
    src = """. = $fffc
    dcw code_start
    . = $%x
    code_start:lda #2
               sta 0x00
               ldx #1
               sta 0x00, x
        ldx #0x00
    clear_zero:
        txa
        sta 0x00, x
        dex
        bne clear_zero
    done:
    jmp done
    """
    expected_memory_data = [(i,i) for i in range(256)]

#c test_6502_mem_loop256_cross_page
class test_6502_mem_loop256_cross_page(test_6502_mem_loop256):
    num_cycles = 5000
    src_args = (0x2f4,)

#c test_6502_bit
class test_6502_bit(c_6502_test):
    """
    Test bit zpg, bit abs
    N = zpg[7], V=zpg[6], Z=((A and zpg)==0)
    Kinda like AND and ROL ish?
    """
    logic_data = (0xff,0xfe,0x80,0x40,0xf0,0x1,0)
    num_cycles = 50000
    src = """. = $fffb
    jmp code_start
    """
    mem_data = (0,1,2,3,4,8,16,32,64,128,0xff,0xfe,0xfd,0xfb,0xf7,0xef,0xdf,0xbf,0x7f)
    acc_data = (0,1,2,3,7,15,31,63,127,255,128,64,32,16,8,4)
    src += ". = $0\n"
    for md in mem_data:
        src += " dcb $%02x\n"%md
        pass
    src += ". = $feff\n"
    for md in mem_data:
        src += " dcb $%02x\n"%md
        pass
    src += """
    . = $200
    code_start:
       """
    for mda in range(len(mem_data)):
        md = mem_data[mda]
        for (mdb, mdb_l) in ((0,"zp"), (0xfeff,"abs")):
            for acc in acc_data:
                src_l = """
                clc
                lda #{0}
                bit {1}
                b{5} {3}
                b{6} {3}
                b{7} {3}
                bcs {3}
                sec
                bit {1}
                bcc {3}
                cmp #{0}
                bne {3}
                lda {1}
                cmp #{2}
                bne {3}
                jmp {4}
                {3}: jmp fail
                {4}:
                """
                label = "l_%02x_%02x_%s"%(acc,mda,mdb_l)
                fail_label = label + "_fail"
                pass_label = label + "_pass"
                mi_or_pl = ["mi","pl"][0 or ((md&128)!=0)]
                vs_or_vc = ["vs","vc"][0 or ((md&64)!=0)]
                eq_or_ne = ["eq","ne"][0 or ((md&acc)==0)]
                src += src_l.format(acc, mda+mdb, md, fail_label, pass_label, mi_or_pl, vs_or_vc, eq_or_ne)
                pass
            pass
        pass
    src += """
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    for i in range(len(mem_data)):
        if i<2: continue
        expected_memory_data.append((i,mem_data[i]))
        pass
    verbose = False

#c test_6502_nop
class test_6502_nop(c_6502_test):
    """
    Test nop (ea)
    """
    num_cycles = 5000
    src = """. = $fffb
    jmp code_start
    . = $200
    code_start:
        ldx #2
        ldy #3
        txs
        lda #$c3
        pha
        lda #1
        plp
        php
        dcb $ea
        bne fail
        bpl fail
        bvc fail
        bcc fail
        cmp #1
        bne fail
        cpx #2
        bne fail
        cpy #3
        bne fail
        pla
        cmp #0xc3
        bne fail
                jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_brk_rti
class test_6502_brk_rti(c_6502_test):
    num_cycles = 5000
    src = """. = $fffa
    dcw nmi_start
    dcw code_start
    dcw irq_start
    . = $200
    code_start:
        ldx #0xff
        txs
        clv
        clc
        lda #0x14
        dcb 0 ; brk
        dcb 0x4c
        clv
        sec
        lda #0x15
        dcb 0 ; brk
        dcb 0 ; brk
        clv
        sec
        cli
        lda #0x11
        dcb 0 ; brk
        dcb 0 ; brk
        clv
        clc
        cli
        lda #0x10
        dcb 0 ; brk
        dcb 0 ; brk
        clv
        clc
        cli
        lda #0x90
        dcb 0 ; brk
        dcb 0 ; brk
        clv
        sec
        sei
        lda #0x95
        dcb 0 ; brk
        dcb 0 ; brk
        dcb 0 ; brk
        dcb 0 ; brk
        jmp pass

    nmi_start:
        jmp fail
    irq_start:
        sta $40
        pla
        pha
        cmp $40
        bne fail
        dcb 0x40 ; rti
    
    """

    #b Trailer
    src +=  """       
            jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    verbose = False

#c test_6502_nmi
class test_6502_nmi(c_6502_test):
    num_cycles = 50000
    src = """. = $fffa
    dcw nmi_start
    dcw code_start
    dcw irq_start
    . = $400
    code_start:
        cli
        ldx #0
        lda #53
    loop:
        sta 0x00, x
        sei
        pha
        and #0x13
        cli
        bne skip
    skip:
        sei
        jsr subroutine
        cli
        pla
        tay
        iny
        tya
        dex
        bne loop
        jmp pass
    subroutine:
        pha
        pla
        rts

    nmi_start:
        dcb 0x40 ; rti

    irq_start:
        pha
        txa
        pha
        tya
        pha
        sec
        lda #0xc0
        sta 0x200
        bit 0x200
        pla
        tay
        pla
        tax
        pla
        dcb 0x40 ; rti
    
    """

    #b Trailer
    src +=  """       
            jmp pass

    pass:
                lda #0x12
                sta 0x00
                lda #0x34
                sta 0x01
                jmp done
    fail:
                lda #0
                sta 0x00
                sta 0x01
    done: jmp done
    """
    expected_memory_data = [(0,0x12), (1,0x34)]
    for i in range(2,255):
        x = 256-i
        a = (53+i)&0xff
        expected_memory_data.append((x,a))
        pass
    verbose = False

#c Test6502Base
class Test6502Base(unittest.TestCase):
    auto_test_classes = []
    #c c_compiled_test
    class c_compiled_test(object):
        def __init__(self,test, load_data, num_cycles, expected_memory_data, verbose):
            self.test = test
            self.load_data = load_data
            self.num_cycles = num_cycles
            self.expected_memory_data = expected_memory_data
            self.verbose = verbose
            pass
        pass
    #f compile_cpu_test
    def compile_cpu_test(self, test=None, data=[], num_cycles=20, expected_memory_data=None, verbose=False):
        if test is not None:
            data=[("src",0,test.src%test.src_args)]
            num_cycles = test.num_cycles
            expected_memory_data = test.expected_memory_data
            verbose = test.verbose
            pass
        ass = c_assembler(c_6502_instruction_set())
        load_data = []
        for d in data:
            if d[0] == "src":
                code = ass.assemble(base_address=d[1], program=d[2])
                for (s,e,m) in code:
                    load_data.append( (s,m) )
                pass
            else:
                load_data.append( (d[1],d[2]) )
                pass
            pass
        return Test6502Base.c_compiled_test(test, load_data, num_cycles, expected_memory_data, verbose)
    #f run_cpu_test
    def run_cpu_test(self, test=None, data=[], num_cycles=20, expected_memory_data=None, verbose=False):
        compiled_test = self.compile_cpu_test(test, data, num_cycles, expected_memory_data, verbose)
        system = c_system()
        for (s,m) in compiled_test.load_data:
            system.memory.add_code(s,m)
            pass
        for i in range(compiled_test.num_cycles):
            system.tick(verbose=compiled_test.verbose)
            pass
        if compiled_test.expected_memory_data is not None:
            system.memory.dump(0)
            for (a,e) in compiled_test.expected_memory_data:
                v = system.memory.read(a)
                self.assertEqual(v,e,"Expected address %04x to have data %02x but had %02x"%(a,e,v))
                pass
            pass
        pass
    #f get_subclasses
    @classmethod
    def get_subclasses(cls):
        r = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if (issubclass(obj, cls)) and (obj is not cls):
                    r.append(obj)
                    pass
                pass
            pass
        return r
    #f create_tests
    @classmethod
    def create_tests(cls):
        for t in cls.auto_test_classes:
            def run_test(self, test=t):
                self.run_cpu_test(test)
                pass
            setattr( cls, "test_atc_%s"%(t.__name__), run_test )
            pass
        pass
    #f create_subclass_tests
    @classmethod
    def create_subclass_tests(cls):
        for tc in cls.get_subclasses():
            tc.create_tests()
            pass
        pass
    #f All done
    pass

#c Test6502_Base
class Test6502_Base(Test6502Base):
    auto_test_classes = ( test_6502_simplest,
                          test_6502_nop,
                          test_6502_coverage,
                          )

#c Test6502_Reg
class Test6502_Reg(Test6502Base):
    auto_test_classes = ( test_6502_xy_reg,
                          )

#c Test6502_ALU
class Test6502_ALU(Test6502Base):
    auto_test_classes = ( test_6502_adc,
                          test_6502_adds,
                          test_6502_logical,
                          test_6502_addsub,
                          test_6502_cmp,
                          test_6502_shift,
                          test_6502_incdec,
                          test_6502_bit,
                          )

#c Test6502_Memory
class Test6502_Memory(Test6502Base):
    auto_test_classes = ( test_6502_mem_loop256,
                          test_6502_mem_loop256_cross_page,
                          )

#c Test6502_Stack
class Test6502_Stack(Test6502Base):
    auto_test_classes = ( test_6502_stack,
                          test_6502_push_pull,
                          test_6502_flags,
                          )

#c Test6502_Branch
class Test6502_Branch(Test6502Base):
    auto_test_classes = ( test_6502_branches,
                          )

#c Test6502_Addressing
class Test6502_Addressing(Test6502Base):
    auto_test_classes = ( test_6502_addressing_logical_ora,
                          test_6502_addressing_logical_and,
                          test_6502_addressing_logical_eor,
                          test_6502_addressing_logical_adc,
                          test_6502_addressing_logical_sbc,
                          test_6502_addressing_logical_lda,
                          test_6502_addressing_logical_cmp,
                          test_6502_sta,
                          test_6502_sta_flags_set,
                          )

#c Test6502_Interrupt
class Test6502_Interrupt(Test6502Base):
    auto_test_classes = ( test_6502_brk_rti,
                          test_6502_nmi,
                          )

#c Tests
Test6502Base.create_subclass_tests()

#a Toplevel
if __name__=="__main__":
    unittest.main()

