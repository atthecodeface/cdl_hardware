#!/usr/bin/env python
#a Imports
import sys, re, unittest

#a Classes
#c c_fsm
class c_fsm:
    def __init__(self, cdl_file):
        self.name          = "fsm%d"%cdl_file.get_uid()
        self.dot_filename  = "dots/%s__fsm__%s.dot"%(cdl_file.filename_leaf_root,self.name)
        self.current_state   = "no known state"
        self.states = []
        self.transitions = []
        pass
    def add_state(self, state):
        self.states.append(state)
        pass
    def add_transition(self, src=None, tgt=None):
        if src is None: src=self.states[-1]
        if tgt is None: src=self.states[-1]
        self.transitions.append((src,tgt))
        pass
    def header(self):
        return "/** @dotfile %s **/"%self.dot_filename
    def write_dotfile(self):
        dot_file = open(self.dot_filename, "w")
        print >> dot_file, "digraph fsm__%s {"%self.name
        print >> dot_file, " node [shape=record, fontname=Helvetica, fontsize=10];  "
        for s in self.states:
            print >> dot_file, ' %s [ label="%s" ]; '%(s,s)
            pass
        for (s,t) in self.transitions:
            print >> dot_file, ' %s -> %s [ arrowhead="open", style="dashed" ]; '%(s,t)
            pass
        print >> dot_file, '}'
        dot_file.close()
        pass


