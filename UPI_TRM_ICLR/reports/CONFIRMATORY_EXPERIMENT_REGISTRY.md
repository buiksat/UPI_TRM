# Confirmatory experiment registry

Status: **DRAFT, NOT LOCKED, NO CONFIRMATORY RUN IS AUTHORIZED**

Created before inspecting any repaired-run outcome. This registry becomes
locked only after every `TBD-BEFORE-RUN` field is replaced, the generated data
and ordered evaluation manifests are hashed, the repaired code commit is
recorded, and that version is committed. Debug runs use a separate seed set and
cannot enter any confirmatory result.

## Common protocol

- Training interaction: one call to a training environment's `step` method.
  A vector step counts once per environment. Evaluation interactions are
  excluded from this budget and reported separately.
- Domain: hard 4 by 4 Sudoku with 6 to 8 empty cells.
- Training generator seed: `26080301`.
- Validation generator seed: `26080302`.
- Held-out test generator seed: `26080303`.
- The three generated record sets must be pairwise disjoint by canonical
  record hash. Any overlap aborts all registered runs.
- Training records: 1,024 unique records.
- Validation records: 256 unique records.
- Held-out test records: 512 unique records, evaluated once each in one fixed
  manifest order with no cycling.
- Confirmatory training seeds: `101,102,103,104,105,106,107,108,109,110`.
- Debug-only seeds: `9001,9002,9003`.
- Training budget: exactly 80,000 environment interactions per method and
  seed.
- Reporting checkpoints: 10,000, 20,000, 40,000, and 80,000 interactions.
- Primary endpoint: held-out exact-checker success at 80,000 interactions.
- Secondary endpoints: undiscounted shaped episode return, exact-checker
  score, invalid-action rate, recurrent forward passes, action-value
  evaluations, optimizer updates, wall time, peak device memory, and all
  theorem-facing finite-batch diagnostics declared below.
- No early stopping and no best-checkpoint selection. Infrastructure failures
  remain in the registry. A rerun is permitted only after a documented
  infrastructure diagnosis, using the original seed and configuration.
- Per-seed means use sample standard deviation. Paired method differences use
  a hierarchical bootstrap over seeds and held-out instances with 10,000
  resamples and analysis seed `26080311`, plus the exact paired sign-flip test
  over ten seed-level differences.
- Repeated evaluation instances are not treated as independent training
  seeds.
- All raw per-instance outcomes, counters, configurations, code commits,
  ordered record hashes, checkpoint hashes, and generation commands must be
  retained before a result can be described as verified.
- Every fully theory-oriented UPI-TRM cell must set
  `training_protocol=fixed_base_exact`. Setting
  `theory_exact_mixture=true` on the legacy training path is insufficient and
  must be labeled legacy. Historical reconstruction and compatibility cells
  use `training_protocol=legacy` explicitly.

Fields that must be locked before execution:

| Field | Required value |
| --- | --- |
| Code commit | `TBD-BEFORE-RUN` |
| Configuration schema hash | `TBD-BEFORE-RUN` |
| Training manifest SHA-256 | `TBD-BEFORE-RUN` |
| Validation manifest SHA-256 | `TBD-BEFORE-RUN` |
| Held-out manifest SHA-256 | `TBD-BEFORE-RUN` |
| Environment configuration SHA-256 | `TBD-BEFORE-RUN` |
| Action-mask configuration SHA-256 | `TBD-BEFORE-RUN` |
| Environment lock SHA-256 | `TBD-BEFORE-RUN` |
| Output root | `results/iclr_confirmatory/TBD-BEFORE-RUN` |

## C1: one-factor bridge

Hypothesis: one predeclared factor or the `F_z` by `F_d` interaction explains
the historical persistent versus episodic gap under a corrected held-out,
clock-complete protocol.

Reference cell `B0` keeps the reconstructible historical algorithm choices:
persistent latent, parameter-interpolated deployment, historical target,
historical baseline, and clock-complete replay. It uses the common data,
architecture, optimizer, learning-rate schedule, depth, discount, projection,
clamping, interaction budget, checkpoints, and seeds above. This is a valid
implementation comparison cell, not a theorem-aligned cell.

Primary one-factor cells change exactly one setting from `B0`:

| Cell | Only changed factor |
| --- | --- |
| `Bz` | persistent latent to episodic latent |
| `Bd` | parameter-interpolated deployment to the direct pointwise probability-space mixture |
| `Bt` | historical target to the exact K-step target with terminal masking and incomplete-segment rejection |
| `Bb` | historical baseline to exact action summation on the complete augmented state |

`Bs-legacy` runs the incomplete plan-only replay representation only as a
compatibility diagnostic. It is excluded from confirmatory performance
contrasts and cannot be called theorem aligned.

The predeclared interaction uses four cells with the same fixed settings for
all other factors:

| Cell | Latent | Deployment |
| --- | --- | --- |
| `I00` | persistent | parameter interpolation |
| `I01` | persistent | exact mixture |
| `I10` | episodic | parameter interpolation |
| `I11` | episodic | exact mixture |

