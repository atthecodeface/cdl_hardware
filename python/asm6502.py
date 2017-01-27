#a Imports
import re
import sys, inspect
#from instr6502 import 

#a Assembler
#c c_assembler_line
class c_assembler_line(object):
    def __init__(self):
        self.comment = None
        self.mnemonic = None
        self.ie = None
        self.addressing = None
        self.label = None
        self.assignment = None
        self.pc = None
        self.assembly = None
        self.data_define = None
        self.value = None
        pass
    def set_label(self, label):
        self.label = label
        pass
    def set_assignment(self, what, value):
        self.assignment = (what, value)
        pass
    def set_mnemonic_ie(self, mnemonic, ie):
        self.mnemonic = mnemonic
        self.ie = ie
        pass
    def set_comment(self, comment):
        self.comment = comment
        pass
    def set_addresing(self, addressing):
        self.addressing = addressing
        pass
    def set_data_definition(self, data_define, value):
        self.data_define = data_define
        self.value = value
        pass
    def assemble(self, instruction_set, scope, asm_pass):
        self.pc = scope.pc
        if self.label: scope.set_symbol(self.label, self.pc)
        if self.assignment is not None:
            e = scope.evaluate(self.assignment[1], False)
            if e is None: raise Exception("Could not resolve '%s' in assignment"%str(self.assignment[1]))
            if self.assignment[0] in ["."]:
                scope.set_pc(e)
                pass
            else:
                scope.set_symbol(self.assignment[0], e)
                pass
            pass
        if self.data_define is not None:
            e = scope.evaluate(self.value, relative=False)
            if (asm_pass>=1) and (e is None): raise Exception("Could not resolve '%s' in data definition"%str(self.value))
            if e is None: e=0
            a = []
            if self.data_define[-1] in "bBwW":
                a.append(e&0xff)
                pass
            if self.data_define[-1] in "wW":
                a.append((e>>8)&0xff)
                pass
            self.assembly = a
            return len(self.assembly)
        if self.mnemonic is None:
            return 0
        self.assembly = instruction_set.assemble(self.addressing, self.ie, scope, asm_pass)
        return len(self.assembly)
    def __str__(self):
        r = ""
        if self.pc is not None: r += "%04x "%self.pc
        if self.assembly is not None:
            for i in range(3):
                if i>=len(self.assembly):      r += "   "
                elif self.assembly[i] is None: r += "   "
                else:                          r += "%02x "%self.assembly[i]
        if self.label: r += "%s:"%(self.label)
        if self.mnemonic: r += "%s"%(self.mnemonic)
        if self.addressing: r += " %s"%(self.addressing)
        if self.comment: r += " ; %s"%(self.comment)
        return r

#c c_assembler_scope
class c_assembler_scope(object):
    def __init__(self):
        self.pc = None
        self.labels = {}
        pass
    def set_pc(self, value):
        self.pc = value
        pass
    def advance_pc(self, value):
        self.pc += value
        pass
    def set_symbol(self, symbol, value=None):
        if value is None: value = self.pc
        if symbol in self.labels:
            if (self.labels[symbol]!=None) and (self.labels[symbol]!=value):
                raise Exception("Setting of symbol %s to different values not permitted"%symbol)
            pass
        self.labels[symbol] = value
        pass
    def resolve_symbol(self, symbol):
        if symbol==".": return self.pc
        if re.match("%([fFbF])([0-9][0-9])",symbol): die
        if symbol not in self.labels: return None
        return self.labels[symbol]
    def evaluate(self, string, relative):
        string = string.strip()
        if relative:
            v = self.evaluate(string, relative=False)
            if v is None: return None
            v = v - (self.pc+2)
            if (v<-128) or (v>127): return None
            return (v&0xff)
            pass
        m=re.match("^([$&]|0x|0X)([0-9a-fA-f]+)$",string)
        if m: return int(m.group(2),16)
        m=re.match("^([0-9]+)$",string)
        if m: return int(m.group(1))
        return self.resolve_symbol(string)

#c c_assembler
class c_assembler(object):
    blank_re = "^ *$"
    strip_comment_re = "^([^;]*);(.*)"
    assignment_directive_re = "^ *([.]) *= *(.*)$"
    define_directive_re = "^ *define *([a-zA-Z0-9_]*) *(.*)$"
    label_re = "^ *([a-z0-9A-Z_]+): *(.*)"
    define_data_re = "^ *(dcb|dcw) *(.*)"
    mnemonic_re = "^ *([a-zA-Z]+) *(.*)"
    def __init__(self, instruction_set):
        self.instruction_set = instruction_set
        pass
    def parse_line(self, string):
        l = c_assembler_line()
        m = re.match(self.strip_comment_re, string)
        if m:
            string = m.group(1)
            l.set_comment(m.group(2))
            pass
        m = re.match(self.assignment_directive_re, string)
        if m:
            l.set_assignment(m.group(1),m.group(2))
            string = ""
            pass
        m = re.match(self.define_directive_re, string)
        if m:
            l.set_assignment(m.group(1),m.group(2))
            string = ""
            pass
        m = re.match(self.label_re, string)
        if m:
            l.set_label(m.group(1))
            string = m.group(2)
            pass
        m = re.match(self.define_data_re, string)
        if m:
            data_define = m.group(1)
            value = m.group(2)
            l.set_data_definition(data_define,value)
            string = ""
            pass
        m = re.match(self.mnemonic_re, string)
        if m:
            mnemonic = m.group(1)
            addressing = m.group(2)
            ie = self.instruction_set.find_ie_of_mnemonic(mnemonic, addressing)
            if ie is not None:
                l.set_mnemonic_ie(m.group(1), ie)
                l.set_addresing(m.group(2))
                string = ""
                pass
            pass
        if re.match(self.blank_re,string):
            return l
        raise Exception("Unparsed assembler line (what remains...) %s"%string)
    def assemble(self, program, base_address=0, verbose=False):
        code = []
        parsed_program = []
        for l in program.split("\n"):
            parsed_program.append(self.parse_line(l))
            pass
        scope = c_assembler_scope()
        for asm_pass in range(2):
            scope.set_pc(base_address)
            for p in parsed_program:
                n = p.assemble(self.instruction_set, scope, asm_pass)
                scope.advance_pc(n)
                pass
            pass
        code_fragment = None
        for p in parsed_program:
            if p.assembly is not None:
                if (code_fragment is not None) and (code_fragment[1] != p.pc):
                    code_fragment = None
                    pass
                if code_fragment is None:
                    code_fragment = [p.pc, p.pc, []]
                    code.append(code_fragment)
                    pass
                code_fragment[2].extend(p.assembly)
                code_fragment[1] += len(p.assembly)
                pass
            if verbose:
                print p
                pass
            pass
        return code
    pass
    