#c c_cdl_file
class c_cdl_file:
    @staticmethod
    #f get_sigtype_and_name
    def get_sigtype_and_name(signal_desc):
        sigtype = None
        signal_desc = signal_desc.strip()
        signal_desc = signal_desc.split()
        if signal_desc[0] == "clocked": sigtype="clocked"
        if signal_desc[0] == "comb":   sigtype="comb"
        if signal_desc[0] == "net":   sigtype="net"
        return (sigtype,signal_desc[-1])
    #f __init__
    def __init__(self, filename, verbose=False):
        self.verbose = verbose
        self.filename_leaf       = filename[filename.rfind("/")+1:]
        self.filename_ext        = self.filename_leaf[self.filename_leaf.rfind(".")+1:]
        self.filename_leaf_root  = self.filename_leaf[:self.filename_leaf.rfind(".")]

        self.is_header_file = (self.filename_ext=="h")
        self.is_source_file = (self.filename_ext=="cdl")
        self.internal = ("@internal", "@endinternal")
        if self.is_header_file:
            self.internal = ("", "")
            pass
        pass
    #f get_uid
    def get_uid(self):
        self.uid = self.uid + 1
        return self.uid
    #f enter_module
    def enter_module(self):
        """Source files use a group to pull the module documentation together; header files are global"""
        if self.is_source_file:
            return "namespace %s {/** @addtogroup %s %s */ /**@{ */"%(self.filename_leaf_root,
                                                                             self.filename_leaf_root,
                                                                             self.filename_leaf_root)
        return ""
    #f leave_module
    def leave_module(self):
        """Leaving a module - for example before an include - permits namespace separation (kinda)"""
        if self.is_source_file:
            return " /** @} */ }"
            pass
        return ""
    #f header
    def header(self):
        """
        Return any header line for the file, without newlines (to not effect line numbers)
        """
        r = ""
        r += self.enter_module()
        return r
    #f footer
    def footer(self):
        """
        Output any footer line for the file, without a newline at the
        end (to not effect line numbers)
        """
        r = self.leave_module()
        return r
    #f find_first
    def find_first(self, l, r, strings):
        """
        Find the earliest occurence in l of any of the strings in
        'strings' If there are none, return ("", r+l, None) - i.e. a
        non-match with a skipped result of r+l.

        If at least one is found, then pick that which is earliest in
        l, and return (post-found-string, r+pre-found-string+string,
        string)
        """
        min_pos = (-1, "")
        for s in strings:
            p = l.find(s)
            if (p>=0) and ((p<min_pos[0]) or (min_pos[0]==-1)):
                min_pos = (p, s)
                pass
            pass
        if min_pos[0]<0:
            return ("", r+l, None)
        pend = min_pos[0]+len(min_pos[1])
        r = r + l[:pend]
        return (l[pend:], r, min_pos[1])
    #f try_parse_user_id
    def try_parse_user_id(self, l):
        """
        Try to find a user id at the start of the string, possibly
        after whitespace. Return None if none.
        """
        m=re.match("(\s*)([a-zA-Z_][a-zA-Z_0-9]*)(.*)",l)
        if m is None: return (None,None,l)
        return (m.group(2),m.group(1),m.group(3)+"\n")
    #f parse_init
    def parse_init(self):
        self.comment_start_strings = ["/*", "//", '"""', '"']
        self.pending_documentation = ""
        self.uid = 0
        self.parse_states = ["head"]
        self.parse_fns = {"head":self.parse_head,
                          "include":self.parse_include,
                          "comment":self.parse_comment,
                          "typedef":self.parse_typedef,
                          "typedef_fsm":self.parse_typedef_fsm,
                          "typedef_fsm_body":self.parse_typedef_fsm_body,
                          "typedef_fsm_transitions":self.parse_typedef_fsm_transitions,
                          "singleline_doc":self.parse_singleline_doc,
                          "multiline_doc":self.parse_multiline_doc,
                          "module_header":self.parse_module_header,
                          "module_ports":self.parse_module_ports,
                          "module_port_declaration":self.parse_module_port_declaration,
                          "module_body":self.parse_module_body,
                          "code_block":self.parse_code_block,
                          "code_block_brace":self.parse_code_block,
                          "signal_declaration":self.parse_signal_declaration,
                          "finish_statement":self.parse_finish_statement,
                          }
        pass
    #f parse_line
    def parse_line(self, l, result_so_far=""):
        self.post_newline = ""
        while len(l)>0:
            (l,result_so_far,states) = self.parse_fns[self.parse_states[-1]](l, result_so_far)
            if states is not None: self.parse_states=states
            pass
        return result_so_far+self.post_newline
    #f parse_comment
    def parse_comment(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ["*/"])
        if which is None: return ("", nr, None)
        self.parse_states.pop()
        return (nl, nr, None)
    #f parse_multiline_doc
    def parse_multiline_doc(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ['"""'])
        if which is None: return ("", nr, None)
        self.parse_states.pop()
        return (nl, nr[:-3]+'*/', None)
    #f parse_singleline_doc
    def parse_singleline_doc(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ['"'])
        if which is None: # An error really - newline in single-line comment
            return ("", nr, None)
        self.parse_states.pop()
        return (nl, nr[:-1]+'*/', None)
    #f parse_include
    def parse_include(self, l, r):
        r += self.leave_module()
        r += '#include'
        if self.is_source_file:
            self.post_newline += self.enter_module()
            pass
        self.parse_states.pop()
        return ("", r+l, None)
    #f parse_typedef
    def parse_typedef(self, l, r):
        enum = re.match(r'(\s*enum)(\s*\[.*\])(.*$)',l)
        fsm  = re.match(r'(\s*)fsm(.*$)',l)
        if enum is not None:
            r += enum.group(1)
            l = enum.group(3)+"\n"
            self.parse_states.pop()
            return (l, r, None)
            pass
        if fsm is not None:
            self.fsm = c_fsm(self)
            r = r[:-7] + self.fsm.header() + "typedef" + fsm.group(1)+"enum"
            l = fsm.group(2)+"\n"
            self.parse_states[-1] = "typedef_fsm"
            return (l, r, None)
            pass
        self.parse_states.pop()
        return (l, r, None)
    #f parse_typedef_fsm
    def parse_typedef_fsm(self, l, r):
        """Parse everything post 'typedef fsm'"""
        (nl, nr, which) = self.find_first(l, r, ["{", ] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: return (nl, nr, which)
        if which is not None:
            self.parse_states[-1] = "typedef_fsm_body"
            return (nl, nr, None)
        return ("", r+l, None)
    #f parse_typedef_fsm_body
    def parse_typedef_fsm_body(self, l, r):
        """Parse everything post 'typedef fsm {'"""
        (u,ws,nl) = self.try_parse_user_id(l)
        if u is not None:
            self.fsm.add_state(u)
            pass
        (nl, nr, which) = self.find_first(l, r, [";", "{", "}", ] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: return (nl, nr, which)
        if which == "{":
            return (nl, nr[:-1], self.parse_states + ["typedef_fsm_transitions"])
        if which == "}":
            self.fsm.write_dotfile()
            self.parse_states.pop()
            return (nl, nr, None)
        if which == ";":
            return (nl, nr[:-1]+",", None)
        return ("", r+l, None)
    #f parse_typedef_fsm_transitions
    def parse_typedef_fsm_transitions(self, l, r):
        """Parse a list of transition targets"""
        (u,ws,nl) = self.try_parse_user_id(l)
        if u is not None:
            self.fsm.add_transition(tgt=u)
            l = nl
        (nl, nr, which) = self.find_first(l, r, ["}", "," ] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: return (nl, nr, which)
        if which == "}":
            self.parse_states.pop()
            return (nl, nr[:-1], None)
        if which == ",":
            return (nl, nr[:-1], None)
        return ("", r+l, None)
    #f parse_comment_start_string
    def parse_comment_start_string(self, nl, nr, which):
        if which == "/*":  return (nl, nr, self.parse_states+["comment"], True)
        if which == '"': 
            if self.pending_documentation=="": self.pending_documentation=" "
            result = (nl, nr[:-1]+"/**"+self.pending_documentation,  self.parse_states+["singleline_doc"], True)
            self.pending_documentation = ""
            return result
        if which == '"""':
            if self.pending_documentation=="": self.pending_documentation=" "
            result = (nl, nr[:-3]+"/**"+self.pending_documentation,  self.parse_states+["multiline_doc"], True)
            self.pending_documentation = ""
            return result
        if which == "//":  return ("", nr+nl, None, True)
        return (nl, nr, which, False)
    #f parse_head
    def parse_head(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ["module", "include", "typedef"] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: return (nl, nr, which)
        if which == "module": return (nl, nr, ["module_header"])
        if which == "include": return (nl, nr[:-7], self.parse_states+["include"])
        if which == "typedef": return (nl, nr, self.parse_states+["typedef"])
        return ("", r+l, None)
    #f parse_module_header
    def parse_module_header(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ["(", "{"]  + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: 
            return (nl, nr, which)
        if which == "(":
            return (nl, nr, self.parse_states+["module_ports"])
        if which == "{":
            return (nl, nr, ["module_body"])
        return ("", r+l, None)
    #f parse_module_ports
    def parse_module_ports(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ["clock", "input", "output", ")"]  + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: 
            return (nl, nr, which)
        if which in ["clock", "input", "output"]:
            return (nl+which, nr, self.parse_states+["module_port_declaration"])
        if which == ")":
            self.parse_states.pop()
            return (nl, nr, None)
        return ("", r+l, None)
    #f parse_module_port_declaration
    def parse_module_port_declaration(self, l, r):
        which = None # in case of multiline declaration
        if l[-5:]=="clock": which="clock"
        if l[-5:]=="input": which="input"
        if l[-6:]=="output": which="output"
        if which is not None:
            self.pending_documentation = '<%s '%({"clock":"[in]","input":"[in]","output":"[out]"}[which])
            l = l[:-len(which)]
            pass
        (nl, nr, which) = self.find_first(l, r, [",", ")"]  + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: 
            return (nl, nr, which)
        if which in [","]:
            self.parse_states.pop()
            return (nl, nr, None)
        if which == ")":
            self.parse_states.pop()
            return (nl+")", nr[:-1], None)
        return ("", r+l, None)
    #f parse_module_body
    def parse_module_body(self, l, r):
        self.pending_documentation = ""
        code_block_match = re.match(r'\s*([^ ]*)\s*"""',l)
        if code_block_match:
            self.pending_documentation="%s @section %s__%s"%(self.internal[0], self.filename_leaf_root,code_block_match.group(1))
            pass
        (nl, nr, which) = self.find_first(l, r, ["clocked", "comb", "net", ":"] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: 
            return (nl, nr, which)
        if which in ["clocked", "comb", "net"]:
            return (which+nl, nr, self.parse_states+["signal_declaration"])
        if which in [":"]:
            return (nl, nr, self.parse_states+["code_block"])
        return ("", r+l, None)
    #f parse_code_block
    def parse_code_block(self, l, r):
        (nl, nr, which) = self.find_first(l, r, ["{", "}"] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: 
            return (nl, nr, which)
        if which in ["{"]:
            return (nl, nr, self.parse_states+["code_block_brace"])
        if which in ["}"]:
            if self.parse_states[-1] != "code_block_brace":
                raise Exception("Mismatch in braces")
            self.parse_states.pop()
            if self.parse_states[-1] == "code_block_brace":
                return (nl, nr, None)
            if self.parse_states[-1] != "code_block":
                raise Exception("Mismatch in braces - expected end of code block")
            self.parse_states.pop()
            return (nl, nr + "/** %s */"%(self.internal[1]), None)
        return ("", r+l, None)
    #f parse_finish_statement
    def parse_finish_statement(self, l, r):
        (nl, nr, which) = self.find_first(l, r, [";"] + self.comment_start_strings )
        (nl, nr, which, parsed) = self.parse_comment_start_string( nl, nr, which )
        if parsed: 
            return (nl, nr, which)
        if which==";":
            self.parse_states.pop()
            return (nl, nr, None)
        return (nl, nr, None)
    #f parse_signal_declaration
    def parse_signal_declaration(self, l, r):
        if   l[:3] == "net":     which="net"
        elif l[:4] == "comb":    which="comb"
        elif l[:7] == "clocked": which="clocked"
        l = l[len(which):]
        p0 = l.find("=")
        p1 = l.find(";")
        p2 = l.find('"')
        if p0<0: p0=1e9
        if p1<0: p1=1e9
        if p2<0: p2=1e9
        p = min(p0,p1,p2)
        if p>len(l): # bail if bad
            self.parse_states.pop()
            return ("", r+l, None)
        (sigtype,signame) = c_cdl_file.get_sigtype_and_name(which+" "+l[:p])
        has_documentation = (p2<len(l))
        if signame is None:
            self.parse_states.pop()
            return ("", r+l, None)
        self.pending_documentation = '%s @param %s:%s '%(self.internal[0],sigtype,signame)
        r += l[:p]
        l = l[p:]
        # Do the following to 'insert' documentation - probably unwise, and better to encourage documentation in the code
        # It also breaks if reset values spread across a line and documentation is therefore on the next line
        #if not has_documentation:
        #    l = '""' + l
        self.parse_states.pop()
        return (l, r, self.parse_states+["finish_statement"])
    #f All done
    pass

#a Tests
#c c_base_test
class c_base_test(unittest.TestCase):
    filename = "a.cdl" # Source code
    input_text = r"""
    """
    output_text = r"""/** \addtogroup a **/namespace a {
    
}"""
    verbose=False
    def base_test(self):
        cdl_file = c_cdl_file(self.filename, self.verbose)
        r = ""
        r += cdl_file.header()
        cdl_file.parse_init()
        for l in self.input_text.split("\n"):
            r += cdl_file.parse_line(l+"\n")
            pass
        r += cdl_file.footer()
        if r != self.output_text:
            import difflib
            r = r.split("\n")
            r = [(l+"\n") for l in r]
            e = self.output_text.split("\n")
            e = [(l+"\n") for l in e]
            for l in difflib.context_diff(r,e, fromfile='result', tofile='expectation'):
                sys.stdout.write(l)
                pass
            self.assertTrue(False, "Result differs from output_text")
            pass
        pass
    pass

#c c_test_source
class c_test_source(c_base_test):
    input_text = r"""
    This is test text"""
    output_text = r"""/** \addtogroup a **/namespace a {
    This is test text
}"""
    test0 = c_base_test.base_test
    pass

#c c_test_include
class c_test_include(c_base_test):
    input_text = r"""
    include "fred.h" """
    output_text = r"""/** \addtogroup a **/namespace a {
    }#include "fred.h" 
namespace a {}"""
    test0 = c_base_test.base_test
    pass

#c c_test_single_comment
class c_test_single_comment(c_base_test):
    input_text = r"""
    This is test text // /* """
    output_text = r"""/** \addtogroup a **/namespace a {
    This is test text // /* 
}"""
    test0 = c_base_test.base_test
    pass

#c c_test_single_comment_with_include
class c_test_single_comment_with_include(c_base_test):
    input_text = r"""
    This is test text // include "a.h" """
    output_text = r"""/** \addtogroup a **/namespace a {
    This is test text // include "a.h" 
}"""
    test0 = c_base_test.base_test
    pass

#c c_test_multiline_comment
class c_test_multiline_comment(c_base_test):
    input_text = r"""
    This is test text /*
    */"""
    output_text = r"""/** \addtogroup a **/namespace a {
    This is test text /*
    */
}"""
    test0 = c_base_test.base_test
    pass

#c c_test_multiline_comment_with_include
class c_test_multiline_comment_with_include(c_base_test):
    input_text = r"""
    This is test text /* include "a.h"
    include"b.h"
    */"""
    output_text = r"""/** \addtogroup a **/namespace a {
    This is test text /* include "a.h"
    include"b.h"
    */
}"""
    test0 = c_base_test.base_test
    pass

#c c_test_singleline_document
class c_test_singleline_document(c_base_test):
    filename = 'a.h'
    input_text = r'''
    This is test "text" /
    " Stuff in comments
    Continues """
    done'''
    output_text = r"""
    This is test /** text*/ /
    /**  Stuff in comments
    Continues *//** */
    done
"""
    test0 = c_base_test.base_test
    pass

#c c_test_multiline_document
class c_test_multiline_document(c_base_test):
    filename = 'a.h'
    input_text = r'''
    This is test """text""" /
    """ Stuff in comments
    Continues """
    done'''
    output_text = r"""
    This is test /** text*/ /
    /**  Stuff in comments
    Continues */
    done
"""
    test0 = c_base_test.base_test
    pass

#c c_test_multiline_document_comments
class c_test_multiline_document_comments(c_base_test):
    filename = 'a.h'
    input_text = r'''
    // /* """
    /* """ */
    This is test """text""" /
    """ Stuff in comments
    Continues """
    """ // fred """
    """ /* fred """ */
    done'''
    output_text = r'''
    // /* """
    /* """ */
    This is test /** text*/ /
    /**  Stuff in comments
    Continues */
    /**  // fred */
    /**  /* fred */ */
    done
'''
    test0 = c_base_test.base_test
    pass

#c c_test_enum
class c_test_enum(c_base_test):
    filename = 'a.h'
    input_text = r"""
    typedef enum[4] {
    } fred;"""
    output_text = r"""
    typedef enum {
    } fred;
"""
    test0 = c_base_test.base_test
    pass

#c c_test_fsm_simple
class c_test_fsm_simple(c_base_test):
    filename = 'a.h'
    input_text = r"""
    typedef fsm {
    joe;
    jim;
    } fred;"""
    output_text = r"""
    typedef enum {
    joe,
    jim,
    } fred;
"""
    test0 = c_base_test.base_test
    pass

#c c_test_fsm_transitions
class c_test_fsm_transitions(c_base_test):
    filename = 'a.h'
    input_text = r"""
    typedef fsm {
    joe {peter, bunny};
    jim;
    } fred;"""
    output_text = r"""
    typedef enum {
    joe,
    jim,
    } fred;
"""
    test0 = c_base_test.base_test
    pass

#c c_test_module_simple
class c_test_module_simple(c_base_test):
    filename = 'a.h'
    input_text = r"""
    module fred() {
    }"""
    output_text = r"""
    module fred() {
    }
"""
    test0 = c_base_test.base_test
    pass

#c c_test_module_signal
class c_test_module_signal(c_base_test):
    filename = 'a.h'
    input_text = r"""
    module fred() {
    net bit joe2 "documentation";
    net bit joe;
    comb bit joe3;
    clocked t_banana joe3={*={fred=0}};
    clocked t_banana joe4={*={fred=0}} "And documented";
    }"""
    output_text = r"""
    module fred() {
    net bit joe2 /** @param net:joe2 documentation*/;
    net bit joe/** @param net:joe */;
    comb bit joe3/** @param comb:joe3 */;
    clocked t_banana joe3/** @param clocked:joe3 */={*={fred=0}};
    clocked t_banana joe4={*={fred=0}} /** @param clocked:joe4 And documented*/;
    }
"""
    test0 = c_base_test.base_test
    pass

#c c_test_module_code_block
class c_test_module_code_block(c_base_test):
    filename = 'a.h'
    input_text = r'''
    module fred() {
    code_block """
    My documented code block
    """ : {
    }
    }'''
    output_text = r"""
    module fred() {
    code_block /** @section a__code_block
    My documented code block
    */ : {
    }
    }
"""
    test0 = c_base_test.base_test
    pass

#c c_test_module_code_block2
class c_test_module_code_block2(c_base_test):
    filename = 'a.h'
    input_text = r'''
module led_seven_segment( input bit[4] hex   "Hexadecimal to display on 7-segment LED",
                          output bit[7] leds "1 for LED on, 0 for LED off, for segments a-g in bits 0-7"
    )
    /*b Documentation */
"""
Simple module to map a hex value to the LEDs required to make the
appropriate symbol in a 7-segment display.

The module combinatorially takes in a hex value, and drives out 7 LED
values.
"""{}'''
    output_text = r"""
module led_seven_segment( input bit[4] hex   /** Hexadecimal to display on 7-segment LED*/,
                          output bit[7] leds /** 1 for LED on, 0 for LED off, for segments a-g in bits 0-7*/
    )
    /*b Documentation */
/** 
Simple module to map a hex value to the LEDs required to make the
appropriate symbol in a 7-segment display.

The module combinatorially takes in a hex value, and drives out 7 LED
values.
*/{}
"""
    test0 = c_base_test.base_test
    verbose=False
    pass

#a Toplevel
a=re.compile(r'"(.*)"')
infilename = sys.argv[1]

if infilename == "___test___":
    unittest.main(argv=[""])
    sys.exit(0)

outfile=sys.stdout
print >> sys.stderr, "Filter", infilename

f = open(infilename)
cdl_file = c_cdl_file(infilename)
outfile.write(cdl_file.header())
cdl_file.parse_init()
for l in f:
    outfile.write(cdl_file.parse_line(l))
    pass
outfile.write(cdl_file.footer())
sys.exit(0)

