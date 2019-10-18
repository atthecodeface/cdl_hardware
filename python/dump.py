#!/usr/bin/env python
#a Imports
import re
import sys, inspect
import elftools.elf.elffile

#a Classes
#c c_dump
class c_dump(object):
    #b Static properties
    res = {}
    res["hex"]        = r"([0-9a-fA-f]+)"
    res["opt_whitespace"] = r"\s*"
    res["whitespace"] = r"(\s+)"
    res["uid"]        = r"([a-zA-Z_][a-zA-Z_0-9]*)"
    res["label_match"] = re.compile(r"%s%s%s<%s>:"%(res["opt_whitespace"], res["hex"], res["whitespace"], res["uid"]))
    res["data_match"]  = re.compile(r"%s%s:%s%s.*"%(res["opt_whitespace"], res["hex"], res["whitespace"], res["hex"]))
    res["data_label_match"]  = re.compile(r"#%s%s%s<%s>"%(res["whitespace"], res["hex"], res["whitespace"], res["uid"]))
    res["mif_label_match"]       = re.compile(r"#%s%s:%s:"%(res["whitespace"], res["hex"], res["uid"]))
    res["mif_data_match"]        = re.compile(r"%s:%s%s.*"%(res["hex"], res["whitespace"], res["hex"]))
    res["mif_data_label_match"]  = re.compile(r"#%s%s%s<%s>"%(res["whitespace"], res["hex"], res["whitespace"], res["uid"]))
    def __init__(self):
    #f __init__
        self.reset()
        pass
    #f reset
    def reset(self):
        self.labels = {}
        self.data   = {}
        pass
    #f load
    def load(self, f, base_address=0, address_mask=0xffffffff):
        self.reset()
        for l in f:
            label_match = self.res["label_match"].match(l)
            data_match  = self.res["data_match"].match(l)
            data_label_match  = self.res["data_label_match"].search(l)
            if label_match:
                self.add_label(label_match.group(3), int(label_match.group(1),16), base_address, address_mask)
                pass
            if data_match:
                self.add_data(int(data_match.group(3),16), int(data_match.group(1),16), base_address, address_mask)
                pass
            if data_label_match:
                self.add_label(data_label_match.group(4), int(data_label_match.group(2),16), base_address, address_mask)
                pass
            pass
        pass
    #f load_mif
    def load_mif(self, f, base_address=0, address_mask=0xffffffff):
        self.reset()
        for l in f:
            label_match = self.res["mif_label_match"].match(l)
            data_match  = self.res["mif_data_match"].match(l)
            data_label_match  = self.res["mif_data_label_match"].search(l)
            if label_match:
                self.add_label(label_match.group(3), int(label_match.group(1),16), base_address, address_mask)
                pass
            if data_match:
                self.add_data(int(data_match.group(3),16), 4*int(data_match.group(1),16), base_address, address_mask)
                pass
            if data_label_match:
                self.add_label(data_label_match.group(4), int(data_label_match.group(2),16), base_address, address_mask)
                pass
            pass
        pass
    #f load_elf
    def load_elf(self, f, base_address=0, address_mask=0xffffffff):
        self.reset()
        elf = elftools.elf.elffile.ELFFile(f)
        for i in elf.iter_sections():
            #print i.name, i.header
            if i.header.sh_type=='SHT_SYMTAB':   self.load_elf_symtab_section(i, base_address, address_mask)
            if i.header.sh_type=='SHT_PROGBITS': self.load_elf_data_section(i, base_address, address_mask)
        pass
    #f load_elf_symtab_section
    def load_elf_symtab_section(self, section, base_address=0, address_mask=0xffffffff):
        for s in section.iter_symbols():
            self.add_label(s.name, s.entry.st_value)
            pass
        pass
    #f load_elf_data_section
    def load_elf_data_section(self, section, base_address=0, address_mask=0xffffffff):
        address = section.header.sh_addr
        size = section.data_size
        data = section.data()
        print "Load section %s of %d bytes to %08x"%(section.name,size,address)
        n = 0
        for d in data:
            self.add_data_byte(ord(d),address+n,base_address,address_mask)
            n += 1
            pass
        pass
    #f add_label
    def add_label(self,label,address,base_address=0, address_mask=0xffffffff):
        address = (address-base_address) & address_mask
        self.labels[label] = address
        pass
    #f add_data_byte
    def add_data_byte(self,data,address,base_address=0, address_mask=0xffffffff):
        address = (address-base_address) & address_mask
        offset = address&3
        address = address/4
        data = data << (8*offset)
        if address in self.data:
            mask = (0xff << (8*offset)) ^ 0xffffffff
            data = data | (self.data[address] & mask)
            pass
        self.data[address] = data
        pass
    #f add_data
    def add_data(self,data,address,base_address=0, address_mask=0xffffffff):
        address = (address-base_address) & address_mask
        offset = address&3
        address = address/4
        if offset!=0:
            self.add_data((data<<(8*offset))&0xffffffff,address*4,base_address=0)
            self.add_data((data>>(32-8*offset))&0xffffffff,address*4+4,base_address=0)
            return
        if address in self.data:
            data = data | self.data[address]
            pass
        self.data[address] = data
        pass
    #f resolve_label
    def resolve_label(self, label):
        if label not in self.labels:
            raise Exception("Unable to find label '%s'"%label)
        return self.labels[label]
    #f package_data
    def package_data(self, max_per_base=1024):
        """
        Package data in to a list of (base, [data*])
        """
        package = []
        addresses = self.data.keys()
        addresses.sort()
        while len(addresses)>0:
            base = addresses[0]
            data = []
            i = base
            while (len(addresses)>0) and (i==addresses[0]) and (len(data)<max_per_base):
                data.append(self.data[i])
                addresses.pop(0)
                i += 1
                pass
            package.append((base,data))
            pass
        return package
    #f write_mif
    def write_mif(self, f):
        labels = self.labels.keys()
        labels.sort(cmp=lambda a,b:cmp(self.labels[a],self.labels[b]))

        label_addresses_map = {}
        for l in labels:
            la = self.labels[l]
            if la not in label_addresses_map: label_addresses_map[la]=[]
            label_addresses_map[la].append(l)
            pass

        for l in labels:
            print >>f, "#%8x:%s"%(self.labels[l],l)
            pass

        addresses = self.data.keys()
        addresses.sort()
        for a in addresses:
            r = "%08x: "%a
            r += "%08x" % self.data[a]
            if a in label_addresses_map:
                r += " #"
                for l in label_addresses_map[a]:
                    r += " %s"%l
                    pass
                pass
            print >>f, r
            pass
        pass
    #f write_mem
    def write_mem(self, f):
        fmt = "%08x"
        addresses = self.data.keys()
        addresses.sort()
        for a in addresses:
            r = "@%08x "%a
            r += fmt % self.data[a]
            print >>f, r
            pass
        pass
    #f write_c_data
    def write_c_data(self, f):
        print >>f, "static uint32_t data[] = {"
        addresses = self.data.keys()
        addresses.sort()
        r = ""
        for a in addresses:
            r += " %d, 0x%08x,"%(a,self.data[a])
            if (len(r)>50):
                print >>f, r
                r = ""
                pass
            pass
        r += " -1, -1"
        print >>f, r
        print >>f, "};"
        pass
    #f All done
    pass
