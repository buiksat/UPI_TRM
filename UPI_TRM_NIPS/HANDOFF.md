# HANDOFF: Paper / Baseline Status (2026-04-22)

This handoff supersedes the older 2026-04-19 note. It is the current
state for the NeurIPS paper repo and the related `trm_bellman` baseline
audit / follow-up sweeps.

## Repos and Current Heads

- Paper repo:
  `/home/buiksat/UPI_TRM`
- Paper repo `HEAD`:
  `ec462c04f81e92c3d63a38d639a2841acfcaeb8b` (`ASD`)
- Important paper cleanup commit directly below `HEAD`:
  `e9cfd8e` (`Clean paper-side baseline provenance and remove withdrawn appendix artifact`)
- Code repo:
  `/home/buiksat/trm_bellman`
- Code repo `HEAD`:
  `27741bf31f4a808a6b487da24b222ec2f6860ac1` (`ASD`)

Important caveat:

- The live masked-control rerun below is anchored to code SHA
  `0a96c712fb00da041047d979f332cc8c21158ad3`, not the current
  `trm_bellman` `HEAD`.
- `trm_bellman` is currently dirty only because the live log
  `results/hp_tuning_sweep_post0a96c71_11cfg_seed42/ppo_deep_unroll_s42.log`
  is still growing.

## Non-Negotiable Trusted Paper-Facing Baseline Package

Use only the **post-second-audit clean rerun** for the paper's
architecture-matched Table 1 baseline numbers.

Authoritative provenance doc:

- `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/TABLE1_PROVENANCE.md`

Trusted locked no-mask hard-4x4 numbers:

- `UPI-TRM`: `57.4% +/- 12.2%` over `10` seeds
- `TRM+PPO`: `32.0% +/- 15.3%` over `10` seeds
- `TRM+A2C`: `0.0% +/- 0.0%` over `10` seeds
- `TRM+DQN`: `0.0% +/- 0.0%` over `10` seeds

These are **TRM-backed architecture-matched baselines**, not alternate
non-TRM backbones.

Configs:

- `/home/buiksat/trm_bellman/configs/baselines/ppo_trm_feasibility.yaml`
- `/home/buiksat/trm_bellman/configs/baselines/a2c_trm_feasibility.yaml`
- `/home/buiksat/trm_bellman/configs/baselines/dqn_trm_feasibility.yaml`

Each sets:

```yaml
model_type: "trm"
```

They also use the in-repo checker-shaped reward path rather than plain
SB3 reward wiring.

## Why Older PPO/DQN Numbers Were Invalid

There were **two audit rounds** in `trm_bellman`.

Round 1 fixed:

- PPO clipped-objective scalar/broadcast corruption in
  `/home/buiksat/trm_bellman/rl/algos/ppo.py`
- DQN TRM Q-head flatten sizing in
  `/home/buiksat/trm_bellman/rl/algos/dqn.py`
- DQN terminal-next-mask batch handling in
  `/home/buiksat/trm_bellman/rl/algos/dqn.py`

Round 2 fixed:

- DQN NoRec backbone dispatch bug in
  `/home/buiksat/trm_bellman/rl/algos/dqn.py`
- DQN epsilon schedule being computed in train-step units instead of
  env-step units
- eval `task_config` propagation mismatch across PPO/A2C/DQN evaluation
  paths

Additional hardening landed around mask stacking, baseline pretrain
guards, and PPO parameter-group fail-fast behavior.

Regression suite:

- `/home/buiksat/trm_bellman/tests/test_rl_algos_mock.py`

Validation command:

```bash
buck2 test fbcode//buiksat_trm:test_rl_algos_mock --local-only
```

Previous validated result from the audit session:

- `Pass 18, Fail 0`

Fresh-context review after the fixes found no remaining blocking
correctness issue for the locked Table 1 TRM-backed baseline package.

## Paper Repo State Right Now

### 1. Table 1 stays the only active baseline anchor

No change here: the paper's active baseline narrative still points only
to the no-mask hard-4x4 Table 1 package and
`TABLE1_PROVENANCE.md`.

### 2. 9x9 post-audit PPO provenance is complete

Authoritative doc:

- `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/9X9_PROVENANCE.md`

Current status:

- complete / consolidated on `2026-04-21`
- post-audit TRM+PPO 9x9 result is `0.000 +/- 0.000` success over `3`
  seeds at `50k` steps
- aggregate mean score is `28.913 +/- 0.657`
- selected scenario is **A**:
  keep `main.tex` unchanged

Interpretation:

- the post-audit PPO null result does not contradict the paper's current
  appendix-only 9x9 framing
- `main.tex` intentionally does **not** add a PPO/A2C/DQN 9x9 contrast
  paragraph

### 3. Masked single-seed baseline-tuning appendix artifact was removed

The manuscript no longer renders the old masked-control appendix tuning
subsection/table.

Audit-only withdrawn-artifact note:

- `/home/buiksat/UPI_TRM/UPI_TRM_NIPS/BASELINE_TUNING_PROVENANCE.md`

Why it was removed:

- masked-control protocol, not the no-mask hard-4x4 benchmark
- historical numbers were pre-audit
- post-audit rerun materially contradicted the historical `0%` story
- rerun was incomplete at withdrawal time

