#!/usr/bin/env python
#c rom
class rom(object):
    opcodes = {
        "opcode_class_alu": 0,
        "opcode_class_set_parameter": 1,
        "opcode_class_apb_request": 2,
        "opcode_class_branch": 3,
        "opcode_class_wait": 4,
        "opcode_class_finish": 5
        }

    opcode_subclass = {
        "rom_op_alu_or": 0,
        "rom_op_alu_and": 1,
        "rom_op_alu_bic": 2,
        "rom_op_alu_xor": 3,
        "rom_op_alu_add": 4,

        "rom_op_set_address": 0,
        "rom_op_set_repeat": 1,
        "rom_op_set_accumulator": 2,
        "rom_op_set_increment": 3,

        "rom_op_branch": 0,
        "rom_op_beq": 1,
        "rom_op_bne": 2,
        "rom_op_loop": 3,

        "rom_op_req_read": 0,
        "rom_op_req_write_arg": 1,
        "rom_op_req_write_acc": 2,
        "rom_op_req_read_inc": 4, # auto-increment
        "rom_op_req_write_arg_inc": 5,
        "rom_op_req_write_acc_inc": 6,
        }
    #f op_alu
    @classmethod
    def op_alu(cls, alu_op, data):
        return (cls.opcodes["opcode_class_alu"]<<(32+5)) | (cls.opcode_subclass["rom_op_alu_"+alu_op]<<32) | data
        pass
    #f op_branch
    @classmethod
    def op_branch(cls, branch_op, data):
        return (cls.opcodes["opcode_class_branch"]<<(32+5)) | (cls.opcode_subclass["rom_op_"+branch_op]<<32) | data
        pass
    #f op_set
    @classmethod
    def op_set(cls, set_op, data):
        return (cls.opcodes["opcode_class_set_parameter"]<<(32+5)) | (cls.opcode_subclass["rom_op_set_"+set_op]<<32) | data
        pass
    #f op_req
    @classmethod
    def op_req(cls, req_op, data):
        return (cls.opcodes["opcode_class_apb_request"]<<(32+5)) | (cls.opcode_subclass["rom_op_req_"+req_op]<<32) | data
        pass
    #f op_wait
    @classmethod
    def op_wait(cls, data):
        return (cls.opcodes["opcode_class_wait"]<<(32+5)) | data
        pass
    #f op_finish
    @classmethod
    def op_finish(cls):
        return (cls.opcodes["opcode_class_finish"]<<(32+5))
        pass
    #f compile_program
    @staticmethod
    def compile_program(program, address=0):
        """
        Does a two-pass compile of a program

        A program consists of a list of (op | (op*labels tuple))

        labels is a list of label string

        A label string can be a 'set label' if it ends in a colon e.g. 'retry:'
        A label string is otherwise a 'use label as data'

        An op is
        op_alu("or|and|bic|xor|add",data)
        op_branch("branch|beq|bne|loop",data)
        op_set("address|repeat|accumulator",data)
        op_req("read|write_arg|write_acc|read_inc|write_arg_inc|write_acc_inc",data)
        op_wait(data)
        op_finish()

        inc is a post-increment
        """
        compiled = {"labels":{},
                    "object":[]}
        label_addresses = {}
        for p in range(2):
            prog_address = address
            for op_labels in program["code"]:
                if len(op_labels)==1:
                    op=op_labels[0]
                    labels=[]
                    pass
                else:
                    (op,labels) = op_labels
                    pass
                if p==0:
                    for l in labels:
                        if l[-1]==':': label_addresses[l] = prog_address
                        pass
                    pass
                else:
                    for l in labels:
                        if l[-1]!=':': op |= label_addresses[l+":"]
                        pass
                    compiled["object"].append( (prog_address,op) )
                    pass
                prog_address = prog_address + 1
                pass
            pass
        compiled["labels"] = label_addresses
        return compiled
    pass
    #f mif_of_compilation
    @staticmethod
    def open_filename(filename):
        import sys
        if filename=='': return (sys.stdout, lambda x:None)
        f = open(filename,"w")
        if not f:
            die
            pass
        return (f, lambda x:f.close() )
    @staticmethod
    def mif_of_compilation(compiled, filename=''):
        fmt = "%02x: %010x"
        (f,c) = rom.open_filename(filename)
        for (a,d) in compiled["object"]:
            print >>f, fmt%(a,d)
            pass
        c(None)
        pass
    @staticmethod
    def mem_of_compilation(compiled, filename=''):
        fmt="%010x"
        (f,c) = rom.open_filename(filename)
        addresses = []
        code = {}
        for (a,d) in compiled["object"]:
            addresses.append(a)
            code[a] = d
            pass
        addresses.sort()
        for i in range(addresses[-1]+1):
            value = 0
            if i in code: value = code[i]
            print >>f, fmt%value
            pass
        c(None)
        pass

#a Toplevel
def get_define_int(defines, k, default):
    if k in defines:
        return int(defines[k],0)
        pass
    return default

if __name__ == "__main__":
    import argparse, sys, re
    parser = argparse.ArgumentParser(description='Generate MIF or READMEMH files for APB processor ROM')
    parser.add_argument('--src', type=str, default=None,
                    help='Source for APB ROM')
    parser.add_argument('--mif', type=str, default=None,
                    help='Output MIF filename')
    parser.add_argument('--mem', type=str, default=None,
                    help='Output READMEMH filename')
    parser.add_argument('--define', type=str, action='append', default=[],
                    help='Defines for the ROM program')
    args = parser.parse_args()
    show_usage = False
    if args.src is None:
        show_usage = True
        pass
    if show_usage:
        parser.print_help()
        sys.exit(0)
        pass
    defines = {}
    dre = re.compile(r"(.*)=(.*)")
    for d in args.define:
        m = dre.match(d)
        if m is None:
            defines[d] = True
            pass
        else:
            defines[m.group(1)] = m.group(2)
            pass
        pass
    import importlib
    m = importlib.import_module(args.src)
    program = m.program(defines)
    compilation = rom.compile_program(program)
    if args.mif is not None:
        rom.mif_of_compilation(compilation, filename=args.mif)
        pass
    if args.mem is not None:
        rom.mem_of_compilation(compilation, filename=args.mem)
        pass
    pass
