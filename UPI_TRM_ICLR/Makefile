.PHONY: pdf clean

PDFLATEX_FONT_COUNT := $(shell { kpsewhich phvb.tfm; kpsewhich ptmr8t.tfm; } 2>/dev/null | wc -l)

ifeq ($(PDFLATEX_FONT_COUNT),2)
LATEX = pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
else
LATEX = xelatex -interaction=nonstopmode -halt-on-error -file-line-error
endif

pdf:
	$(LATEX) main.tex
	bibtex main
	$(LATEX) main.tex
	$(LATEX) main.tex
	$(LATEX) main.tex

clean:
	$(RM) main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log main.out main.pdf main.synctex.gz main.toc
