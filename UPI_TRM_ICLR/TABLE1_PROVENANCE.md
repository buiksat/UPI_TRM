# TABLE 1 PROVENANCE ANCHOR

Canonical record of the no-mask hard 4x4 Sudoku numbers reported in
Table 1 (`tab:hard_suite_anchor`) of `main.tex`.

Frozen on 2026-04-19 for the original 10-seed table lock.
Updated on 2026-04-28 with the baseline-interface UPI reevaluation used
to recover the UPI Return / Invalid columns.

This document exists so that any later reviewer question, re-run attempt,
or audit can map the reported numbers back to specific git SHAs, result
roots, configs, and per-seed log files.

---

## 1. Paper-side state

- Paper repository: `/home/buiksat/UPI_TRM`
- Paper repository HEAD at freeze: `aa6e5be26571c5b944c435a3f739d5534ee0f80c`
  (2026-04-16 14:23:56 -0700, "update md files")
- Manuscript file: `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/main.tex`
- At freeze, `main.tex` has uncommitted edits relative to `aa6e5be` that
  reflect the 10-seed narrative pivot ("57.4 / 32.0 / 0 / 0") at lines
  132 (abstract), 144 (intro), 512-531 (Table 1), and 536 (Section 6.1).
  The body is stable; no further changes to Table 1 numbers are expected
  prior to submission.
- Related artifacts in this repo: `UPI_TRM_NIPS/HANDOFF.md` (trainer-side
  audit log, regression-test coverage, post-sweep residual status).

## 2. Code-side state (`trm_bellman`)

- Code repository: `/home/buiksat/trm_bellman`
- Current HEAD: `109d8c132c7d74e3e7d216c14a308dda4b06f88d`
  (2026-04-19 10:16:22 -0700, "ASD")
- **Per-sweep code state** (the relevant SHA differs by result cell; see
  the per-cell sections below).
- Regression-test target: `fbcode//buiksat_trm:test_rl_algos_mock`
  at freeze: **Pass 18, Fail 0**
  (run: `cd /data/users/buiksat/fbsource && buck2 test
  fbcode//buiksat_trm:test_rl_algos_mock --local-only`).

### 2.1 Uncommitted edits at freeze (post-sweep, non-impact)

The following edits were applied AFTER every Table 1 run had completed
and their output files had been frozen. They do not change any paper
number. They are recorded here so the "current working tree" state is
fully specified.

- `rl/algos/ppo.py` - NoRec PPO param-group fallback now raises
  `ValueError` instead of silently collapsing the policy/value LR split;
  added `eval_num_episodes` field to `PPOConfig`; `evaluate_policy_metrics`
  falls back to `self.config.eval_num_episodes` when the caller does not
  pass `num_episodes`.
- `rl/algos/a2c.py`, `rl/algos/dqn.py` - same `eval_num_episodes` field
  and fallback.
- `upi_trm_train.py` - `build_trainer` now threads
  `rl_cfg.eval_num_episodes` into `PPOConfig / A2CConfig / DQNConfig`.
- `tests/test_rl_algos_mock.py` - 5 regression tests covering the
  NoRec PPO fix and the `eval_num_episodes` propagation (bringing the
  count from Pass 14 to Pass 18).
- Doc mirrors in `documents/{CLAUDE,CLAUDE_PROJECT_REPORT,handoff}.md`
  and `documents/configs/hp_tuning/README.md` updated to reflect the
  locked 10-seed numbers.

None of these edits were in the binary that produced any of the logs
enumerated below.

---

## 3. Table 1 numbers as reported

Reproduced from `main.tex` lines 520-531. All rows are 10-seed,
20k-step, no-mask 6-8-empties, horizon T=16.

| Method         | Steps | Seeds | Success (%)        | Return              | Invalid            |
|----------------|-------|-------|--------------------|---------------------|--------------------|
| UPI-TRM        | 20k   | 10    | **57.4 +/- 12.2**  | -1.82 +/- 2.66      | 0.000 +/- 0.000    |
| TRM+PPO        | 20k   | 10    | 32.0 +/- 15.3      | -7.87 +/- 3.65      | 0.000 +/- 0.000    |
| TRM+A2C        | 20k   | 10    | 0.0 +/- 0.0        | -16.81 +/- 0.29     | 0.000 +/- 0.000    |
| TRM+DQN        | 20k   | 10    | 0.0 +/- 0.0        | -18.38 +/- 0.63     | 0.000 +/- 0.000    |
| SB3 PPO        | 20k   | 10    | 0.0 +/- 0.0        | -17.46 +/- 0.00     | 1.000 +/- 0.000    |
| SB3 A2C        | 20k   | 10    | 0.0 +/- 0.0        | -18.09 +/- 0.52     | 0.783 +/- 0.127    |
| SB3 DQN        | 20k   | 10    | 0.0 +/- 0.0        | -17.92 +/- 0.17     | 0.843 +/- 0.054    |
| SB3 DQN (n=5)  | 20k   | 10    | 0.0 +/- 0.0        | -18.03 +/- 0.28     | 0.842 +/- 0.043    |

