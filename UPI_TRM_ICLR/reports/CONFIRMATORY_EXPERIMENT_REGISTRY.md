# Confirmatory experiment registry

Status: **REGISTERED, NOT AUTHORIZED, NO CONFIRMATORY RUN HAS STARTED**

The executable registry is
`CODE_REPO/configs/iclr_confirmatory/run_matrix.json`, SHA-256
`d2c064de22b6cb90a569f7b1000c2dd40087a40153a5070b0cdbd12ac0d22b81`.
Its status is `registered_not_authorized`. The bound producer is code commit
`e4c924cc721e9f4f356789eba03a09f6c8ca1913`. Changing a registered cell,
seed, budget, data manifest, schedule, architecture field, or configuration
layer requires a documented pre-outcome registry amendment and a new hash.

The current executable matrix contains six C1 bridge cells and two C2 matched
cells. C3 diagnostics, C4 projection experiments, and C5 second-domain work
are not executable cells in this matrix. They remain follow-on work and may
not be described as registered or completed experiments.

## Locked identities

| Field | Registered value |
| --- | --- |
| Producer code commit | `e4c924cc721e9f4f356789eba03a09f6c8ca1913` |
| Run-matrix SHA-256 | `d2c064de22b6cb90a569f7b1000c2dd40087a40153a5070b0cdbd12ac0d22b81` |
| Training manifest SHA-256 | `8def4f59387c1ab9466d043c40a7fdd3c7c670e2778b8d949295811ae7b6088a` |
| Validation manifest SHA-256 | `4644a3b1bb8b6e384896888154c9e56252368c1fc2f32962b089ade95a5bc1f2` |
| Held-out test manifest SHA-256 | `163a083a9f5744b7cc485663b269b89acc3103d9e1ec64c7e93f78e36fa79d40` |
| Dataset lock | `CODE_REPO/configs/iclr_confirmatory/dataset.json` |
| Runtime output | `$UPI_TRM_EVIDENCE_ROOT/iclr-confirmatory-v1` |
| Standalone environment-lock SHA-256 | `not verifiable from supplied evidence` |

Each prepared run lock records its complete effective configuration,
configuration-layer hashes, dataset-provenance hash, runtime fingerprint,
device, seed, cell, and run ID. Effective-configuration hashes differ by cell,
so there is no single configuration hash for the matrix.

## Common protocol

- Domain: hard 4 by 4 Sudoku with 6 to 8 empty cells.
- A training interaction is one call to a training environment's `step`
  method. Evaluation interactions are excluded from the 80,000-interaction
  training budget and reported separately.
- Training, validation, and held-out generator seeds are `26080301`,
  `26080302`, and `26080303`, respectively.
- The materialized splits contain 1,024 training, 256 validation, and 512
  held-out test records. Their canonical record hashes must be pairwise
  disjoint. Any overlap aborts execution.
- Confirmatory evaluation uses every held-out record once in fixed manifest
  order with no cycling. Debug evaluation uses the validation split only.
- Confirmatory seeds are `101,102,103,104,105,106,107,108,109,110`.
  Debug-only seeds are `9001,9002,9003`.
- Every confirmatory run uses exactly 80,000 training environment
  interactions. Reporting checkpoints are 10,000, 20,000, 40,000, and
  80,000 interactions.
- The common TRM dimensions are hidden size 64, two H cycles, two L cycles,
  one L layer, and puzzle-embedding dimension zero.
- Every cell sets `policy_epsilon=0`; no epsilon-random action overlay changes
  the registered deployment distributions.
- Initialization is random and paired by training seed. Loading a checkpoint
  is forbidden.
- The primary endpoint is held-out exact-checker success at 80,000
  interactions. There is no early stopping or best-checkpoint selection.
- Secondary endpoints include undiscounted shaped episode return, checker
  score, invalid-action rate, recurrent updates, logit and value evaluations,
  optimizer updates, wall time, and peak device memory.
- Per-seed summaries use the sample standard deviation. Paired method
  differences use a hierarchical bootstrap over seeds and held-out instances
  with 10,000 resamples and analysis seed `26080311`, plus an exact paired
  sign-flip test over the ten seed-level differences.
- Repeated test records are not treated as independent training seeds. All
  per-instance outcomes, counters, effective configurations, checkpoint
  hashes, and ordered record hashes must be retained.
- An infrastructure rerun keeps the original cell and seed and requires a
  documented diagnosis. Failed and null runs remain in the registry.

## C1: one-factor bridge

The registered question is whether one factor, or the predeclared latent by
deployment interaction, explains the historical persistent-versus-episodic
gap under corrected data, interaction counting, and clock-complete replay.

All six cells use the legacy training protocol, `K=1`, the same architecture,
optimizer, schedules, projection/clamping settings, data, seed, and budget.
`B0_I00` is the reference. It uses a persistent latent, historical EMA target,
historical batch-centered baseline, and stochastic evaluation of the deployed
parameter-interpolated actor. Clock-complete replay is retained. The invalid
plan-only replay implementation is not reintroduced.

| Cell | Configuration layers | Registered change from `B0_I00` |
| --- | --- | --- |
| `B0_I00` | `bridge_base.yaml`, `bridge_b0.yaml` | Reference |
| `Bz_I10` | reference plus `bridge_bz.yaml` | Persistent latent to episodic reset |
| `Bd_I01` | reference plus `bridge_bd.yaml` | Checkpoint evaluator samples the exact probability-space mixture of the retained pre-interpolation base/candidate pair |
| `Bt` | reference plus `bridge_bt.yaml` | Bootstrap network changes from the EMA target to the current evaluator |
| `Bb` | reference plus `bridge_bb.yaml` | Batch-centered baseline changes to exact action summation |
| `I11` | reference plus `bridge_i11.yaml` | Episodic reset and exact-mixture checkpoint evaluator |

