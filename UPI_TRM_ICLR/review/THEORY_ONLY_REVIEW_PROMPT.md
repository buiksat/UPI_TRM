# Independent Theory-Only Review Prompt

Act as an independent ICLR reviewer, mathematical proof auditor, and LaTeX
consistency checker. Review `paper.tex` and `paper.pdf` completely. Compare the
rendered PDF with the TeX source, including every theorem, proof, algorithm,
caption, appendix, and limitation.

## Scope

This revision intentionally reports **no experiments, learned-task results,
numerical theorem checks, ablations, or method comparisons**. Do not infer that
an experiment was run. Do not reconstruct a result from prose, filenames, or
expected behavior. Evaluate the paper as a theory-only submission and state how
the absence of empirical evaluation affects the acceptance case.

The review bundle contains the manuscript, not the complete runtime repository.
For any implementation, runtime, artifact, checkpoint, dataset, or reproducibility
claim that cannot be established from the supplied PDF and TeX, write exactly:

> not verifiable from supplied evidence

Do not replace that phrase with a synonym. Mathematical definitions and
pseudocode may be audited directly; claims about what executable code actually
does require executable evidence.

## Required Audit

1. Re-derive every theorem, proposition, corollary, lemma, and dependent
   constant. Check quantifiers, function spaces, boundedness, closure,
   measurability, policy dependence, common initialization, norms, terminal
   boundaries, and zero-error/equality cases.
2. Audit the finite-reference residual certificate, including its bounded
   Bellman domain and the countable-state counterexample to an unqualified
   statement.
3. Check the finite-horizon residual recursion for `h=0`, `K>h`, final partial
   blocks, `gamma=0`, and the shared absorbing state.
4. Check the centered CPI bounds, candidate-policy bias, exact pointwise
   mixture, strictness statements, occupancy constants, and deployment TV/KL
   constants.
5. Check persistent-latent results on the clock-complete state `(x,y,z,h)`, the
   carried pre-unroll latent, shared frozen recurrent map, and absorbing
   transition.
6. Check Algorithm 2's folded terminal target against the formal nonzero
   absorbing boundary. Confirm that the folded terminal reward includes the
   discounted boundary once, post-terminal padding is zero, and terminal
   bootstrap is zero.
7. Check projection claims carefully. Radial projection is non-expansive; call
   the composed evaluator contractive only when the displayed global upper
   bound is strictly below one. Local or finite-batch quantities are not global
   certificates.
8. Check that no empirical result or completed-sounding experimental claim
   remains. Flag any claim whose wording exceeds its displayed assumptions.
9. Check all references, theorem numbering, notation, anonymity, PDF rendering,
   and duplicate or broken hyperlink destinations.

## Output

Lead with verified findings ordered by severity. For each finding, cite exact
TeX lines and PDF pages, show the failed derivation or counterexample, and state
the minimal repair. Then list the high-risk items you checked and cleared.
Finish with one verdict: `below threshold`, `borderline`, or
`submission-ready`, judged as a theory-only paper. Do not claim that an issue is
fixed unless the supplied manuscript itself establishes the fix.
