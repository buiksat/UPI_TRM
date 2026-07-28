# Episodic-z hard-suite rerun log

## Goal
Run the theorem-aligned episodic-z rerun on the no-mask hard 4x4 Sudoku
6--8-empty suite and record the frozen-batch theorem-contact diagnostics
required by `EXPERIMENTS_PROTOCOL.md` without modifying the locked
protocol.

## Inputs (fill before running)
- Locked protocol: `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/EXPERIMENTS_PROTOCOL.md`
  at commit `c399fef`
- Persistent-z comparator provenance:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/TABLE1_PROVENANCE.md` Section 4.1
- Persistent-z checkpoint paths:
  `/home/buiksat/trm_bellman/checkpoints/m1_nomask_persistent_nc_seed{0..9}/rl_checkpoint_step_20000.pt`
- Persistent-z checkpoint seed list: `0,1,2,3,4,5,6,7,8,9`
  (from checkpoint/training artifacts; not from paper text)
- Episodic-z rerun seeds: `41,42,43,44,45,46,47,48,49,50`
- Seed-pairing note: persistent-z uses seeds `0..9` while the locked
  episodic-z rerun uses seeds `41..50`, so episodic-vs-persistent
  comparison is a non-paired 10-seed aggregate comparison.
- Canonical persistent-z hard-suite config:
  `/home/buiksat/trm_bellman/configs/ablations/upi_trm_feasibility_persistent_z_no_contraction_no_mask.yaml`
- Planned episodic-z rerun config path:
  `/home/buiksat/trm_bellman/configs/revision/upi_trm_feasibility_episodic_z_hard_suite_theory_exact.yaml`
- Training binary:
  `fbcode//buiksat_trm:upi_trm_train`
- Closure-batch materializer (to be created under `trm_bellman`):
  `fbcode//buiksat_trm:materialize_hard4x4_closure_batch`
- Finite-MDP validation / checkpoint diagnostic runner (to be created
  under `trm_bellman`):
  `fbcode//buiksat_trm:episodic_z_hard_suite_diagnostics`
- Dataset path:
  `/home/buiksat/trm_bellman/data/sudoku-4x4-easy_6to8empties`
- Evaluation interface:
  same greedy plan-policy interface used for architecture-matched
  baselines (`UPITrmTrainer.evaluate_policy_metrics` /
  `rl.evaluator.evaluate_plan_policy_with_scores`)
- Alpha grid: `{0.05, 0.1, 0.2, 0.4}`
- Primary diagnostic checkpoints: `{5000, 10000, 15000, 20000}`

## Output
- Closure batch:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/closure_batch_seed1729.npz`
- Fixed `L_V` / latent perturbation directions:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/lv_directions_seed1729_eps1e-4.npz`
- Finite-MDP validation output:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/`
- Episodic-z training results root:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/`
- Episodic-z checkpoint root:
  `/home/buiksat/trm_bellman/checkpoints/episodic_z_hard_suite_20k_seed41_50/`
