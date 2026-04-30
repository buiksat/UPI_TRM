# 9x9 POST-AUDIT PPO PROVENANCE

Record of the post-audit TRM+PPO rerun on 9x9 Sudoku. This is an
**exploratory/appendix-only** artifact; it does not anchor any main-text
table. It exists to replace the pre-audit PPO/A2C/DQN comparisons in
`trm_bellman/documents/results/9x9_experiments_seed0/EXPERIMENT_REPORT.md`
with numbers produced under current, post-audit baseline trainer code.

Status: **complete / consolidated (2026-04-21)**.

---

## 1. Motivation

- Pre-audit 9x9 comparison (Feb 2026) reported PPO/A2C/DQN all at 0.0%
  success on 9x9 at 50k steps, vs UPI-TRM 4.0 +/- 4.0% (3 seeds). The
  Feb 2026 report makes a "UPI-TRM is the only method that solves any
  9x9 Sudoku" claim.
- On 4x4 the same trainer code bugs caused TRM+PPO to appear to collapse
  (0% reported in early draft tables) but the post-audit rerun moved
  TRM+PPO to 32.0 +/- 15.3% at 20k steps. A2C/DQN stayed at 0%.
- Question for this rerun: **does PPO on 9x9 at 50k steps also benefit
  from the trainer fixes, and if so, how does it change the 9x9 claim?**
- A2C and DQN are NOT re-run here: they were 0% both pre- and post-fix
  on 4x4, and the Feb 2026 9x9 scores (A2C 31.9 mean, DQN 29.5 mean)
  showed no learning trend, so the expected 9x9 post-fix result is
  still 0% for them. If PPO changes materially at 9x9, we can revisit.

## 2. Code-side state

