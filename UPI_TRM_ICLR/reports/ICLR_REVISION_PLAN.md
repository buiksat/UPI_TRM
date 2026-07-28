# ICLR Scientific Revision Plan

## Status and governing scope

The anonymous ICLR-template baseline passed the mandatory compile gate and was committed as `d729d0dde5c6df8f5a77469474090c1762774543` before this plan was written. The complete manuscript was then read, including the CPI derivation, persistent-state construction, all proofs, every experiment section, implementation details, and provenance documents.

The revision will present a fixed-parameter-snapshot analysis of finite-depth evaluators. It will not claim an end-to-end training theorem, sample-efficiency advantage, equal-interaction advantage, uniform empirical certificate, or validation of a theorem by the hard-Sudoku implementation. No new experimental result will enter the paper until its locked protocol has run and its artifacts have been audited.

## Formal conventions to lock before changing theorem text

1. **One frozen MDP and policy pair.** Fix `theta`, `psi`, evaluator depth `n`, the recurrent map, reward, transition kernel, current policy `pi`, and candidate action policy `pi_cand`. A deeper `U_m` is a diagnostic evaluation of the same frozen state under the same policy pair; it does not replace the deployed policy or transition kernel.
2. **State completeness.** If the `T=16` edit budget affects termination or reward, the remaining budget is part of the Markov state and is suppressed in the `(x,y)` notation. The persistent notation `bar s=(x,y,z)` uses that clock-complete `(x,y)` state.
3. **Measurable closure.** Replace positive-point-mass reachability with a measurable, almost-sure policy-pair closure. It contains the current-policy occupancy support and one-step successors for the supports of both policies, and it is forward invariant under the current policy. The finite Sudoku construction is a special case.
4. **Boundedness and measurability.** Rewards, the finite-depth evaluators used in each statement, update maps, value head, edit kernel, and policy kernels are measurable; rewards and evaluator outputs are bounded on the stated closure.
5. **Absorbing boundary.** Every depth uses the same explicit value at `s_abs` (the shaped value `-C_max` under the current convention), so depth differences vanish there.
6. **Common recurrent path.** `z^(j)(s)` lies in the same normed latent space (`R^d` in the implementation), starts from the same `z_init(s)`, and uses the same frozen recurrence and value head for all `j` between `n` and `m`.
7. **Bellman residual semantics.** `T_K^pi U_m` bootstraps with `U_m` itself. A sampled target-network TD loss is not automatically this residual.
8. **Augmented-policy comparison.** Current and candidate augmented policies share the frozen recurrent update `T_{x,y}^{o n}`. If a candidate changes that map, it changes the augmented MDP and ordinary CPI does not apply.

## Change map

