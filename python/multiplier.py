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
    #f __init__
    def __init__(self):
        self.accumulator = 0 # 64 bits
        self.multiplier = 0 # 32 bits
        self.multiplicand = 0 # 32 bits
        self.stage = 0 # 4 bits (maybe 5)
        self.a_reg = 0
        self.b_reg = 0
    #f comb_new
    def comb_new(self, a_in, b_in, mult4, shf, ah_0, ah_1, al_1, set_bit, bit_to_set, carry_chain, ar, br):
        sel0123 = mult4 & 3
        sel048c = (mult4>>2) & 3
        stage1_0 = 0
        stage1_1 = self.a_reg
        stage1_2 = self.a_reg<<1
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

        alu_h_in_0 = 0
        if ah_0 == ah_0_acc:      alu_h_in_0 = acc_h
        if ah_0 == ah_0_abs_a_in: alu_h_in_0 = abs_a_in
        if ah_0 == ah_0_neg_a_in: alu_h_in_0 = neg_a_in

        alu_h_in_1 = 0
        if ah_1 == ah_1_shf:      alu_h_in_1 = shf_h
        if ah_1 == ah_1_abs_b_in: alu_h_in_1 = abs_b_in
        if ah_1 == ah_1_neg_b_in: alu_h_in_1 = neg_b_in

        alu_l_in_0 = shf_l

        alu_l_in_1 = 0
        if al_1 == al_1_acc:      alu_l_in_1 = acc_l

        #print "%08x %016x %08x %08x %d"%(stage1_1, shf_hl, alu_l_in_0, alu_l_in_1, mult4)

        alu_l = alu_l_in_0 + alu_l_in_1
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
        if ar == a_reg_b_shf:    next_a_reg = b_reg << shfb

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
        results = self.comb_new(a_in=0, b_in=0, mult4=self.b_reg&0xf, shf=self.stage, ah_0=ah_0_acc, ah_1=ah_1_shf, al_1=al_1_acc, set_bit=False, bit_to_set=0, carry_chain=True, ar=a_reg_hold, br=b_reg_hold )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.a_reg = next_a_reg
        self.b_reg = self.b_reg >> 4 # next_b_reg
        self.stage = self.stage + 1
        return self.b_reg==0

    #f div_init_new
    def div_init_new(self, a, b, signed=False):
        results = self.comb_new(a_in=a, b_in=b, mult4=0, shf=0, ah_0=ah_0_zero, ah_1=ah_1_zero, al_1=al_1_zero, set_bit=False, bit_to_set=0, carry_chain=False, ar=a_reg_abs_a_in, br=b_reg_abs_b_in )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.a_reg = next_a_reg
        self.b_reg = next_b_reg
        self.stage = 0
        pass

    #f div_shift
    def div_shift(self):
        results = self.comb_new(a_in=a, b_in=b, mult4=0, shf=0, ah_0=ah_0_zero, ah_1=ah_1_zero, al_1=al_1_zero, set_bit=False, bit_to_set=0, carry_chain=False, ar=a_reg_abs_a_in, br=b_reg_abs_b_in )
        (next_acc_l, next_acc_h, next_a_reg, next_b_reg, alu_l_carry) = results
        self.accumulator = next_acc_l | (next_acc_h<<32)
        self.a_reg = next_a_reg
        self.b_reg = next_b_reg
        self.stage = 0
        pass

    #f combinatorial
    def combinatorial(self, mult4, areg, subtract_acc, acc, shift):
        sel0123 = mult4 & 3
        sel048c = (mult4>>2) & 3
        stage1_0 = 0
        stage1_1 = areg
        stage1_2 = areg<<1
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
        stage2 = mux_0123 + mux_048c # 36-bit adder
        if subtract_acc:
            acc_result = ((stage2<<shift) - acc) & mask64
            pass
        else:
            acc_result = ((stage2<<shift) + acc) & mask64
            pass
        return acc_result

    #f div_init
    def div_init(self, a, b, signed=False):
        self.divisor      = b & mask32
        self.stage = 0
        self.accumulator = (a&mask32)<<32
        while (self.divisor & sign_bit)==0:
            self.divisor  = self.divisor<<1
            self.stage = self.stage + 1
            pass
        while (self.accumulator & (sign_bit<<32))==0:
            self.accumulator  = self.accumulator<<1
            self.stage = self.stage - 1
            pass
        print "%08x %08x  %016x %08x %d"%(a&mask32,b&mask32,self.accumulator,self.divisor,self.stage)
        pass
    #f mul_init
    def mul_init(self, a, b, sa=False, sb=False):
        self.multiplier   = a & mask32
        self.multiplicand = b & mask32
        self.stage = 0
        acc_in = 0
        add_in = 0
        if (sa and (a&sign_bit)):
            acc_in = (b&mask32)<<32
            if sb: acc_in = acc_in & (mask31<<32)
        if (sb and (b&sign_bit)):
            add_in = a&mask32
            if sa: add_in = add_in & mask31
        next_acc = self.combinatorial(mult4=1, areg=add_in, subtract_acc=0, acc=acc_in, shift=32)
        self.accumulator = next_acc & mask64
        pass
    #f mul_step
    def mul_step(self):
        next_acc = self.combinatorial(mult4 = self.multiplier & 15,
                                      areg = self.multiplicand,
                                      subtract_acc = (self.stage==0),
                                      acc = self.accumulator,
                                      shift = self.stage*4)
        self.accumulator = next_acc
        self.stage = self.stage + 1
        self.multiplier = self.multiplier >> 4
        return (self.multiplier==0)
    #f div_init
    def div_init(self, a, b, signed=False):
        self.divisor      = b & mask32
        self.stage = 0
        self.accumulator = (a&mask32)<<32
        while (self.divisor & sign_bit)==0:
            self.divisor  = self.divisor<<1
            self.stage = self.stage + 1
            pass
        while (self.accumulator & (sign_bit<<32))==0:
            self.accumulator  = self.accumulator<<1
            self.stage = self.stage - 1
            pass
        self.accumulator = -self.accumulator # Mask bottom 32 is unnecessary since acc is <<32... & (mask32<<32)
        print "%08x %08x  %016x %08x %d"%(a&mask32,b&mask32,self.accumulator,self.divisor,self.stage)
        pass
    #f div_step
    def div_step(self): # uses 64-bit accumulator adder
        next_acc = self.combinatorial( mult4 = 1,
                                       shift = 32,
                                       subtract_acc = False,
                                       acc = self.accumulator,
                                       areg = self.divisor )
        if ((next_acc<0) and (self.stage>=0)):
            next_acc = next_acc + (1<<self.stage)
            self.accumulator = next_acc
            pass
        self.divisor  = self.divisor >> 1
        self.stage = self.stage-1
        return self.stage<0
    #f div_remainder
    def div_remainder(self, a, b, signed=False):
        return (self.accumulator>>32) & mask32
    #f div_result
    def div_result(self, a, b, signed=False):
        return self.accumulator & mask32

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
    for signed in [False]: #,True]:
        for (na,nb) in [(1,1), (-1,1), (1,-1), (-1,-1)]:
            a = (na * test_a) & mask32
            b = (nb * test_b) & mask32
            if (a & sign_bit): a = a - (1<<32)
            if (b & sign_bit): b = b - (1<<32)
            x = multdiv()
            x.div_init(a,b,signed)
            while not x.div_step():
                pass
            r = x.div_result(a,b,signed)
            rem = x.div_remainder(a,b,signed)
            m    = (a&mask32) / (b&mask32) # unsigned
            mrem = (a&mask32) % (b&mask32) # unsigned
            err = ""
            if (r!=m) : err = "DIFFERENT"
            print("%08x/%08x : %13d / %13d : %13d %13d: %08x %08x  (%08x %08x) %s" % ((a&mask32),(b&mask32),a,b,r,rem,r,rem,m,mrem,err))

if True:
    test_mult(4,5)
    test_mult(0x40000000,5)
    test_mult(5,0x40000000)
    test_mult(0x89abcdef,5)
    test_mult(5,0x89abcdef)
    test_mult(0x12345670,0xdeadbeef)
    test_mult(0xdeadbeef,0x12345670)

if False:
    test_div(4,5)
    test_div(0x40000000,5)
    test_div(5,0x40000000)
    test_div(0x89abcdef,5)
    test_div(5,0x89abcdef)
    test_div(0x12345670,0xdeadbeef)
    test_div(0xdeadbeef,0x12345670)
