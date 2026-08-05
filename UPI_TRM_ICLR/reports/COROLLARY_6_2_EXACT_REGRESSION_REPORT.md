# Corollary 6.2 Independent Exact Regression

## Scope

This regression is independent of the floating-point finite-MDP figure
generator. It uses only the Python standard library and
`fractions.Fraction`. It checks the bounded-function premise and the value,
advantage, candidate-bias, and CPI constants implicated by Corollary 6.2.

This is a theorem-pipeline regression, not learned-model evidence.

## Command

Run from `UPI_TRM_ICLR`:

```bash
python3 experiments/corollary_6_2_exact_checks.py \
  --output results/finite_mdp_certificate_validation/corollary_6_2_exact_checks.json
```

Observed output:

```text
PASS corollary_6_2_independent_exact_regression: 146 exact checks; output=results/finite_mdp_certificate_validation/corollary_6_2_exact_checks.json
```

## Result

- Status: `all_passed=true`
- Exact checks: `146`
- Cases: `4`
- Arithmetic: `fractions.Fraction`
- Determinism: a second execution produced byte-identical JSON

The retained cases cover:

1. The unbounded deterministic countable chain with zero residual for
   `K in {1,2,3,5,8}` and infinite supremum value error. The case is marked
   outside the bounded-function domain.
2. A bounded one-state self-loop attaining equality in the residual
   certificate for `K in {1,2,4,7}`.
3. The bounded countable chain `U(s_i)=(-1)^i`, with equality for even `K`
   and a strict residual bound for odd `K`.
4. An exact three-state oracle with a candidate-only one-step successor and a
   shared absorber. It checks the Bellman residual, actual value error,
   centered advantage error, candidate-policy bias, exact probability-space
   mixture, and CPI constants. The CPI lower bound attains equality for
   `alpha in {0,1/3,1}`. The comparison
   `alpha * epsilon_A,cand <= epsilon_A` is strict at `alpha=0` and `1/3`
   and is an equality at `alpha=1`. A separate cancellation row checks
   `epsilon_A,cand < epsilon_A`. The residual-derived CPI substitution is an
   equality at `alpha=0` and strict at `alpha=1/3` and `1`.

The candidate-only successor case records a zero residual on the base-only
restricted domain and a nonzero residual on the complete advantage-evaluation
closure. This directly exercises why one-step deviation successors must be in
the norm domain.

## Artifacts

| Artifact | SHA-256 |
|---|---|
| `experiments/corollary_6_2_exact_checks.py` | `992702b6019ff0597491982a96b7e9b565ee2aefa27e192ba0ee647db81135f3` |
| `results/finite_mdp_certificate_validation/corollary_6_2_exact_checks.json` | `a79fac9e9cf0b95ee57f7ecf3d08c780accd21f227b0ff520ed189a0f59c0455` |

The regression does not establish theorem assumptions for a learned model and
does not change any learned experimental result.
