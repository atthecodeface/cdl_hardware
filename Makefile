CDL_HARDWARE = ../cdl_hardware

help:
	@echo "To update, build documentation in a cdl_hardware repo"
	@echo "(cd ${CDL_HARDWARE}; make documentation"
	@echo ""
	@echo "Then copy the required documentation out to here"
	@echo "cp -r ${CDL_HARDWARE}/doc/cdl_external_html ."
	@echo "cp    ${CDL_HARDWARE}/doc/cdl_external_latex/refman.pdf ./cdl_external_refman.pdf"
	@echo ""
	@echo "Then add the files as required"
	@echo "git add cdl_external_html"