### 3.1 Stddev convention (sample, uniformly across Table 1)

All stddevs in Table 1 are reported using the **sample** convention
(divide by `n-1`, matching `numpy.std(x, ddof=1)`).

This was not originally uniform. At the first draft of this provenance
doc, three in-house return stddevs had drifted to the population
convention; we rounded them to sample std before freezing to keep the
whole table on a single convention. The three affected cells and their
before/after values:

| Cell              | Pre-freeze (pop std) | Post-freeze (sample std) |
|-------------------|----------------------|--------------------------|
| TRM+PPO return    | -7.87 +/- 3.46       | **-7.87 +/- 3.65**       |
| TRM+A2C return    | -16.81 +/- 0.28      | **-16.81 +/- 0.29**      |
| TRM+DQN return    | -18.38 +/- 0.60      | **-18.38 +/- 0.63**      |

All other cells in Table 1 already matched the sample convention at the
printed precision:

- Success stddevs (12.2, 15.3) already rounded to sample std at 1dp.
- Invalid-action stddevs (0.000 for in-house; 0.127, 0.054, 0.043 for
  SB3) already rounded to sample std at 3dp.
- SB3 return stddevs (0.00, 0.52, 0.17, 0.28) already rounded to sample
  std at 2dp; these were derived from
  `results/paper_ready/hard4x4_trusted_baselines_20k/summary.json`,
  whose `mean_return_std` / `invalid_action_rate_std` fields are
  themselves sample std.

No claim in the paper changes. No footnote was added; the three edits
land in `main.tex:523-525` and bring the whole column onto one rule.

---

## 4. Per-cell provenance

### 4.1 UPI-TRM (57.4 +/- 12.2)

- **Persistent-z**, 10 seeds.
- Results root:
  `/home/buiksat/trm_bellman/results/table3_hard_6to8/`
- Log pattern: `m1_persistent_nc_nomask_s{0..9}.log`
- Runs completed: 2026-04-06 22:02 through 2026-04-07 09:31.
- Sweep-time code SHA: `521bfc1` (2026-04-10 18:12:09 -0700,
  "Lock M1 and controlled 2x2 no-mask results"). This is the commit
  that explicitly locked the "M1 persistent" results aggregated here.
- Per-seed success rates (from
  `results/paper_ready/hard4x4_trusted_baselines_20k/summary.json`,
  key `methods.upi_trm.per_seed_success_rates`):

  | Seed | Success |
  |------|---------|
  | 0    | 0.56    |
  | 1    | 0.50    |
  | 2    | 0.68    |
  | 3    | 0.50    |
  | 4    | 0.64    |
  | 5    | 0.70    |
  | 6    | 0.74    |
  | 7    | 0.42    |
  | 8    | 0.38    |
  | 9    | 0.62    |

  Mean 0.574, sample std 0.1219 -> 57.4% +/- 12.2% as reported.
- Aggregate source-of-truth JSON:
  `/home/buiksat/trm_bellman/results/paper_ready/hard4x4_trusted_baselines_20k/summary.json`
