# Historical Provenance Audit

## Scope and path conventions

This audit covers the current paper and implementation repositories without
modifying either source tree. It does not inspect the protected legacy paper
repository.

- `PAPER_REPO/` denotes the root of the current ICLR paper source.
- `CODE_REPO/` denotes the root of the implementation repository.

The classifications below distinguish an arithmetically auditable retained
record from an experiment that can be rerun. A historical aggregate is not a
valid method comparison merely because its mean can be recomputed.

## Executive finding

The finite-MDP calculation is the only retained result that is reproducible as
a numeric unit test from the supplied source and data. The learned-model runs
are not reproducible end to end. Neither repository contains a UPI checkpoint,
and the hard 4x4 dataset used by the learned runs is absent. The successful
persistent checkpoints therefore cannot be used for the requested augmented
residual, centering, deployment-gap, or slow-drift diagnostics.

A scan of JSON provenance in both repositories found 76 unique path strings
that name a checkpoint, evaluation batch, NPZ artifact, or dataset. After
resolving relative paths against `CODE_REPO/`, 74 of the 76 path strings did
not resolve to an existing artifact. This count is over unique recorded path
strings, so absolute and relative spellings of one logical target remain
distinct.

## Classification summary

| Record | Classification | What is retained | What is missing or invalid |
| --- | --- | --- | --- |
| Finite-MDP theorem-pipeline calculation | Fully reproducible numeric unit test, with environment-packaging gaps | Generator, 101-row CSV, stdout, plot data, generated tables and figures, and replot script | Exact saved invocation and a lock for external plotting tools |
| Episodic-z hard-suite endpoint | Partially reconstructible | 40 evaluation rows, 40 diagnostic aggregate rows, 10-seed summary, config, launcher, and postprocessor | Checkpoints, raw training logs, hard dataset, closure batch, fixed directions, per-state diagnostics, validation summary, ordered-pool hashes, and pinned run-code commit |
| Persistent UPI-TRM 57.4% record | Historical record only | Ten complete training logs, config, ten seed-level aggregate outcomes, and sanitized reevaluation summary | Checkpoints, historical dataset, ordered evaluation pool, per-instance outcomes, exact training binary commit, and theorem-facing diagnostics |
| Architecture-matched PPO/A2C/DQN records | Historical record only | Thirty complete per-seed logs, configs, and job manifest | Checkpoints, historical dataset, ordered-pool hashes, per-instance outcomes, and matched environment-interaction counts |
| Projection x clamping factorial | Partially reconstructible arithmetic; historical record only as scientific evidence | Forty per-seed logs, four configs, launcher, and parser | Checkpoints, historical dataset, ordered-pool hashes, per-instance outcomes, and original statistical-test script |
| External SB3 baselines | Partially reconstructible | Forty run configs, forty summaries, forty evaluation histories, and training logs | Every referenced final model, the dataset, ordered-pool hashes, per-instance outcomes, and a valid common-pool comparison |
| Equal-environment-interaction attempt | Incomplete; irrecoverable as a completed comparison | Partial PPO/A2C/DQN logs | UPI-TRM cell and several baseline completions; no valid comparison exists |
| Legacy appendix diagnostic sweeps | Partially reconstructible summaries only | Per-state CSV/JSON outputs and paper-ready aggregates | Referenced checkpoints and raw evaluation batches |
| Second-domain work | Infrastructure only; missing experiment | ARC builder/evaluator, exact-pixel ARC task config, maze builder, and raw ARC inputs | Built release dataset, UPI training run, matched baseline, checkpoints, registry entry, and empirical result |

## 1. Finite-MDP theorem-pipeline unit test

Retained files:

