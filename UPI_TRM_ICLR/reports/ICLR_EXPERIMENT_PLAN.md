# Locked ICLR Experiment Plan

## Purpose and non-claims

This document specifies experiments that are missing from the current evidence. It reports no new result. No job described here has been launched.

The current manuscript already contains many ablations, so experimental overfitting is a material risk. For every confirmatory run below, hypotheses, configurations, seed lists, interaction budgets, evaluation pools, reporting intervals, stopping rules, primary metrics, confidence intervals, and tests must be committed before training starts. Exploratory follow-ups must be labeled exploratory and cannot replace an unfavorable confirmatory endpoint.

The historical experiment repository `/home/buiksat/trm_bellman`, configs, checkpoints, and Buck targets cited by the provenance documents are not present in this workspace. Therefore no executable new-run command can be truthfully supplied or tested today. **Launching is prohibited until that repository is restored, a command manifest with exact executable commands is added to this report, and a one-seed smoke test establishes wall time and interaction accounting.** Command names must not be invented from the paper repository.

## Shared confirmatory lock

Unless a factor definition below necessarily changes an item, all Sudoku experiments use:

- Domain: no-mask hard `4x4` Sudoku, 6–8 empties.
- Episode horizon: `T=16` edits.
- Architecture: the same TRM backbone, latent width, value/policy heads, action interface, reward, and checker as the persistent headline configuration.
- Evaluator/training constants: `n=2`, `K=1`, `gamma=0.99`, projection setting/radius, optimizer, learning-rate schedule, batch sizes, replay behavior, and target-network behavior copied verbatim from the restored frozen headline config unless the named factor changes one of them.
- Primary environment-interaction budget: exactly `1,280,000` transitions per method/stage.
- Reporting grid: evaluation after `0, 64k, 128k, ..., 1,280k` interactions. Interim points are descriptive; the primary endpoint is fixed at `1,280k`.
- Confirmatory training seeds: `101,102,103,104,105,106,107,108,109,110`.
- Tuning/development seeds: `201,202,203,204,205`; these never enter confirmatory estimates.
- Data/evaluation sampling seed: `1729`; random latent diagnostic directions use a separate seed `1730`.
- Fixed evaluation pool: all 99 viable puzzles in the canonical fixed 6–8-empty test split, sorted by stable puzzle identifier after the documented blank-identifier filter. The materialized ordered pool and SHA-256 must be committed before training.
- Evaluation: greedy action selection, every puzzle evaluated once per checkpoint, identical tie-breaking, horizon, reward, and reporting code across methods.
- Per-seed outputs: success count/rate, return, checker score, invalid-action rate, exact environment interactions, optimizer updates, wall time, device type, checkpoint hash, config hash, code commit, and failure status.
- Stopping: run to the primary budget unless NaN, OOM, corrupted checkpoint, or hardware failure. Hardware failures may be rerun with the same seed/config and must retain both logs. No early stopping on performance.
- Primary estimand: mean per-seed difference in final success rate.
- Uncertainty: paired nonparametric bootstrap 95% confidence interval over the 10 common seed labels, with 100,000 resamples using analysis seed `314159`.
- Prespecified primary test: exact two-sided paired sign-flip randomization test on the 10 seed-level final success differences, `alpha=0.05`. Report the effect and interval regardless of significance. Return and invalid rate are secondary and receive no confirmatory significance claim.
- Budget multiplicity: no selection of the most favorable checkpoint or budget. Any inference at interim points is exploratory.
- Artifact gate: a result may enter the manuscript only after logs, configs, per-seed records, analysis code/output, failure manifest, and hashes are present and independently checked against this lock.

If the restored implementation reveals that `1,280,000` interactions cannot be represented identically for one method, stop and amend this protocol before any confirmatory seed runs. Do not substitute “outer steps.”

## Experiment 1: interaction-equalized UPI–TRM versus TRM+PPO

### Hypothesis

At the prespecified `1,280,000`-interaction endpoint on the fixed hard-Sudoku pool, persistent UPI–TRM and architecture-matched TRM+PPO may differ in success rate. The protocol is two-sided: it does not presuppose that UPI–TRM is better.

### Arms

1. Persistent UPI–TRM using the restored frozen headline configuration, including its actual distillation behavior.
2. Architecture-matched TRM+PPO using the restored frozen Table 1 configuration.

Both arms must count an interaction as one environment transition. Gradient steps, recurrent inner iterations, action-enumeration forwards, and replay samples are reported separately and do not alter the interaction counter.

### Tuning separation

- Existing published configurations are the default and require no confirmatory tuning.
- If restoration forces a compatibility choice, only seeds `201–205` may be used, at a development budget fixed before those runs.
- One configuration per method is frozen before any seed `101–110` is run.
- Evaluation-pool outcomes are unavailable to the tuning process.

### Acceptance criterion

