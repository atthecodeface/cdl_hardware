#!/usr/bin/env python
import sys, re
a=re.compile(r'"(.*)"')
infilename = sys.argv[1]
outfile=sys.stdout
print >> sys.stderr, "Filter", infilename
f = open(infilename)

def get_sigtype_and_name(signal_desc):
    sigtype = None
    signal_desc = signal_desc.strip()
    signal_desc = signal_desc.split()
    if signal_desc[0] == "clocked": sigtype="clocked"
    if signal_desc[0] == "comb":   sigtype="comb"
    return (sigtype,signal_desc[-1])

infile_leaf = infilename[infilename.rfind("/")+1:]
infile_ext  = infile_leaf[infile_leaf.rfind(".")+1:]
infile_leaf_root = infile_leaf[:infile_leaf.rfind(".")]

in_header_file = (infile_ext=="h")
in_source_file = (infile_ext=="cdl")
if in_source_file:
    outfile.write(r"/** \addtogroup %s **/namespace %s {"%(infile_leaf_root, infile_leaf_root))
    pass
in_comment = False
in_multiline_documentation = False
in_fsm_enum = False
in_module_header = False
in_module_body   = False
for l in f:
    if in_comment:
        if (l.rfind("*/")>=0):
            in_comment = False
            pass
        pass
    elif in_multiline_documentation:
        mc=l.find('"""')
        if mc>=0:
            l=re.sub(r'"""',r'*/',l)
            in_multiline_documentation = False
            pass
        pass
    else:
        if "module " in l:
            in_module_header = True
            pass
        if in_module_header:
            if re.match(r'\s*{\s*',l):
                in_module_body = True
                pass
            pass
        if in_module_body:
            has_documentation = (re.search(r'"([^"]+)"',l) is not None)
            (sigtype,signame) = (None,None)
            if re.match(r'\s*clocked\s.*=.*',l):
                sigtype,signame = get_sigtype_and_name(l[:l.find("=")])
                pass
            if re.match(r'\s*comb\s.*;',l):
                if has_documentation:
                    sigtype,signame = get_sigtype_and_name(l[:l.find('"')])
                    pass
                else:
                    sigtype,signame = get_sigtype_and_name(l[:l.find(";")])
                    pass
                pass
            if signame is not None:
                if has_documentation:
                    l = re.sub(r'"([^"]+)"',r'/** @param %s:%s \1 */'%(sigtype,signame),l)
                    pass
                else:
                    l = ("/** @param %s:%s */"%(sigtype,signame))+l
                    pass
                pass
            code_block_match = re.match(r'\s*([^ ]*)\s*"""',l)
            if code_block_match:
                l=re.sub(r'"""',r'/** \section %s'%code_block_match.group(1),l)
                in_multiline_documentation = True
                pass
            pass

        (l,n)=re.subn(r'(include\s*".*")',r'#\1',l)
        if n!=0:
            if in_source_file:
                l = "}%s namespace %s {"%(l,infile_leaf_root)
                pass
            pass
        else:
            l=re.sub(r'"([^"]+)"',r'/** \1 */',l)
            pass

        l=re.sub(r'typedef\s*enum(.*\[.*\])',r'typedef enum',l)
        (l,n) = re.subn(r'typedef\s*fsm',r'typedef enum',l)
        if (n>0):
            in_fsm_enum = True
            pass
        if in_fsm_enum and ("}" in l):
            in_fsm_enum = False
            pass
        if in_fsm_enum:
            l = re.sub(r';', r',', l)
            pass

        mc=l.find('"""')
        if (mc>=0):
            if l[mc+1].find('"""')>=0:
                l=re.sub(r'"""(.*)"""',r'/** \1 */',l)
                pass
            else:
                l=re.sub(r'"""',r'/**',l)
                in_multiline_documentation = True
                pass
            pass
        pass
    if not in_multiline_documentation:
        c=l.rfind("/*")
        if c>=0:
            in_comment = c>l.rfind("*/")
            pass
        pass
    outfile.write(l)
    pass
if infile_ext=="cdl":
    outfile.write(r"}")
sys.exit(0)