| Proposed paper change | Reviewer concern addressed | Exact location affected | Change type | Existing evidence sufficient? | New computation? | Acceptance criterion |
|---|---|---|---|---|---|---|
| Rename the paper to foreground finite-depth evaluator analysis rather than policy-training improvement | C: claim/evidence alignment | Title and PDF metadata | Claim/presentation | Yes | No | Title contains “finite-depth” and does not imply an end-to-end training guarantee |
| Rewrite the abstract around a finite-reference-depth bound, transient computation, and fixed-snapshot scope | A, C | Abstract | Claim/presentation | Yes | No | Every positive statement is tied to a theorem or existing table; hard-Sudoku and negative-run limitations appear explicitly |
| Reframe the introduction and scope as fixed-snapshot finite-depth error analysis | A, C | Introduction and scope paragraph | Claim/presentation | Yes | No | No sentence suggests convergence of SGD/TD/BPTT or arbitrary TRM latent convergence |
| Replace the first contribution with the fixed-point-free finite-reference-depth theorem | A | Contributions list | Claim/presentation | Yes | No | The finite `m>n` result appears first; the triangle inequality itself is not called novel |
| Describe contraction as an optional conditional error-control specialization | A, C | Related work; current Section 5; discussion | Claim/presentation | Yes | No | Contraction is not called a demonstrated hard-task performance dial or a design requirement for arbitrary TRMs |
| State a clock-complete frozen MDP, common policy pair, common initialization, boundedness, and absorbing-state convention | A, B | Background/setup; theorem preamble; notation appendix | Proof/presentation | Yes | No | Every object in the new norms and Bellman operators is defined and dimensionally consistent |
| Repair the advantage-evaluation closure for general measurable state spaces | A, B | Appendix “Constructive Definition of the Advantage-Evaluation Closure” | Proof | Yes for the formal repair and finite Sudoku | No | Restricted Bellman contraction follows from almost-sure forward invariance; no use of `P(s'|s,a)>0` for nonatomic spaces |
| Make current Proposition 6.1 a Theorem 6.1 finite-reference-depth decomposition for every finite `0 <= n < m` | A | Section 6.1 and proof appendix; preserve label `prop:error_bounds` and add `thm:finite_reference_depth` | Proof/claim | Yes | No | The exact requested inequality holds on the same policy-pair closure without contraction or a latent fixed point |
| Add the Lipschitz path-length inequality | A | Theorem 6.1 and proof | Proof | Yes | No | Supremum is over the stated closure, the sum is `j=n,...,m-1`, and the value head is uniformly Lipschitz on the finite iterate set |
| Explain the finite-time interpretation and non-novelty of the triangle step | A | Immediately after Theorem 6.1 | Claim/presentation | Yes | No | Text states that no behavior beyond depth `m` and no recurrent convergence is assumed |
| Derive the old contractive fixed-point formula as a secondary specialization | A | Section 6.1; Banach proposition; proof of `prop:error_bounds` | Proof/claim | Yes | No | Geometric path bound includes `1-L_z^(m-n)`; uniform residual convergence is shown; `m -> infinity` yields the existing equation |
| Make the finite-reference advantage bridge primary | A | Corollary 6.3 (`cor:epsA_dials`) and advantage appendix | Proof | Yes | No | `epsilon_A <= 2 gamma B_{n,m}` for one-step centered advantages; `2 gamma^K` is stated for the K-step version |
| Propagate `B_{n,m}` into the sufficient condition and CPI parameter corollary | A | Corollaries 6.6–6.7, preserving Theorem 6.5 | Proof | Yes | No | Exact mixture, exact centering, same policy pair, and closure requirements remain visible; fixed-point expression is only a limit specialization |
| Retain the direct depth-`n` residual certificate and distinguish when it is tighter | A | Corollary 6.2 | Proof/presentation | Yes | No | The direct certificate is not conflated with the two-depth decomposition or sampled residual estimates |
| Formalize persistent state as a frozen augmented MDP with initialization law | B | Setup and Appendix B | Proof/presentation | Partly; implementation audit remains | No paper computation | `bar rho`, measurable update, policy, reward, clock, absorbing state, and shared recurrent kernel are explicit |
| Add the direct augmented finite-depth residual certificate | B | New first result in Appendix B; proof appendix | Proof | Yes | No | Requested inequality is proved using Bellman contraction and assumes no fixed point, recurrent contraction, Lipschitz head, projection, or slow drift |
| Add the exact-centered augmented advantage/CPI consequence | B | Appendix B after the direct certificate | Proof | Yes | No | Centering is pointwise on full `bar s`; exact mixture is deployed directly rather than distilled or parameter-interpolated |
| Recast slow drift as an optional comparison to the memoryless fixed-point reference | B | Existing slow-drift subsection and `cor:persistent_cpi_augmented` | Proof/claim | Yes, conditional | No | No sentence says slow drift is needed for the direct augmented residual certificate |
| Repair the slow-drift closure hypothesis and remove circular advantage assumptions | B | Assumption B.1, Lemma B.?, persistent corollary/proof | Proof | Yes | No | Tracking error is uniform over starts used by the augmented closure; the result derives rather than assumes its advantage bound |
| Remove unsupported “learned manifold is constructed” and “unconditional stability” language | B, C | Slow-drift remarks | Claim | No support for those statements | No | Remaining wording is explicitly conditional and does not infer properties from successful training |
| Distinguish episodic, augmented finite-depth, and augmented fixed-point residuals in notation | B | Notation table; diagnostics table; persistent appendix | Presentation | Yes | No | Symbols cannot be read as interchangeable and each has a stated closure/operator |
| Correct the fresh-initialization latent diagnostic name | B | Implementation details | Presentation | Yes | No | It is called a discrepancy, not an upper bound on fixed-point tracking error |
| Add a compact claim / condition / evidence / status table | D | End of main theory or start of experimental appendix | Presentation | Yes | No | Table covers finite-reference theorem, direct persistent certificate, exact-mixture CPI, hard suite, projection, contraction, and finite-MDP unit test |
| Present hard `4x4` Sudoku as an implementation result | C, D | Experiments opener, hard-suite subsection, conclusion | Claim/presentation | Yes | No | `57.4%` is never described as theorem validation; persistent distillation is stated explicitly |
| Foreground the theory-aligned episodic hard-suite result of `0%` | C, D | Experiments opener/main hard-suite discussion and appendix | Claim/presentation | Yes | No | `0%` over 10 seeds is visible in the main narrative and is not demoted to a diagnostic footnote |
| State that equal-interaction and sample-efficiency advantages over PPO are not established | C | Table 1 caption/text, discussion, conclusion | Claim | Yes | No | No “outperforms PPO” sentence lacks the nominal-budget qualifier; no sample-efficiency claim remains |
| Describe projection’s `+13.0` pp as a combined algorithmic effect | C | Main factorial and appendix duplicates | Claim | Yes | No | Text names both forward-pass geometry and training-dynamics/optimizer channels and does not attribute the lift to one bound term |
| Describe contraction’s `+2.2` pp, `p approx 0.6` as inconclusive | C | Main factorial, diagnostics, discussion, conclusion | Claim | Yes | No | It is a conditional stability/error-control mechanism, not a demonstrated hard-task performance control |
| Call the finite-MDP study a numerical certificate/unit test | C, D | Main theory, experimental appendix, figure caption, conclusion | Claim/presentation | Yes | No | It is not called an empirical discovery or evidence of task-level performance |
| State the empirical scope as current `4x4` Sudoku only | C | Abstract, experiments, discussion, conclusion | Claim | Yes | No | No result claim extends to `9x9`, ARC, LLM reasoning, or a second domain |
| State exact-mixture failure for the distilled headline policy as known, not unverified | B, C | Algorithm, hard-suite limitations, persistent appendix, implementation details | Claim | Yes | No | The paper says the headline implementation distills and therefore does not deploy the exact mixture required by Theorem 6.5 |
| State that exact centering and the uniform augmented residual are not established for the headline run | B, C | Hard-suite limitations and claim-status table | Claim | Yes | No | Episodic finite-batch diagnostics are not offered as persistent uniform certificates |
| Reorganize experimental evidence around decisions | D | Experiments and experimental appendix | Presentation | Yes | No | Reading order is hard-suite scope, factorial, negative theory-aligned run, interaction audit, finite-MDP unit test, then secondary diagnostics |
| Move exploratory/redundant ablations to a clearly labeled secondary-diagnostics block without deletion | D | Experimental appendix | Presentation | Yes | No | All reproducibility tables/figures remain reachable; exploratory evidence is labeled exploratory |
| Rewrite discussion and conclusion around what is established, conditional, inconclusive, and missing | C, D | Discussion/limitations/conclusion | Claim/presentation | Yes | No | Every numerical claim points to existing evidence and every theorem-dependent empirical limitation is explicit |
| Update labels/references and notation after reorganization | A–D | Entire manuscript | Mechanical | Yes | No | Zero undefined references/citations; theorem 6.5 remains the centered-error CPI theorem |
| Bring the main text within the official ICLR limit without style changes | Formatting | Main paper | Presentation | Yes | No | Main-text count is reported; official margins, spacing, and font sizes remain untouched; excess pages are reported if unresolved |

