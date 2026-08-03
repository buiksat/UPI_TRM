# Pre-repair paper build

## Repository baseline

- Repository: `UPI_TRM_ICLR`
- Branch: `iclr-evidence-aligned-revision`
- Source commit: `0fc168dd144f46d68517437df75b72ecfb777d7f`
- Build state: isolated copy of that source tree, before the current repair

The build ran in an isolated clean copy so existing generated files in the working tree were not reused or overwritten.

## Command

```bash
make clean
make pdf
```

The two commands completed successfully. The retained build products are:

- `build/main_pre_repair.pdf`
- `build/main_pre_repair.log`

## PDF result

- SHA-256: `00d0d235e208c36d2a8cbd2d06b74acfb2454099819f54084df94862459ef5c3`
- Size: 1,170,606 bytes
- Total pages: 38
- Main text: pages 1--9
- References: pages 10--11
- Appendix: pages 12--38

## LaTeX diagnostics

- Fatal LaTeX errors: 0
- Undefined citations: 0
- Undefined references: 0
- Overfull boxes: 0
- Hyperref PDF-string warnings: 30
- Underfull `hbox` warnings: 12
- Underfull `vbox` warnings: 5
- Float placement changes from `h` to `ht`: 1

The build log records Type 1 PFB font files. `pdffonts` is not installed in the baseline environment, so this phase did not independently certify the absence of Type 3 fonts in the rendered PDF. A final font inspection remains required.

## Baseline interpretation

This result establishes that the pre-repair source compiles and resolves its references. It does not validate theorem statements, numerical claims, evidence provenance, anonymity, page-limit compliance, or reproducibility of any experiment.