- Per-seed training logs:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/logs/`
- Per-seed eval metrics:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/per_seed_eval.jsonl`
- Per-seed diagnostics:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/per_seed_diagnostics.jsonl`
- Aggregate task metrics:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/summary.json`
- Aggregate diagnostics:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/diagnostics_summary.json`
- Predicted-vs-measured CPI penalty table:
  `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/cpi_penalty_grid.json`

## Locked before run
- `EXPERIMENTS_PROTOCOL.md` remains unchanged. All run-specific notes live
  in this file only.
- Hard constraints inherited from the locked protocol:
  - suite: no-mask hard 4x4 Sudoku, 6--8 empties
  - budget: 20k environment steps
  - horizon: `T=16`
  - seeds: `41..50`
  - latent mode: episodic-z
  - baseline: exact action-space summation
  - alpha grid: `{0.05, 0.1, 0.2, 0.4}`
  - closure batch: 256 held-out instances, RNG seed `1729`
  - `L_V` finite-difference epsilon: `1e-4`
  - stopping rule: run every seed to 20k unless NaN, OOM, or hardware failure
- Episodic-z config policy:
  start from the persistent-z hard-suite config above and change only:
  - `episodic_latent: true`
  - `exact_baseline_summation: true`
  - `theory_exact_mixture: true`
  - `distill_mixture_policy: false`
  - `batch_centered_advantage: false`
  - `policy_epsilon: 0.0`
  - `exact_k_step_targets: true`
  - `latent_ball_radius: 10.0` (made explicit rather than left implicit)
- Closure-batch source split:
  user-authorized deviation on 2026-04-28: draw from the fixed `train/`
  split of `data/sudoku-4x4-easy_6to8empties` with seed `1729`, because
  the fixed `test/` split has only `99` viable instances after
  blank-identifier filtering and therefore cannot satisfy the locked
  `256`-instance closure-batch requirement.
- Held-out RNG independence rule:
  the closure-batch sampler uses a dedicated local RNG seeded at `1729`
  and does not share mutable RNG state with any per-seed training loader.
- Fixed reference-evaluator depth for advantage-bias proxies:
  `n_ref = 32`
- Fixed stochastic rollout repeats for the surrogate-true gap proxy:
  `8` repeats per held-out start state and per alpha.
- Fixed perturbation-direction count:
  `16` unit directions, materialized once in
  `lv_directions_seed1729_eps1e-4.npz`
- Theory banner semantics note (2026-04-28):
  the trainer banner's `Is theory-exact` field is computed from
  `RLConfig.is_theory_exact()`, which requires forward-invariant
  projection, enforced contraction (`enable_contraction=True` and
  `target_Lz < 1`), exact K-step targets, exact baseline summation,
  theory-exact policy-space mixture, and no distillation. The locked
  episodic-z rerun intentionally retains `enable_contraction=False` to
  match the persistent-z hard-suite anchor, so the banner prints
  `False`. This does not mean the exact-centering / exact-mixture
  overrides failed to land: the live trainer still uses exact baseline
  summation, explicit policy-space mixture (`theory_exact_mixture=True`),
  `policy_epsilon=0.0`, and `batch_centered_advantage=false`.
- Diagnostic proxy conventions (all are empirical proxies on the frozen
  held-out batch; none is reported as a theorem verification):
  1. `eps_res,n`:
     max over the frozen held-out start states of
     `|U_n(s) - T_1^{pi_old} U_n(s)|`, with the `T=16` hard-suite reward
     and exact action-space summation under `pi_old`.
  2. `eps_cent`:
     max over held-out start states of
     `|E_{a~pi_old}[Ahat_n(s,a)]|`.
  3. `eps_A,cand`:
     max over held-out start states of
     `|E_{a~pi_cand}[Ahat_n(s,a) - Ahat_ref(s,a)]|`, where
     `Ahat_ref` is the exact one-step centered advantage built from
     `U_{n_ref}` on the same state/action set.
  4. surrogate-true gap at alpha:
     `Lhat_alpha - eta_alpha_proxy`, where `Lhat_alpha` uses the exact
     one-step centered `Ahat_n` on the frozen batch and
     `eta_alpha_proxy` is the mean discounted return of the explicit
     stochastic mixture policy on that same frozen batch with `8` fixed
     Monte Carlo repeats.
  5. predicted CPI penalty at alpha:
     the projection-aware decomposition penalty
     `2*alpha*gamma/(1-gamma) * (eps_res,n/(1-gamma^K) + 2*L_V*R*(L_z_post^n)/(1-L_z_post))`
     plus the quadratic CPI term
     `2*eps_CPI_ref*gamma/(1-gamma)^2 * alpha^2`, where
     `eps_CPI_ref := max_s |E_{a~pi_cand}[Ahat_ref(s,a)]|`.
     If `L_z_post >= 1`, this penalty is recorded as `+inf`.
  6. `L_V`:
     fixed-direction finite-difference max over the frozen held-out batch
     using the saved `16` directions and epsilon `1e-4`.
  7. `rho_R`:
     minimum pre-projection latent norm
     `min_s ||f_theta(z_n(s), x, y)||_2` over the frozen held-out batch at
     the training evaluator depth `n`.
  8. `L_z_post`:
     fixed-direction finite-difference max of the projected latent update
     map on the frozen held-out batch, using the same saved directions and
     epsilon `1e-4`.
  9. projection-active rate:
     fraction of held-out start states whose pre-projection latent norm
     exceeds `R=10.0` at the measured update point.
- Finite-MDP validation conventions:
  - diagnostics `1`--`5` must match the finite-MDP certificate values
    exactly within the protocol tolerance.
  - in the projection-free finite-MDP setting, diagnostics `6`--`9` are
    validated against the trivial ground truth
    `L_V=1`, `rho_R=+inf`, `L_z_post=L_z`, and
    `projection-active rate = 0`.

## Run record (fill after running)
- Date:
  - closure batch + fixed directions materialized: 2026-04-28
  - finite-MDP validation gate recorded: 2026-04-28
  - episodic-z launcher start: 2026-04-28 16:23 PDT
  - final aggregate artifacts written: 2026-04-29 14:30 PDT
- Command(s):
  - closure batch / direction materialization:
    `buck2 run --local-only //buiksat_trm:materialize_hard4x4_closure_batch -- ...`
    with dataset
    `/home/buiksat/trm_bellman/data/sudoku-4x4-easy_6to8empties`,
    seed `1729`, `256` instances, fixed `16` directions, and the
    user-authorized `train/` split deviation recorded above
  - finite-MDP validation gate:
    `buck2 run --local-only //buiksat_trm:episodic_z_hard_suite_diagnostics -- validate-finite-mdp --out-dir /home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation`
  - episodic-z training + checkpoint diagnostics:
    `bash scripts/run_episodic_z_hard_suite_10seed_2gpu.sh`