This experiment is complete when both methods have valid final artifacts for all 10 seeds or a fully documented failure manifest; their interaction counters match exactly at every reporting point; and the prespecified effect, interval, and test are reproduced from the retained per-seed file. An unfavorable or null result still satisfies completion. No sample-efficiency or equal-interaction claim is permitted before this gate.

### Planned compute

Historical provenance reports roughly 9 GPU-hours per architecture-matched 20k-step seed. That is not a verified runtime for the new interaction-counted protocol or for UPI–TRM. A planning envelope is `180–240 GPU-hours` for the 20 confirmatory runs, plus up to `90 GPU-hours` if the 10 development runs are needed. Replace this envelope with a smoke-test estimate and exact device count before launch.

## Experiment 2: one-factor-at-a-time bridge from the persistent configuration

### Purpose

The existing theory-aligned run changed several factors simultaneously and reached `0%`. The bridge isolates where performance is lost without post-hoc factor selection.

### Locked cumulative stages

Each adjacent stage changes exactly one named factor. All shared-lock items remain identical whenever the factor permits it.

| Stage | Latent across edits | Policy mixture | K-step target | Baseline construction | Only change from prior stage |
|---|---|---|---|---|---|
| P0 | carried | headline distillation | headline/original | headline/original | Frozen successful-configuration reference rerun |
| P1 | reinitialized from current plan | headline distillation | headline/original | headline/original | Carry → reinitialization |
| P2 | reinitialized | direct exact statewise mixture; no distillation | headline/original | headline/original | Distillation → direct mixture |
| P3 | reinitialized | direct exact mixture | exact `K`-step target | headline/original | Original → exact target |
| P4 | reinitialized | direct exact mixture | exact `K`-step target | exact action-space baseline | Original → exact baseline |

The stage order is fixed before runs. Results may motivate a later exploratory factorial, but that factorial cannot replace this confirmatory sequence.

### Required implementation invariants

- Config diffs are machine-generated and must show that only the designated fields change between adjacent stages.
- Direct mixture means sampling/deploying `(1-alpha) pi + alpha pi_cand` pointwise; parameter interpolation and distillation do not qualify.
- Exact baseline means explicit action-space expectation for every complete state used by the policy; batch-mean centering does not qualify.
- Exact target bootstraps with the declared evaluator and policy, not merely a target-network loss with a similar name.
- `alpha` and all optimization constants are frozen from the restored reference config; no stage-specific retuning.

### Analysis and acceptance

- Use seeds `101–110`, the same 99-puzzle pool, `1.28M` interactions, and the shared reporting grid.
- Report all adjacent paired differences `P1-P0`, `P2-P1`, `P3-P2`, and `P4-P3` with paired bootstrap intervals.
- The family is descriptive mechanism analysis; no factor is declared beneficial from an unadjusted p-value. If hypothesis tests are desired, use Holm correction across the four adjacent primary contrasts and record that choice before training.
- Completion requires per-seed artifacts for every stage and a machine-audited config-diff report. A zero-success stage is retained and reported.

### Planned compute

Five stages × 10 seeds gives 50 training runs. At the historical 9 GPU-hour scale, the initial planning envelope is `450–550 GPU-hours`, excluding diagnostics. Exact-mixture action evaluation may increase runtime; a P0/P2 smoke comparison must replace this estimate before launch.

## Experiment 3: persistent-state finite-batch diagnostics

### Scope

These measurements are finite-batch diagnostics for frozen snapshots. They are never called uniform theorem certificates or upper bounds on closure suprema.

### Frozen augmented-state batch

For each confirmatory seed and stage, roll out the frozen policy on the ordered 99-puzzle pool and retain complete states `(x,y,z,remaining_budget)` at edit indices `0,4,8,12` when present. Store reward/termination information, policy logits, recurrent parameters, and snapshot hashes. The batch must be materialized once per snapshot and never filtered based on diagnostic values.

### Required diagnostics

1. **Augmented Bellman residual.** Compute the finite-batch maximum and quantiles of
   `|U_tilde_n(bar s) - bar T_K^bar pi U_tilde_n(bar s)|`
   using the actual carried-latent transition, actual frozen policy, exact discrete action expectation, and the same evaluator on the bootstrap side. Report separately from the episodic residual.
2. **Centering defect.** Compute `|E_{a~bar pi}[Ahat(bar s,a)]|` by exact action summation on the complete augmented state. Report maximum and quantiles.
3. **Distillation KL.** For P0/P1 and any distilled arm, compute `KL(pi_mix || pi_phi)` per augmented state before the next update. For direct-mixture stages, record structural zero/not-applicable rather than an estimated KL.
4. **Recurrent path length.** For depths `j=0,...,31`, store `d_j(bar s)=||z^(j+1)-z^(j)||`; report `sum_{j=n}^{m-1} d_j` for locked pairs `(n,m) in {(2,4),(2,8),(2,16),(2,32)}`.
5. **Ratio diagnostic.** Store `q_j=d_(j+1)/d_j` only when `d_j >= 1e-12`; otherwise record undefined. Report distributions rather than a fitted contraction constant.
6. **Value-head depth drift.** Store `|U_(j+1)-U_j|`, `|U_n-U_m|`, and the corresponding Lipschitz path proxy for the locked depth pairs.
7. **Multiple-initialization behavior.** For each `(x,y)`, evaluate the actual carried latent, fresh `z_init(x,y)`, zero latent, and five fixed projected random initializations generated with seed `1730`. Report pairwise latent/value diameters at depths `0,2,4,8,16,32` and action agreement. Do not label decreasing finite-depth diameter as convergence without a proved limit.
8. **Closure/evidence status.** Record batch size, state-source policy, edit-index coverage, and the fact that no finite batch establishes a uniform supremum.

