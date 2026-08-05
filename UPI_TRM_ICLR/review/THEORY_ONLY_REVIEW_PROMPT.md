# GPT Pro Prompt: Theory-Only Audit and Strengthening

Act as an independent ICLR theory reviewer, reinforcement-learning theorist,
mathematical proof auditor, and LaTeX editor. Review these four supplied files
completely:

- `main.pdf`;
- `main.tex`;
- `trm_rl.bib`;
- this `REVIEW_PROMPT.md`.

The submission is intentionally theory-only. It reports no learned-task
experiment, numerical theorem check, ablation, or method comparison. Do not
infer or reconstruct experimental evidence. Evaluate the mathematical
contribution on its own merits and determine how it can be made materially
stronger without making unsupported claims.

For any implementation, runtime, checkpoint, dataset, or reproducibility claim
that cannot be established from the supplied files, write exactly:

> not verifiable from supplied evidence

Do not ask questions. Resolve ambiguity conservatively, show your derivations,
and distinguish a proved improvement from a possible research direction.

## 1. Verify the Existing Theory

Read every theorem, proposition, corollary, lemma, proof, definition,
algorithm, remark, caption, appendix, and limitation. Re-derive every displayed
bound and constant. Audit:

- quantifiers and policy dependencies;
- fixed-MDP and fixed-snapshot scope;
- finite/countable versus measurable-space scope;
- reward and evaluator boundedness;
- Bellman operator domains and self-map properties;
- successor, one-deviation, and policy-pair closure;
- measurability, supported actions, and essential versus ordinary suprema;
- common recurrent map, initialization, latent norm, and absorbing boundary;
- terminal masking, `h=0`, `K>h`, partial final blocks, and `gamma=0`;
- exact statewise centering, candidate-policy bias, and mixture semantics;
- equality, strictness, zero-error, and vacuous-bound cases.

In particular, verify the finite-depth residual certificate on its declared
bounded-function space. Check the countable deterministic chain with zero
reward and `U(s_i)=gamma^{-i}` as a counterexample to any unqualified
residual-to-value statement. Confirm that the repaired assumptions exclude it
without claiming more than necessary.

For each formal result, classify it as:

- correct as stated;
- correct but assumptions are redundant or stronger than necessary;
- correct but the constant is loose;
- incomplete or ambiguous;
- false, with a concrete counterexample.

For every defect, cite exact TeX lines and PDF pages, show the failed step, and
give the smallest valid repair.

## 2. Minimize the Assumptions

Determine which assumptions are logically necessary, which are proof
conveniences, and which can be replaced by weaker conditions. Do not merely
suggest deleting an assumption. Supply a valid replacement proof or a
counterexample showing why the weakening fails.

Investigate at least:

1. Whether global boundedness of both `U_n` and `V^pi` can be replaced by a
   minimal Bellman-domain condition, a weighted sup norm, a Lyapunov/drift
   condition, a transversality condition, or another precise hypothesis.
2. Whether the finite/countable closure restriction can be extended cleanly to
   measurable state and action spaces. State all domination, measurability,
   kernel-invariance, and essential-supremum assumptions needed for a valid
   extension. Do not claim a general-space theorem if these details do not
   close.
3. Whether one-deviation and policy-pair closure assumptions can be reduced to
   the exact sets needed by each value, advantage, CPI, and deployment result.
4. Whether exact centering can be replaced by the smallest explicit centering
   defect, including state-dependent or occupancy-weighted variants.
5. Whether exact probability-space mixing is essential to each CPI step. If a
   broader update family is possible, state the exact realization-error term
   and prove it.
6. Whether persistent-latent results truly require the same frozen recurrent
   map for the base and candidate policies. If different maps can be admitted,
   derive an explicit map-mismatch penalty. Otherwise give a counterexample.
7. Whether the slow-drift assumptions can be localized, made stage-dependent,
   or replaced by a finite-path condition that avoids a latent fixed point.
8. Whether the contractive specialization can safely admit `L_z=0`, giving
   `L_z in [0,1)`, with explicit conventions for `n=0` and every expression
   containing a geometric denominator.
9. Whether the central CPI inequality needs pointwise centering, or whether an
   exactly stated occupancy-averaged centering condition suffices. Keep
   pointwise centering and uniform candidate bias as transparent sufficient
   conditions unless the weaker master statement is fully proved.

Produce an assumption-minimization table with columns: result, current
assumption, role in proof, necessary or convenient, valid weakening, changed
constant, and proof location.

## 3. Tighten the Bounds

Search systematically for avoidable triangle inequalities, duplicated suprema,
worst-case occupancy replacements, loose TV conversions, and unnecessary
uniformization. Re-derive constants independently rather than editing them
mechanically.

At minimum, examine:

1. The finite-reference decomposition. Determine whether
   `||U_n-U_m|| + ||U_m-T_K U_m||/(1-gamma^K)` is worst-case sharp under the
   displayed assumptions. Give a matching construction if sharp. If it can be
   tightened, state and prove the stronger inequality.
2. Stage-dependent finite-horizon residuals. Prefer an exact discounted sum of
   per-block residuals before taking a uniform maximum. Check partial final
   blocks and whether `ceil(h/K)` loses avoidable information.
3. Recurrent path bounds. Compare the sum of observed depth increments with
   geometric specializations and determine whether local or nonuniform moduli
   yield a strictly stronger valid theorem without assuming global
   contraction.
4. The value-to-advantage bridge. Check every factor of `gamma` and `2`, the
   role of the baseline, and whether reward cancellation or exact centering can
   improve the uniform constant.