- Repository: `/home/buiksat/trm_bellman`
- Sweep-time branch: `feature/upi-trm-clean`
- Sweep-time commit: `0a96c712fb00da041047d979f332cc8c21158ad3`
  (2026-04-19 "Add 9x9 TRM+PPO post-audit launcher (3 seeds, 50k steps)").
  This commit adds ONLY the launcher script
  `scripts/run_9x9_trm_ppo_post_audit_3seed.sh`; the trainer code is
  byte-identical to its parent
  `1ab1434c97b43e88b3d71c9a8ee803f82045b9ee` ("Post-audit trainer
  hygiene: fail-fast NoRec PPO, config-driven eval_num_episodes").
- Regression-test state at launch:
  `fbcode//buiksat_trm:test_rl_algos_mock` passes 18/18.
- Fixes incorporated (all already landed; none specific to 9x9):
  - Round 1: PPO clipped-objective broadcast bug, DQN puzzle_emb_len
    flatten bug, DQN batch next-mask bug, A2C shape cleanup.
  - Round 2: DQN NoRec dispatch, DQN epsilon-schedule env-step units,
    eval env task_config propagation, baseline imitation-pretrain guard.
  - Post-audit hygiene: NoRec PPO fail-fast, config-driven
    eval_num_episodes across baselines.

## 3. Dataset

- Path: `/home/buiksat/trm_bellman/data/sudoku-9x9/`
- Regeneration command (deterministic, seed 42, sizes matching the Feb
  2026 protocol):

  ```
  cd /data/users/buiksat/fbsource
  buck2 run fbcode//buiksat_trm:gen_sudoku9x9 --local-only -- \
      --output-dir /home/buiksat/trm_bellman/data/sudoku-9x9 \
      --num-train 1000 --num-val 100 --num-test 100 --seed 42
  ```

- Splits:
  - train: 1000 puzzles (300 easy / 400 medium / 300 hard)
  - val:   100 puzzles (30 / 40 / 30)
  - test:  100 puzzles (30 / 40 / 30)
- Difficulty bands (from the generator):
  - easy:   30-35 given clues
  - medium: 24-29 given clues
  - hard:   17-23 given clues
- Action space: `81 * 10 + 1 = 811` actions (81 positions x {PAD,
  empty, digits 1-9}, plus one STOP action).

**Caveat on dataset identity:** Feb 2026's dataset is not preserved on
disk and its exact generation invocation was not logged. The regenerated
dataset uses seed 42 per the generator's docstring example; if Feb used
the same seed, the puzzle set is identical, otherwise the rerun
evaluates on different puzzles. This does not invalidate a post-fix
comparison but precludes direct seed-wise comparability with Feb 2026.

## 4. Protocol (matches Feb 2026 protocol, not 4x4 Table 1)

| Field                | Value                                                    |
|----------------------|----------------------------------------------------------|
| Task                 | 9x9 Sudoku, feasibility-checker reward                   |
| Config               | `buiksat_trm/configs/sudoku9x9/ppo_9x9.yaml`             |
| Algorithm            | PPO (in-house trainer, TRM backbone)                     |
| Training steps       | 50,000                                                   |
| Max edits per ep (T) | 81                                                       |
| Discount gamma       | 0.99                                                     |
| Batch size           | 256                                                      |
| PPO rollout steps    | 128                                                      |
| PPO epochs           | 4                                                        |
| GAE lambda           | 0.95                                                     |
| Policy LR            | 1.0e-4                                                   |
| Value LR             | 1.0e-4                                                   |
| Entropy coef         | 0.05                                                     |
| LR schedule          | cosine, 500-step warmup, 0.1 min factor                  |
| Latent mode          | episodic                                                 |
| Eval interval        | 500 steps                                                |
| Eval episodes        | 100                                                      |
| Stop action          | disabled                                                 |
| Reward shaping       | filled - 2*violations - 5*zero_candidates                |
| Solve bonus          | +1                                                       |
| Fail penalty         | -81                                                      |
| Seeds                | 0, 1, 2                                                  |

## 5. Runtime and scheduling

- Per-seed wall-clock estimate: ~37 hours (from Feb 2026 log
  `results/9x9_experiments_seed0/ppo_50k_s0.log`: tqdm final elapsed
  `36:51:57`). Post-audit PPO has slightly different code paths
  (mask-stacking, eval task_config, Optional-typed num_episodes) but
  none of these touch per-step cost, so the Feb estimate is the right
  anchor.
- Scheduling: 3 seeds on 3 GPUs in parallel (GPUs 0, 1, 2); GPU 3 idle
  for the duration.
- Expected wall-clock: ~37 hours.
- Launcher:
  `/home/buiksat/trm_bellman/scripts/run_9x9_trm_ppo_post_audit_3seed.sh`

## 6. Results

### 6.1 Per-seed final step-50000 eval metrics

| Seed | success_rate | mean_score | mean_return | invalid_action_rate | Peak score |
|------|--------------|------------|-------------|---------------------|------------|
| 0    | 0.000        | 28.160     | -101.835    | 0.000               | 41.00      |
| 1    | 0.000        | 29.370     | -101.515    | 0.000               | 43.00      |
| 2    | 0.000        | 29.210     | -101.680    | 0.000               | 47.00      |

### 6.2 Aggregate (sample std, ddof=1)

| Metric       | Mean | Sample std | vs. Feb 2026 |
|--------------|------|------------|--------------|
| success_rate | 0.000 | 0.000     | Feb: 0.0 +/- 0.0 (3 seeds, pre-audit) |
| mean_score   | 28.913 | 0.657     | Feb: 29.45 +/- 0.58 (3 seeds, pre-audit) |
| mean_return  | -101.677 | 0.160     | Feb: N/A in report                        |

### 6.3 Decision trail

Selected scenario: **(A)**.

The post-audit TRM+PPO rerun remained at **0.000 +/- 0.000 success**
across all 3 seeds at 50k steps, so it does not change the current
appendix-only 9x9 framing in `main.tex`. The aggregate mean score
(`28.913 +/- 0.657`) is slightly below the Feb 2026 pre-audit PPO mean
score (`29.45 +/- 0.58`), and no seed solved any of the 100 eval
episodes at the final checkpoint. Relative to the Feb-era UPI-TRM 9x9
reference of `4.0%` success, PPO still shows no solved 9x9 episodes in
this protocol. `main.tex` is not edited in this session; this
provenance doc is sufficient to record the null post-audit PPO result.

## 7. Reproducibility recipe

### 7.1 Recompute per-seed aggregates from the logs

```
cd /home/buiksat/trm_bellman/results/9x9_trm_baselines_post3c2e959_3seed
python3 -c "
import re, math, glob
rows = []
for f in sorted(glob.glob('ppo_9x9_s*.log')):
    with open(f) as fh:
        text = fh.read()
    m = re.search(r'\\[step 50000\\] eval_success_rate=([0-9.]+).*eval_mean_score=([0-9.]+).*eval_mean_return=(-?[0-9.]+).*eval_invalid_action_rate=([0-9.]+)', text)
    if m:
        rows.append([f] + [float(x) for x in m.groups()])
        print(f, m.groups())
# aggregates
if rows:
    for j, name in enumerate(['success','score','return','invalid'], start=1):
        xs = [r[j] for r in rows]; n = len(xs); m = sum(xs)/n
        s = math.sqrt(sum((x-m)**2 for x in xs)/(n-1)) if n > 1 else 0.0
        print(f'{name}: mean={m:.4f} sample_std={s:.4f} n={n}')
"
```

### 7.2 Re-run a single seed

```
cd /data/users/buiksat/fbsource/fbcode && \
  CUDA_VISIBLE_DEVICES=0 buck2 run fbcode//buiksat_trm:upi_trm_train -- \
    --config buiksat_trm/configs/sudoku9x9/ppo_9x9.yaml \
    --seed 0 \
    --dataset-paths buiksat_trm/data/sudoku-9x9 \
    --checkpoint-dir /home/buiksat/trm_bellman/checkpoints/9x9_trm_baselines_post3c2e959_3seed/ppo_s0 \
    --train-steps 50000 \
    --no-wandb
```

## 8. Scope/anti-drift notes

- This document anchors only a single-method (PPO) 9x9 rerun. It does
  not anchor any of the 4x4 Table 1 numbers; those remain in
  `TABLE1_PROVENANCE.md`.
- The Feb 2026 UPI-TRM 9x9 value (4.0 +/- 4.0%) is NOT being re-run
  here. Its provenance remains
  `trm_bellman/results/9x9_experiments_seed0/upi_trm_50k_s{0,1,2}.log`
  under the Feb-era commit (pre-3c2e959). The UPI-TRM trainer was not
  in the Round 1 or Round 2 bug-fix scope; only the baseline trainers
  changed. Main text cites the UPI-TRM 9x9 4.0% at `main.tex:587` under
  "scaling feasibility check, not a claimed result", which is still
  valid.
- The pre-audit `EXPERIMENT_REPORT.md` at
  `trm_bellman/documents/results/9x9_experiments_seed0/EXPERIMENT_REPORT.md`
  should be treated as exploratory only for its PPO/A2C/DQN comparison.