- Wall time:
  - launcher wall time (training + per-seed diagnostics + postprocess):
    `22:07:13`
- Closure batch artifact:
  - `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/closure_batch_seed1729.npz`
  - `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/lv_directions_seed1729_eps1e-4.npz`
- Finite-MDP validation output:
  - `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/validation_summary.json`
- Training output root:
  - `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/`
- Diagnostics output root:
  - `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/diagnostics/`
- Aggregate output artifacts:
  - task summary:
    `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/summary.json`
  - diagnostics summary:
    `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/diagnostics_summary.json`
  - CPI penalty grid:
    `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/cpi_penalty_grid.json`
  - per-seed eval stream:
    `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/per_seed_eval.jsonl`
  - per-seed diagnostics stream:
    `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_hard_suite_20k_seed41_50/per_seed_diagnostics.jsonl`
- Anomalies:
  - no NaN, OOM, or hardware failures; all `10/10` seeds trained to `20k`
    under the locked stopping rule
  - diagnostics dominated wall-clock after training completed; this affected
    completion time but not the measured checkpoints or frozen closure batch
  - the trainer banner's `Is theory-exact: False` field remained expected
    throughout because `enable_contraction=False` is retained from the
    persistent-z anchor; exact-centering / explicit-mixture behavior was
    confirmed separately and `eps_cent` stayed numerically tiny at every
    checkpoint
  - at `20k`, seeds `41` and `46` had `L_z_post >= 1`, so the
    projection-aware predicted CPI penalty is recorded as `+inf` for those
    seeds at every alpha

### Per-seed `L_z_post` at `20k`

| Seed | `L_z_post` | penalty status |
| --- | ---: | --- |
| 41 | 1.328475 | `+inf` |
| 42 | 0.567540 | finite |
| 43 | 0.529271 | finite |
| 44 | 0.491896 | finite |
| 45 | 0.549628 | finite |
| 46 | 1.675811 | `+inf` |
| 47 | 0.528209 | finite |
| 48 | 0.619084 | finite |
| 49 | 0.775281 | finite |
| 50 | 0.736700 | finite |

- Finite-subset (`8/10`) summary:
  `L_z_post = 0.5997 ± 0.0970`, range `[0.4919, 0.7753]`