## Claim-status table content to implement

| Claim | Required condition | Measured/existing evidence | Intended status |
|---|---|---|---|
| Finite-reference value decomposition | Frozen policy pair/MDP; bounded measurable evaluators; uniform residual on a forward-invariant closure | Analytic proof | Established theorem |
| Finite recurrent path control | Same initialization/path; uniformly Lipschitz scalar value head | Analytic proof; proposed batch diagnostics are not certificates | Established theorem, diagnostics pending |
| Direct persistent-state value certificate | Frozen augmented MDP; uniform augmented residual | No uniform headline measurement | Established conditional theorem; not empirically certified |
| Linear-in-alpha CPI tightening | Exact statewise centering and exact deployed mixture | Theory-aligned episodic run uses these but reaches `0%`; headline policy is distilled | Theorem condition; known unmet by headline exact-mixture deployment |
| Hard-suite `57.4%` result | Reproduced persistent implementation under nominal outer-step protocol | 10 seeds and retained provenance | Implementation result only |
| UPI versus PPO efficiency | Equal interactions and locked common evaluation | Not run for both methods | Missing experiment; no advantage claim |
| Projection `+13.0` pp | Controlled `2x2`; same protocol | Existing 10-seed factorial | Algorithmic effect across forward/training channels |
| Contraction `+2.2` pp | Controlled `2x2` | `p approx 0.6`, 10 seeds | Inconclusive hard-task effect |
| Composed finite-MDP inequalities | Exactly computable finite MDP | 101 checked configurations, zero violations | Numerical certificate/unit test |