5. Infinite- and finite-horizon CPI. Re-derive the linear candidate-bias term
   and quadratic policy-shift penalty. Test whether state-dependent advantage
   ranges, exact occupancies, TV rather than a worst-case range, or finite
   horizon can tighten the constants. In particular, determine whether the
   exact-mixture coupling yields the sharper infinite-horizon quadratic term
   `2 epsilon_CPI gamma alpha^2 / ((1-gamma)(1-gamma+gamma alpha))`
   instead of `2 epsilon_CPI gamma alpha^2/(1-gamma)^2`. Require a dominance
   proof, equality cases, and all `alpha=0`, `alpha=1`, and `gamma=0`
   boundaries; retain the current bound if this derivation fails.
6. Deployment perturbation. Check whether the TV and Pinsker constants use the
   reward supremum or reward span optimally, whether either KL direction is
   valid, and whether a coupling or occupancy argument gives a smaller
   finite-horizon constant. Check whether the KL corollary should use
   `min{1,sqrt(kappa/2)}` and whether a combined CPI-plus-deployment lower
   bound follows under one common frozen MDP and invariant domain.
7. Projection-aware results. Keep forward invariance, non-expansiveness, and
   strict contraction separate. The projected evaluator is contractive only
   when a proved global product modulus is strictly below one.

For each proposed tightening, provide:

- the new theorem statement;
- a complete derivation or proof detailed enough to audit;
- all added assumptions;
- comparison with the existing constant;
- equality or near-equality cases;
- a counterexample if the stronger form fails.

Do not call a bound tighter if it merely moves a difficult quantity into an
unmeasured assumption.

## 4. Seek Stronger Theoretical Contributions

Identify at most five additions that would materially improve the paper rather
than add theorem volume. Prioritize results that address the actual recurrent
evaluator and finite edit horizon, such as:

- a sharp finite-reference or stagewise residual theorem;
- a weighted-norm extension with verifiable drift conditions;
- a finite-path persistent-state theorem avoiding a fixed-point assumption;
- a recurrent-map mismatch theorem for policy improvement;
- an occupancy-aware or realization-aware CPI theorem;
- a sharper finite-horizon exact-mixture versus deployed-policy result.

For each candidate contribution, say whether it is already implied by the
current paper, a standard consequence of known results, or plausibly new. Use
`trm_rl.bib` to audit the supplied citation coverage. For every headline result,
classify its mathematical core as a known theorem, direct corollary,
domain-specific specialization, synthesis, or genuinely new result. If source
retrieval is available, verify prior art from primary sources and cite exact
theorem, equation, and page locations. Do not infer a paper's contents from its
title and do not invent citations. If primary sources cannot be checked, state
that an external literature review is required rather than declaring novelty.

Keep two fixed-point statements separate: the primary result assumes no
recurrent latent fixed point, but its Bellman argument still uses the value
fixed point `V^pi`. Do not describe it as eliminating fixed points altogether.

Only recommend including a new theorem when its statement and proof are clean,
relevant, and stronger than what is already present. Mark incomplete ideas as
research directions, not completed results.

## 5. Check Internal Consistency

Verify that the persistent state is `(x,y,z,h)`, where `z` is the carried
pre-unroll latent and `h` is the remaining budget. Check the post-unroll carry,
shared absorber, recurrent initialization, and frozen-map quantifiers.

Check Algorithm 2's folded terminal accounting against the formal nonzero
absorbing boundary. The terminal reward must include the discounted boundary
exactly once, post-terminal padding must be zero, and terminal bootstrap must
be zero.

Resolve the domain of the recurrent path supremum around Eq. 9. The declared
advantage closure includes the absorbing state, while no absorbing latent path
is defined. Determine whether the supremum must be restricted explicitly to
the nonabsorbing closure, and provide the exact correction if so.

Verify that an exact policy mixture is a pointwise mixture of action
probabilities. Parameter interpolation, logit interpolation, hidden-state
interpolation, and distillation are different objects unless separately
bounded.

Audit all high-risk uses of `exact`, `guarantee`, `certificate`, `contraction`,
`uniform`, `finite-horizon`, `persistent`, and `deployment`. Confirm theorem
numbering, notation, citations, anonymity, and PDF/TeX agreement.

## 6. Required Output

Return a rigorous report in this order:

1. **Blocking correctness findings**, ordered by severity.
2. **Verified results**, including the key derivation for each.
3. **Assumption-minimization table**.
4. **Bound-tightening table**, with old and proposed constants.
5. **Proposed stronger theorems**, each with a proof or a clear rejection.
6. **Novelty and positioning assessment** against the supplied bibliography.
7. **Exact manuscript edits**, with replacement LaTeX for accepted changes.
8. **Prioritized revision list**, separating essential fixes from optional
   theory extensions.
9. **ICLR verdict**: `below threshold`, `borderline`, or `submission-ready` as
   a theory-only paper.

Do not say that a theorem is improved unless you have supplied a valid proof.
Do not claim that an experiment, code path, or artifact was verified. Preserve
all limitations and negative conclusions.

## Bundle Identity

Expected files and hashes:

- `main.tex`:
  `69f3eb3f3b1951780714fc82ec216476d2d724fc999229a415c46b9e12d4b625`
- `main.pdf`:
  `f15d1c1d453477e56148bd24af34cdd6dd658d29558ac41d78dee735bc3ddce6`
  (29 pages)
- `trm_rl.bib`:
  `2e420066b2f54d80e99a4e31f2e466ea36998e8583b4f1f4818ea16b4f86bdc9`

Report a bundle-integrity finding if a hash, filename, or PDF page count differs.