- `PAPER_REPO/experiments/finite_mdp_certificate.py`
- `PAPER_REPO/results/finite_mdp_certificate_validation/finite_mdp_summary.csv`
- `PAPER_REPO/reports/finite_mdp_certificate_validation.log`
- `PAPER_REPO/results/finite_mdp_certificate_validation/fig_value_decomposition.dat`
- `PAPER_REPO/results/finite_mdp_certificate_validation/fig_cpi_certificate.dat`
- `PAPER_REPO/scripts/replot_finite_mdp_certificate.py`

The CSV has 101 data rows: 80 value-curve rows and 21 CPI-curve rows.
`certificate_holds_decomp` and `certificate_holds_exact_A` equal one in all
101 rows. The generator uses a fixed default seed and exact finite-state
calculations. This is a reproducible theorem-pipeline unit test, not empirical
validation of a learned recurrent model.

The original exact command and versions of external plotting tools are not
recorded. Reproduction of the numeric CSV is supported; bit-for-bit recreation
of every rendered figure is not verifiable from supplied evidence.

## 2. Episodic-z hard-suite endpoint

Retained files:

- `PAPER_REPO/results/episodic_z_hard_suite_20k_seed41_50/per_seed_eval.jsonl`
- `PAPER_REPO/results/episodic_z_hard_suite_20k_seed41_50/per_seed_diagnostics.jsonl`
- `PAPER_REPO/results/episodic_z_hard_suite_20k_seed41_50/summary.json`
- `PAPER_REPO/results/episodic_z_hard_suite_20k_seed41_50/diagnostics_summary.json`
- `PAPER_REPO/results/episodic_z_hard_suite_20k_seed41_50/cpi_penalty_grid.json`
- `PAPER_REPO/results/episodic_z_hard_suite_20k_seed41_50/job_manifest.tsv`
- `CODE_REPO/configs/revision/upi_trm_feasibility_episodic_z_hard_suite_theory_exact.yaml`
- `CODE_REPO/scripts/run_episodic_z_hard_suite_10seed_2gpu.sh`
- `CODE_REPO/scripts/episodic_z_hard_suite_diagnostics.py`

The retained streams contain four checkpoints for each of seeds 41 through 50.
The final aggregate is 0% success across all ten seeds. The retained values are
auditable as aggregate records.

The following named run inputs are absent:

- every training checkpoint;
- every raw per-seed training log;
- the hard 4x4 dataset;
- `closure_batch_seed1729.npz`;
- `lv_directions_seed1729_eps1e-4.npz`;
- per-state diagnostic JSON files;
- the finite-MDP `validation_summary.json` named by the run log.

The run record also does not pin the implementation commit. Commits related to
the launcher and diagnostics landed around the run window, so one current
source snapshot cannot be assigned to all stages from the retained metadata.
The identity of the exact code used for each stage is not verifiable from
supplied evidence.

The closure batch was drawn from the training split after the test split proved
too small. A dedicated random generator prevents shared RNG state, but does not
make a training-split sample held out from training data. Claims that this is a
disjoint held-out dataset are not verifiable from supplied evidence.

The endpoint evaluator recorded the old-policy component rather than proving
that it evaluated the configured exact probability-space mixture. Performance
of the configured mixture is not verifiable from supplied evidence.

## 3. Persistent 57.4% historical record

Retained files:

- `CODE_REPO/results/table3_hard_6to8/m1_persistent_nc_nomask_s0.log` through
  `m1_persistent_nc_nomask_s9.log`
- `CODE_REPO/configs/ablations/upi_trm_feasibility_persistent_z_no_contraction_no_mask.yaml`
- `PAPER_REPO/results/persistent_upi_20k/per_seed_eval.csv`
- `PAPER_REPO/results/persistent_upi_20k/summary.json`
- `PAPER_REPO/TABLE1_PROVENANCE.md`
- `PAPER_REPO/REEVAL_LOG.md`

All ten logs reach nominal step 20,000 and reproduce the seed-level success
rates `0.56, 0.50, 0.68, 0.50, 0.64, 0.70, 0.74, 0.42, 0.38, 0.62`.
Their mean is 0.574 and their sample standard deviation is approximately
0.121856.

