# Final Theory-Only Build Report

Date: 2026-08-04

## Scope

This report records the final build and visual check of the theory-only ICLR
manuscript. The manuscript intentionally reports no experiments or learned
performance results. No change to `main.tex` was required during this final
verification.

## Repository state

- Branch: `iclr-evidence-aligned-revision`
- Baseline HEAD: `ca9cf0109e42d150a9d8a711c2d1739cda017ad1`
- The working tree contained the retained manuscript and supporting changes;
  this was a clean LaTeX rebuild, not a claim that the Git working tree was
  clean.

## Build

Commands:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_ICLR
PATH=/home/buiksat/texlive/2026/bin/x86_64-linux:$PATH make clean
PATH=/home/buiksat/texlive/2026/bin/x86_64-linux:$PATH make pdf \
  2>&1 | tee build/theory_only_final_build.stdout.log
cp main.pdf build/main_iclr_final.pdf
cmp -s main.pdf build/main_iclr_final.pdf
```

Result:

- Build completed successfully.
- Final PDF: 29 pages, 491,061 bytes.
- Main-body text reaches page 9. References begin on page 9 and end on page
  10. The appendix begins on page 11.
- The final LaTeX pass has no undefined references, undefined citations,
  duplicate destination warnings, or fatal errors. The full multi-pass
  transcript contains expected undefined-reference warnings from intermediate
  passes before BibTeX resolution.
- The remaining messages are non-fatal PDF-bookmark math-token warnings and
  underfull-box notices.
- No Type 3 font reference appears in the final LaTeX log; the emitted font
  files listed there are Type 1 `.pfb` files. `pdffonts` was unavailable, so
  this is a log-level check rather than an independent PDF font inventory.
- `build/main_iclr_final.pdf` is byte-identical to `main.pdf`.

## Hashes

SHA-256:

```text
69f3eb3f3b1951780714fc82ec216476d2d724fc999229a415c46b9e12d4b625  main.tex
f15d1c1d453477e56148bd24af34cdd6dd658d29558ac41d78dee735bc3ddce6  main.pdf
f15d1c1d453477e56148bd24af34cdd6dd658d29558ac41d78dee735bc3ddce6  build/main_iclr_final.pdf
7c5037c2651dec8df21b8ec8626fc359f68d21e4443defb8f3ce307a3b2a91cf  review/THEORY_ONLY_REVIEW_PROMPT.md
```

## Visual inspection

An independent DVI rendering was generated with `latex`, `bibtex`, and
`dvipng`. Pages 1, 5, 8, 9, 10, 15, 18, 27, and 29 were inspected at 160 DPI.
They cover the title and abstract, core theorem, final main-text bounds,
conclusion and reference boundary, appendix theory, deployment theorem,
Algorithm 2, and the final page.

No clipped text, incoherent overlap, missing content, or blocking layout issue
was observed. Algorithm 2 is legible and contained on page 27; its folded
terminal target, zero post-terminal rewards, and zero terminal bootstrap are
visible and consistent.

## Review deliverable

`review/THEORY_ONLY_REVIEW_PROMPT.md` requests an independent proof and
rendering audit. It explicitly states that the paper contains no experiments
and requires the exact wording `not verifiable from supplied evidence` for
unsupported runtime or evidence claims.
