#!/usr/bin/env python

sign_bit = 1<<31
mask64 = 0xffffffffffffffff
mask32 = 0xffffffff
mask31 = 0x7fffffff
ah_0_zero     = 0
ah_0_acc      = 1
ah_0_abs_a_in = 2
ah_0_neg_a_in = 3

ah_1_zero     = 0
ah_1_shf      = 1
ah_1_abs_b_in = 2
ah_1_neg_b_in = 3

al_1_zero = 0
al_1_acc  = 1

a_reg_hold = 0
a_reg_a_in = 1
a_reg_abs_a_in = 2
a_reg_b_shf = 3

b_reg_hold = 0
b_reg_b_in = 1
b_reg_abs_b_in = 2

#c multdiv
class multdiv:
    """
    The basic data path is a multiplier/shifter, which feeds a 64-bit value to two 32-bit adders (low and high) which may be chained.

    The multiplier uses the multitplier/shifter to multiply the 'b_reg' by 0-15 * 2^4N and accumulate a result

    The divider uses the multiplier/shifter in a first step to left-shift the divisor by 2^N and the low adder to negate it.

    The divider uses the multiplier/shifter in its divide step to generate 1<<N and the adder to add -divisor to the current remainder and the shifter result to the result, storing conditionally on the carry from the low adder

    """
    #f __init__
    def __init__(self):
        self.accumulator = 0 # 64 bits
        self.stage = 0 # 4 bits (maybe 5)
        self.a_reg = 0
        self.b_reg = 0
    #f comb_new
    def comb_new(self, a_in, b_in, mult4, shf, ah_0, ah_1, al_1, set_bit, bit_to_set, carry_chain, ar, br):
        mult4 = mult4 & 15
        shf = shf & 7
        sel0123 = mult4 & 3
        sel048c = (mult4>>2) & 3
        stage1_0 = 0
        stage1_1 = self.b_reg
        stage1_2 = self.b_reg<<1
        stage1_3 = stage1_2 + stage1_1 # 34-bit ADDER
        stage1_4 = stage1_1 << 2
        stage1_8 = stage1_2 << 2
        stage1_c = stage1_3 << 2
        if sel0123==0: mux_0123 = stage1_0
        if sel0123==1: mux_0123 = stage1_1
        if sel0123==2: mux_0123 = stage1_2
        if sel0123==3: mux_0123 = stage1_3
        if sel048c==0: mux_048c = stage1_0
        if sel048c==1: mux_048c = stage1_4
        if sel048c==2: mux_048c = stage1_8
        if sel048c==3: mux_048c = stage1_c
        mult_result = mux_0123 + mux_048c # 36-bit adder

        shf_hl = mult_result << (4*shf)
        shf_l = shf_hl & mask32
        shf_h = (shf_hl>>32) & mask32

        acc_l = self.accumulator & mask32
        acc_h = (self.accumulator>>32) & mask32

        a_in = a_in & mask32
        neg_a_in = (-a_in) & mask32
        abs_a_in = a_in
        if (a_in & sign_bit): abs_a_in = neg_a_in

        b_in = b_in & mask32
        neg_b_in = (-b_in) & mask32
        abs_b_in = b_in
        if (b_in & sign_bit): abs_b_in = neg_b_in

        alu_h_in_0 = 0 # mul_init
        if ah_0 == ah_0_acc:      alu_h_in_0 = acc_h    # mul_step, div_step
        if ah_0 == ah_0_abs_a_in: alu_h_in_0 = abs_a_in # UNUSED
        if ah_0 == ah_0_neg_a_in: alu_h_in_0 = neg_a_in # mul_init

        alu_h_in_1 = 0 # mul_init
        if ah_1 == ah_1_shf:      alu_h_in_1 = shf_h    # mul_step
        if ah_1 == ah_1_abs_b_in: alu_h_in_1 = abs_b_in # UNUSED
        if ah_1 == ah_1_neg_b_in: alu_h_in_1 = neg_b_in # mul_init

        alu_l_in_0 = shf_l # optional negate?

        alu_l_in_1 = 0 # mul_init
        if al_1 == al_1_acc:      alu_l_in_1 = acc_l    # mul_step, div_step

        alu_l = alu_l_in_0 + alu_l_in_1 # optional carry in?
        alu_l_carry = (alu_l >> 32) & 1
        alu_l = alu_l & mask32

        alu_h = alu_h_in_0 + alu_h_in_1
        if carry_chain: alu_h = alu_h + alu_l_carry
        alu_h_carry = (alu_h >> 32) & 1
        alu_h = alu_h & mask32

        next_acc_l = alu_l
        next_acc_h = alu_h
        if set_bit: next_acc_h = alu_h | (1<<bit_to_set)

        next_a_reg = self.a_reg
        if ar == a_reg_a_in:     next_a_reg = a_in
        if ar == a_reg_abs_a_in: next_a_reg = abs_a_in
        if ar == a_reg_b_shf:    next_a_reg = b_reg << shfb #  UNUSED

        next_b_reg = self.b_reg
        if br == b_reg_b_in:     next_b_reg = b_in
        if br == b_reg_abs_b_in: next_b_reg = abs_b_in

        #print "%08x %08x"%(next_a_reg, next_b_reg)
        return (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry)

    #f mul_init_new
    def mul_init_new(self, a, b, sa=False, sb=False):
        ah_0=ah_0_zero
        ah_1=ah_1_zero
        if sa and (a & sign_bit): ah_1 = ah_1_neg_b_in
        if sb and (b & sign_bit): ah_0 = ah_0_neg_a_in
        results = self.comb_new(a_in=a, b_in=b, mult4=0, shf=0, ah_0=ah_0, ah_1=ah_1, al_1=al_1_zero, set_bit=False, bit_to_set=0, carry_chain=False, ar=a_reg_a_in, br=b_reg_b_in )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.a_reg = next_a_reg
        self.b_reg = next_b_reg
        self.stage = 0
        pass

    #f mul_step_new
    def mul_step_new(self):
        results = self.comb_new(a_in=0, b_in=0, mult4=self.a_reg&0xf, shf=self.stage, ah_0=ah_0_acc, ah_1=ah_1_shf, al_1=al_1_acc, set_bit=False, bit_to_set=0, carry_chain=True, ar=a_reg_hold, br=b_reg_hold )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.b_reg = next_b_reg
        self.a_reg = self.a_reg >> 4 # next_b_reg
        self.stage = self.stage + 1
        return self.a_reg==0

    #f div_init_new
    def div_init_new(self, a, b, signed=False):
        """
        Get abs of a and b if signed, else just a and b
        Determine shift
        """
        self.negate_result    = False
        self.negate_remainder = False
        if signed:
            results = self.comb_new(a_in=a, b_in=b, mult4=0, shf=0, ah_0=ah_0_zero, ah_1=ah_1_zero, al_1=al_1_zero, set_bit=False, bit_to_set=0, carry_chain=False, ar=a_reg_abs_a_in, br=b_reg_abs_b_in )
            self.negate_remainder = ((a & sign_bit)!=0)
            self.negate_result    = (((a ^ b) & sign_bit)!=0)
        else:
            results = self.comb_new(a_in=a, b_in=b, mult4=0, shf=0, ah_0=ah_0_zero, ah_1=ah_1_zero, al_1=al_1_zero, set_bit=False, bit_to_set=0, carry_chain=False, ar=a_reg_a_in, br=b_reg_b_in )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.a_reg = next_a_reg
        self.b_reg = next_b_reg
        self.stage = 0
        self.a_shift = 0
        self.b_shift = 0
        for i in range(32):
            if self.a_reg&(1<<i): self.a_shift = 31-i
            if self.b_reg&(1<<i): self.b_shift = 31-i
            pass
        self.b_shift = self.b_shift - self.a_shift
        self.a_shift = 0
        #print "%08x %08x %016x %d %d"%(self.a_reg, self.b_reg, self.accumulator, self.a_shift, self.b_shift)
        pass

    #f div_shift
    def div_shift(self):
        results = self.comb_new(a_in=0, b_in=0, mult4=1<<(self.b_shift&3), shf=self.b_shift>>2, ah_0=ah_0_zero, ah_1=ah_1_zero, al_1=al_1_zero, set_bit=False, bit_to_set=0, carry_chain=False, ar=a_reg_abs_a_in, br=b_reg_abs_b_in )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.b_reg = (-self.b_reg) & mask32
        self.accumulator = self.a_reg
        #print "%08x %08x %016x"%(self.a_reg, self.b_reg, self.accumulator)
        self.stage = self.b_shift
        return self.stage<0

    #f div_step_new
    def div_step_new(self):
        results = self.comb_new(a_in=0, b_in=0, mult4=1<<(self.stage&3), shf=(self.stage>>2), ah_0=ah_0_acc, ah_1=ah_1_zero, al_1=al_1_acc, set_bit=(self.stage>=0), bit_to_set=self.stage, carry_chain=False, ar=a_reg_abs_a_in, br=b_reg_abs_b_in )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        #print "%d:%1d:%08x %08x"%(self.stage,alu_l_carry, next_acc_l, next_acc_h)
        if (alu_l_carry==1) or (next_acc_l==0):
            self.accumulator = next_acc_l | (next_acc_h<<32)
        self.stage = self.stage-1
        #print "%08x %08x %016x"%(self.a_reg, self.b_reg, self.accumulator)
        return (self.stage<0) or (next_acc_l==0)

    #f div_remainder
    def div_remainder(self, a, b, signed=False):
        remainder = self.accumulator & mask32
        if self.negate_remainder: return (-remainder) & mask32
        return remainder
    #f div_result
    def div_result(self, a, b, signed=False):
        result = (self.accumulator>>32) & mask32
        if self.negate_result: return (-result) & mask32
        return result