The training log reports 32 records. The historical evaluation ran 50 episodes
by cycling those 32 records, and those records came from the training split
used during training. The reevaluation driver explicitly preserves this
historical `50-on-32` behavior. The 57.4% record is therefore in-sample and is
not evidence of held-out generalization.

The historical configuration also reports:

- persistent latent state;
- exact K-step targets disabled;
- exact baseline summation disabled;
- exact probability-space mixture disabled;
- parameter-space interpolation used for deployment;
- contraction enforcement disabled.

The sanitized summary records `eb24c73` as `training_repo_git_sha`, but that
commit adds the baseline-interface reevaluation driver and postdates the
training runs. The provenance document instead cites `521bfc1`, a later commit
whose subject locks the M1 and factorial results. The logs were first retained
in another later commit. No training log embeds the producing Git SHA. The
exact training binary commit is unresolved and is not verifiable from supplied
evidence.

No persistent checkpoint remains in either repository or the released code
archive. Consequently, augmented Bellman residuals, exact augmented-state
centering, exact-mixture versus deployed-policy discrepancy, recurrent path
length, latent drift, initialization sensitivity, and remaining-budget
dependence for the successful checkpoints are not verifiable from supplied
evidence.

## 4. Architecture-matched historical baselines

Retained files:

- `CODE_REPO/results/hard4x4_trm_baselines_nomask_10seed/`
- `CODE_REPO/configs/baselines/ppo_trm_feasibility.yaml`
- `CODE_REPO/configs/baselines/a2c_trm_feasibility.yaml`
- `CODE_REPO/configs/baselines/dqn_trm_feasibility.yaml`
- `CODE_REPO/configs/table3_hard_controlled/no_mask_overlay.yaml`
- `CODE_REPO/scripts/run_hard4x4_trm_baselines_nomask_10seed_4gpu.sh`

There are 30 per-seed logs and all 30 contain a final step-20,000 evaluation
line. The PPO seed-level values and the zero-success A2C/DQN values can be
recomputed from these logs. The claim that the per-seed architecture-matched
artifact is unavailable is true of the paper-only bundle, but false when the
implementation repository is part of the supplied evidence.

These records still do not form a valid comparison with persistent UPI-TRM.
The persistent logs report 32 loaded records, whereas the architecture-matched
PPO log reports 256 loaded records under the same legacy dataset name. No
historical content hashes establish corpus identity. No ordered evaluation-pool
hash exists, and the nominal outer-step units imply different environment
interaction counts. Comparative performance is not verifiable from supplied
evidence.

## 5. Projection x clamping factorial

Retained files:

- `CODE_REPO/results/table3_hard_6to8_controlled_nomask/`
- `CODE_REPO/configs/table3_hard_controlled/episodic_nc_r0_hard.yaml`
- `CODE_REPO/configs/table3_hard_controlled/episodic_c_r0_hard.yaml`
- `CODE_REPO/configs/table3_hard_controlled/episodic_nc_r10_hard.yaml`
- `CODE_REPO/configs/table3_hard_controlled/episodic_c_r10_hard.yaml`
- `CODE_REPO/scripts/run_table3_hard_controlled_nomask_4gpu.sh`
- `CODE_REPO/scripts/plot_table3_hard_controlled.py`

All 40 per-seed logs exist and contain one final step-20,000 evaluation. Direct
parsing reproduces these cells as mean plus or minus sample standard deviation:

| Clamping condition | Projection | Success |
| --- | --- | ---: |
| disabled | off | 35.0% +/- 8.86% |
| enabled | off | 37.4% +/- 7.78% |
| disabled | on | 48.2% +/- 7.15% |
| enabled | on | 50.2% +/- 10.48% |

These cells reproduce the reported +13.0 percentage-point projection contrast
and +2.2 percentage-point clamping-enabled contrast. The per-seed artifact is
available in `CODE_REPO/`, even though it is absent from the paper-only bundle.

