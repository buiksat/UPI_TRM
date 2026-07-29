# GPT Pro review prompt

Act as a highly skeptical ICLR reviewer and mathematical proof auditor.

Review the attached UPI--TRM manuscript as a new anonymous ICLR submission. Read the entire paper, including all proofs, appendices, tables, limitations, and experiment descriptions. Use the supplied evidence files only to verify claims; do not assume missing evidence exists.

Audit the paper along five dimensions.

## 1. Mathematical correctness

- Check Theorem 6.1: the finite-reference-depth decomposition, path-length bound, quantifiers, dimensions, norms, policy-pair closure, initialization convention, boundedness, measurability, absorbing-state convention, and the contraction-based limit as `m -> infinity`.
- Check Theorem 6.5 and every constant and factor in the conservative policy-improvement derivation.
- Check the persistent-latent augmented-MDP construction, direct residual certificate, initial law, Markov state, transition kernel, policy dependencies, closure, exact-centering requirement, exact-mixture requirement, and separation of the direct certificate from optional slow drift.
- Identify circular arguments, hidden assumptions, invalid limit operations, inconsistent policy dependencies, or dimension mismatches.
- Do not treat the triangle inequality itself as a novelty claim.

## 2. Claim--evidence alignment

- Verify every empirical and numerical claim against the supplied artifacts.
- Check that the 57.4% hard-Sudoku result is presented only as an implementation result, not theorem validation.
- Check that the 0% theory-aligned episodic result is sufficiently prominent.
- Check that the manuscript claims no equal-interaction or sample-efficiency advantage over PPO.
- Check that projection's +13.0 percentage-point contrast is described as a composite algorithmic effect spanning forward-pass and training-dynamics channels.
- Check that contraction's +2.2 percentage-point contrast and source-reported `p approximately 0.6` are described as inconclusive, with the missing per-seed factorial provenance disclosed.
- Check that the finite-MDP calculation is described as a numerical certificate/unit test rather than an empirical discovery.
- Flag any completed-sounding statement about an experiment that was not run.
- Treat finite-batch diagnostics as distinct from uniform theorem certificates.

## 3. ICLR reviewer assessment

- Assess novelty, correctness, significance, clarity, reproducibility, and empirical strength.
- Distinguish fatal flaws from weaknesses repairable through writing.
- Predict likely reviewer objections.
- Give an overall ICLR score and confidence, using the current ICLR review scale and explaining your interpretation of the scale.

## 4. Presentation and organization

- Find unclear definitions, inconsistent notation, unsupported abstract statements, organizational problems, excessive appendix material, and poor transitions.
- Check whether the contribution and its limitations are understandable from the first two pages.
- Identify exact passages that should be shortened, moved, or rewritten.
- Check the claim/condition/evidence/status presentation for internal consistency.

## 5. Required response format

Return these sections:

A. Blocking correctness issues, ordered by severity.

B. Major reviewer concerns.

C. Minor issues and presentation fixes.

D. Claim-by-claim evidence audit, preferably as a table with columns `claim`, `required condition`, `supplied evidence`, and `status`.

E. Exact proposed textual edits, quoting the current text where possible.

F. Missing experiments ranked by expected impact on acceptance, clearly separating necessary experiments from useful follow-ups.

G. Overall ICLR score, confidence, and a concise mock review.

For every finding, cite the PDF page and the relevant section, theorem, equation, figure, table, or appendix. Do not invent results, citations, diagnostics, assumptions, or execution outcomes. If something cannot be verified from the supplied files, label it exactly `not verifiable from supplied evidence`.

The PDF is the authoritative rendered manuscript. Use `main.tex` when exact notation, labels, or proof text is easier to inspect there. The revision and experiment plans describe intended scope and future work; do not mistake planned experiments for completed results.
