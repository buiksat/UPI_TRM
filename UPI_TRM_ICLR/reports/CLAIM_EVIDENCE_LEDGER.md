# Claim-evidence ledger

Manuscript state: theory-only source commit
`594e21bed2d8f717228346d19a74665a8c81d1c9`. The committed `main.tex`
SHA-256 is `69f3eb3f3b1951780714fc82ec216476d2d724fc999229a415c46b9e12d4b625`.

Implementation state: repaired code commit
`97dbf56fb02bd34c7ebdea7e9a81bac5d5e7d08e`. The final Buck gate ran all
33 `python_unittest` targets: 397 passed, 0 failed, 0 timed out. The training
and persistent-diagnostics binaries both built successfully. These checks
verify the tested implementation paths; they are not learned-task evidence.

The active manuscript explicitly reports no learned-task result, numerical
theorem check, ablation, or method comparison. Repository experiments and
regression outputs are retained for auditability but are not manuscript
evidence. The confirmatory matrix remains `registered_not_authorized`; no
confirmatory training run has executed.

`CODE_REPO/` denotes the implementation repository without embedding a private
workstation path in release-facing artifacts.

## Status vocabulary

- `proved`: a proof is present in `main.tex`, conditional on its displayed assumptions.
- `repository-only regression`: retained executable output used for development; absent from the manuscript and not empirical evidence.
- `repository archive only`: retained historical or debug material; absent from the manuscript and excluded from active claims.
- `implementation regression verified`: the named behavior is covered by the final code regression suite at the recorded producer commit; this is not evidence of learned performance or a uniform theorem premise.
- `missing experiment`: no authorized confirmatory result exists.
- `not verifiable from supplied evidence`: the evidence required for the stated claim is absent.

## Active manuscript claims

| ID | Stable manuscript location and claim | Material conditions | Status | Repository-only support |
|---|---|---|---|---|
| T01 | Theorem `thm:finite_reference_depth`: finite-reference recurrent-path and residual decomposition | One frozen MDP and policy pair; finite/countable successor and one-deviation closure; bounded rewards and evaluators; common recurrence, initialization, norm, and absorbing boundary | `proved` | Finite-MDP and exact-rational checks are `repository-only regression`, not part of the paper. |
| T02 | Corollary `cor:finite_depth_residual_certificate`: direct finite-depth residual certificate | Fixed discounted MDP and policy; bounded-function Bellman domain; closure under required successors; bounded `U_n` and `V^pi`; Bellman self-map and fixed point; common absorber | `proved` | `corollary_6_2_exact_checks_20260804` is `repository-only regression`. The unbounded countable-chain construction documents why the bounded-domain premise is necessary. |
| T03 | Theorem `thm:monotone_with_error` and Corollaries `cor:one_step_improvement_condition`, `cor:cpi_dials_main`: centered CPI bounds | Fixed MDP; finite candidate-policy bias; exact statewise centering; exact pointwise probability-space mixture; declared closure and CPI constants | `proved` | Finite exact cases are `repository-only regression`; no learned policy is claimed to satisfy the premises. |
| T04 | Corollary `cor:persistent_cpi_augmented`: direct persistent-state residual and CPI implication | Clock-complete state `(x,y,z,h)`; shared absorbing atom; common frozen recurrent map; uniform augmented residual; exact augmented-state centering and exact mixture | `proved` | Learned-checkpoint instantiation is `not verifiable from supplied evidence`. |
| T05 | Lemma `lem:drift_bound`: optional slow-drift comparison to a memoryless fixed-point reference | Uniform contraction and fixed-point conditions; edit-drift bound; Lipschitz head; uniformly quantified initial tracking error; nonabsorbing trajectory segments | `proved` | Learned-model calibration is `not verifiable from supplied evidence`. |
| T06 | Theorem `thm:finite_horizon_reference`: clock-aware finite-horizon residual and finite-reference bounds | Finite/countable stage closures; exact terminal boundary; truncated final blocks; common frozen recurrence; bounded head | `proved` | Official and stress finite-horizon checks are `repository-only regression`. |
| T07 | Theorem `thm:finite_horizon_cpi`: finite-horizon centered CPI bound | Fixed time-indexed MDP; exact stagewise mixture and centering; finite candidate bias; recursive occupancy closure; shared terminal boundary | `proved` | Finite-horizon checks are `repository-only regression`. |
| T08 | Theorem `thm:deployment_perturbation` and Corollary `cor:deployment_pinsker`: deployment perturbation from the exact mixture | One fixed MDP; closure invariant under both policies; bounded reward range; uniform statewise TV or finite either-direction KL | `proved` | A finite-batch KL or TV value does not instantiate the theorem. Learned deployment gap is `not verifiable from supplied evidence`. |
| T09 | Propositions `prop:proj_sat_contraction` and `prop:proj_residual_anchor`: projection-aware bounds | Uniform saturated-annulus premise and global pre-projection modulus; strict product below one for contraction; declared anchor and absorber assumptions | `proved` | `projection_modulus_exact_checks_20260804` is `repository-only regression`, not a learned-network certificate. |

