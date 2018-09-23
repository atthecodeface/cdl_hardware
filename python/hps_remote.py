#!/usr/bin/env python

import socket
import dump


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
    def __init__(self, remote_address="192.168.3.12", remote_port=1234):
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

    def start_riscv(self):
        self.skt.sendall("APBW 4 2 1\n")
        self.get_responses()

    def stop_riscv(self):
        self.skt.sendall("APBW 4 2 0\n")
        self.get_responses()


riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"
mif_filename = riscv_atcf_regression_dir+"hps_ps2_term.dump"
test_image = dump.c_dump()
f = open(mif_filename)
test_image.load(f, base_address=0, address_mask=0x7fffffff)
f.close()


skt = hps_remote_socket()
skt.send_dump(test_image)
skt.start_riscv()
import time
time.sleep(10)
skt.stop_riscv()