#a Useful invocation function
def get_define_int(defines, k, default):
    if k in defines:
        return int(defines[k],0)
        pass
    return default

def file_write(filename, fn):
    if filename=='-':
        fn(sys.stdout)
        pass
    else:
        f = open(filename,"w")
        fn(f)
        f.close()
        pass
    pass

def file_read(filename, args, fn):
    must_close = False
    f = sys.stdin
    if filename!='-':
        f = open(filename,"r")
        must_close = True
        pass
    mem = c_dump()
    fn(mem, f) # base_address, address_mask, sections, ...
    if must_close:
        f.close()
        pass
    return mem

def dump_main(dump=None, allow_load=True, description='Generate MEM, MIF or C data of memory'):
    import argparse, sys, re
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--mif', type=str, default=None,
                    help='Output MIF filename')
    parser.add_argument('--mem', type=str, default=None,
                    help='Output READMEMH filename')
    parser.add_argument('--c_data', type=str, default=None,
                    help='Output C data filename')
    if allow_load:
        parser.add_argument('--load_mif', type=str, default=None,
                            help='MIF file to load')
        parser.add_argument('--load_elf', type=str, default=None,
                            help='ELF file to load')
        parser.add_argument('--load_dump', type=str, default=None,
                            help='Dump file to load')
    args = parser.parse_args()
    if args.load_mif is not None:
        dump = file_read(args.load_mif, args, c_dump.load_mif)
        pass
    if args.load_elf is not None:
        dump = file_read(args.load_elf, args, c_dump.load_elf)
        pass
    if args.load_dump is not None:
        dump = file_read(args.load_dump, args, c_dump.load_dump)
        pass
    if dump is None:
        parse_args.print_help()
        pass
    if args.mif    is not None: file_write(args.mif,    dump.write_mif)
    if args.mem    is not None: file_write(args.mem,    dump.write_mem)
    if args.c_data is not None: file_write(args.c_data, dump.write_c_data)
    pass

if __name__ == "__main__":
    dump_main()
