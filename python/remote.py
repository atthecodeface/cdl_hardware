#!/usr/bin/env python
import serial_remote
import dump
import readline
import cmd
import traceback

#a Useful operations class
class remote_operations:
    apb_sel = {"rv_sram":4,
               "rv_debug":9,
    }
    #f __init__
    def __init__(self):
        self.rv_ctrl = 0
        self.verbose = True
        self.disconnect()
        pass

    #f connect
    def connect(self, server):
        self.s_apbr, self.s_apbw = server.get_apb_fns()
        self.server = server
        pass

    #f disconnect
    def disconnect(self):
        self.s_apbr, self.s_apbw = None, None
        self.server = None
        pass

    #f apbw
    def apbw(self, select, reg, data):
        if self.s_apbw is not None:
            return self.s_apbw( address = (1<<20) | (select<<16) | (reg<<2), data=data )
        raise Exception("No APBW method - is a server connected?")

    #f apbr
    def apbr(self, select, reg):
        if self.s_apbr is not None:
            return self.s_apbr( address = (1<<20) | (select<<16) | (reg<<2) )
        raise Exception("No APBR method - is a server connected?")

    #f sgmii_an
    def sgmii_an(self, adv):
        self.apbw(4,2,(1<<20) | (0<<4) | 9 )
        self.apbw(4,2,(1<<20) | (0<<4) | 1 )
        self.apbw(4,2,(adv<<8) | (1<<4) | 9 )
        self.apbw(4,2,(adv<<8) | (1<<4) | 1 )
        self.apbw(4,2,1 | (2<<4) | 9 )
        self.apbw(4,2,1 | (2<<4) | 1 )
        self.apbw(4,2,1)
        pass
    
    #f anal_trigger_always
    def anal_trigger_always(self):
        self.apbw(14,0,1) # config trigger reset, not circular, not enable, apb not reading trace
        self.apbw(14,1,(3<<20)|(3<<28)) # trigger action if either action 3 store and reside
        self.apbw(14,2,0) # transition 0 mask 0
        self.apbw(14,3,0) # transition 0 compare 0
        self.apbw(14,0,6) # enable and allow apb trace readback
        pass
    
    #f anal_mux_control
    def anal_mux_control(self, mux):
        self.apbw(14,4,mux)
        pass
    
    #f anal_capture_mask_compare
    def anal_capture_mask_compare(self, mask, compare):
        self.apbw(14,0,1) # config trigger reset, not circular, not enable, apb not reading trace
        self.apbw(14,1,(3<<20)) # trigger action if true action 3 store and reside
        self.apbw(14,2,mask) # transition 0 mask 0
        self.apbw(14,3,compare) # transition 0 compare 0
        self.apbw(14,0,6) # enable and allow apb trace readback
        pass
    
    #f anal_status
    def anal_status(self):
        status = self.apbr(14,0)
        print "Analyzer status %08x"%status
        pass
    
    #f anal_read_trace
    def anal_read_trace(self):
        data = self.apbr(14,8)
        print "Analyzer data %08x"%data
        pass
    
    #f anal_read_fifo
    def anal_read_fifo(self, max):
        data = ""
        for i in range(max):
            status = self.apbr(14,0)
            if (status & 8)==0: break
            data += "%08x "%(self.apbr(14,8))
            pass
        print data
        pass
    
    #f axi4s_reset
    def axi4s_reset(self):
        self.apbw(13,0,2047)
        self.apbw(13,9,0)
        self.apbw(13,10,0)
        self.apbw(13,8,2047)
        pass
    
    #f axi4s_send_pkt
    def axi4s_send_pkt(self):
        self.apbw(13,9,18)
        self.apbw(13,10,0)
        self.apbw(13,9,0)
        self.apbw(13,10,64)
        pass
    
    #f sram_read
    def sram_read(self, select, base, n):
        self.apbw(select,0,base)
        for i in range(n):
            r = self.apbr(select,3)
            if r is not None: print "%08x"%r
            pass
        pass

    #f modify_rv_control
    def modify_rv_control(self, do_set=0, do_clear=0):
        self.rv_ctrl = ((self.rv_ctrl &~ do_clear) | do_set) & 0xffffffff
        self.apbw(self.apb_sel["rv_sram"],2,self.rv_ctrl)
        pass

    #f riscv_unreset
    def riscv_unreset(self):
        self.modify_rv_control(do_set = 1)
        pass

    #f riscv_reset
    def riscv_reset(self):
        self.modify_rv_control(do_clear = 1)
        pass

    #f riscv_enable_debug
    def riscv_enable_debug(self):
        self.modify_rv_control(do_set = (1<<12))
        pass

    #f riscv_debug_status
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

    #f riscv_debug_halt
    def riscv_debug_halt(self, hart=0):
        self.apbw(self.apb_sel["rv_debug"], 0x10, (1<<31) | 1)
        pass

    #f riscv_debug_resume
    def riscv_debug_resume(self, hart=0):
        self.apbw(self.apb_sel["rv_debug"], 0x10, (1<<30) | 1)
        pass

    #f riscv_debug_resume_remove
    def riscv_debug_resume_remove(self, hart=0):
        self.apbw(self.apb_sel["rv_debug"], 0x10, (0<<30) | 1)
        pass

    #f riscv_debug_set_reg
    def riscv_debug_set_reg(self,reg,value):
        self.apbw(self.apb_sel["rv_debug"], 4, value)
        self.apbw(self.apb_sel["rv_debug"], 0x17, (2<<20)|(1<<17)|(1<<16)| reg)
        pass

    #f riscv_debug_get_reg
    def riscv_debug_get_reg(self,reg):
        self.apbw(self.apb_sel["rv_debug"], 0x17, (2<<20)|(1<<17)|(0<<16)| reg)
        value = self.apbr(self.apb_sel["rv_debug"], 4)
        if value is not None:
            print "%0x:%0x"%(reg,value)
        pass
    pass

