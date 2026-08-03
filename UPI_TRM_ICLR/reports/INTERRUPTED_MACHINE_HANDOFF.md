# ICLR repair handoff

Date: 2026-08-03

This report distinguishes committed implementation and paper work from missing
scientific evidence.

## Repositories and branches

- Paper: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, baseline before this update `baf196b`.
- Code: `/home/buiksat/trm_bellman`, branch `iclr-confirmatory-repair`, commit
  `8d79ba79917a7be8b14540bedb600f51076738c7` (protocol implementation commit
  `8109978`; persistent diagnostic runner commit `ac624cd`; schema-v5 identity
  hardening commit `6400959`; corpus builder `94a7199`; materialized corpus
  `8d79ba7`).
- Protected NeurIPS tree: unchanged at tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376` with scoped tracked-file digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.

The paper repository contains an exact Git bundle for the ten code commits at:

`handoff/trm_bellman_iclr-confirmatory-repair.bundle`

SHA-256:

`22299bf3b7efcfad8dd8cc474c2813fbfbf6d92536b7c288711ed3205de7ab60`

Fetch it into a clone containing base commit
`6d5a241027fe72921d5fc039dd6a12434999088b`:

```bash
git fetch trm_bellman_iclr-confirmatory-repair.bundle \
  refs/heads/iclr-confirmatory-repair:refs/heads/iclr-confirmatory-repair-recovered
git switch iclr-confirmatory-repair-recovered
```

`git bundle verify` passes, and fetching into a repository containing the base
commit reproduces tree `400d42e3395b26cea2e98bc60620bb8a9c5348d7`, exactly
matching code commit `8d79ba7`. The older `.patch.gz` file is retained only as
the prior six-commit recovery artifact; it does not contain the diagnostic
runner or schema-v5 commit.

## Paper work completed

- Restricted formal results to finite/countable closures and repaired the
  general-kernel discussion.
- Fixed the absorbing anchor boundary, projection language, CPI assumptions,
  strictness condition, persistent clock quantifiers, and clock-complete
  Algorithm 1.
- Added proof-audited finite-horizon residual/CPI results and a
  deployment-perturbation theorem.
- Removed unsupported historical performance and factorial tables from the
  active evidence narrative.
- Reproduced the finite-MDP theorem pipeline, including 101 primary rows and
  boundary checks.
- Created claim/evidence, historical provenance, experiment triage,
  confirmatory registry, compute estimate, and run-registry reports.
- A pre-current-edit source state was reported to build at 31 pages with zero
  undefined citations, undefined references, fatal errors, or overfull boxes.
  The current fixed-base wording has not been rebuilt because this host no
  longer has a TeX engine. See `POST_FIXED_BASE_PAPER_BUILD_ATTEMPT.md`; do not
  treat the restored stale PDF as the current source build.

## Code work completed

See the code repository's `reports/ICLR_REPAIR_HANDOFF.md` and
`reports/POST_HANDOFF_EXECUTION_REPORT.md`. The implementation now contains
clock-complete replay, persistent exact centering, fixed-K segment validation,
exact live interaction budgets, schema-v5 confirmatory resume, complete dataset provenance,
held-out CleanRL evaluation, PPO/DQN boundary fixes, seeded dataset builders,
and a registered finite-batch persistent-checkpoint diagnostic runner.

Schema 5 binds explicit run/seed/config/source/runtime/initialization and parent
lineage, validates all state on shadow objects before live mutation, records
actual optimizer-step counters, and publishes checkpoints atomically without
overwrite. Schema 3 and 4 remain historical formats and are rejected for new
`fixed_base_exact` confirmatory runs.

The former multi-update exact-mode ambiguity is resolved by the explicit
`fixed_base_exact` protocol. It collects from a sealed base policy, freezes the
base recurrent map, fits only the value head, optimizes one candidate policy
head, and evaluates the exact probability-space mixture without recursively
promoting it. Legacy behavior remains available but is not labeled exact.

The authoritative partitioned Buck gate covers all 344 declared runtime cases:
322 cases across 33 non-logging targets and 22 logging/checkpoint cases in
isolation. A combined invocation recorded 320 passes and lost two TPX result
files even though both unittest bodies reported `OK`; the isolated target
rerun passed all 31 cases. The focused schema/diagnostic gate passed 48 cases.
The full `rl` typecheck retains nine pre-existing errors outside the changed
files; no schema-v5 type error remains.
`git diff --check` passed. Every failed or interrupted attempt is retained and
hashed in the code report.

## Open scientific and implementation work

- The strict persistent checkpoint runner exists at code commit `6400959`, but
  no learned checkpoint exists from which to produce a diagnostic output
  bundle. The hard held-out manifest now exists at `8d79ba7`.
- No learned checkpoint is present in either repository. Historical persistent
  theorem-facing diagnostics are `not verifiable from supplied evidence`.
- `configs/iclr_confirmatory/persistent_diagnostics.json` registers the
  diagnostic protocol. The unique 1,024/256/512 hard train/validation/test
  split is materialized, byte-rebuilt, and locked by manifest hashes. The
  strict diagnostic provenance file still awaits the locked environment and
  action-mask configuration.
- Learned persistent diagnostic outputs, the one-factor bridge,
  equal-interaction UPI-TRM/PPO comparison, projection cross-design, and second
  domain remain missing experiments.
- Checkpoint run identity and raw dataset materialization are no longer the
  next dependencies. Exact-budget PPO, per-instance evaluation artifacts,
  executable cell configs, and the final registry lock now block debug smokes.
- The registered minimum Sudoku matrix is at least 245 serial GPU-hours. No
  repaired learned-model run was started.
- Final proof/evidence/reproducibility reports, an anonymous supplement, and a
  final evidence-aligned PDF remain incomplete.

## Push status

Both GitHub pushes failed because this host could not resolve `github.com`.
Retry these commands from a networked machine:

```bash
git -C /home/buiksat/trm_bellman push -u origin iclr-confirmatory-repair
git -C /home/buiksat/UPI_TRM push -u origin iclr-evidence-aligned-revision
```

No result was fabricated or inferred from an unexecuted experiment.
