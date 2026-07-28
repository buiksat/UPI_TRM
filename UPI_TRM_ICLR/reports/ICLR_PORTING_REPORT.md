# ICLR Template Porting Report

## Source and destination

- Source manuscript: `/home/buiksat/UPI_TRM/UPI_TRM_NIPS`
- Shared Git top level: `/home/buiksat/UPI_TRM`
- Parent branch at the corrected Phase 0 inspection: `iclr-revision`
- Source manuscript snapshot: `cf5db0da7ba9564e0846f852b0507291493efeae` (identical to `main` for the source subtree)
- Source Phase 0 status: clean; `git diff --quiet cf5db0d -- UPI_TRM_NIPS` returned success
- Source content-tree aggregate SHA-256: `fc506971ac98006166f295a693f56123fcb9beb2e8f87c5e6a7b8fed35624d5d`
- Source manuscript root: `main.tex`
- Source generated manuscript PDF: none; source PDFs are figure assets
- Source build documentation: `HANDOFF.md` records a single `pdflatex` command, but no complete bibliography-producing builder existed
- Destination: `/home/buiksat/UPI_TRM/UPI_TRM_ICLR`
- Destination state at Phase 0: absent, so no destination work could be overwritten
- Destination branch: `iclr-revision`

The paper workspaces are sibling subtrees of one parent Git repository, not independent nested repositories. The prior mispathed revision was preserved on `iclr-revision-mispath-backup`; the active `iclr-revision` branch was recreated from the clean pre-port commit. The archival sibling matches that pre-port commit and is not an input to this corrected ICLR build.

## Controlled source copy

The direct NeurIPS-to-ICLR copy command was:

```bash
rsync -a --itemize-changes \
  --exclude='.git/' \
  --exclude='__pycache__/' \
  --exclude='.pytest_cache/' \
  --exclude='.mypy_cache/' \
  --exclude='.ruff_cache/' \
  --exclude='.cache/' \
  --exclude='.venv/' \
  --exclude='venv/' \
  --exclude='env/' \
  --exclude='*.swp' \
  --exclude='*.swo' \
  --exclude='*~' \
  --exclude='.DS_Store' \
  --include='results/' \
  --include='results/finite_mdp_certificate/' \
  --include='results/finite_mdp_certificate/fig_value_decomposition.png' \
  --include='results/finite_mdp_certificate/fig_cpi_certificate.png' \
  --exclude='results/***' \
  --exclude='*.aux' \
  --exclude='*.bbl' \
  --exclude='*.blg' \
  --exclude='*.fdb_latexmk' \
  --exclude='*.fls' \
  --exclude='*.log' \
  --exclude='*.out' \
  --exclude='*.synctex.gz' \
  --exclude='main.pdf' \
  --exclude='*.zip' \
  --exclude='*.tar' \
  --exclude='*.tar.gz' \
  --exclude='*.tgz' \
  /home/buiksat/UPI_TRM/UPI_TRM_NIPS/ \
  /home/buiksat/UPI_TRM/UPI_TRM_ICLR/
```

This copied the TeX root, bibliography, required figures and generated tables, provenance/build documentation, the finite-MDP images read by LaTeX, and paper-specific scripts. It excluded Git metadata, caches, virtual environments, editor temporaries, raw result dumps not read by LaTeX, LaTeX build products, the old manuscript PDF, and archives. No destructive `--delete` was used.

The source aggregate SHA-256 remained unchanged after copying and after both baseline builds. The copied NeurIPS style file was removed during template conversion; it is not present in the ICLR workspace.

## Official ICLR template conversion

No next-cycle ICLR kit was available. The corrected port uses the latest official kit available locally, ICLR 2026, from the separate local author-kit workspace `/home/buiksat/UPI_TRM/UPI_TRM_ICLR_RSI`:

- `iclr2026_conference.sty`, SHA-256 `a4852f68e080d6c5245057ca2039100b409e31727898aa93c03d78ddb84374a3`
- `iclr2026_conference.bst`, SHA-256 `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5`

The root loads `\usepackage{iclr2026_conference,times}` in the style's default anonymous-review mode and uses `\bibliographystyle{iclr2026_conference}`. No final-copy command is present. The active NeurIPS package, final/preprint comments, checklist, and unused `cleveref` dependency were removed. One artifact filename list was changed mechanically from `\texttt` to line-breaking `\path`; its text is unchanged.

The scientific-body comparison against the source was inspected before the gate. Differences were limited to the venue header/package, anonymous template configuration, bibliography style, checklist removal, unused-package compatibility, and that filename line-break fix. The title, abstract, theorem statements, experiments, numerical claims, conclusions, figures, tables, bibliography, and appendix content were not revised before the successful baseline gate.

No ICML style file, bibliography style, command, or template was used. After the archive restoration, the corrected copy, template conversion, and build did not read from the archival sibling directory.

## Baseline compile gate

A minimal Makefile supplies the complete bibliography-producing command because `latexmk` is unavailable and the source documentation's single `pdflatex` pass is insufficient.

Exact canonical command:

```bash
(make clean && make pdf) > build/iclr_template_baseline_build_pass5_clean.stdout.log 2>&1
```

`make pdf` runs `pdflatex`, `bibtex`, and three further `pdflatex` passes. The command succeeded twice from a clean LaTeX state.

- Baseline PDF: `/home/buiksat/UPI_TRM/UPI_TRM_ICLR/build/upi_trm_iclr_template_baseline.pdf`
- Final baseline log: `build/upi_trm_iclr_template_baseline.log`
- First build transcript: `build/iclr_template_baseline_build_pass1.stdout.log`
- Reproducibility build transcript: `build/iclr_template_baseline_build_pass5_clean.stdout.log`
- Exit status: 0 for both builds
- Total pages: 40
- Main text: pages 1--9
- References: pages 10--11
- Appendix: starts on page 12
- Fatal LaTeX errors: none
- Undefined citations or references in the final pass: none
- Multiply-defined labels: none
- Missing figures or tables: none
- Overfull boxes: none
- Bibliography and appendix references: rendered and resolved
- Anonymity: rendered text says `Anonymous authors` and `Paper under double-blind review`; PDF author metadata is blank by construction

`pdfinfo`, `pdffonts`, and `pdftotext` are unavailable. Ghostscript opened every page, reported 40 pages, extracted text for the anonymity/reference checks, and rendered the requested pages. Visual inspection covered the title/abstract, Figure 1, Proposition 6.1, Theorem 6.5, the hard-Sudoku table, the projection-by-contraction table, both reference pages, and the first appendix page. No clipping, overlap, malformed equation/table, missing figure, bad page boundary, author identity, or stale venue label was observed.

Remaining nonfatal warnings are underfull boxes/vboxes and `hyperref` PDF-bookmark warnings for mathematical section titles. Imported Matplotlib figure PDFs contain Type 3 DejaVu fonts; regenerate those assets with embedded Type 1/TrueType fonts if the submission checker rejects them.

## Gate confirmation

The ICLR-formatted baseline compiled reproducibly before any scientific revision. The NeurIPS source subtree remains byte-for-byte unchanged, and the ICML archive remains at its pre-port tracked state. No experiment, theorem, citation, diagnostic, or build result was fabricated.