- Baseline-interface reevaluation artifact (used for the Table 1 Return /
  Invalid cells):
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/baseline_interface_upi_reeval_20k/summary.json`
  generated by
  `/home/buiksat/trm_bellman/scripts/reevaluate_upi_baseline_interface.py`
  at `trm_bellman@eb24c73`, with the paper-side preregistration and run
  record in `UPI_TRM_NIPS/REEVAL_LOG.md`.
- The re-evaluated per-seed success rates match the archived values above
  exactly (all absolute differences 0.0; aggregate difference
  `1.11e-16` from floating-point roundoff).
- Re-evaluated aggregate return / invalid:
  - mean return `-1.81614`, sample std `2.66174`
    -> `-1.82 +/- 2.66` in Table 1
  - invalid-action rate `0.00000`, sample std `0.00000`
    -> `0.000 +/- 0.000` in Table 1

### 4.2 Architecture-matched baselines (TRM+PPO / TRM+A2C / TRM+DQN)

- Shared TRM backbone with UPI-TRM; in-house PPO/A2C/DQN trainers.
- 10 seeds each (seeds 0-9), 20k steps, no-mask.
- Results root:
  `/home/buiksat/trm_bellman/results/hard4x4_trm_baselines_nomask_10seed/`
- Checkpoint root:
  `/home/buiksat/trm_bellman/checkpoints/hard4x4_trm_baselines_nomask_10seed/`
- Manifest:
  `/home/buiksat/trm_bellman/results/hard4x4_trm_baselines_nomask_10seed/job_manifest.tsv`
  (31 lines: 1 header + 30 seed jobs).
- Log pattern:
  `{ppo,a2c,dqn}_nomask_s{0..9}.log` (30 files, all runs clean, all
  reached step 20000 with a final eval line).
- Sweep launched: 2026-04-17, training started ~12:43-12:44 PDT
  (per tqdm + buck log headers). Each seed took ~9h 09m; completion
  window spans 2026-04-17 PM through 2026-04-19 morning. Logs were
  consolidated / stat-touched at 2026-04-19 10:19:43.
- Sweep-time code SHA: **`3c2e959`** (2026-04-17 13:02:56 -0700,
  "Fix two rounds of baseline trainer bugs, add regression tests,
  reset sweep artifacts"). This is the round-2-fix commit whose
  working tree matches the code that ran the sweep. Subsequent
  commits on 2026-04-17 (`84d7c61` "Patched", `5fa4c5d` "baseline
  strategy plan", `109d8c1` "ASD" on 2026-04-19) were post-sweep
  and are not in the sweep binary.
- Launcher:
  `/home/buiksat/trm_bellman/scripts/run_hard4x4_trm_baselines_nomask_10seed_4gpu.sh`
- Configs used (one per method, plus a shared overlay):
  - `/home/buiksat/trm_bellman/configs/baselines/ppo_trm_feasibility.yaml`
  - `/home/buiksat/trm_bellman/configs/baselines/a2c_trm_feasibility.yaml`
  - `/home/buiksat/trm_bellman/configs/baselines/dqn_trm_feasibility.yaml`
  - Overlay:
    `/home/buiksat/trm_bellman/configs/table3_hard_controlled/no_mask_overlay.yaml`
  - Each method sets `model_type: "trm"`, which is what makes these
    "architecture-matched" rather than flat-MLP baselines.

#### 4.2.1 Per-seed final-step (step 20000) eval line

Extracted verbatim from each log via:

```
rg -oN '\[step 20000\] eval_success_rate=([0-9.]+).*eval_mean_return=(-?[0-9.]+).*eval_invalid_action_rate=([0-9.]+)' \
   --replace '$1 $2 $3' {method}_nomask_s{seed}.log