### Acceptance criterion

The diagnostic package is complete only when every frozen snapshot has the same schema, exact action-summation audit, missing-value rules, and hashes; all per-state rows are retained; and the paper labels every reported number finite-batch. No performance acceptance threshold is used.

### Planned compute

The prior 10-seed episodic training-plus-diagnostics launcher took 22:07 wall hours on two GPUs (`~44 GPU-hours`) and diagnostics dominated late wall time. The new diagnostic cost cannot be inferred exactly because the augmented batch and multiple initializations are larger. Reserve a provisional `50–80 GPU-hours per 10-snapshot stage`, or `250–400 GPU-hours` for all five bridge stages, then replace it with a one-snapshot benchmark before launch.

## Experiment 4: second verifier-guided domain

### Launch gate

This experiment may begin only after Experiments 1 and 2 have complete, audited artifact manifests. It cannot be used to select a favorable Sudoku budget or bridge stage.

### Locked domain: 8-puzzle

- Task: standard `3x3` sliding-tile 8-puzzle.
- Verifier: exact goal-state checker; legal-move checker; BFS distance used only to construct/split instances and audit difficulty, never as a demonstration or training target.
- Instance universe: enumerate all 181,440 solvable states and compute exact goal distance by BFS.
- Difficulty band: initial optimal distance `16–24`, fixed before training.
- Split: stable hash of the board permutation with split salt `upi-trm-iclr-8p-v1`; take 50,000 train states, 5,000 tuning states, and 5,000 evaluation states from the band in hash order, with no overlap. Commit ordered manifests and hashes before training.
- Actions: four slide directions with explicit invalid-action accounting.
- Horizon: `T=32` moves.
- Reward: goal success plus a prespecified checker-derived shaping function that is identical for both methods. The exact formula must be committed before any tuning run and may not use the BFS optimal action.
- Methods: UPI–TRM and architecture-matched TRM+PPO.
- Architecture: same latent/value-policy capacity, `n`, `K`, `gamma`, projection setting, optimizer, interaction budget, and reporting grid as the matched Sudoku experiment, except for the four-action input/output adapters and `T=32`.
- Seeds: development `201–205`, confirmatory `101–110`, generator/split seed encoded by the fixed hash salt.
- Budget: `1,280,000` environment interactions per method; checkpoints every `64k`.
- Primary endpoint: solve rate on the fixed 5,000-state evaluation pool within 32 moves.
- Secondary endpoints: return, invalid-action rate, and steps among solved instances.
- Statistics: the same paired seed-level effect, bootstrap interval, and exact sign-flip test as Experiment 1.
- No domain switching: if 8-puzzle results are null or negative, another domain is exploratory and cannot replace this confirmatory result.

### Acceptance criterion

The second-domain result may enter the manuscript only if generator/BFS tests, split hashes, reward definition, exact interaction counters, all 20 seed runs, and prespecified analysis artifacts pass review. It must be described as one additional verifier-guided domain, not evidence of broad generality.

### Planned compute

No implementation exists in the present workspace. A provisional envelope is `180–260 GPU-hours` for the 20 confirmatory runs plus development, based only on the historical Sudoku per-seed scale. This is a planning bound, not a measured estimate; a one-seed smoke run and exact commands are mandatory before launch.

## Required exact-command manifest before any launch

The restored experiment repository must add a committed manifest containing, for every run family:

- repository commit and clean status;
- exact working directory;
- exact executable command, all flags, config paths, dataset/split paths, output roots, seed, device, and interaction budget;
- scheduler command and requested GPU/CPU/RAM/time;
- environment/package lock and Buck target resolution;
- expected artifact list and failure handling;
- measured one-seed smoke runtime and projected total GPU-hours.

Historical provenance names `fbcode//buiksat_trm:upi_trm_train` and several launchers, but those paths are currently absent and are not treated as executable new-run commands. This report must be amended with commands that are actually resolved and smoke-tested. Until then, estimated compute is reported above and **all expensive launches remain blocked**.

## Manuscript admission rule

No placeholder, planned value, partial seed aggregate, best checkpoint, or exploratory budget may appear as a completed result. The manuscript may describe these protocols as future work. A result is admissible only after the full locked endpoint and artifact gate are complete; any deviation is listed prominently and the result is labeled exploratory.
