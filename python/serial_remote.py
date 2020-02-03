import serial
class server:
    verbose = False
    #f get_apb_fns
    def get_apb_fns(self):
        return (self.apbr, self.apbw, self.prod)
    
    #f __init__
    def __init__(self, device, baud):
        print "Opening serial device '%s' at baud rate %d"%(device,baud)
        self.serial = serial.Serial(device, baud, timeout=0.2)
        self.expectations = []
        self.responses = []    
        while len(self.serial.read(10))>0:
            pass
        self.read_data = []
        self.read_buffer = ""
        pass

    #f add_expectation
    def add_expectation(self, e):
        self.expectations.append(e)
        pass

    #f read_serial
    def read_serial(self, min_data=None):
        while self.serial.in_waiting>0:
            c = self.serial.read(1)
            self.read_buffer += c
            if self.verbose: print "rx",c
            pass
        if min_data is not None:
            if len(self.read_buffer)<min_data:
                self.read_buffer += self.serial.read(min_data-len(self.read_buffer))
                pass
            pass
        pass
    #f get_responses
    def get_responses(self, min_data=None):
        self.read_serial( min_data=min_data)
        if len(self.read_buffer)>0:
            if self.read_buffer[0]=='W':
                self.read_buffer = self.read_buffer[1:]
                self.responses.append(('W', True))
                pass
            elif self.read_buffer[0]=='w':
                self.read_buffer = self.read_buffer[1:]
                self.responses.append(('W', False))
                pass
            elif self.read_buffer[0]=='r':
                self.read_buffer = self.read_buffer[1:]
                self.responses.append(('R', False, 0))
                pass
            elif self.read_buffer[0]=='R':
                self.read_buffer = self.read_buffer[1:]
                self.read_serial(min_data=8)
                if len(self.read_buffer)>=8:
                    data = int(self.read_buffer[0:8],16)
                    self.responses.append(('R', True, data))
                    self.read_buffer = self.read_buffer[8:]
                    pass
                else:
                    raise(Exception("Read data not what expected '%s'"%self.read_buffer))
                pass
            elif self.read_buffer[0]=='p':
                self.read_buffer = self.read_buffer[1:]
                self.responses.append(('P', False, 0))
                pass
            elif self.read_buffer[0]=='P':
                self.read_buffer = self.read_buffer[1:]
                self.read_serial(min_data=8)
                if len(self.read_buffer)>=8:
                    data = int(self.read_buffer[0:8],16)
                    self.responses.append(('P', True, data))
                    self.read_buffer = self.read_buffer[8:]
                    pass
                else:
                    raise(Exception("Read data not what expected '%s'"%self.read_buffer))
                pass
            else:
                raise(Exception("Unexpected data in serial buffer '%s'"%self.read_buffer))
            pass
        pass
    #f wait_expectations
    def wait_expectations(self):
        while len(self.expectations)>0:
            self.get_responses(min_data=1)
            if len(self.responses)==0:
                raise Exception("No responses ready when expecting them")
            e = self.expectations.pop(0)
            if e=='W':
                r = self.responses.pop(0)
                if r[0]!='W':
                    raise Exception("Write expectation got '%s' response not a write response"%(str(r)))
                    pass
                if not r[1]:
                    raise Exception("Write failed")
                pass
            elif e=='R':
                r = self.responses.pop(0)
                if r[0]!='R':
                    raise Exception("Read expectation got '%s' response not a read response"%(str(r)))
                    pass
                if not r[1]:
                    raise Exception("Read failed")
                self.read_data.append(r[2])
                pass
            elif e=='P':
                r = self.responses.pop(0)
                if r[0]!='P':
                    raise Exception("Prod expectation got '%s' response not a read response"%(str(r)))
                    pass
                if not r[1]:
                    raise Exception("Prod failed")
                self.read_data.append(r[2])
                pass
            else:
                raise Exception("Bad expectation %s"%(e))
            pass
        pass
    #f apbw
    def apbw(self, address, data):
        s = "W%x %x\n"%((address&0xffffffff),(data&0xffffffff))
        self.serial.write(s)
        if self.verbose: print "Serial write",s
        self.add_expectation("W")
        self.wait_expectations()
        pass
    
    #f apbr
    def apbr(self, address):
        s = "R%x\n"%((address&0xffffffff))
        self.serial.write(s)
        if self.verbose: print "Serial write",s
        self.add_expectation("R")
        self.wait_expectations()
        if len(self.read_data)==1:
            return self.read_data.pop()
        self.read_data = []
        return None
    #f prod
    def prod(self, value):
        self.serial.write("P%x\n"%((value&0xffffffff)))
        self.add_expectation("P")
        self.wait_expectations()
        if len(self.read_data)==1:
            return self.read_data.pop()
        self.read_data = []
        return None
