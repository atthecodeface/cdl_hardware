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

#a AXI mixin
#c axi4s_mixin
class axi4s_mixin:
    axi4s_properties = ["strb", "keep", "user", "id", "dest", "last", "data"]
    #f axi4s_init
    def axi4s_init(self):
        self.axi_bfm.axi4s("axi4s")
        self.axi4s.set("strb",0xf)
        self.axi4s.set("keep",0xf)
        self.axi4s.set("user",0)
        self.axi4s.set("id",0)
        self.axi4s.set("dest",0)
        self.axi4s.set("last",0)
        self.axi4s.set("data",0)
        pass
    #f axi4s_set_data
    def axi4s_set_data(self, obj, axi_data):
        for p in self.axi4s_properties:
            if p in axi_data: obj.set(p, axi_data[p])
            pass
        pass
    #f axi4s_master_enqueue
    def axi4s_master_enqueue(self, axi_data):
        self.axi4s_set_data(self.axi4s, axi_data)
        self.axi4s.master_enqueue()
        pass
        
