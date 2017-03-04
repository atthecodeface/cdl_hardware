DOCUMENTATION = $(SRC_ROOT)/doc
DOXYGEN = DOCUMENTATION=$(DOCUMENTATION) SRC_ROOT=$(SRC_ROOT) doxygen 

clean: clean_doc

clean_doc:
	(cd $(DOCUMENTATION); rm -rf cdl_*latex cdl_*html dots/*dot)

documentation: $(DOCUMENTATION)/doc_pdf

.PHONY: doxygen_cdl
# Must do documents twice to generate the dotfiles
doxygen_cdl:
	(cd $(DOCUMENTATION); DOC_INTERNAL=yes DOC_TYPE=internal DOXYGEN_INPUTS=$(SRC_ROOT)/cdl $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)
	(cd $(DOCUMENTATION); DOC_INTERNAL=yes DOC_TYPE=internal DOXYGEN_INPUTS=$(SRC_ROOT)/cdl $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)
	(cd $(DOCUMENTATION); DOC_INTERNAL=no  DOC_TYPE=external DOXYGEN_INPUTS=$(SRC_ROOT)/cdl $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)

.PHONY: doxygen_cmodel
doxygen_cmodel:
	(cd $(DOCUMENTATION); DOXYGEN_INPUTS=$(SRC_ROOT)/cmodel $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)

.PHONY: doxygen_python
doxygen_python:
	(cd $(DOCUMENTATION); DOXYGEN_INPUTS=$(SRC_ROOT)/python $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)

$(DOCUMENTATION)/doc_pdf: doxygen_cdl
	(cd $(DOCUMENTATION)/cdl_latex; $(MAKE))
