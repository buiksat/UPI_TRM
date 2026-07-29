# ICLR Final Validation

Updated 2026-07-29 after the external mathematical and evidence audit.

## Scope and provenance

- Validated workspace: `/home/buiksat/UPI_TRM/UPI_TRM_ICLR`
- Branch: `iclr-revision`
- Corrected baseline commit: `3cc3653` (`Port NeurIPS manuscript to official ICLR template without content changes`)
- Last staged scientific commit before final evidence corrections: `2efb893` (`Fit revised manuscript within ICLR main-text limit`)
- The current validation covers the post-audit working-tree revision; commit hashes above identify the porting baseline, not the revised manuscript state.
- `git diff --quiet cf5db0d -- UPI_TRM_NIPS` succeeds; the NeurIPS source was not modified
- A targeted Git diff against `cf5db0d` succeeds for the archival sibling; it is restored to its pre-port tracked state

## Style, anonymity, and page allocation

- Active style: official ICLR 2026 temporary porting baseline, `iclr2026_conference.sty` and `iclr2026_conference.bst`, sourced from the separate local author-kit workspace `UPI_TRM_ICLR_RSI`
- No active NeurIPS or ICML package, bibliography style, checklist, final/preprint option, or ICLR final-copy command remains
- No source, report, generated script, or build configuration in the ICLR workspace contains an accidental reference to the old mispathed workspace
- PDF author metadata is empty by construction; rendered/text inspection shows `Anonymous authors` and `Paper under double-blind review`
- Baseline PDF: 40 total pages; main text 1--9, references 10--11, appendix from 12
- Revised PDF: 38 total pages; main text 1--9, references 10--11, appendix from 12
- No official margin, spacing, or font-size parameter was overridden to meet the nine-page main-text allocation

## Canonical build

Command:

```bash
make pdf > build/iclr_review_fixes_build.stdout.log 2>&1
```

Result: exit status 0.

Retained artifacts:

- `build/upi_trm_iclr_revised.pdf`
- `build/upi_trm_iclr_revised.log`
- `build/iclr_review_fixes_build.stdout.log`
- `build/upi_trm_iclr_template_baseline.pdf`

PDF SHA-256 values:

- Revised: `2a831d08134e974767c7ab359974225a59220e613877236bea0ce16fc79d3f4a`
- Baseline: `f3b222c1f05fe759a7b7b71fcde5f7e3855f20f0f5d014c9f65a3fd5f8dce52b`

The final LaTeX log contains no fatal error, undefined control sequence, undefined citation, undefined reference, multiply-defined label, missing-file error, or overfull box. BibTeX reports zero warnings. Nonfatal messages are underfull boxes/vboxes, PDF-bookmark math-token warnings from `hyperref`, and one `h`-to-`ht` float adjustment.

`pdfinfo`, `pdffonts`, and `pdftotext` are unavailable. Ghostscript successfully opened the final PDF, counted 38 pages, listed embedded font resources, and produced PNG renderings for inspection. The final font list contains no DejaVu or Type 3 figure font; the only offending figure was removed from the manuscript.

## Numerical certificate rerun

Executed command:

```bash
python3 experiments/finite_mdp_certificate.py \
  --outdir results/finite_mdp_certificate_validation \
  > reports/finite_mdp_certificate_validation.log 2>&1
```

Result: exit status 0. The retained CSV has 80 `value_curve` rows and 21 `cpi_curve` rows. `certificate_holds_decomp` and `certificate_holds_exact_A` are true for every row. Generated data, figures, CSV, TeX summary, plotting scripts, and stdout are retained under `results/finite_mdp_certificate_validation/` and `reports/finite_mdp_certificate_validation.log`.

The episodic hard-suite evidence cited by the manuscript is retained under `results/episodic_z_hard_suite_20k_seed41_50/`, including the per-seed diagnostics and CPI penalty grid omitted from the first review bundle. A sanitized persistent UPI--TRM reevaluation summary and per-seed CSV are retained under `results/persistent_upi_20k/`. No training job or expensive experiment was launched.

## Rendered inspection

Inspected the final rendered title/abstract page, finite-reference theorem page, primary hard-suite table and conclusion page, and the repaired projection-aware anchor proposition. No clipping, overlapping text, missing figure, malformed equation, broken table, author identity, stale venue label, or bad page boundary was observed.

## Independent audits

The line-by-line theory, persistent-state, manuscript, and evidence audits were replayed against the corrected source. Their required fixes are present: formal results use finite/countable closures and ordinary sup norms; a separate remark states the common-domination and total-variation requirements for general kernels; the projection-aware anchor and zero-anchor baselines define the absorbing boundary; empirical factors use clamping terminology; exact centering is not equated exclusively with explicit summation; and unsupported interaction-equalized numerical rows are absent from active claims.

## Remaining nonfatal submission issues

- The intended next-cycle kit was unavailable. ICLR 2026 is a temporary official porting baseline and must be rechecked when the intended-cycle kit is published or reachable.
- The source-reported clamping contrast and `p≈0.6` are labeled inconclusive and are not independently auditable because the retained per-seed factorial artifact and test script are absent.
- The TRM+PPO per-seed run artifact is absent. The manuscript labels its seed values as manuscript-recorded and treats derived statistics as arithmetic consistency checks only.
- No numerical interaction-matched UPI--TRM versus PPO result exists; unauditable baseline-only rows were removed from active manuscript claims.
- The historical training repository is absent, so persistent carry order, timeout encoding, and frozen recurrent-map behavior for the headline implementation remain unaudited.

No result was fabricated or inferred from an unexecuted experiment. Planned experiments remain explicitly future work in `ICLR_EXPERIMENT_PLAN.md`.
