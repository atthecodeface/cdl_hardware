# pandoc needs the path to pdflatex
PANDOC = PATH="/Library/TeX/texbin/:${PATH}" pandoc --pdf-engine=pdflatex  

DIAGRAM_INSTALL_BIN := $(shell which diagram)
all:

%.svg: dml/%.dml dss/%.dss $(DIAGRAM_INSTALL_BIN)
	@echo "Use diagam on DML/DSS files to create $@"
	@diagram --f dml/$*.dml dss/$*.dss --svg $@


%.pdf: %.md
	@echo "Run pandoc on $*.md to generate $@"
	@${PANDOC} --toc $*.md -o $@


%.pdf: %.md
	@echo "Run pandoc on $*.md to generate $@"
	@${PANDOC} --toc $*.md -o $@

reve_r__images  += pipeline.svg
reve_r__sources += reve_r/title.md
reve_r__sources += reve_r/introduction.md
reve_r__sources += reve_r/architecture.md
reve_r__sources += reve_r/implementation.md
reve_r__sources += reve_r/interfacing.md
reve_r__sources += reve_r/modes.md
reve_r__sources += reve_r/exceptions_and_interrupts.md
reve_r__sources += reve_r/debug.md
reve_r__sources += reve_r/trace.md
reve_r__sources += reve_r/extensions.md
reve_r__sources += reve_r/coprocessors.md

#f cmodel_template
define cmodel_template
# @param $1 c filename
# @param $2 object filename
# @param $3 model name
# @param $4 options

${TARGET_DIR}/$2 : ${SRC_ROOT}/$1
	@echo "CC $1 -o $2" 
	$(Q)$(CXX) $(CXXFLAGS) -c -o ${TARGET_DIR}/$2 ${SRC_ROOT}/$1 $4

MODELS += $3
C_MODEL_SRCS += ${SRC_ROOT}/$1
C_MODEL_OBJS += ${TARGET_DIR}/$2

endef

reve_r.pdf: $(reve_r__images)
reve_r.pdf: $(reve_r__sources)
	@echo "Run pandoc on reve_r source md files to generate $@"
	@${PANDOC} --toc $(reve_r__sources) -o $@

all: reve_r.pdf

