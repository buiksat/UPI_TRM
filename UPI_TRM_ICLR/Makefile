.PHONY: pdf clean

LATEX = pdflatex -interaction=nonstopmode -halt-on-error -file-line-error

pdf:
	$(LATEX) main.tex
	bibtex main
	$(LATEX) main.tex
	$(LATEX) main.tex
	$(LATEX) main.tex

clean:
	$(RM) main.aux main.bbl main.blg main.fdb_latexmk main.fls main.log main.out main.pdf main.synctex.gz main.toc