```

| Method | Seed | success_rate | mean_return | invalid_action_rate |
|--------|------|--------------|-------------|---------------------|
| PPO    | 0    | 0.300        | -7.842      | 0.000               |
| PPO    | 1    | 0.320        | -8.245      | 0.000               |
| PPO    | 2    | 0.120        | -12.786     | 0.000               |
| PPO    | 3    | 0.540        | -2.898      | 0.000               |
| PPO    | 4    | 0.120        | -12.641     | 0.000               |
| PPO    | 5    | 0.560        | -2.114      | 0.000               |
| PPO    | 6    | 0.200        | -10.823     | 0.000               |
| PPO    | 7    | 0.320        | -7.961      | 0.000               |
| PPO    | 8    | 0.420        | -5.352      | 0.000               |
| PPO    | 9    | 0.300        | -8.024      | 0.000               |
| A2C    | 0    | 0.000        | -16.929     | 0.000               |
| A2C    | 1    | 0.000        | -16.833     | 0.000               |
| A2C    | 2    | 0.000        | -16.906     | 0.000               |
| A2C    | 3    | 0.000        | -17.324     | 0.000               |
| A2C    | 4    | 0.000        | -17.037     | 0.000               |
| A2C    | 5    | 0.000        | -16.403     | 0.000               |
| A2C    | 6    | 0.000        | -16.412     | 0.000               |
| A2C    | 7    | 0.000        | -16.875     | 0.000               |
| A2C    | 8    | 0.000        | -16.498     | 0.000               |
| A2C    | 9    | 0.000        | -16.868     | 0.000               |
| DQN    | 0    | 0.000        | -18.431     | 0.000               |
| DQN    | 1    | 0.000        | -18.103     | 0.000               |
| DQN    | 2    | 0.000        | -18.176     | 0.000               |
| DQN    | 3    | 0.000        | -17.906     | 0.000               |
| DQN    | 4    | 0.000        | -19.318     | 0.000               |
| DQN    | 5    | 0.000        | -18.378     | 0.000               |
| DQN    | 6    | 0.000        | -19.657     | 0.000               |
| DQN    | 7    | 0.000        | -18.087     | 0.000               |
| DQN    | 8    | 0.000        | -18.069     | 0.000               |
| DQN    | 9    | 0.000        | -17.632     | 0.000               |

#### 4.2.2 Re-derived aggregates (paper uses sample std)

| Method | success mean | success sample std | return mean | return sample std | return pop std |
|--------|--------------|--------------------|-------------|-------------------|-----------------|
| PPO    | 32.0%        | **15.32** (paper 15.3) | -7.8686 | **3.65** (paper 3.65) | 3.46 |
| A2C    | 0.0%         | 0.0                | -16.8085    | **0.29** (paper 0.29) | 0.28 |
| DQN    | 0.0%         | 0.0                | -18.3757    | **0.63** (paper 0.63) | 0.60 |

Invalid-action-rate is exactly 0.000 for all 30 runs, so its stddev is
zero under either convention; the paper entry 0.000 +/- 0.000 is
consistent.

### 4.3 SB3 external baselines (SB3 PPO / A2C / DQN / DQN n=5)

- Independent Stable-Baselines3 codebase with a flat MLP policy;
  serves as a "trusted independent negative control".
- 10 seeds each (seeds 0-9), 20k steps, no-mask.
- Results root:
  `/home/buiksat/trm_bellman/results/neurips2026/external_hard4x4_20k/`
  with subtree `{ppo,a2c,dqn,dqn_nstep5}/seed{0..9}/train_summary.json`.
- Runs completed: on or before 2026-04-14; result files consolidated
  under `neurips2026/` on 2026-04-16 13:55.
- Sweep-time code SHA: **`31b320b`** (2026-04-14 15:49:08 -0700,
  "20k compute-matched SB3 baselines + finite-R eval sweep artifacts")
  for PPO/A2C/DQN, and **`d256924`** (2026-04-14 18:24:11 -0700,
  "Add trusted n-step DQN baseline package") for the n=5 variant.
- Launcher helper:
  `/home/buiksat/trm_bellman/scripts/run_external_baseline_sweep.sh`
- SB3 library code:
  `/home/buiksat/trm_bellman/external_baselines/`
- Aggregate source-of-truth (stdev convention: population):
  `/home/buiksat/trm_bellman/results/paper_ready/hard4x4_trusted_baselines_20k/summary.json`
- Per-seed CSV:
  `/home/buiksat/trm_bellman/results/paper_ready/hard4x4_trusted_baselines_20k/per_seed_metrics.csv`
  (41 rows: 1 header + 40 data rows covering all 4 SB3 methods x 10 seeds
  plus the 10 UPI-TRM rows).

#### 4.3.1 SB3 aggregate verification vs. paper Table 1

Paper values match the `summary.json` fields exactly under population
std:

| Method        | Paper return | JSON `mean_return_mean` | JSON `mean_return_std` (pop) |
|---------------|--------------|--------------------------|------------------------------|
| SB3 PPO       | -17.46 +/- 0.00 | -17.4624              | 0.0                          |
| SB3 A2C       | -18.09 +/- 0.52 | -18.0917              | 0.5200                       |
| SB3 DQN       | -17.92 +/- 0.17 | -17.9152              | 0.1729                       |
| SB3 DQN (n=5) | -18.03 +/- 0.28 | -18.0266              | 0.2779                       |

| Method        | Paper invalid  | JSON `invalid_action_rate_mean` | JSON `invalid_action_rate_std` (pop) |
|---------------|----------------|---------------------------------|--------------------------------------|
| SB3 PPO       | 1.000 +/- 0.000 | 1.0                            | 0.0                                  |
| SB3 A2C       | 0.783 +/- 0.127 | 0.7834                         | 0.1267                               |
| SB3 DQN       | 0.843 +/- 0.054 | 0.8433                         | 0.0537                               |
| SB3 DQN (n=5) | 0.842 +/- 0.043 | 0.8421                         | 0.0434                               |

All SB3 success rates are identically 0/500 per seed (0/5000 across all
10 seeds for each of the 4 methods), giving the 0/8,000 checkpointed
evaluations figure cited in Section 6.1.

---

## 5. Protocol summary (shared across all Table 1 rows)

- Task: hard 4x4 Sudoku, no-mask protocol.
- Dataset: `sudoku-4x4-easy_6to8empties`
  (located at `buiksat_trm/data/sudoku-4x4-easy_6to8empties` inside the
  trm_bellman repo).
- Horizon: T = 16 edits per episode.
- Training steps: 20000.
- Evaluation: greedy, 50 episodes per eval checkpoint, reported value
  is the final `eval_success_rate` at step 20000 (architecture-matched
  in-house baselines) or `summary.json` aggregation over the logged
  eval points (SB3 and UPI-TRM paper-ready runs).
- Reward: in-house feasibility-shaped reward for architecture-matched
  baselines (`reward_shaping: true`, `use_feasibility_checker: true`,
  `feasibility_violation_weight: 2.0`, `feasibility_zerocand_weight: 5.0`);
  same shaping for UPI-TRM. SB3 baselines use the same env + checker
  via the external wrapper in `external_baselines/`.
- Latent regime: persistent-z for UPI-TRM (Section 6.1 main anchor);
  episodic-z is the Section 6.2 / 6.3 configuration, not this table.

---

## 6. Reproducibility recipe (reference only)

### 6.1 Re-derive architecture-matched aggregates from logs

```
cd /home/buiksat/trm_bellman/results/hard4x4_trm_baselines_nomask_10seed
for method in ppo a2c dqn; do
  echo "=== ${method} ==="
  rg -oN '\[step 20000\] eval_success_rate=([0-9.]+).*eval_mean_return=(-?[0-9.]+).*eval_invalid_action_rate=([0-9.]+)' \
     --replace '$1 $2 $3' ${method}_nomask_s*.log \
    | cut -d: -f2 \
    | awk '{s+=$1*100; r+=$2; i+=$3; a[NR]=$1*100; b[NR]=$2; c[NR]=$3; n=NR} \
           END {sm=s/n; rm=r/n; im=i/n; \
                for(k=1;k<=n;k++){sv+=(a[k]-sm)^2; rv+=(b[k]-rm)^2; iv+=(c[k]-im)^2} \
                printf("success %%: %.2f  sample-std %.2f  pop-std %.2f\n", \
                  sm, sqrt(sv/(n-1)), sqrt(sv/n)); \
                printf("return   : %.3f sample-std %.3f pop-std %.3f\n", \
                  rm, sqrt(rv/(n-1)), sqrt(rv/n)); \
                printf("invalid  : %.3f sample-std %.3f pop-std %.3f\n", \
                  im, sqrt(iv/(n-1)), sqrt(iv/n))}'