Primary estimands are the paired 80,000-interaction success differences
`Bz-B0`, `Bd-B0`, `Bt-B0`, and `Bb-B0`. Apply Holm correction across these four
tests. The interaction estimand is
`(I11-I10)-(I01-I00)` and is secondary. Report every cell and every failed or
null run.

Failure rule: if no single contrast survives correction and the interaction is
also inconclusive, report that the gap remains unexplained. Do not choose a new
factor after seeing these outcomes.

## C2: interaction-matched UPI-TRM versus PPO

Hypothesis: corrected UPI-TRM has higher held-out success than
architecture-matched TRM+PPO at exactly 80,000 training interactions.

UPI-TRM uses the fully theory-oriented combination of persistent latent,
clock-complete augmented replay, exact K-step target, exact augmented-state
baseline summation, direct pointwise probability-space mixture, and
`training_protocol=fixed_base_exact`. PPO uses the same recurrent backbone and
the same train/test manifests. Both methods use the common seeds, ordered
512-record held-out pool, checkpoints, and interaction budget.

The primary estimand is the paired per-seed difference in held-out success at
80,000 interactions. The primary interval and test are the common
hierarchical bootstrap and exact sign-flip test. Curves indexed by environment
interactions are primary. Curves indexed by recurrent forward passes and wall
time are secondary. No unpaired Welch test is used.

Decision rule: if the interval does not support a positive difference, remove
the performance-superiority claim and present the work as analysis. Preserve
the null or negative result.

## C3: persistent theorem-facing diagnostics

Hypothesis: at least one predeclared finite-batch quantity connecting the
corrected persistent endpoint to the conditional theory is small on the fixed
held-out diagnostic set.

Run diagnostics for every `B0` and fully theory-oriented endpoint checkpoint,
not only successful seeds. Retain actual augmented states `(x,y,z,h)` from the
first 128 held-out records in manifest order. Use depths `n` from the run
configuration and `m in {n+1,n+2,n+4}`. Use diagnostic RNG seed `26080321`.
For Monte Carlo K-step estimates, use 256 independent rollouts per retained
state.

Report per seed, clock, and policy:

- exact finite-batch one-step augmented Bellman residual;
- Monte Carlo K-step residual estimate and standard error, separately from
  realized-path TD errors;
- exact statewise centering defect;
- candidate-policy bias;
- direct-mixture versus deployed-policy TV, KL, and support mismatch rate;
- recurrent path length, depth discrepancy, per-depth increments, local ratio
  undefined rate, and value-head drift;
- sensitivity to the actual, reset, and predeclared perturbed initial latents;
- carried-latent continuity and inter-edit drift;
- remaining-budget strata;
- current/candidate shared-map identity hash;
- projection-active rate and latent norms.

Summaries include maximum, 99th percentile, median, and mean. Every output must
state `scope: finite_batch`. No diagnostic is called a uniform certificate.
If the required endpoint checkpoint does not retain the base and candidate
proposal needed to reconstruct deployment, the deployment claim is exactly
`not verifiable from supplied evidence`.

## C4: projection train/evaluation cross-design

Hypothesis: the trained projection effect contains separable training and
frozen forward-pass components.

Train with `R_train in {off,10}` and evaluate every frozen checkpoint under
`R_eval in {off,10}`. Other settings follow the fully theory-oriented UPI-TRM
cell. The primary frozen-checkpoint estimand is the paired test-time
`R_eval=10` minus `R_eval=off` success difference. The training-radius effect
and interaction are secondary. Report success, return, action agreement,
value change, augmented residual, recurrent path length, projection-active
rate, latent norms, and depth discrepancy.

Use the terms `projection enabled` and `clamping enabled`. Do not infer a
global contraction modulus from a local proxy or from success.

## C5: second verifier-guided domain

Selected before running a performance pilot: 8-puzzle.

Selection basis: exact verifier, deterministic transitions, fixed edit budget,
negligible random success, and direct compatibility with plan editing. The
selection is not based on preliminary performance. Generator seeds are
`26080401` for training, `26080402` for validation, and `26080403` for held-out
test data. The exact record counts, horizon, and interaction budget remain
`TBD-BEFORE-RUN` until the environment and costed smoke test exist.

Required methods are corrected UPI-TRM, the same-backbone PPO baseline, and the
bridge cell selected by this predeclared rule: choose the bridge factor with
the largest absolute corrected paired effect from C1; break ties in the fixed
order `F_z`, `F_d`, `F_t`, `F_b`. This selection is secondary and must be
reported as transferred from C1, not as a new confirmatory discovery.

If the transfer fails, retain the failure and narrow the paper's scope.

## Lock and amendment rules

1. Only commits made before the first confirmatory training action may fill the
   `TBD-BEFORE-RUN` fields or clarify an ambiguity.
2. After lock, amendments correct infrastructure defects only. Each amendment
   records the old text, new text, reason, timestamp, and whether any outcome
   was inspected.
3. Debug results cannot alter seeds, budget, endpoint, evaluation pool,
   statistics, or failure rules.
4. No result enters the paper until its run registry entry and all expected
   raw artifacts exist and reproduce.
