DOXYGEN = doxygen

documentation: doc_pdf

doxygen:
	$(DOXYGEN) Doxyfile

doc_pdf: doxygen
	(cd latex; $(MAKE))
