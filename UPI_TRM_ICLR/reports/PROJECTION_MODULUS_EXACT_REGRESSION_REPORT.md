# Exact radial-projection modulus regression

## Audit result

The retained finite-MDP, finite-horizon, and learned-diagnostic suites did not
separately check the radial-projection factor and its composite modulus below,
at, and above one. Learned sensitivity records are sampled diagnostics and do
not fill this theorem-pipeline coverage gap.

## Exact construction

`experiments/projection_modulus_exact_checks.py` uses only the Python standard
library and `fractions.Fraction`. On a two-point metric space it sets

- projection radius `R = 1`;
- minimum pre-projection norm `rho_R = 2`;
- exact radial-projection factor `R / rho_R = 1/2`;
- pre-projection moduli `1`, `2`, and `4`.

The two outputs are `-2` and `2`, so radial projection maps them to `-1` and
`1`. Choosing input distances `4`, `2`, and `1` makes the composite moduli
exactly `1/2`, `1`, and `2`. The retained classifications are respectively
`strict_contraction`, `unit_modulus`, and `superunit_modulus`. Thus only a
modulus strictly below one receives contraction terminology.

## Execution

Run from `UPI_TRM_ICLR`:

```bash
python3 experiments/projection_modulus_exact_checks.py \
  --output results/finite_mdp_certificate_validation/projection_modulus_exact_checks.json
```

The command was executed twice. Both runs passed 41 exact assertions and
produced the same output bytes.

| Artifact | SHA-256 |
|---|---|
| `experiments/projection_modulus_exact_checks.py` | `f5cca90caf527441cf8c02921d22a2807c29910cb9867ff22b639302a9e437b0` |
| `results/finite_mdp_certificate_validation/projection_modulus_exact_checks.json` | `d6806c787ad8fd706131c50dfcb1b29c32df51788bce6407ad2b39914d3988fd` |

This is an exact theorem-pipeline regression on a fixed analytic construction.
It is not a global contraction certificate for a learned recurrent evaluator.
