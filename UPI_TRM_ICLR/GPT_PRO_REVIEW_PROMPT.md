# GPT Pro review prompt

Review the latest commit in this repository as an adversarial mathematical
reviewer. Compare `HEAD` with `HEAD^` and review the actual diff, not a summary.
Do not edit files, commit, push, or propose experiments. Return review findings
only.

The canonical paper is `UPI_TRM_ICLR/main.tex`; its generated artifact is
`UPI_TRM_ICLR/main.pdf`. Read the complete canonical source, every transitive
input/style/bibliography dependency, and the full changed diff before judging
it. Build the paper through its canonical path:

```bash
cd UPI_TRM_ICLR
make clean && make pdf
```

The review is limited to theory, assumptions, proofs, notation, and algorithm
pseudocode. Do not request, design, reinterpret, or discuss experiments.

## Scope that must remain fixed

Every result is conditional on one fixed MDP, one fixed current/candidate
policy pair, one fixed parameter snapshot, and one shared frozen recurrent map
whenever both policies are analyzed in the same persistent-latent augmented
MDP. Reject any wording that broadens the results to SGD, TD convergence,
BPTT, distillation, learned-model performance, or training dynamics.

## Changes to verify

1. Algorithm 1 and Algorithm 2 store every terminal transition and immediately
   terminate collection for any terminal flag or budget exhaustion. They must
   sample no later action, construct no nonabsorbing successor, and carry no
   persistent latent after termination.
2. The bounded-head assumption quantifies both value heads over an explicitly
   declared nonabsorbing state domain and invariant latent set, while handling
   the absorber only through a finite scalar boundary. It must not weaken any
   explicit `B_b` premise.
3. Algorithm 2 has typed inputs, a real projection-disabled identity mode
   rather than `R=0`, and explicit outputs for the fitted head, candidate
   policy, exact mixture, and updated target head.
4. The recurrent specializations of the infinite- and finite-horizon results
   include the direct endpoint inequality before both path-length inequalities.
5. The span-based safe-step corollary uses one alpha-independent candidate
   defect `b`, one-sided occupancy bound `overline beta_d`, and
   `M_d = ghat - overline beta_d`. Verify the proof of
   `ghat = E_{d_pi}[g+b]`, all three defect specializations, and every boundary
   case. The nontrivial threshold must be exactly
   `M_d(1-gamma)/(gamma(Delta_g-M_d))`, with no redundant outer minimum.
6. The target-network bridge retains the propagated lag
   `||P_pi^K(bar V-U_q)||_infty` before its ordinary sup-norm fallback. Verify
   the value, finite-reference, candidate-defect, and CPI corollaries, including
   the persistent augmented-MDP analogue. The fixed-target population operator
   must never be identified with the self-bootstrap Bellman operator.
7. The fixed-point measurability result correctly derives measurable iterates
   and a measurable pointwise fixed-point limit from joint measurability,
   measurable initialization, invariance, and uniform contraction. Metric
   contraction alone must still be described as insufficient.

## Constants and distinctions that must not change

Check each derivation independently. In particular, preserve:

- Bellman modulus `gamma^K` and residual divisor `1-gamma^K`.
- Exact-mixture occupancy TV bound
  `gamma alpha/(1-gamma+gamma alpha)` and the countable-space factor-two
  `l1` form.
- Signed surrogate identity `Xi_alpha/(1-gamma)`.
- Span CPI penalty
  `gamma alpha^2 Delta_g/((1-gamma)(1-gamma+gamma alpha))`.
- Scalar CPI penalty with numerator
  `2 epsilon_CPI gamma alpha^2` and the same denominator.
- Policy-overlap factors `2 gamma delta_V tau(s)` and
  `2 gamma^K delta_V tau(s)`.
- Deployment perturbation
  `Delta_r delta_dep/((1-gamma)(1-gamma+gamma delta_dep))`.
- Projection modulus `(R/rho_R)L_z^pre(R)`.
- `L_z^0=1`; when `L_z=0`, `L_z^n=0` for integer `n>=1`.
- Occupancy before decision `t` uses `1-(1-alpha)^t`; reward mismatch after
  decision `t` uses `1-(1-delta_dep)^(t+1)`.
- No extra factor two in the span-versus-TV expectation inequality.
- The common absorbing tail is counted exactly once.
- A Bellman value fixed point and a recurrent latent fixed point are distinct.
- Exact probability mixing is not parameter, logit, or hidden-state
  interpolation, clipping, trust-region optimization, or distillation.
- The direct persistent residual certificate needs no recurrent fixed point,
  contraction, projection, Lipschitz head, or slow-drift assumption.

Explicitly test these edge cases: `gamma=0`; `alpha=0` and `alpha=1`;
`M_d<0`; `M_d=0`; `Delta_g=0`; `M_d=gamma Delta_g`; `L_z=0` with
`n=0` and `n>=1`; `H=0`; `h=0`; `K>h`; terminal STOP; solved terminal;
budget exhaustion; and `delta_dep=0,1`.

## Reporting standard

Adversarially verify each candidate issue and default to rejecting it. Report
only defects that survive verification. For each finding, give:

- severity: blocking, major, or minor;
- exact file and line;
- the violated premise or incorrect derivation;
- a concrete counterexample or derivation where possible;
- the smallest mathematically valid repair.

Also state what you checked and cleared. If no defect survives, say exactly:
`No surviving theory or pseudocode defects found.` Include the build command,
page count, and final LaTeX diagnostics in the review.
