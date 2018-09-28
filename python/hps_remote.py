#!/usr/bin/env python

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
    def get_responses(self):
        try:
            while True:
                t=self.skt.recv(8192)
                if (len(t)==0): break
                print t,
                pass
            pass
        except:
            pass
        pass
    def __init__(self, remote_address="10.1.17.219", remote_port=1234):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.connect((remote_address, remote_port))
        self.skt.settimeout(0.1)
    def send_sram_data(self, select, base, data):
        csum = checksum_data(data)
        print "SRAM %d 0x%x 0x%x 0x%08x\n"%(select, base, len(data), csum)
        self.skt.sendall("SRAM %d 0x%x 0x%x 0x%08x\n"%(select, base, len(data), csum) )
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
        self.skt.sendall("APBW %d %d 0x%x\n"%(select,reg,data))
        self.get_responses()
        pass
    
    def apbr(self, select, reg):
        self.skt.sendall("APBR %d %d\n"%(select,reg))
        self.get_responses()
        pass

    def sram_read(self, select, base, n):
        self.skt.sendall("APBW %d 0 0x%x\n"%(select,base))
        self.get_responses()
        for i in range(n):
            self.skt.sendall("APBR %d 3\n"%(select))
            self.get_responses()
            pass
                  
    def start_riscv(self):
        self.skt.sendall("APBW 4 2 1\n")
        self.get_responses()
        pass

    def stop_riscv(self):
        self.skt.sendall("APBW 4 2 0\n")
        self.get_responses()
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
    def do_rv_start(self, arg):
        "Start the RISC-V" 
        try:
           self.skt.start_riscv()
        except Exception as e:
            print "Failed: %s"%(e)
        pass
    def do_rv_stop(self, arg):
        "Stop the RISC-V"
        try:
            self.skt.stop_riscv()
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
