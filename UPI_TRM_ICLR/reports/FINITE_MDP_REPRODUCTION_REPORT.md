# Finite-MDP theorem-pipeline reproduction

## Scope

This report records a fresh reproduction of the retained 101-row finite-MDP artifact and a separate deterministic boundary suite. These calculations test the implementation of the paper's finite-state inequalities. They are theorem-pipeline numerical unit tests, not empirical validation of learned TRMs.

The existing generator remained unchanged, so the primary CSV contract is still 80 value-curve rows plus 21 CPI rows.

## Execution context

- Repository branch: `iclr-evidence-aligned-revision`
- Source commit at execution: `896af29fb4970964d35505fbb45983a90834828d`
- Python: `3.12.13+meta`
- gnuplot: `5.4 patchlevel 3`
- Generator: `experiments/finite_mdp_certificate.py`
- Boundary suite: `experiments/finite_mdp_boundary_checks.py`
- Retained command output: `reports/finite_mdp_reproduction.stdout.txt`

## Commands

Run from the `UPI_TRM_ICLR` directory:

```text
python3 experiments/finite_mdp_certificate.py --outdir results/finite_mdp_certificate_validation
python3 experiments/finite_mdp_boundary_checks.py --primary-csv results/finite_mdp_certificate_validation/finite_mdp_summary.csv --out results/finite_mdp_certificate_validation/finite_mdp_boundary_checks.json
python3 -m py_compile experiments/finite_mdp_boundary_checks.py
```

All commands exited with status 0.

## Primary 101-row result

The fresh generator run reproduced the committed primary artifacts byte for byte.

| Check | Result |
| --- | ---: |
| CSV data rows | 101 |
| Value-curve rows | 80 |
| CPI-curve rows | 21 |
| Decomposition flags true | 101 |
| Exact-candidate-bias flags true | 101 |
| Worst finite-reference margin, lhs minus rhs | `-2.943e-01` |
| Worst residual-to-value margin, lhs minus rhs | `-2.943e-01` |
| Worst candidate-bias margin, lhs minus rhs | `-1.423e+00` |
| Worst centered-CPI decomposition margin, lhs minus rhs | `0.000e+00` |
| Worst centered-CPI exact-bias margin, lhs minus rhs | `0.000e+00` |

A nonpositive margin passes the corresponding inequality. The zero CPI margins occur at the exact `alpha=0` endpoint.

## Boundary suite

The separate suite ran seven checks, all of which passed. It retains detailed floating-point values in `results/finite_mdp_certificate_validation/finite_mdp_boundary_checks.json`.

| Required case or inequality | Check | Result |
| --- | --- | --- |
| Residual-to-value inequality | `depth_boundaries`, `one_step_and_zero_residual`, `gamma_zero`, `terminal_and_absorbing_boundaries` | passed |
| Finite-reference inequality | `depth_boundaries` | passed for all three depth pairs |
| Path-length inequality | `depth_boundaries` | passed, including the finite geometric path bound |
| Value-to-advantage inequality | `advantage_candidate_centered_cpi_and_exact_mixture` | error `0.1404667`, bound `0.3557407` |
| Candidate-policy bias | `advantage_candidate_centered_cpi_and_exact_mixture` | bias `0.0583611`, below both checked bounds |
| Exact statewise centering | `advantage_candidate_centered_cpi_and_exact_mixture` | maximum defect `9.37e-17` |
| Centered CPI inequality | `advantage_candidate_centered_cpi_and_exact_mixture`, `zero_advantage_error`, `gamma_zero` | passed at every retained mixture weight |
| Exact probability-space mixture | `advantage_candidate_centered_cpi_and_exact_mixture` | normalized statewise; recomputed returns match |
| `alpha=0` | exact-mixture endpoint and primary CSV | policy and return errors `0` |
| `alpha=1` | exact-mixture endpoint and primary CSV | policy and return errors `0` |
| `n=0` | `depth_boundaries` | `U_0=0`; all bounds passed |
| `m=n+1` | `depth_boundaries` | tested at `n=5, m=6` |
| large `m` | `depth_boundaries` | tested at `m=128` |
| `gamma=0` | `gamma_zero` | residual equals value error exactly to retained precision |
| `K=1` | `one_step_and_zero_residual`, `gamma_zero` | passed with nonzero and zero discount |
| zero residual | `one_step_and_zero_residual` | `2.50e-16`, below the `1e-10` zero tolerance |
| zero advantage error | `zero_advantage_error` | advantage error and candidate bias both `0` |
| `K` beyond remaining horizon | `terminal_and_absorbing_boundaries` | `K=5` on a three-edit clock chain; backup equals exact value |
| absorbing initial state | `terminal_and_absorbing_boundaries` | exact return `0` |
| absorbing boundary | `terminal_and_absorbing_boundaries` | zero boundary fixed; incorrect boundary detected by residual |
| terminal boundary | `terminal_and_absorbing_boundaries` | final action values equal immediate rewards; no bootstrap leakage |

The boundary JSON is deterministic. Two consecutive runs produced the same SHA-256 digest.

## SHA-256 inventory

| File | SHA-256 |
| --- | --- |
| `experiments/finite_mdp_certificate.py` | `1571aaabd0d383b58da4be3f26be7115e218b4b7a34736116f098eb4e723d922` |
| `experiments/finite_mdp_boundary_checks.py` | `86127165ba952291f9fb6a8b1303684a63d96e58d9b7465f252f6c342d2429e3` |
| `results/finite_mdp_certificate_validation/finite_mdp_summary.csv` | `52875311ee5d7144ffce5afc2853c746440de5810836c631bc69f8fdb85996d6` |
| `results/finite_mdp_certificate_validation/finite_mdp_summary.tex` | `cbad8dd1f651acd0f46ca4fdd6ecc33e0087bcba20b13e99fd4f65c5d7f821dd` |
| `results/finite_mdp_certificate_validation/finite_mdp_boundary_checks.json` | `ee0867af8e24fce5e8b047b08d32fed3225db98c1bb2699e23dd8616dbc9512a` |

## Numerical scope

The suite uses deterministic finite MDPs and tolerances of `1e-8` for inequalities and `1e-10` for numerical zero. It checks code paths and boundary conventions. It does not establish a uniform residual for any learned evaluator, certify global contraction, or support a task-level performance claim.
