# Post-fixed-base paper build attempt

Date: 2026-08-03, America/Los_Angeles

## Source state

- Repository: `/home/buiksat/UPI_TRM`
- Branch: `iclr-evidence-aligned-revision`
- Baseline before the current paper edit: `baf196b`
- `main.tex` SHA-256:
  `d6c3e5eac568c6db6b8d2a9c22a1e5326ec27455a978fd3bd242129377548a5b`

## Command and result

The build was attempted from a clean generated-file state:

```bash
make clean
make pdf
```

It failed before parsing the manuscript because `pdflatex` is not installed or
available on `PATH`:

```text
make: pdflatex: No such file or directory
make: *** [Makefile:6: pdf] Error 127
```

The retained stdout log is
`build/post_fixed_base_build.stdout.log`, SHA-256
`7b053767cbe86c4dd76b644c2150c61cb6bbe05bd44a97407f1e3e6543abb5cc`.
An isolated conda environment was also attempted, but the host could not reach
the conda-forge package channel. No system package was modified.

## Prior PDF preservation

`make clean` removed the ignored prior `main.pdf` and `main.log`. Both were
restored from the untouched pre-existing GPT Pro review bundle:

- prior `main.pdf` SHA-256:
  `ca4b555b4c05d67a4e32a597f2f96178283d7b25a494dd575d5786fa20bf78b4`;
- prior `main.log` SHA-256:
  `e728159abd0ec346131c21267892d47d37889849943a7c8b9716f3d32f67f5c4`.

These restored files predate the current source edit. They are stale and are
not evidence of a successful current build. Current PDF syntax, page count,
font status, and visual layout are **not verifiable from supplied evidence**
on this host until a TeX toolchain is available.
