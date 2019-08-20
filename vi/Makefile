MAIN_TEX := presentation_example
TEX_ENGINE := pdflatex
BIBTEX_ENGINE := bibtex
TEX_FLAGS := -shell-escape
LATEXMK_FLAGS := -recorder -pvc -shell-escape -quiet

TEX_FILES := $(shell find . -type f -name "*.tex")
BIB_FILES := $(shell find . -type f -name "*.bib")

BUILDID=$(shell date +%Y%m%d-%H:%M:%S)

PDF_FILE := $(MAIN_TEX).pdf
TEX_COMMAND := $(TEX_ENGINE) $(TEX_FLAGS)

#	Set up viewer and number of parallel jobs for figures
VIEWER :=
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    VIEWER = evince
    NJOBS=$(shell nproc --all)
endif
ifeq ($(UNAME_S),Darwin)
    VIEWER = open
    NJOBS=$(shell sysctl -n hw.ncpu)
endif

#	Set up latexmk flags
ifeq ($(TEX_ENGINE),pdflatex)
	LATEXMK_FLAGS += -pdf
else
	LATEXMK_FLAGS += -$(TEX_ENGINE)
endif


$(PDF_FILE): $(TEX_FILES) $(BIB_FILES)
	$(TEX_COMMAND) $(MAIN_TEX)
	[ -f $(MAIN_TEX).makefile ] && $(MAKE) -f $(MAIN_TEX).makefile -j$(NJOBS) || echo Skip making figures
	$(TEX_COMMAND) $(MAIN_TEX)
	# $(BIBTEX_ENGINE) $(MAIN_TEX)
	# $(TEX_COMMAND) $(MAIN_TEX)
	# $(TEX_COMMAND) $(MAIN_TEX)


figures:
	$(TEX_COMMAND) $(MAIN_TEX)
	[ -f $(MAIN_TEX).makefile ] && $(MAKE) -f $(MAIN_TEX).makefile -j$(NJOBS) -B || echo Skip making figures
	$(TEX_COMMAND) $(MAIN_TEX)

incremental:
	latexmk $(LATEXMK_FLAGS) -g $(MAIN_TEX) 

view: $(PDF_FILE)
	$(VIEWER) $(PDF_FILE) &

clean:
	rm -rf *.sav *.bak *.aux *.bcf *.fdb_latexmk *.fls *.makefile *.run.xml *.bbl *.blg *.figlist *.log *.pdf *.out *.toc *.xdv *nav *snm *vrb
	find . -name "*.log" -type f -delete
	find . -name "*.dep" -type f -delete
	find . -name "*.dpth" -type f -delete
	@find . -name "*.md5" -type f -delete

superclean: clean
	@find . -name *.pdf -type f -delete


commit: $(PDF_FILE)
	@status=$$(git status --porcelain); \
    if test "x$${status}" != x; then \
		git add -A .; \
		git commit -s -m "[ci] Automatic commit of successful build $(BUILDID)"; \
	fi 

push: commit
	git push origin master