## Proof acceptance checklist

- Quantifiers fix `pi`, `pi_cand`, `K`, `gamma`, `n`, `m`, parameters, norm, and closure before an inequality.
- `U_j` and `V^pi` are scalar-valued; `z^(j)` lies in one stated normed latent space.
- Bellman contraction is valid in the restricted norm because the closure is current-policy forward invariant almost surely.
- The absorbing state is included consistently in every norm and finite-depth evaluator.
- The finite-reference proof does not invoke Banach, `z*`, completeness, or `L_z<1`.
- The path proof uses `sup_s sum_j <= sum_j sup_s` in the correct direction.
- The fixed-point limit proves uniform `U_m -> U_*` and residual convergence with factor `1+gamma^K`.
- Persistent current/candidate policies do not change the augmented transition map.
- Augmented centering is conditioned on the complete augmented state, not only `(x,y)`.
- Distillation and parameter interpolation are never identified with the statewise exact policy mixture.
- Finite-batch maxima are called diagnostics, never uniform upper bounds.

## Planned commit sequence

1. `Add fixed-point-free finite-reference-depth theory`
2. `Clarify direct persistent-state certificate and slow-drift scope`
3. `Align ICLR title abstract and claims with evidence`
4. `Reorganize experimental evidence and diagnostics`
5. `Fit and validate the anonymous ICLR manuscript`

Each content commit must pass `make pdf` before the next begins. The baseline PDF remains unchanged at `build/upi_trm_iclr_template_baseline.pdf`.

## Unresolved items to report, not silently assume

- The experiment implementation repository and historical checkpoint/config paths referenced by provenance are absent in this workspace, so the augmented-state carry order, timeout handling, action masking, and shared recurrent map cannot be re-audited here.
- The uniform augmented Bellman residual for the headline persistent run has not been measured.
- Exact centering has not been uniformly established for the headline persistent run.
- The headline distilled policy is known not to satisfy the direct exact-mixture deployment condition.
- No interaction-equalized UPI–TRM versus TRM+PPO comparison exists.
- The fixed-point Lipschitz/slow-drift assumptions remain unverified on Sudoku and are not needed for the new direct persistent certificate.
- Type 3 and unembedded DejaVu fonts remain in imported figure PDFs and must be regenerated from source before submission if the ICLR checker rejects them.
- ICLR 2027 style files were unavailable; the ICLR 2026 files are a temporary porting baseline and must be replaced/verified when the intended-cycle kit is published or reachable.
