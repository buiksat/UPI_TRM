# Legacy and Archived Experiment Report

## Purpose

This report is the proposed home for experiments removed from the paper's
active evidence narrative. It preserves null, negative, incomplete, and
historical outcomes. It does not upgrade their provenance or claim status.
No file has been physically moved or deleted yet.

Recommended future archive roots:

- `artifacts/legacy_exploratory/paper_tables/`
- `artifacts/legacy_exploratory/paper_figures/`
- `artifacts/legacy_exploratory/derived_results/`
- `artifacts/legacy_exploratory/provenance/`

Raw implementation outputs should remain in their current version-controlled
locations or move through a separate manifest-preserving operation. Never
discard a negative cell.

## Historical performance records

### Persistent UPI--TRM and architecture-matched baselines

Current paper locations:

- `main.tex`, `app:headline_significance`
- `tab:hard_suite_anchor`

Preserved outcome:

- Persistent UPI--TRM: 57.4% +/- 12.2% over ten recorded seeds.
- TRM+PPO: 32.0% +/- 15.3% over ten recorded seeds.
- TRM+A2C and TRM+DQN: 0.0% +/- 0.0%.
- External PPO/A2C/DQN variants: recorded 0% success under a different budget
  unit and with high invalid-action rates.

Interpretation limits:

- The UPI evaluator cycles 50 episodes over 32 training records.
- Persistent UPI and PPO use unequal interaction semantics and incompatible
  dataset records.
- Checkpoints, historical data, ordered evaluation outcomes, and the producing
  training commit are absent.
- A held-out or comparative performance claim is not verifiable from supplied evidence.

Retain the seed lists and arithmetic for forensic audit only. Do not retain the
old Welch test as method evidence.

### Incomplete equal-interaction attempt

Current paper locations:

- `main.tex`, `app:equalized_baselines`
- `tab:equalized_baselines`

Preserved outcome: the baseline-only attempt is incomplete and has no UPI--TRM
arm. PPO has nine complete seeds, A2C eight complete plus one partial, DQN nine
complete plus one partial, and five-step DQN eight complete plus two partial.
There is no matched comparison. This is a missing experiment, not a null
comparison.

## Theory-oriented episodic record

Current paper locations:

- `main.tex`, `sec:episodic_negative_main`
- `main.tex`, `app:episodic_z_hard_suite_rerun`
- `tab:episodic_z_branch_d`
- `tab:episodic_z_penalty`

Preserved negative outcomes at the nominal 20k endpoint, seeds 41--50:

- success: 0.0% +/- 0.0%;
- shaped undiscounted return: -21.733 +/- 0.512;
- final checker score: 3.906 +/- 0.606;
- invalid rate: 0.000 +/- 0.000;
- finite-batch residual: 5.047 +/- 0.175;
- finite-batch post-projection local proxy: 0.600 +/- 0.104 over 8/10 seeds;
- seeds 41 and 46 have a proxy at least one;
- the derived all-seed predicted CPI penalty is positive infinity at every
  retained alpha because of those two seeds.

This run jointly changed latent persistence, baseline computation, target
construction, and collection policy. Its endpoint evaluator scored the old
policy, not the configured exact mixture, and reused a materialized 32-record
training pool. Checkpoints, hard data, source logs, raw per-instance outcomes,
and a pinned producing commit are absent. Exact-mixture endpoint performance
and diagnostic regeneration are not verifiable from supplied evidence.

The 0% endpoint and the nonfinite penalty are unfavorable results and must
remain in this external report even if later corrected runs succeed.

## Projection and clamping records

### Historical hard-suite 2x2

Current paper locations:

- `main.tex`, `sec:controlled_2x2_main`
- duplicate discussion at `app:controlled_2x2`
- `tab:controlled_2x2_main`

Preserved arithmetic, ten seeds per cell:

| Condition | Success |
| --- | ---: |
| Clamping disabled, projection off | 35.0% +/- 8.9% |
| Clamping disabled, radius 10 | 48.2% +/- 7.1% |
| Clamping enabled, projection off | 37.4% +/- 7.8% |
| Clamping enabled, radius 10 | 50.2% +/- 10.5% |

The projection contrast is +13.0 percentage points averaged over clamping
status. The clamping-enabled contrast is +2.2 points averaged over projection
status. Both are historical composite contrasts. The original statistical
script, checkpoints, data, ordered pool, and per-instance outcomes are absent.
The source-reported p-value and a causal mechanism claim are not verifiable from supplied evidence.

### Projection dominance and failed dial

Current paper locations and sources:

- `main.tex`, `app:exp2_sweep`
- `tables/table_exp2_dial_does_not_control_Lz.tex`
- `tables/table_exp2_projection_effect.tex`
- unused `tables/table_exp2_contraction_sweep.tex`

Preserved null/mechanism-limiting outcome: at radius 10, projection is active
on 100% of the retained batch and the local post-projection proxy stays in the
narrow 0.219--0.242 range across nominal clamping targets. The target does not
control the measured proxy monotonically. Projection reduces depth-mismatch
value drift in the retained aggregate, but this is a composite exploratory
comparison. It does not establish a global modulus below one.

### Projection-free range tests

Current paper locations and sources:

- `main.tex`, `app:exp4_projection_free_dial`
- `tables/table_exp4_projection_free_dial_range_test.tex`
- `main.tex`, `app:exp4_projection_free_dial_v2`
- `tables/table_exp4_projection_free_dial_v2.tex`

