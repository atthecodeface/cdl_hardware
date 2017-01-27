from model6502 import c_6502
from system6502 import c_memory
class c_bbc(object):
    def __init__(self):
        self.cpu = c_6502()
        self.memory = c_memory()
        self.memory.load_binary(0xc000, file("../../BeebEm3/BeebFile/BBCINT/OS12.ROM","r"))
        self.memory.load_binary(0x8000, file("../../BeebEm3/BeebFile/BBCINT/BASIC2.ROM","r"))
        self.cpu.reset()
        pass
    def tick(self, n):
        for i in range(n):
            ts = self.cpu.tick_start()
            data_in = 0xff
            if ts["mem"] is not None:
                if ts["mem"][0] in ["read"]:
                    data_in = self.memory.read(ts["mem"][1])
                    pass
                elif ts["mem"][0] in ["write"]:
                    self.memory.write(ts["mem"][1], ts["mem"][2])
                    pass
                pass
            te = self.cpu.tick_end(data_in=data_in)
            print "%02x"%data_in, te
            print self.cpu
            pass
        pass

if len(sys.argv)>=2 and sys.argv[1]=="bbc":
    bbc = c_bbc()
    bbc.tick(100000)
    die
    pass