- Saturating seeds (`2/10`):
  `41`, `46`

### Per-seed predicted CPI penalty at `20k` (finite subset only)

Finite seeds: `42,43,44,45,47,48,49,50`

| Seed | `alpha=0.05` | `0.10` | `0.20` | `0.40` |
| --- | ---: | ---: | ---: | ---: |
| 42 | 5269.1743 | 10902.7586 | 23263.1571 | 52356.8735 |
| 43 | 5266.0103 | 10925.2929 | 23423.6752 | 53139.7074 |
| 44 | 5009.1470 | 10498.1052 | 22915.4547 | 53507.8870 |
| 45 | 5039.8796 | 10467.0776 | 22483.4288 | 51163.9515 |
| 47 | 5079.7327 | 10508.6500 | 22414.0380 | 50415.0283 |
| 48 | 5465.5837 | 11318.0152 | 24183.4213 | 54556.4061 |
| 49 | 5207.3800 | 10802.2729 | 23154.5970 | 52509.3991 |
| 50 | 5383.9820 | 11056.0858 | 23264.6590 | 51139.2671 |

Finite-subset alpha-grid summary:

| alpha | predicted penalty mean ± std | min | max |
| --- | --- | ---: | ---: |
| `0.05` | `5215.11 ± 164.00` | 5009.15 | 5465.58 |
| `0.10` | `10809.78 ± 303.85` | 10467.08 | 11318.02 |
| `0.20` | `23137.80 ± 561.71` | 22414.04 | 24183.42 |
| `0.40` | `52348.56 ± 1387.43` | 50415.03 | 54556.41 |

- All-seed mean predicted penalty at every alpha is literally `+inf`, because
  `2/10` seeds (`41`, `46`) have `L_z_post >= 1`
- At `20k`, exact centering remained uniform:
  `eps_cent = 1.782e-06 ± 3.007e-07`
- At `20k`, the dominant loose-bound source was the held-out residual:
  `eps_res,n = 5.0465 ± 0.1750`
- At `20k`, projection remained active on every held-out state:
  `projection_active_rate = 1.0`, `rho_R = 45.2547 ± 1.29e-05`
- Protocol immutability check:
  `git log --oneline UPI_TRM_NIPS/EXPERIMENTS_PROTOCOL.md` still shows only
  `c399fef`

## Decision branch
- Branch:
  - `D: episodic-z underperforms`
- Condition check:
  - persistent-z reference success:
    `S_P = 57.4`
  - Branch `D` threshold:
    `0.85 * 57.4 = 48.79`
  - episodic-z rerun success at `20k`:
    `S_E = 0.000 ± 0.000`
  - margin to threshold:
    `48.79` percentage points below the Branch `A/B/C` gate
  - final `20k` task aggregate across `10/10` seeds:
    - success: `0.000 ± 0.000`
    - return: `-21.733 ± 0.512`
    - score: `3.906 ± 0.606`
    - invalid-action rate: `0.000 ± 0.000`
- Notes for Section 7 / appendix wording:
  - apply the protocol's Branch `D` action exactly:
    persistent-z remains the empirical algorithm; episodic-z is the
    theory companion
  - if paper text is updated later, describe these as
    `finite-batch theorem-contact diagnostics on a frozen held-out closure batch`
  - do not write `we verify Theorem 6.5` or `we prove Corollary 6.7`
  - theorem-contact observations at `20k`:
    - exact centering held uniformly across seeds (`eps_cent ≈ 1.78e-6`)
    - projection was active on every held-out state (`projection_active_rate = 1.0`)
    - the residual term remained large (`eps_res,n ≈ 5.05`)
    - `2/10` seeds (`41`, `46`) had `L_z_post >= 1`, so the all-seed
      predicted CPI penalty mean is `+inf` at every alpha
  - manuscript wording that `L_z_post` is pinned around `0.22`--`0.24`
    should be scoped to the persistent-z Appendix `exp2` sweep cell if
    later paper edits mention the episodic-z hard-suite rerun
