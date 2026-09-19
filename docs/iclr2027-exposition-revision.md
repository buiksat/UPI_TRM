# ICLR 2027 exposition revision

Date: 2026-09-19

Starting paper revision:
`1a5f04f6f574e4f8e4bd873b67a8d3373b8e97df`.

This pass revises the unlocked exposition from Related Work through the
limitations. It does not change the title, anonymity metadata, abstract,
Introduction, Figure 1 or its caption, Algorithm 1, AI Use Statement, formal
mathematics, numerical results, bibliography, verifier, Makefile, or ICLR
style files.

## Reader-facing changes

- Related Work groups the existing citations around CPI and safe improvement,
  approximate dynamic programming, finite recurrent computation, and task
  context.
- The setup introduces the environment and recurrent clocks before their
  notation, then separates reset and carried-latent state.
- The algorithm discussion identifies one fixed-base proposal and states that
  comparison depth is outside collection and action selection.
- The finite-reference section leads from its value-radius deliverable to the
  direct comparator, strict gain condition, and value-to-advantage conversion.
- The target-network section separates target-head regression from the
  self-bootstrap residual and presents propagated lag before the sup-lag
  fallback.
- The CPI section introduces exact centering and the exact probability mixture
  before separating signed evaluation error from occupancy shift.
- The persistent-state section leads with the stored latent, remaining clock,
  and shared frozen recurrent map. Its full corollary moves byte-for-byte to
  Appendix C.1.2 (Corollary C.2). The main text contains an explicitly informal summary with the
  required domain, boundedness, common-boundary, residual, exact-expectation,
  and exact-mixture premises.
- The exact example and learned diagnostic answer separate questions. The
  learned result remains a conditional finite-census proxy comparison.
- The conclusion states the fixed-snapshot and one-proposal scope, then lists
  the limits on convergence, recursive improvement, uniform certification,
  monotone depth, and learned-task performance.

## Appendix organization

The appendices now have six groups:

A. Notation, domains, and absorbing normalization.
B. Exact finite-MDP derivation.
C. Complete formal statements, constructions, and proofs.
D. Optional contraction and weighted norms.
E. Finite-census learned-evaluator diagnostic.
F. Implementation and original-TRM mapping.

All 43 theorem-like and proof blocks from the starting source remain
byte-identical as a multiset. Of the 96 equation or alignment display
environments, 95 remain byte-identical. Eq. (30) differs only by the authorized
terminal comma-to-period change; all mathematics and all 88 equation labels
are unchanged across 82 labeled environments. All five tables, Figure 1, and
Algorithm 1 remain byte-identical. The moved
persistent-state corollary keeps its full body and label
`cor:persistent_cpi_augmented`. The new grouping label
`app:formal_results` is the only added label.

## Independent reconstruction

The prior local candidate was treated as untrusted input. The starting and
candidate manuscripts, their full diff, the implementation constraints, and
the cited bibliography entries were checked independently. The initial
reconstruction differed from that candidate by removing two unnecessary
logical transitions from unlocked prose. The follow-up changes below add only
reviewer-requested clarifications. The PDF and validation evidence were rebuilt
from the exact starting revision rather than copied from the prior candidate.

## Reviewer follow-up

The approved follow-up pass restores the explicit `clock-complete` definition
and the measurable-kernel premise. It defines the augmented `K`-step Bellman
operator, its unique bounded fixed point, the full-state surrogate, and the
current-policy-domain action qualifier before those objects are used in the
informal persistent-state summary. Appendix C.1.1 now gives the concrete
frozen-MDP and measurability antecedent consumed by Corollary C.2 without
changing the corollary itself.

## Build and validation

The starting source clean-builds to 29 pages with the scientific main text
ending on page 10. Its tracked PDF predates that source revision. The revised
source clean-builds to 29 pages with the scientific main text ending on page
9. Statements and references occupy pages 10 and 11; appendices occupy pages
12 through 29.

The build used the repository Makefile, PDFLaTeX with shell escape disabled,
and the preserved read-only URW font tree required on this host. Fresh checks
produced these results:

- The unchanged exact finite-MDP verifier exits 0 before and after the edit,
  with byte-identical output.
- The clean four-pass PDFLaTeX and BibTeX build exits 0.
- There are no undefined citations or references, duplicate labels, missing
  files, unresolved rerun requests, double-question markers, or overfull
  boxes. The baseline and final logs each contain nine underfull-box warnings.
- The PDF has 29 letter-size pages, uses PDF 1.5, embeds all 26 fonts, has no
  attachments or signatures, and passes qpdf and Ghostscript parsing.
- Title metadata matches the visible title. Author, Creator, Producer,
  Subject, and Keywords metadata are empty.
- All 29 rendered pages were inspected in contact sheets. Every changed page
  was covered, and the main-text pages, appendix transitions, relocated
  statement, diagnostic tables, and final page were also inspected at full
  render resolution.

Final source SHA-256:
`36c80a300d7483f693b947dcfd3fe2043b5448d16881fc0b43145564129ec5a2`.

Final PDF SHA-256:
`bca230f89a7cb5919ce6e92de2c9bb0c7434143199f6f768c02517b2f433c30a`.

The fresh command logs, inventories, hashes, patch, rendered pages, manual
review notes, and reopened source package are stored outside the repository
under task identifier `exposition-resume-20260919-a1`.

## Verification boundary

No training, evaluation, calibration, replay, resampling, statistical
analysis, or restricted-data access ran during this pass. Remote ref checks
over HTTPS and SSH remained unavailable because the execution proxy returned
HTTP 403. The local revision stays pinned to the supplied starting SHA. A
separate paper-and-theory review remains required before any push.