These are conditional mathematical statements. The manuscript does not claim
that their uniform premises hold for a learned evaluator or deployed policy.

## Implementation inventory

The paper describes a theorem-facing implementation. The following code paths
were regression-tested at the recorded producer commit, but no learned training
run or theorem-premise certificate follows from those tests.

| ID | Required implementation property | Current paths | Current status |
|---|---|---|---|
| I01 | Persistent replay and serialization retain `(x,y,z,h)`, the pre-unroll input latent, post-unroll successor carry, terminal cause, and one shared absorber | `CODE_REPO/rl/replay.py`, `rl/upi_trm_trainer.py`, `rl/persistent_diagnostics.py`, `upi_trm_train.py` | `implementation regression verified` at `97dbf56`; no learned checkpoint was evaluated. |
| I02 | Exact statewise centering enumerates legal actions on the full augmented state, records its maximum defect, and fails closed above its numerical tolerance | `CODE_REPO/rl/upi_trm_trainer.py`, `utils/lipschitz.py`, `rl/persistent_diagnostics.py` | `implementation regression verified` at `97dbf56`; no uniform learned-model centering bound is claimed. |
| I03 | The theorem-facing deployed policy is the pointwise probability-space mixture; parameter interpolation and distillation remain separate objects | `CODE_REPO/rl/upi_trm_trainer.py`, `rl/persistent_diagnostics.py` | `implementation regression verified` at `97dbf56`; no performance result was produced. |
| I04 | K-step targets, truncation, termination, zero-budget initialization, and absorbing transitions do not bootstrap across a terminal boundary | `CODE_REPO/rl/value_targets.py`, `rl/upi_trm_trainer.py`, environment adapters | `implementation regression verified` at `97dbf56`, including nonfinite terminal-successor cases. |
| I05 | Exact interaction counters and immutable artifacts support a future matched comparison | `CODE_REPO/utils/compute_accounting.py`, `utils/evaluation_artifacts.py`, `upi_trm_train.py` | Mechanics are `implementation regression verified`; the matched learned comparison is a `missing experiment`. |
| I06 | Confirmatory execution requires a complete registered cell-by-seed product, canonical nonoverlapping device queues, immutable locks, and no-replace publication | `scripts/run_registered_matrix.py` in this paper repository and the registered code matrix | Seven executor regression tests pass; the matrix is still `registered_not_authorized`, so no training was launched. |

The final implementation test log is
`CODE_REPO/reports/GPT_PRO_REPAIR_FINAL_UNITTESTS_20260804.log`; the build log is
`CODE_REPO/reports/GPT_PRO_REPAIR_FINAL_BUILDS_20260804.log`. The earlier
408-pass/1-fail log is retained as failed pre-final evidence. Historical runtime
logs and code archives validate only their named commits.

## Repository-only evidence inventory

| ID | Retained material | Classification | Manuscript status |
|---|---|---|---|
| R01 | Six finite-MDP, finite-horizon, exact-rational, and projection theorem-pipeline runs in `results/RUN_REGISTRY.jsonl` | `repository-only regression` | Not cited, tabulated, plotted, or counted in `main.tex`. It is not proof or empirical validation. |
| R02 | Eight seed-9001, 80-interaction debug runs and staged validation artifacts | `repository archive only`; every record is `excluded_from_confirmatory` | Not a learned result, ablation, bridge, or method comparison. |
| R03 | Historical episodic and persistent summaries, per-seed rows, diagnostics, and narrative logs under `results/`, `EPISODIC_Z_RUN_LOG.md`, `TABLE1_PROVENANCE.md`, and `REEVAL_LOG.md` | `repository archive only`; produced by superseded or incompletely reconstructible protocols | No historical outcome value appears in the manuscript. Corrected-algorithm performance is `not verifiable from supplied evidence`. |
| R04 | Registered Sudoku train/validation/test corpus and split manifests in the code repository | Repository-only input provenance | Not a task result and not evidence for any theorem premise. |
| R05 | Confirmatory bridge and matched-comparison registration: 8 cells x 10 seeds at the registered interaction budget | Pre-experiment registration | `missing experiment`; status remains `registered_not_authorized`, with zero confirmatory training runs. |

## Artifact-supply claims

The active manuscript does not state that numerical result files, learned
checkpoints, CSVs, validation logs, or per-seed outcomes are submitted. It also
does not present a paper-visible numerical result requiring those artifacts.
The current manifest is a working repository inventory, not a complete
anonymous supplement manifest.

## Future empirical gate

Any later empirical revision must use a finalized producer commit and a newly
executed repaired protocol. Historical and debug outputs cannot be promoted.
At minimum, the revision needs fresh persistent theorem-facing diagnostics, the
registered one-factor bridge, and the interaction-matched UPI--TRM/PPO
comparison. Every run must retain exact interactions, seeds, split hashes,
checkpoint hashes, per-instance outputs, and the evaluated policy identity.
