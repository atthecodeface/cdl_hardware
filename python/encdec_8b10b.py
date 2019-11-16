#!/usr/bin/env python
def count_ones(n, sum=0):
    if n==0: return sum
    if n&1: return count_ones(n/2,sum+1)
    return count_ones(n/2,sum)

class encoding:
    encoded_bits = 6
    fmt="%02d"
    def __init__(self, disparity_in, is_control, data, encoding):
        self.disparity_in = disparity_in
        self.is_control = is_control
        self.data = data
        self.encoding = encoding
        self.num_ones = count_ones(encoding)
        self.disparity_out = disparity_in
        if self.num_ones > self.encoded_bits/2:
            if disparity_in==1: raise Exception("Bad symbol with encoding having too many ones with positive disparity_in")
            self.disparity_out = 1
            pass
        elif self.num_ones < self.encoded_bits/2:
            if disparity_in==0: raise Exception("Bad symbol with encoding having too many zeros with negative disparity_in")
            self.disparity_out = 0
            pass
        if abs(self.num_ones - self.encoded_bits/2)>1: raise Exception("Too many ones or zeros in encoding")
        self.subsequent_encoding = None
        pass
    def set_subsequent_encoding(self, encoding):
        self.subsequent_encoding = encoding
        pass
    def matches(self, d):
        for k in ["disparity_in", "data", "encoding", "disparity_out", "is_control"]:
            if k in d:
                if getattr(self,k)!=d[k]: return False
                pass
            pass
        return True
    def __str__(self):
        r = ""
        if self.disparity_in:
            r+="+"
            pass
        else:
            r+="-"
            pass
        if self.is_control:
            r+="K"
            pass
        else:
            r+="D"
            pass
        r+=self.fmt%self.data
        if self.disparity_out:
            r+="+"
            pass
        else:
            r+="-"
            pass
        return r
    pass
class encoding_6b5b(encoding):
    encoded_bits = 6
    pass
class encoding_4b3b(encoding):
    encoded_bits = 4
    pass
class encoding_8b10b(encoding):
    encoded_bits = 10
    def __init__(self, enc_pair):
        (enc_6b5b, enc_4b3b) = enc_pair
        self.enc_pair = enc_pair
        self.enc_6b5b = enc_6b5b
        self.enc_4b3b = enc_4b3b
        encoding.__init__( self,
                           disparity_in = enc_6b5b.disparity_in,
                           data         = enc_6b5b.data + 32*enc_4b3b.data,
                           is_control   = enc_6b5b.is_control,
                           encoding     = enc_6b5b.encoding*16 + enc_4b3b.encoding )

        pass
    def __str__(self):
        return "%s = %s%s (%03x)"%(encoding.__str__(self),str(self.enc_6b5b),str(self.enc_4b3b),self.encoding)
    
def create_encodings_list(enc_neg, neg_pos_diff, mask, is_control, enc_class):
    encodings = []
    tbe = range(len(enc_neg))
    if type(enc_neg)==dict: tbe=enc_neg.keys()
    for i in tbe:
        diff  = neg_pos_diff[i]
        xor   = 0
        if diff: xor = mask
        encodings.append(enc_class(0, is_control, i, enc_neg[i] ))
        encodings.append(enc_class(1, is_control, i, enc_neg[i] ^ xor ))
        pass
    return encodings

data_6b5b_encode_neg_pos_diff = [
    1,1,1,0, 1,0,0,1, 1,0,0,0, 0,0,0,1,
    1,0,0,0, 0,0,0,1, 1,0,0,1, 0,1,1,1]

data_6b5b_encode_negative = [
    0x27, 0x1d, 0x2d, 0x31, 0x35, 0x29, 0x19, 0x38,
    0x39, 0x25, 0x15, 0x34, 0x0d, 0x2c, 0x1c, 0x17,
    0x1b, 0x23, 0x13, 0x32, 0x0b, 0x2a, 0x1a, 0x3a,
    0x33, 0x26, 0x16, 0x36, 0x0e, 0x2e, 0x1e, 0x2b
    ]

control_6b5b_encode_negative = {
    23:data_6b5b_encode_negative[23],
    27:data_6b5b_encode_negative[27],
    29:data_6b5b_encode_negative[29],
    30:data_6b5b_encode_negative[30],
    28:0x0f
}

data_4b3b_encode_neg_pos_diff = [
    1,0,0,1, 1,0,0,1
    ]

data_4b3b_encode_negative = [
    0xb, 0x9, 0x5, 0xc, 0xd, 0xa, 0x6, 0xe
    ]

