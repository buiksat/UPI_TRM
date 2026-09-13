.PHONY: pdf clean
LATEX = pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
BIBTEX ?= bibtex
pdf:
	$(LATEX) main.tex
	$(BIBTEX) main
	$(LATEX) main.tex
	$(LATEX) main.tex
	$(LATEX) main.tex
clean:
	$(RM) main.aux main.bbl main.blg main.log main.out main.pdf main.fls main.fdb_latexmk
