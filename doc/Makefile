DOCUMENTATION = $(SRC_ROOT)/doc
DOXYGEN = DOCUMENTATION=$(DOCUMENTATION) SRC_ROOT=$(SRC_ROOT) doxygen

documentation: $(DOCUMENTATION)/doc_pdf

.PHONY: doxygen_cdl
doxygen_cdl:
	(cd $(DOCUMENTATION); DOXYGEN_INPUTS=$(SRC_ROOT)/cdl $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)

.PHONY: doxygen_cmodel
doxygen_cmodel:
	(cd $(DOCUMENTATION); DOXYGEN_INPUTS=$(SRC_ROOT)/cmodel $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)

.PHONY: doxygen_python
doxygen_python:
	(cd $(DOCUMENTATION); DOXYGEN_INPUTS=$(SRC_ROOT)/python $(DOXYGEN) $(DOCUMENTATION)/doxyfile.bbc_cdl)

$(DOCUMENTATION)/doc_pdf: doxygen_cdl
	(cd $(DOCUMENTATION)/cdl_latex; $(MAKE))