This was the right paper decision. A fresh-context Claude review found
**no findings** on the cleanup.

### 4. Compute wording was narrowed and is now technically honest

Two paper-side wording changes matter:

- experiment setup now says the comparison matches architecture and
  budget without claiming identical constant-factor wall-clock cost
- implementation appendix now explicitly states PPO/A2C use separate
  policy/value forwards through the TRM backbone during optimization, so
  per-update wall-clock can exceed UPI-TRM

Build status:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_NIPS
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

This passed after the appendix cleanup, with no undefined-reference
errors from the removal.

## Live Masked-Control Rerun Status (Audit-Only, Not Paper Evidence)

This is the post-audit rerun of the **withdrawn** masked-control tuning
artifact. It is not manuscript evidence.

Launcher:

- `/home/buiksat/trm_bellman/scripts/run_hp_tuning_post_audit_11cfg.sh`

Results root:

- `/home/buiksat/trm_bellman/results/hp_tuning_sweep_post0a96c71_11cfg_seed42/`

Checkpoint root:

- `/home/buiksat/trm_bellman/checkpoints/hp_tuning_sweep_post0a96c71_11cfg_seed42/`

Live session:

- `tmux` session `hp_tuning_0a96c71`

Status at `2026-04-22 09:59 PDT`:

- `10 / 11` configs complete
- all `10 / 10` completed configs show **nonzero** success
- `failed_jobs.txt` is empty (`0` bytes)
- only `ppo_deep_unroll` remains live
- latest observed progress: about `13820 / 20000`
- current pace is about `5.3 s / step`
- latest durable checkpoint is still `step 13000`

Implication:

- the historical appendix claim that all `11` configurations got `0%`
  success is decisively overturned under the post-audit code
- this is exactly why the artifact was removed from the manuscript

Operational note:

- at the observed pace, `ppo_deep_unroll` still had roughly `9` hours to
  finish from the 09:59 PDT check
- that is later than the user's original `2026-04-22 13:15 PDT` machine
  cutoff, so a host migration / resume may be required

Resume note:

- the launcher is already written to resume from the latest
  `rl_checkpoint_step_*.pt`
- for `ppo_deep_unroll`, the latest durable checkpoint currently present
  is:
  `/home/buiksat/trm_bellman/checkpoints/hp_tuning_sweep_post0a96c71_11cfg_seed42/ppo_deep_unroll_s42/rl_checkpoint_step_13000.pt`

If continuation is needed on another machine:

```bash
cd /home/buiksat/trm_bellman
bash scripts/run_hp_tuning_post_audit_11cfg.sh
```

The prior session already verified that this resume path uses
`--resume-checkpoint` and continues toward `20000`, not `33000`.

## What A New Session Should Do

### If the question is about the paper

Do this:

- use `TABLE1_PROVENANCE.md` for the paper's active baseline claims
- use `9X9_PROVENANCE.md` for the appendix-only 9x9 PPO null result
- use `BASELINE_TUNING_PROVENANCE.md` only as an audit note for the
  withdrawn masked artifact

Do **not** do this:

- do not reintroduce the masked single-seed appendix table into
  `main.tex`
- do not reinterpret the masked-control rerun as if it were no-mask
  evidence
- do not cite pre-audit baseline numbers from the historical
  `EXPERIMENT_REPORT.md` as paper evidence

### If the question is about the live rerun

1. Check whether `ppo_deep_unroll` finished.
2. If the current host is gone, resume with the launcher on another
   host.
3. If it eventually finishes, update only the audit note unless there is
   a deliberate decision to reopen the withdrawn artifact discussion.

### If someone wants to revive the masked artifact later

That should only happen after:

- all `11 / 11` reruns are complete
- the artifact is labeled explicitly as **masked-control**
- the strongest claims are checked with multi-seed replication

Right now the clean paper state is to keep it **out** of the manuscript.

## Useful Commands For The Next Session

Check the live masked rerun:

```bash
tmux list-sessions 2>/dev/null | rg hp_tuning_0a96c71
tr '\r' '\n' < /home/buiksat/trm_bellman/results/hp_tuning_sweep_post0a96c71_11cfg_seed42/ppo_deep_unroll_s42.log | tail -40
wc -c /home/buiksat/trm_bellman/results/hp_tuning_sweep_post0a96c71_11cfg_seed42/failed_jobs.txt
```

Check the largest available resume checkpoint:

```bash
ls -1 /home/buiksat/trm_bellman/checkpoints/hp_tuning_sweep_post0a96c71_11cfg_seed42/ppo_deep_unroll_s42/rl_checkpoint_step_*.pt | sed 's#.*step_##; s#.pt##' | sort -n | tail -1
```

Build the paper:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_NIPS
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Find the paper cleanup commit:

```bash
git -C /home/buiksat/UPI_TRM log --oneline --decorate -5
```

## One-Sentence New-Session Summary

> The paper is now in the correct state: Table 1 remains anchored to the post-second-audit no-mask TRM-backed baseline sweep, 9x9 post-audit PPO provenance is complete and keeps `main.tex` unchanged, the confusing masked single-seed appendix artifact was removed and replaced with an audit-only withdrawal note, and the only live loose end is the non-paper `ppo_deep_unroll` masked-control rerun, currently around `13820 / 20000` in `tmux` session `hp_tuning_0a96c71`.