The original script producing the source-reported `p approximately 0.6` is not
present. The exact test definition and source p-value are not verifiable from
supplied evidence. The dataset, checkpoints, ordered evaluation pool, and
per-instance outcomes are also absent. The arithmetic is auditable, but the
factorial remains a historical, in-sample record rather than confirmatory
evidence.

## 6. External SB3 records

`CODE_REPO/results/neurips2026/external_hard4x4_20k/` retains ten seeds for each
of PPO, A2C, DQN, and five-step DQN. Each seed directory includes a run config,
training summary, evaluation history, and log. The 40 summaries reference final
model files, but none of those model files is present. The hard dataset is also
absent, and the records contain split names rather than ordered-pool hashes.

The zero-success arithmetic is reconstructible from the retained JSON. Model
reevaluation, pool identity, and comparison against the UPI records are not
verifiable from supplied evidence.

## 7. Equal-environment-interaction attempt

`CODE_REPO/results/hard4x4_trm_baselines_nomask_envbudget_10seed_20260424/`
contains an incomplete baseline-only sweep:

- PPO: nine of ten seeds complete;
- A2C: eight complete seeds and one partial seed;
- DQN: nine complete seeds and one partial seed;
- five-step DQN: eight complete seeds and two partial seeds.

The launcher queue still lists the missing PPO and A2C seeds. There is no
matched UPI-TRM cell. An interaction-matched UPI-TRM versus PPO result is a
missing experiment and is not verifiable from supplied evidence.

## 8. Legacy appendix diagnostics

`CODE_REPO/results/validation/` and `CODE_REPO/results/paper_ready/` retain many
per-state CSV/JSON outputs and aggregates. For example, the finite-radius
metadata names seed-specific checkpoints under
`CODE_REPO/checkpoints/exp1_v4_refreeze/`, and the evaluation-batch metadata
names `b0.pt` and `b1.pt` files. The checkpoint directory and raw batch files
are absent. `CODE_REPO/artifacts/eval_batches/` contains metadata JSON only.

The retained tables can be recalculated from the retained CSV/JSON, but the
underlying model evaluations cannot be rerun. Any claim requiring checkpoint
identity, raw batch identity, or fresh evaluation is not verifiable from
supplied evidence.

## 9. Dataset status

Only the small `CODE_REPO/data/sudoku-4x4-trivial/` dataset is retained. The
historical hard dataset and legacy ultra-easy path are absent. A restoration
script can generate new 4x4 datasets from a fixed seed, but its own provenance
note states that this is distribution-level regeneration and does not prove
byte identity with the historical corpora. Historical train/test membership
and content identity are therefore not verifiable from supplied evidence.

## 10. Second-domain status

The repository contains partial infrastructure:

- `CODE_REPO/dataset/build_arc_dataset.py`;
- `CODE_REPO/evaluators/arc.py`;
- an exact-pixel `ARCTaskConfig` in `CODE_REPO/rl/task_config.py`;
- `CODE_REPO/dataset/build_maze_dataset.py`;
- raw ARC JSON inputs and a pretraining config.

The task-config factory supports Sudoku, ARC, and a dummy task, but not maze.
No built ARC or maze release dataset, UPI policy-improvement configuration,
matched PPO configuration, checkpoint, run registry entry, or result is
retained. The 9x9 logs remain Sudoku and do not establish a second domain.
Transfer beyond Sudoku is not verifiable from supplied evidence.

## Required interpretation

The retained learned-model artifacts support arithmetic reconstruction and
historical implementation forensics. They do not support a held-out performance
claim, an interaction-matched comparison, or theorem-facing diagnostics on the
successful persistent checkpoints. Until checkpoints and byte-identified data
are recovered, the 57.4% result, factorial, and legacy baselines must remain
historical records. New confirmatory claims require fresh runs under an
immutable held-out pool, exact interaction counters, complete checkpoint and
dataset hashes, and a committed run registry.
