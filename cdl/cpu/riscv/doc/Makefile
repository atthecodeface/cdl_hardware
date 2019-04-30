# pandoc needs the path to pdflatex
PANDOC = PATH="/Library/TeX/texbin/:${PATH}" pandoc --pdf-engine=pdflatex  

DIAGRAM_INSTALL_BIN := $(shell which diagram)
all: riscv_cpu_implementation.pdf

%.svg: dml/%.dml dss/%.dss $(DIAGRAM_INSTALL_BIN)
	@echo "Use diagam on DML/DSS files to create $@"
	@diagram --f dml/$*.dml dss/$*.dss --svg $@


%.pdf: %.md
	@echo "Run pandoc on $*.md to generate $@"
	@${PANDOC} --toc $*.md -o $@


riscv_cpu_implementation.pdf: pipeline.svg