#a Remote class
riscv_atcf_regression_dir = "../riscv-atcf-tests/build/dump/"
mif_filename = riscv_atcf_regression_dir+"hps_ps2_term2.dump"
class remote(cmd.Cmd):
    intro = 'Welcome to the remote server'
    prompt = 'rem> '
    skt = None
    cmd_list = {
        "apbw":     ("iii", "Do an APB write"),
        "apbr":     ("ii",  "Do an APB read"),
        "sgmii_an": ("i",   "Invoke SGMII autonegotiation"),
        "anal_trigger_always": ("",   ""),
        "anal_capture_mask_compare": ("ii",   ""),
        "anal_status": ("",   ""),
        "anal_read_trace": ("",   ""),
        "anal_read_fifo": ("i",   ""),
        "anal_mux_control": ("i",   ""),
        "axi4s_reset": ("",   ""),
        "axi4s_send_pkt": ("",   ""),
    }
    #f __init__
    def __init__(self, *args, **kwargs):
        self.remote = remote_operations()
        for cmd_name, (types,help) in self.cmd_list.iteritems():
            self.add_cmd(cmd_name, types, help)
            pass
        cmd.Cmd.__init__(self, *args, **kwargs)
        pass
    #f get_names
    def get_names(self):
        return dir(self)
    #f add_cmd
    def add_cmd(self, cmd, types, help):
        print "Adding command",cmd,types,help
        fn_name = "do_"+cmd
        setattr(self, fn_name, lambda a: self.cmd(types,cmd,a) )
        fn = getattr(self, fn_name)
        fn.__doc__ = help
        pass
    #f cmd
    def cmd(self, types, remote_fn_name, arg):
        try:
            fn = getattr(self.remote,remote_fn_name)
            if types=="iii":
                (a,b,c) = tuple([int(x,0) for x in arg.split()])
                fn(a,b,c)
            elif types=="ii":
                (a,b) = tuple([int(x,0) for x in arg.split()])
                fn(a,b)
            elif types=="i":
                (a,) = tuple([int(x,0) for x in arg.split()])
                fn(a)
            elif types=="":
                fn()
            else:
                raise Exception("Unknown cmd types '%s'"%types)
        except Exception as e:
            print "Failed: %s"%(e)
            traceback.print_exc()
        pass
    #f do_connect
    def do_connect(self, arg):
        "Connect to a remote socket"
        try:
            self.remote = hps_remote_socket(arg)
        except Exception as e:
            print "Failed: %s"%(e)
            self.remote = None
        pass
    #f do_serial
    def do_serial(self, arg):
        "Connect to a serial device"
        try:
            (device,baud) = tuple(arg.split())
            self.remote.connect(serial_remote.server(device, int(baud,0)))
        except Exception as e:
            print "Failed: %s"%(e)
            self.remote = None
        pass

#a Toplevel
if __name__ == '__main__':
    try:
        readline.read_history_file('.hps_remote')
        pass
    except:
        pass
    rem = remote()
    try:
        rem.cmdloop()
    except:
        print traceback.print_exc()
        pass
    readline.write_history_file('.hps_remote')