Preserved outcomes:

- A single-checkpoint inference-time scale sweep spans a local proxy of about
  0.52--0.95.
- Neither value drift nor action agreement changes monotonically over the
  first five-point range.
- A second four-scale aggregate prints strong Spearman correlations, but four
  settings do not support a confirmatory mechanism claim and the checkpoints
  and raw batches are absent.

Treat both as feasibility observations. Do not carry the
"statistically significant" wording into the paper.

### Easy-suite training projection ablation

Current paper locations and source:

- `main.tex`, `app:exp3_projection_ablation`
- `tables/table_exp3_projection_ablation.tex`

Preserved outcome: all six easy-suite cells pass the stated stability gate and
obtain 94%--98% success. Within that protocol, projection is not necessary for
training stability. The result does not generalize to the hard suite.

## Depth, radius, and local-proxy diagnostics

### B0 and B1 depth mismatch

Current paper locations and sources:

- `main.tex`, `sec:isolation_study` / `app:depth_mismatch_main`
- `main.tex`, `app:exp1_tables`
- `tables/table_exp1_unroll_sensitivity.tex`
- `tables/table_exp1_radius_sweep_main.tex`
- `main.tex`, `app:exp1_b1`
- `tables/table_exp1_radius_sweep_appendix.tex`

Preserved outcome: on the retained 1--4-empty batch, clamping enabled reduces
B0 value drift from 0.166 to 0.064 and raises action agreement from 90.2% to
95.5% at the 2-to-8 depth mismatch. B1 shows the same direction with higher
absolute noise. Moving from projection off to radius 10 produces the larger
stability change. These are finite-batch diagnostics, not contraction
certificates or hard-suite performance evidence.

### Fine-grained finite-radius sweep

Current paper locations and figures:

- `main.tex`, `app:finite_r_b0`
- `fig:exp1_finite_r_b0`
- `figures/fig_exp1_finite_r_primary_b0.png`
- `figures/fig_exp1_finite_r_mechanism_b0.png`
- `figures/fig_exp1_finite_r_theory_b0.png`

Preserved outcome: the projection-active rate stays one through radius 32,
drops to 0.2 at radius 34, and reaches zero at radius 40 and above. The retained
finite-batch residual changes non-monotonically in that transition. This
supports neither a smooth saturation dial nor an end-to-end explanation of
the hard-suite contrast.

### Local value-head proxy

Current paper location and source:

- the unlabeled paragraph preceding `tab:exp1_value_head_lipschitz`
- `tables/table_exp1_value_head_lipschitz.tex`

Preserved outcome: excluding the noisiest `1e-5` perturbation, the two
conditions stay in the same-order 0.085--0.111 local-proxy band. This is not a
global value-head Lipschitz bound. Fresh execution is not verifiable from supplied evidence.

## Single-seed and easy-suite mechanism probes

### Spectral normalization instability

Current paper locations: `main.tex`, `app:sn_instability`, and
`tab:sn_instability`.

Preserved negative outcome: power-iteration spectral normalization produced
local proxy values near 2.7e4 and 4.5e4 in the retained check. Operator-norm
clamping remained numerically stable near 0.6. None of these local values is a
global contraction certificate, and the run cannot be reconstructed from the
retained checkpoints.

### Latent-collapse probe

Current paper locations: `main.tex`, `app:latent_collapse_diagnostic`, and
`tab:latent_collapse`.

Preserved outcome: in one seed, clamping reduces total latent variance by
about 25% and increases cosine similarity, but does not collapse latent norms
to zero. Value-head normalization, not latent clamping, drives the large value
variance and clamp-hitting behavior. This identifies a confound, not a general
mechanism.

### Toy-suite feasibility

Current paper locations: `main.tex`, `app:toy_feasibility`, and
`tab:upi_success_only`.

Preserved outcome: three-seed UPI variants obtain about 90.7%--93.3% success,
while masked random obtains 52%. The task is too easy to support the paper's
practical claim.

### Stability--expressivity sweep

Current paper locations and source:

- `main.tex`, `app:exp5_tradeoff_curve`
- `tables/table_exp5_tradeoff_curve.tex`

Preserved null outcome: success stays essentially flat near 6.7% over the four
scale settings. No clear stability--expressivity tradeoff appears in this
batch.

## Hard-suite definition record

Current paper location: `main.tex`, `app:harder_sudoku_detailed`.

The manuscript describes 6--8-empty Sudoku and 0% random-policy success. The
underlying hard dataset and random-policy run are absent. The random success
rate is not verifiable from supplied evidence and should not appear as an
established fact in the active paper.

## Material that remains active

The finite-MDP calculation is not archived with the learned-model experiments.
It remains an active theorem-pipeline unit test with a generator, 101-row CSV,
and validation log. The clock-complete architecture figure and practical
diagnostic-definition table remain implementation definitions. Neither is
performance evidence.

## Future archive manifest requirements

Before physically moving files, create a machine-readable manifest containing:

- original path;
- archive path;
- SHA-256 before and after the move;
- generating script, when known;
- source commit;
- classification from `reports/EXPERIMENT_TRIAGE.md`;
- reason for removal from the paper;
- evidence status;
- whether the result is null or negative.

The archive operation must preserve every retained row and must not rewrite an
unsupported result as verified. Missing checkpoint, dataset, policy identity,
or execution provenance remains not verifiable from supplied evidence.
