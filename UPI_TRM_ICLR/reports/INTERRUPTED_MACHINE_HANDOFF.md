# ICLR repair handoff

Date: 2026-08-03

This report distinguishes committed implementation and paper work from missing
scientific evidence.

## Repositories and branches

- Paper: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, baseline before this update `baf196b`.
- Code: `/home/buiksat/trm_bellman`, branch `iclr-confirmatory-repair`, commit
  `ac624cda806b455c2ec191bc90718fc084ecc7bd` (protocol implementation commit
  `8109978`; persistent diagnostic runner commit `ac624cd`).
- Protected NeurIPS tree: unchanged at tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376` with scoped tracked-file digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.

The paper repository contains an exact Git bundle for the seven code commits at:

`handoff/trm_bellman_iclr-confirmatory-repair.bundle`

SHA-256:

`5a3a9aea4237dc4f7bbd1edc212abdbf0291ada60004c174e71e8b23f75a90c0`

Fetch it into a clone containing base commit
`6d5a241027fe72921d5fc039dd6a12434999088b`:

```bash
git fetch trm_bellman_iclr-confirmatory-repair.bundle \
  refs/heads/iclr-confirmatory-repair:refs/heads/iclr-confirmatory-repair-recovered
git switch iclr-confirmatory-repair-recovered
```

`git bundle verify` passes, and fetching into a detached worktree at the base
commit reproduces tree `4ed3d025eb97e1eed0dd671952bf980102c81da2`, exactly
matching code commit `ac624cd`. The older `.patch.gz` file is retained only as
the prior six-commit recovery artifact; it does not contain the diagnostic
runner commit.

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
exact live interaction budgets, schema-v4 resume, complete dataset provenance,
held-out CleanRL evaluation, PPO/DQN boundary fixes, seeded dataset builders,
and a registered finite-batch persistent-checkpoint diagnostic runner.

The former multi-update exact-mode ambiguity is resolved by the explicit
`fixed_base_exact` protocol. It collects from a sealed base policy, freezes the
base recurrent map, fits only the value head, optimizes one candidate policy
head, and evaluates the exact probability-space mixture without recursively
promoting it. Legacy behavior remains available but is not labeled exact.

The authoritative partitioned Buck gate passed all 325 declared runtime cases:
311 cases across 31 targets and 14 logging/checkpoint cases in isolation. The
isolation avoids a retained TPX parallel-teardown failure in which the test body
reported `OK`. The focused diagnostic runtime plus packaged CLI typecheck
passed 16 cases. The full `rl` typecheck retains nine pre-existing errors
outside the diagnostic files; no new diagnostic type error remains.
`git diff --check` passed. Every failed or interrupted attempt is retained and
hashed in the code report.

## Open scientific and implementation work

- The strict persistent checkpoint runner exists at code commit `ac624cd`, but
  no learned checkpoint or hard held-out manifest exists from which to produce
  a diagnostic output bundle.
- No learned checkpoint is present in either repository. Historical persistent
  theorem-facing diagnostics are `not verifiable from supplied evidence`.
- `configs/iclr_confirmatory/persistent_diagnostics.json` registers the
  diagnostic protocol. The unique 1,024/256/512 hard
  train/validation/test split has not been materialized or locked. The lone
  local 450/50 trivial corpus has incomplete builder provenance and cannot
  substitute for it.
- Learned persistent diagnostic outputs, the one-factor bridge,
  equal-interaction UPI-TRM/PPO comparison, projection cross-design, and second
  domain remain missing experiments.
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