data_4b3b_encode_negative_alt = data_4b3b_encode_negative[:]
data_4b3b_encode_negative_alt[7] = 0x7

control_4b3b_encode_negative = [
    0xb, 0x6, 0xa, 0xc, 0xd, 0x5, 0x9, 0x7
    ]

# D.x.A7 is used for only x=17/18/20 when RD=-1
# D.x.A7 is used for only x=11/13/14 when RD=+1
encodings_data_4b3b = create_encodings_list( data_4b3b_encode_negative,
                                             data_4b3b_encode_neg_pos_diff,
                                             0xf,
                                             0,
                                             encoding_4b3b )
encodings_data_alt_4b3b = create_encodings_list( data_4b3b_encode_negative_alt,
                                                 data_4b3b_encode_neg_pos_diff,
                                                 0xf,
                                                 0,
                                             encoding_4b3b )
encodings_control_4b3b = create_encodings_list( control_4b3b_encode_negative,
                                                    [1]*8,
                                                    0xf,
                                                    1,
                                                    encoding_4b3b )
encodings_data_6b5b = create_encodings_list( data_6b5b_encode_negative,
                                             data_6b5b_encode_neg_pos_diff,
                                             0x3f,
                                             0,
                                             encoding_6b5b )
encodings_control_6b5b = create_encodings_list( control_6b5b_encode_negative,
                                                [1]*32, # All have inverted encodings if disparity +ve
                                                0x3f,
                                                1,
                                                encoding_6b5b )
# D.x.A7 is used for only x=17/18/20 when RD=-1
# D.x.A7 is used for only x=11/13/14 when RD=+1
for de in encodings_data_6b5b:
    de.set_subsequent_encoding(encodings_data_4b3b)
    if (de.matches({"data":17, "disparity_in":0})): de.set_subsequent_encoding(encodings_data_alt_4b3b)
    if (de.matches({"data":18, "disparity_in":0})): de.set_subsequent_encoding(encodings_data_alt_4b3b)
    if (de.matches({"data":20, "disparity_in":0})): de.set_subsequent_encoding(encodings_data_alt_4b3b)
    if (de.matches({"data":11, "disparity_in":1})): de.set_subsequent_encoding(encodings_data_alt_4b3b)
    if (de.matches({"data":13, "disparity_in":1})): de.set_subsequent_encoding(encodings_data_alt_4b3b)
    if (de.matches({"data":14, "disparity_in":1})): de.set_subsequent_encoding(encodings_data_alt_4b3b)
    pass
for ce in encodings_control_6b5b:
    ce.set_subsequent_encoding(encodings_control_4b3b)
    pass
def find_encoding(encodings, d):
    matches = []
    for e in encodings:
        if e.matches(d):
            matches.append(e)
        pass
    if len(matches)==0: return None
    if len(matches)>1: raise Exception("More than one encoding found")
    return matches[0]
def find_encoding_8b10b(is_control, data, disparity_in):
    encodings = encodings_data_6b5b
    if is_control: encodings = encodings_control_6b5b
    e6b5b = find_encoding(encodings, {"data":data&0x1f, "is_control":is_control, "disparity_in":disparity_in})
    if e6b5b is None: return None
    e4b3b = find_encoding(e6b5b.subsequent_encoding, {"data":(data>>5)&7,
                                                      "is_control":is_control,
                                                      "disparity_in":e6b5b.disparity_out} )
    return (e6b5b, e4b3b)

def enc_pair_str(ep):
    (e6b5b, e4b3b) = ep
    return "%s%s"%(str(e6b5b),str(e4b3b))

#a Toplevel
control_symbols = [a+32*b for (a,b) in (23,7),(27,7),(29,7),(30,7), (28,0),(28,1),(28,2),(28,3),(28,4),(28,5),(28,6),(28,7)]
data_symbols = range(256)
encodings_8b10b = []
for d in control_symbols:
    encodings_8b10b.append(encoding_8b10b(find_encoding_8b10b(1, d, 0)))
    encodings_8b10b.append(encoding_8b10b(find_encoding_8b10b(1, d, 1)))
    pass
for d in data_symbols:
    encodings_8b10b.append(encoding_8b10b(find_encoding_8b10b(0, d, 0)))
    encodings_8b10b.append(encoding_8b10b(find_encoding_8b10b(0, d, 1)))
    pass
if __name__ == '__main__':
    for e in encodings_8b10b:
        print str(e)
    pass