#a Toplevel
def test_mult(test_a,test_b):
    test_a = test_a & mask32
    test_b = test_b & mask32
    for (sa,sb) in [(False,False),(True,True), (False,True), (True,False)]:
        for (na,nb) in [(1,1), (-1,1), (1,-1), (-1,-1)]:
            a = (na * test_a) & mask32
            b = (nb * test_b) & mask32
            if (a & sign_bit): a = a - (1<<32)
            if (b & sign_bit): b = b - (1<<32)
            x = multdiv()
            x.mul_init_new(a,b,sa,sb)
            while not x.mul_step_new():
                pass
            r = x.accumulator
            m = (a&mask32) * (b&mask32) # unsigned
            if sa and sb:m = (a * b)&mask64 # signed
            if sa and (not sb):m = (a * (b & mask32))&mask64
            if sb and (not sa):m = (b * (a & mask32))&mask64
            err = ""
            if (r!=m) : err = "DIFFERENT"
            print("%08x*%08x : %13d * %13d : %26d : %016x  (%016x) %s" % ((a&mask32),(b&mask32),a,b,r,r,m,err))

def test_div(test_a,test_b):
    test_a = test_a & mask32
    test_b = test_b & mask32
    for signed in [False, True]:
        for (na,nb) in [(1,1), (-1,1), (1,-1), (-1,-1)]:
            a = (na * test_a) & mask32
            b = (nb * test_b) & mask32
            if (a & sign_bit): a = a - (1<<32)
            if (b & sign_bit): b = b - (1<<32)
            x = multdiv()
            x.div_init_new(a,b,signed)
            x.div_shift()
            #x.div_step_new()
            #x.div_init(a,b,signed)
            while not x.div_step_new():
                #x.div_step():
                pass
            r = x.div_result(a,b,signed)
            rem = x.div_remainder(a,b,signed)
            m    = (a&mask32) / (b&mask32) # unsigned
            if signed:
                m    = (a/b) & mask32
                if (m & sign_bit): m = (m+1) & mask32
            mrem = (a - (b * m)) & mask32
            err = ""
            if (r!=m) :  err += "DIFF RES"
            if (rem!=mrem) : err = "DIFF REM"
            print("%d %08x/%08x : %13d / %13d : %13d %13d: %08x %08x  (%08x %08x) %s" % (signed,(a&mask32),(b&mask32),a,b,r,rem,r,rem,m,mrem,err))

if True:
    test_mult(4,5)
    test_mult(0x40000000,5)
    test_mult(5,0x40000000)
    test_mult(0x89abcdef,5)
    test_mult(5,0x89abcdef)
    test_mult(0x12345670,0xdeadbeef)
    test_mult(0xdeadbeef,0x12345670)

if True:
    test_div(4,5)
    test_div(0x40000000,5)
    test_div(5,0x40000000)
    test_div(0x89abcdef,5)
    test_div(5,0x89abcdef)
    test_div(0x12345670,0xdeadbeef)
    test_div(0xdeadbeef,0x12345670)