Two interpretation constraints are part of the registration:

1. `Bd_I01` does not train with the direct exact mixture. Its training path is
   identical to `B0_I00`; only the record-local stochastic checkpoint
   evaluator changes. The estimand is therefore a paired evaluator/deployment
   contrast on the retained pre-interpolation policy pair.
2. Because `K=1` is fixed, `Bt` is specifically an EMA-target-versus-current-
   evaluator bootstrap contrast. It is not evidence about a general
   multistep target.

The four primary paired success contrasts at 80,000 interactions are
`Bz_I10-B0_I00`, `Bd_I01-B0_I00`, `Bt-B0_I00`, and `Bb-B0_I00`. Apply Holm
correction across these four tests. The secondary interaction is

```text
(I11 - Bz_I10) - (Bd_I01 - B0_I00).
```

Report all six cells, including failed, null, and negative runs. If no primary
contrast survives correction and the interaction is inconclusive, report
that the gap remains unexplained. `Bs_legacy` is explicitly non-executable.

## C2: interaction-matched UPI-TRM versus TRM+PPO

The registered question is whether the corrected UPI-TRM endpoint has higher
held-out success than the registered TRM+PPO endpoint after exactly 80,000
training interactions. The two cells use the same seeds, split manifests,
ordered test pool, checkpoints, interaction budget, and TRM dimensions.

| Cell | Training and evaluation semantics |
| --- | --- |
| `UPI_TRM` | `fixed_base_exact`; persistent latent; clock-complete replay; exact `K=1` target; exact action-summed baseline; one record-local stochastic rollout from the exact probability-space mixture |
| `TRM_PPO` | PPO with episodic latent reset and joint/full-backbone optimization; one deterministic greedy rollout per held-out record |

This is an interaction-matched comparison between complete deployed
algorithms. It is not a controlled objective-only contrast. Sharing the TRM
model class and dimensions does not imply trainable-parameter parity:
UPI-TRM uses a fixed recurrent base/current map under `fixed_base_exact`, while
PPO optimizes its full backbone. The latent semantics also differ, and the
registered evaluators compare a sampled exact mixture with a greedy PPO
policy. These predeclared differences limit causal attribution. Compute is
reported separately through recurrent updates, model evaluations, optimizer
steps, wall time, and memory.

The primary estimand is the paired per-seed held-out success difference at
80,000 interactions. Use the common hierarchical bootstrap and exact
seed-level sign-flip test. Curves indexed by environment interactions are
primary; compute-indexed and wall-time curves are secondary. Do not use an
unpaired Welch test. If the interval does not support a positive difference,
remove the performance-superiority claim and preserve the null or negative
result.

## Completed debug-only execution

All eight registered cells completed an 80-interaction pipeline smoke run with
seed `9001` and one evaluation over the 256-record validation split. These
runs test configuration locking, training, checkpointing, exact interaction
accounting, evaluation, and artifact publication. They are excluded from all
confirmatory estimates and cannot change this registry.

| Artifact | SHA-256 |
| --- | --- |
| `results/confirmatory_locks/debug_seed9001/index.json` | `3b130e9441561f6ade7ffeba19780933f9ce27f5331874117c8952db6e641a5e` |
| `artifacts/debug_smoke/seed9001/MANIFEST.json` | `056b98f4163aec9fede0d0b734006055b9f7b4bce2f21ee5edb8e107c73c63ca` |

The staged manifest binds eight per-cell effective-configuration hashes,
compute snapshots, metadata, per-instance rows, summaries, logs, and available
checkpoint hashes to the producer commit and run-matrix hash. Seeds `9002` and
`9003` have not been executed. No confirmatory outcome has been inspected
because confirmatory execution remains blocked by the matrix status.

## Follow-on work outside the executable matrix

### Persistent theorem-facing diagnostics

The intended diagnostics include augmented Bellman residuals, reconstructed
centering, exact-mixture deployment discrepancy, recurrent path length,
depth discrepancy, local ratios, value drift, initial-latent sensitivity,
carried-latent drift, clock strata, shared-map identity, projection-active
rate, and latent norms. Every result must be labeled `scope: finite_batch`.
The current eight-cell run matrix does not register or authorize a diagnostic
run, and no eligible 80,000-interaction endpoint exists. Result status:
`missing experiment`.

Without a retained training-time advantage-estimator artifact, the historical
training-time centering claim is exactly
`not verifiable from supplied evidence`.

### Projection train/evaluation cross-design

The proposed `R_train in {off,10}` by `R_eval in {off,10}` design is not in
the current run matrix. Its seeds, cells, and effective configurations must be
registered before execution. Result status: `missing experiment`.

### Second verifier-guided domain

The proposed domain remains 8-puzzle, selected for its exact verifier and
plan-edit structure. Its data counts, horizon, budget, cells, and immutable
manifests are not registered. Result status: `missing experiment`.

## Amendment and authorization rules

1. Confirmatory execution remains prohibited while the authoritative matrix
   status is `registered_not_authorized`.
2. A status change must be committed before the first confirmatory training
   action and must preserve the producer, dataset, cell, seed, budget, and
   analysis identities above unless a documented pre-outcome amendment changes
   them.
3. After authorization, amendments may correct infrastructure defects only.
   Record the old text, new text, reason, timestamp, and whether any outcome
   was inspected.
4. Debug results cannot alter seeds, budget, endpoint, evaluation pool,
   statistics, or failure rules.
5. No result enters the paper until its run-registry row and every expected
   raw artifact exist and reproduce.
