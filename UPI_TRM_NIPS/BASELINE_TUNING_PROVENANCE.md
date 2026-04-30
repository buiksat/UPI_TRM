# Baseline Tuning Artifact Provenance (Withdrawn From Manuscript)

Audit note for the removed masked-protocol baseline-tuning artifact that
was previously considered for the appendix of
`/home/buiksat/UPI_TRM/UPI_TRM_NIPS/main.tex`.

This document does **not** anchor any rendered manuscript table or
claim. The paper's active no-mask baseline claims remain in
`/home/buiksat/UPI_TRM/UPI_TRM_NIPS/TABLE1_PROVENANCE.md`.

Status: **withdrawn from manuscript / audit-only (2026-04-22)**.

---

## 1. Why This Artifact Was Removed

The appendix tuning artifact was removed from the manuscript for four
reasons:

- It used a **masked-control** 4x4 protocol, not the no-mask hard-4x4
  benchmark that anchors the paper's main baseline claim.
- Its original January 2026 numbers were generated **before** the April
  2026 in-house baseline-trainer audit.
- A post-audit rerun on the same single-seed masked protocol materially
  changed the results, so the historical appendix story was not stable.
- The rerun was still incomplete when the manuscript was updated, so the
  artifact was both protocol-mismatched and operationally unfinished.

Because this combination would likely confuse reviewers, the cleanest
paper state was to remove the artifact entirely rather than explain it in
the manuscript.

## 2. Historical Artifact Anchor

- Repository:
  `/home/buiksat/trm_bellman`
- Historical artifact commit:
  `519745e20b6bcb100cf1002458d78962ba10c188`
- Commit subject:
  `Add hyperparameter tuning experiment for baselines`
- Commit date:
  `2026-01-25 12:20:15 -0800`
- Historical report:
  `/home/buiksat/trm_bellman/documents/results/hp_tuning_sweep/EXPERIMENT_REPORT.md`
- Historical logs:
  `/home/buiksat/trm_bellman/results/hp_tuning_sweep/*.log`

Historical protocol:

- task: 4x4 Sudoku, 6-8 empties
- protocol: supplementary masked control
- budget: 20,000 training steps
- seed: 42
- evaluation: 50 puzzles per checkpoint

The historical appendix table contained 11 completed rows and omitted
`ppo_high_lr_epochs`, which did not finish.

## 3. Post-Audit Audit Rerun Anchor

- Repository:
  `/home/buiksat/trm_bellman`
- Code SHA:
  `0a96c712fb00da041047d979f332cc8c21158ad3`
- Launcher:
  `/home/buiksat/trm_bellman/scripts/run_hp_tuning_post_audit_11cfg.sh`
- Results root:
  `/home/buiksat/trm_bellman/results/hp_tuning_sweep_post0a96c71_11cfg_seed42/`
- Checkpoints:
  `/home/buiksat/trm_bellman/checkpoints/hp_tuning_sweep_post0a96c71_11cfg_seed42/`

At manuscript-withdrawal time (`2026-04-22 09:19 PDT`), 10 of the 11
reruns had completed and all 10 completed reruns showed nonzero success.
`ppo_deep_unroll` was still running.

## 4. Historical Vs Post-Audit State At Withdrawal Time

| Config | Historical success / score | Post-audit status at withdrawal time |
|---|---:|---:|
| `a2c_deep_unroll` | `0.000 / 9.36` | `0.920 / 15.46` |
| `a2c_high_entropy` | `0.000 / 11.66` | `0.940 / 15.62` |
| `a2c_high_lr_rollout` | `0.000 / 8.88` | `1.000 / 16.00` |
| `a2c_strong_reward` | `0.000 / 7.60` | `0.880 / 13.72` |
| `dqn_deep_unroll` | `0.000 / 6.16` | `0.760 / 13.90` |
| `dqn_large_buffer` | `0.000 / 1.06` | `0.600 / 11.46` |
| `dqn_slow_explore` | `0.000 / 6.86` | `0.840 / 14.30` |
| `dqn_strong_reward` | `0.000 / 6.08` | `0.860 / 13.58` |
| `ppo_high_entropy` | `0.000 / 5.34` | `0.660 / 13.18` |
| `ppo_strong_reward` | `0.000 / 0.44` | `0.860 / 13.38` |
| `ppo_deep_unroll` | `0.000 / 4.76` | in progress |

The remaining `ppo_deep_unroll` run had reached step `13473/20000` at
that time, with latest durable resume checkpoint:

- `/home/buiksat/trm_bellman/checkpoints/hp_tuning_sweep_post0a96c71_11cfg_seed42/ppo_deep_unroll_s42/rl_checkpoint_step_13000.pt`

## 5. Relationship To The Manuscript

As of the withdrawal update:

- `main.tex` no longer renders a baseline-tuning appendix table or
  subsection.
- The manuscript no longer cites this masked-control artifact as
  evidence.
- Table 1 remains the paper's active baseline anchor and is unaffected,
  because it is a separate no-mask, multi-seed result package.

## 6. Future Use Constraint

If this artifact is ever reintroduced in any future draft, it should
only be done after:

- the remaining rerun is finished,
- the results are framed explicitly as **masked-control** rather than
  no-mask evidence,
- and the strongest claims are checked with multi-seed replication
  rather than a single-seed table.