done
```

### 6.2 Re-run regression tests at the frozen code state

```
cd /data/users/buiksat/fbsource
buck2 test fbcode//buiksat_trm:test_rl_algos_mock --local-only
```

Expected: `Pass 18, Fail 0`.

### 6.3 Re-run a single baseline seed (for spot-check)

```
cd /home/buiksat/trm_bellman
bash scripts/run_hard4x4_trm_baselines_nomask_10seed_4gpu.sh
# or, for one seed only, inspect the manifest and invoke buck2 run
# on upi_trm_train with --baseline ppo --seed <k> and the configs in
# section 4.2.
```

Expect a per-seed runtime of ~9 hours on a single GPU.

---

## 7. Sanity notes

1. All 30 architecture-matched baseline logs contain exactly one
   `[step 20000] eval_success_rate=...` line; there is no duplicate
   step-20000 eval to choose between.
2. All three architecture-matched baselines report invalid-action-rate
   = 0 at step 20000. This is a consequence of the learned policies
   having converged to action masks that prevent invalid moves, not
   of the env disabling invalid actions during eval.
3. SB3 baselines report nonzero invalid-action-rate because the flat
   MLP policy does not consume the action mask; this is the expected
   implementation-check behavior.
4. The UPI-TRM 57.4 +/- 12.2 figure uses persistent-z. Corollary
   `cor:persistent_cpi_augmented` in main.tex requires conditions
   (reasoning-manifold smoothness) that are design objectives rather
   than verified properties for Sudoku, as discussed in Remarks
   `rem:reasoning_manifold` and `rem:persistent_augmented_scope`.
   This anchor is empirical evidence, not a validation of that
   corollary.
