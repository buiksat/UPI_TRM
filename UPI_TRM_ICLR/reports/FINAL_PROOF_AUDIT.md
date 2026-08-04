# Final Proof Audit

## Audit basis

- Audited file: `UPI_TRM_ICLR/main.tex`
- Repository HEAD while audited: `c0c6acae8d591acbd99441eb3b17b6d2306df50d`
- Audited working-tree SHA-256: `f1f7bb567578dbf1b4a3ab1d7c3db4cfdf3acee8b6e7fb9f818a8239550344e7`
- The working tree contained concurrent manuscript edits. This audit treats the file bytes identified above as authoritative.
- Method: independently re-derived each displayed inequality from its definitions, checked quantifiers and recursive domains, and evaluated all endpoint cases listed below. Prior reports were not treated as proof.
- Independent numerical cross-check:
  `python3 experiments/finite_horizon_theory_checks.py --seed 481516 --random-cases 100`
  returned `PASS` with 13,902 assertions. This is a theorem-pipeline unit test, not proof and not learned-model validation.

## Status

**PASS.** No blocking mathematical, boundary, support, constant, or quantifier error remains in the audited finite-reference, finite-horizon, CPI, deployment, or persistent-state results.

Two defects found during this audit were corrected in the audited working tree:

- The optional slow-drift result divided by `1-kappa_n` while permitting `n=0`. It now fixes `n>=1` and states `kappa_n<1` before Lemma `lem:drift_bound` (`main.tex:847-848`). The direct augmented-state residual result still correctly permits depth zero.
- The finite-reference theorem relied on global setup for the MDP and absorbing convention. It now locally fixes `(S,A,P,r,rho,gamma)`, `gamma in [0,1)`, `K`, both policies, the finite/countable closure and supported actions, invariance, the absorbing self-loop reward and value, the frozen recurrence, common initialization, latent norm, boundedness, and operator domain (`main.tex:263-288`).

## Surviving findings

None.

## Checked and cleared

### Finite-reference depth

- `main.tex:290-295`: the residual factor is exactly `1/(1-gamma^K)`, obtained by rearranging the `gamma^K` Bellman-contraction inequality.
- `main.tex:297-304`: the path sum has the correct endpoints `j=n,...,m-1`; the absorbing contribution is zero because every depth uses the same boundary value.
- `main.tex:1864-1901`: the proof uses one frozen policy, one shared recurrent map, one initialization, one latent norm, and a forward-invariant closure. Uniform convergence of `U_m` also implies convergence of the residual norm with factor `1+gamma^K`.
- Boundary cases `n=0`, `m=n+1`, `gamma=0`, and absorbing input do not change the argument.

### Finite-horizon residual theorem

- The definitions following `main.tex:1153` use `ell_h=min(K,h)` and `J_h=ceil(h/K)`, producing residual clocks `h,h-K,...` with weights `1,gamma^K,...`. A final partial block contributes a residual but multiplies the terminal error `e_0=0`; there is no off-by-one error.
- `K>h` gives one truncated backup and factor one. `h=0` gives an empty sum and zero error. `gamma=0` also reduces to the current-stage residual exactly.
- The shared boundary `b`, absorbing padding, and stage-1 transition convention make backups longer than the remaining horizon equivalent to exact terminal handling.
- The persistent specialization correctly requires state `(x,y,z,h)` and one recurrent map shared by both policies.

### CPI and centering

- `main.tex:450-482` needs only exact statewise centering, finite `epsilon_{A,cand}`, the exact probability-space mixture, and one fixed MDP for its central inequality.
- Uniform pointwise advantage error is used only to derive `epsilon_{A,cand} <= epsilon_A` (`main.tex:484-486`, `2147-2154`). It is not silently assumed in the central CPI result.
- The current-policy component cancels exactly; the remaining evaluator penalty is `alpha epsilon_{A,cand}/(1-gamma)`.
- The occupancy calculation gives the stated quadratic penalty `2 gamma alpha^2 epsilon_CPI/(1-gamma)^2`.
- The strictness sentence at `main.tex:2155` is correct under the immediately preceding sufficient condition: strictness holds exactly when `alpha epsilon_{A,cand}<epsilon_A`.
- The finite-horizon coupling term `2 alpha epsilon_CPI,h [1-(1-alpha)^t]` and its bound by `2 alpha^2 t epsilon_CPI,h` have the correct factors. `H=0`, `H=1`, `alpha=0`, and `alpha=1` are handled.

### Deployment TV and KL bounds

- Theorem `thm:deployment_perturbation` (`main.tex:1343` onward) correctly uses a uniform statewise TV bound times the action-value oscillation, not twice that oscillation. Hence the infinite-horizon constant `Delta_r delta/(1-gamma)^2` is correct for the paper's TV convention.
- The finite-horizon oscillation is `Delta_r G_h(gamma)`. Summing it gives
  `Delta_r delta [G_H(gamma)-H gamma^H]/(1-gamma)` exactly.
- The recursive domain contains successors from the union of exact-mixture and deployed-policy supports, so deployed-only actions are covered.
- Pinsker gives `TV <= sqrt(kappa/2)` in either KL direction. The manuscript correctly declines a finite KL corollary when the selected divergence is infinite and retains the TV theorem when TV is independently bounded.
- A persistent deployment comparison is correctly restricted to policies sharing the frozen latent transition map; changing that map changes the MDP.

### Persistent augmented state

- The persistent construction beginning at `main.tex:730` distinguishes pre-unroll carried latent `z`, used latent `F_n(x,y,z)`, successor carried latent, and remaining clock `h`. Terminal outcomes and `h=1` enter the shared absorber.
- The current and candidate action kernels use the same frozen `F_n`. The exact mixture is pointwise on the full augmented state.
- The initial law records the latent initializer and clock. Stochastic initialization is represented by a fixed recorded kernel.
- Corollary `cor:persistent_cpi_augmented` (`main.tex:779` onward) is direct Bellman contraction on the augmented MDP. It does not need a fixed point, latent contraction, projection, or slow drift.
- Centering is conditional on the full augmented state, and the exact baseline and exact transition expectation are stated.
- The slow-drift initial-condition quantifier covers initial-law support and every start used for one-deviation closure trajectories (`main.tex:815-824`). With the new `n>=1` restriction, its recursion and `1-kappa_n` denominator are valid.

## Residual risk

The proof audit establishes conditional mathematics only. Retained finite-batch diagnostics do not instantiate uniform closure assumptions, and no historical checkpoint is shown by these proofs to satisfy the residual, centering, TV, KL, or slow-drift hypotheses.
