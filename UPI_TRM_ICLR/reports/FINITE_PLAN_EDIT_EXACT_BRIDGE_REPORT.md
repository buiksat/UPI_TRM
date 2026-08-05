# Fixed Exact Finite Plan-Edit Bridge

## Scope

This theorem-to-outcome bridge evaluates the current hand-constructed source
registry in `experiments/finite_plan_edit_bridge_exact.py`. The script evaluates
every listed row, but expected outcome labels are encoded in source. The
protocol was not preregistered. Absence of outcome-informed case construction
is not verifiable from supplied evidence. All values are computed with Python
`fractions.Fraction` on a clock-complete two-edit MDP with one shared absorber.

The bridge is an exact finite-state theorem-pipeline experiment. It is not a
learned-model result.

## Command

Run from `UPI_TRM_ICLR`:

```bash
python3 experiments/finite_plan_edit_bridge_exact.py \
  --output results/finite_mdp_certificate_validation/finite_plan_edit_bridge_exact.json
```

Observed output:

```text
PASS fixed_exact_finite_plan_edit_theory_outcome_bridge: 285 exact checks, 4 positive certificates, 6 vacuous; output=results/finite_mdp_certificate_validation/finite_plan_edit_bridge_exact.json
```

## Fixed Protocol

- Discount: `gamma=1/2`
- Bellman block: `K=1`
- Base correct-edit probability: `1/4`
- Terminal success reward: `4`
- Cases: `10`, all retained
- Case-registry SHA-256:
  `1ee6e6dce5966a4bb099e665265bffd7828fa9d466d8591477b9c4c7d6dda437`

Each JSON case records the exact base value and advantage tables, evaluator,
Bellman backup and residual, actual value and advantage errors, candidate bias,
exact pointwise mixture, actual performance change, estimated surrogate, CPI
penalties and lower bounds, certificate status, and slack.

The primary `certificate_status` uses the complete chain from the uniform
Bellman residual through the residual-derived advantage bound and then the CPI
inequality. The JSON also retains the tighter lower bound that uses the exact
candidate-policy bias. This distinguishes a vacuous residual bridge from a
vacuous CPI inequality.

## Results

| Case | Alpha | Residual | Candidate bias | Actual change | Certified change | Status |
|---|---:|---:|---:|---:|---:|---|
| `zero_residual_positive` | `1/20` | `0` | `0` | `1/20` | `1/25` | positive |
| `small_residual_positive` | `1/100` | `1/100` | `1/400` | `1/100` | `369/40000` | positive |
| `moderate_residual_positive` | `1/100` | `1/10` | `1/40` | `1/100` | `117/20000` | positive |
| `residual_bridge_vacuous_exact_bias_positive` | `1/100` | `1/2` | `1/8` | `1/100` | `-183/20000` | vacuous |
| `large_alpha_boundary_vacuous` | `1/4` | `0` | `0` | `1/4` | `0` | vacuous |
| `smaller_candidate_bias_positive` | `1/100` | `1/100` | `1/800` | `1/200` | `353/80000` | positive |
| `null_candidate_with_residual` | `1/2` | `1/2` | `0` | `0` | `-1` | vacuous |
| `unfavorable_candidate_retained` | `1/10` | `1/10` | `1/80` | `-1/20` | `-89/800` | vacuous |
| `alpha_zero_control` | `0` | `1` | `1/4` | `0` | `0` | vacuous |
| `large_residual_positive_but_pipeline_vacuous` | `1/100` | `2` | `1/2` | `1/100` | `-327/5000` | vacuous |

Aggregate outcomes:

- Positive full-pipeline certificates: `4`
- Vacuous full-pipeline certificates: `6`
- Actual positive outcomes: `7`
- Actual null outcomes: `2`
- Actual negative outcomes: `1`

The negative and null cases remain in the output. The bridge also retains cases
where the exact candidate-bias certificate is positive but the residual-derived
certificate is vacuous.

## Determinism and Artifacts

A second execution produced byte-identical JSON.

| Artifact | SHA-256 |
|---|---|
| `experiments/finite_plan_edit_bridge_exact.py` | `fd9a8dd9aadbee5ca19c4f0caeab2b9500250d56091fa31aff9586dd638dedca` |
| `experiments/corollary_6_2_exact_checks.py` | `992702b6019ff0597491982a96b7e9b565ee2aefa27e192ba0ee647db81135f3` |
| `results/finite_mdp_certificate_validation/finite_plan_edit_bridge_exact.json` | `b9c2338b12dcf584ad522335cc1f8db2c3c38f2734d7ad6f1f51229153c920c5` |

The bridge does not establish uniform theorem assumptions for a learned model
and does not change any learned experimental result.
