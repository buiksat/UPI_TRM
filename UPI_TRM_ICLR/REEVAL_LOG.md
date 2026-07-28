# Baseline-interface UPI re-evaluation log

## Goal
Re-evaluate the existing 10-seed UPI-TRM persistent-z hard-suite checkpoints through the same evaluation interface used for TRM+PPO/A2C/DQN, so Table 1 can report UPI Return and Invalid columns alongside success.

## Inputs (fill before running)
- Checkpoint paths: `/home/buiksat/trm_bellman/checkpoints/m1_nomask_persistent_nc_seed{0..9}/rl_checkpoint_step_20000.pt`
- Seeds: `0,1,2,3,4,5,6,7,8,9`
- Evaluator script: `/home/buiksat/trm_bellman/scripts/reevaluate_upi_baseline_interface.py`
  (Buck target `fbcode//buiksat_trm:reevaluate_upi_baseline_interface`)
- Eval interface revision/commit: `trm_bellman@eb24c73`
- Suite: no-mask hard 4x4 Sudoku, 6-8 empties, T=16
- Metrics:
  - Success rate (fraction of episodes producing a feasible solution within T=16)
  - Episode return (sum of shaped reward over the episode, no discount in reporting; matches baseline-interface convention)
  - Invalid-action rate (fraction of steps where the policy's emitted action was outside the per-state valid set)

## Output
- Per-seed CSV: `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/baseline_interface_upi_reeval_20k/per_seed_metrics.csv`
- Aggregate JSON (mean +/- std across seeds): `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/baseline_interface_upi_reeval_20k/summary.json`

## Locked before run
- Diagnostic batch: not applicable; eval set is the original hard-suite test split, identical to the one used for the architecture-matched baseline rows in Table 1.
- No checkpoint cherry-picking: all 10 final checkpoints (step 20k) are evaluated.
- Discrepancy gate: stop and report if any per-seed success differs from the original per-seed success by more than 5 percentage points, or if aggregate success differs from 57.4 by more than 2 percentage points. If only aggregate original success is available, apply only the aggregate gate.
- Evaluator script and eval interface commit are fixed at protocol commit time; if the evaluator is modified after this commit, the modification commit hash is recorded below and the rerun is treated as a new measurement, not a fix.

## Run record (fill after running)
- Date: `2026-04-28`
- Command: `/usr/bin/time -f 'WALL_TIME_SECONDS=%e' buck2 run --local-only fbcode//buiksat_trm:reevaluate_upi_baseline_interface -- --checkpoint-glob '/home/buiksat/trm_bellman/checkpoints/m1_nomask_persistent_nc_seed*/rl_checkpoint_step_20000.pt' --expected-seeds 0 1 2 3 4 5 6 7 8 9 --config-yaml /home/buiksat/trm_bellman/configs/ablations/upi_trm_feasibility_persistent_z_no_contraction_no_mask.yaml --dataset-paths /home/buiksat/trm_bellman/data/sudoku-4x4-easy_6to8empties --output-dir /home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/baseline_interface_upi_reeval_20k --device cpu`
- Wall time: `61.74` seconds
- Anomalies: CUDA execution on this machine failed with `cudaErrorInvalidKernelImage` during the smoke run, so the full reevaluation was executed on CPU. No seed-level eval failures, NaNs, or OOMs occurred. All 10 re-evaluated per-seed success rates exactly matched the archived Table 1 provenance (`0.56, 0.50, 0.68, 0.50, 0.64, 0.70, 0.74, 0.42, 0.38, 0.62`); aggregate success matched `0.574` exactly, so the discrepancy gate passed.
- Resulting per-seed CSV path: `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/baseline_interface_upi_reeval_20k/per_seed_metrics.csv`
- Resulting aggregate JSON path: `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/baseline_interface_upi_reeval_20k/summary.json`

## Decision rule for Table 1 update
- If the discrepancy gate fails, stop and report. Do not update Table 1, do not start the episodic-z rerun, and do not modify `EXPERIMENTS_PROTOCOL.md`.
- If the discrepancy gate passes, update Table 1 to populate the UPI Return and Invalid columns from this re-evaluation while keeping the existing success value unless the paper workflow explicitly switches to the re-evaluated success column.
- If SB3 rows remain invalid-heavy, keep them out of the headline table or describe them as failed external implementation checks rather than capability baselines.
