DOCUMENTATION = $(SRC_ROOT)/doc
DOXYGEN = DOCUMENTATION=$(DOCUMENTATION) SRC_ROOT=$(SRC_ROOT) doxygen 
CDL_EXTERNAL_REF_SED_SCRIPT = '/\\chapter{Namespace Index}/d;/\\input{namespaces}/d;/\\input{.*cdl}/d;s/\\chapter{File Documentation}/\\chapter{Header Files}/;/\\chapter{Namespace Documentation}/d;/\\input{namespace.*}/d;'

clean: clean_doc

clean_doc:
	(cd $(DOCUMENTATION); rm -rf cdl_*latex cdl_*html dots/*dot)
	mkdir -p $(DOCUMENTATION)/cdl_external_latex
	mkdir -p $(DOCUMENTATION)/cdl_internal_latex
	mkdir -p $(DOCUMENTATION)/cdl_external_html
	mkdir -p $(DOCUMENTATION)/cdl_internal_html

documentation: doxygen_cdl $(DOCUMENTATION)/cdl_external_latex/refman.pdf $(DOCUMENTATION)/cdl_internal_latex/refman.pdf

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

$(DOCUMENTATION)/cdl_internal_latex/refman.pdf: doxygen_cdl
	(cd $(DOCUMENTATION)/cdl_internal_latex; sed -i '/\\chapter{Namespace Index}/d;/\\input{namespaces}/d' refman.tex ; $(MAKE))

cdl_external_pdf: $(DOCUMENTATION)/cdl_external_latex/refman.pdf

remake_cdl_external_pdf:
	rm $(DOCUMENTATION)/cdl_external_latex/refman.pdf
	$(MAKE) cdl_external_pdf

$(DOCUMENTATION)/cdl_external_latex/refman.pdf:
	(cd $(DOCUMENTATION)/cdl_external_latex; sed -i $(CDL_EXTERNAL_REF_SED_SCRIPT) refman.tex ; $(MAKE))
