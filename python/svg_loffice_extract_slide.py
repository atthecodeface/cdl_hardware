#!/usr/bin/env python
# ../../../../python/svg_loffice_extract_slide.py
# pandoc riscv_cpu_implementation.md --pdf-engine=pdflatex -o temp.pdf
from xml.dom import minidom

scale=0.02
in_filename = "fred.svg"
out_filename = "pipeline.svg"
slide_id = "container-id1"

doc = minidom.parse(in_filename)
svg = doc.documentElement
contents = []
for d in svg.getElementsByTagName("defs"):
    if d.getAttribute("class")=="ClipPathGroup": contents.append(d)
    pass
for d in svg.getElementsByTagName("g"):
    if d.getAttribute("id")==slide_id:
        d.setAttribute("transform", "scale(%f)"%scale)
        contents.append(d)
        pass
    pass

vb = svg.getAttribute("viewBox")
vb_out=""
for d in vb.split():
    vb_out += "%f "%(int(d)*scale)
    pass
svg.setAttribute("viewBox",vb_out)

while svg.firstChild:
    svg.removeChild(svg.firstChild)
    pass

for x in contents:
    svg.appendChild(x)


out_file = open(out_filename,"w")
out_file.write(doc.toxml("utf-8"))
out_file.close()
