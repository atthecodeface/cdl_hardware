#!/usr/bin/env python
"""
connect 10.1.17.187
rv_enable_debug
apbr 4 2
rv_unreset
rv_debug_status
rv_debug_get_reg 0x1002
rv_debug_set_reg 0x1002 0x12345678
rv_debug_get_reg 0x1002

connect 10.1.17.187
rv_enable_debug
rv_debug_status
rv_unreset
rv_debug_status
rv_debug_set_reg 0x1002 0x1235678
rv_debug_set_reg 0x1003 0xfeedcafe
rv_debug_get_reg 0x1002
rv_debug_get_reg 0x1003

"""
import socket
import dump
import readline
import cmd

def checksum_data(data):
    s = 0
    for d in data:
        s += d
        pass
    print "Csum %x"%s
    return s & 0xffffffff

class hps_remote_socket:
    apb_sel = {"rv_sram":4,
               "rv_debug":9,
    }
    def get_responses(self):
        responses = []
        try:
            while True:
                t=self.skt.recv(8192)
                if (len(t)==0): break
                print t,
                responses.append(t)
                pass
            pass
        except:
            pass
        return responses

    def __init__(self, remote_address="10.1.17.219", remote_port=1234):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.connect((remote_address, remote_port))
        self.skt.settimeout(0.1)
        self.rv_ctrl = 0
        self.verbose = True
        pass
    def sendall(self, text):
        if self.verbose: print "Sending :%s"%text
        self.skt.sendall(text)
        pass
    def send_sram_data(self, select, base, data):
        csum = checksum_data(data)
        self.sendall("SRAM %d 0x%x 0x%x 0x%08x\n"%(select, base, len(data), csum) )
        buffer = bytes()
        for d in data:
            buffer += chr((d>>24)&0xff )
            buffer += chr((d>>16)&0xff )
            buffer += chr((d>> 8)&0xff )
            buffer += chr((d>> 0)&0xff )
            if (len(buffer)>=2*1024):
                print "Sending %d bytes"%(len(buffer))
                self.skt.sendall(buffer)
                self.get_responses()
                buffer = bytes()
                pass
            pass
        print "Sending %d bytes"%(len(buffer))
        self.skt.sendall(buffer)
        self.get_responses()
        pass

    def send_dump(self, image):
        addresses = image.data.keys()
        addresses.sort()
        while len(addresses)>0:
            base = addresses[0]
            data = []
            i = base
            while (len(addresses)>0) and (i==addresses[0]):
                data.append(image.data[i])
                addresses.pop(0)
                i += 1
                pass
            print "Sending sram from base %d length %d"%(base, len(data))
            self.send_sram_data(4, base, data)
            pass
        self.get_responses()
        pass

    def apbw(self, select, reg, data):
        self.sendall("APBW %d %d 0x%x\n"%(select,reg,data))
        self.get_responses()
        pass
    
    def apbr(self, select, reg):
        self.sendall("APBR %d %d\n"%(select,reg))
        r = "".join(self.get_responses())
        if r[:5]=="APBR ":
            try:
                return int(r[5:13],16)
            except:
                return None
        return None

    def sram_read(self, select, base, n):
        self.apbw(select,0,base)
        for i in range(n):
            r = self.apbr(select,3)
            if r is not None: print "%08x"%r
            pass
        pass

    def modify_rv_control(self, do_set=0, do_clear=0):
        self.rv_ctrl = ((self.rv_ctrl &~ do_clear) | do_set) & 0xffffffff
        self.apbw(self.apb_sel["rv_sram"],2,self.rv_ctrl)
        pass

    def riscv_unreset(self):
        self.modify_rv_control(do_set = 1)
        pass

    def riscv_reset(self):
        self.modify_rv_control(do_clear = 1)
        self.get_responses()
        pass

    def riscv_enable_debug(self):
        self.modify_rv_control(do_set = (1<<12))
        self.get_responses()
        pass

    def riscv_debug_status(self):
        r = self.apbr(self.apb_sel["rv_debug"],17)
        if r is not None:
            print "Status %08x:"%r
            print "      version: %d"%((r>> 0)&0xf)
            print "    allhalted: %d"%((r>> 9)&1)
            print "   allrunning: %d"%((r>>11)&1)
            print " allresumeack: %d"%((r>>17)&1)
            pass
        pass

    def riscv_debug_halt(self, hart=0):
        self.apbw(self.apb_sel["rv_debug"], 0x10, (1<<31) | 1)
        pass

    def riscv_debug_resume(self, hart=0):
        self.apbw(self.apb_sel["rv_debug"], 0x10, (1<<30) | 1)
        pass

    def riscv_debug_resume_remove(self, hart=0):
        self.apbw(self.apb_sel["rv_debug"], 0x10, (0<<30) | 1)
        pass

    def riscv_debug_set_reg(self,reg,value):
        self.apbw(self.apb_sel["rv_debug"], 4, value)
        self.apbw(self.apb_sel["rv_debug"], 0x17, (2<<20)|(1<<17)|(1<<16)| reg)
        pass

    def riscv_debug_get_reg(self,reg):
        self.apbw(self.apb_sel["rv_debug"], 0x17, (2<<20)|(1<<17)|(0<<16)| reg)
        value = self.apbr(self.apb_sel["rv_debug"], 4)
        if value is not None:
            print "%0x:%0x"%(reg,value)
        pass
    pass

riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"
mif_filename = riscv_atcf_regression_dir+"hps_ps2_term2.dump"
class hps_remote(cmd.Cmd):
    intro = 'Welcome to the HPS remote'
    prompt = 'hps> '
    skt = None
    def do_connect(self, arg):
        "Connect to a remote socket"
        try:
            self.skt = hps_remote_socket(arg)
        except Exception as e:
            print "Failed: %s"%(e)
            self.skt = None
        pass
    def do_apbw(self, arg):
        "Do an APB write"
        try:
            (select,reg,data) = tuple([int(x,0) for x in arg.split()])
            self.skt.apbw(select, reg, data)
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_apbr(self, arg):
        "Do an APB read"
        try:
            (select,reg) = tuple([int(x,0) for x in arg.split()])
            self.skt.apbr(select, reg)
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_sram_dump(self, arg):
        "Dump SRAM"
        try:
            (select,base,n) = tuple([int(x,0) for x in arg.split()])
            self.skt.sram_read(select, base, n)
        except Exception as e:
            print "Failed: %s"%(e)
        pass

    def do_rv_load(self, arg):
        "Load a RISC-V image in to the HPS"
        test_image = dump.c_dump()
        try:
            f = open(arg)
            test_image.load(f, base_address=0, address_mask=0x7fffffff)
            f.close()
            self.skt.send_dump(test_image)
        except Exception as e:
            print "Failed: %s"%(e)
            pass
        pass
    def do_rv_unreset(self, arg):
        "Start the RISC-V" 
        try:
           self.skt.riscv_unreset()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_reset(self, arg):
        "Stop the RISC-V"
        try:
            self.skt.riscv_reset()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_enable_debug(self, arg):
        "Enable debug on the RISC-V" 
        try:
           self.skt.riscv_enable_debug()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_debug_status(self, arg):
        "Debug halt" 
        try:
           self.skt.riscv_debug_status()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_debug_halt(self, arg):
        "Debug halt" 
        try:
           self.skt.riscv_debug_halt()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_debug_resume(self, arg):
        "Debug halt" 
        try:
           self.skt.riscv_debug_resume()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_debug_set_reg(self, arg):
        "Debug set reg <reg> <value>" 
        try:
            (reg,data) = tuple([int(x,0) for x in arg.split()])
            self.skt.riscv_debug_set_reg(reg, data)
            pass
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_debug_get_reg(self, arg):
        "Debug get reg <reg>>" 
        try:
            (reg,) = tuple([int(x,0) for x in arg.split()])
            self.skt.riscv_debug_get_reg(reg)
            pass
        except Exception as e:
            print "Failed: %s"%(e)
        pass

if __name__ == '__main__':
    try:
        readline.read_history_file('.hps_remote')
        pass
    except:
        pass
    try:
        hps_remote().cmdloop()
        pass
    except:
        pass
    readline.write_history_file('.hps_remote')
