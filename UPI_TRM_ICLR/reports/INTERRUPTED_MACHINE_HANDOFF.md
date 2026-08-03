# ICLR repair handoff

Date: 2026-08-03

This report distinguishes committed implementation and paper work from missing
scientific evidence.

## Repositories and branches

- Paper: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, baseline before this update `baf196b`.
- Code: `/home/buiksat/trm_bellman`, branch `iclr-confirmatory-repair`, commit
  `e61b173` (protocol implementation commit `8109978`).
- Protected NeurIPS tree: unchanged at tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376` with scoped tracked-file digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.

The paper repository contains a recovery copy of the six code commits at:

`handoff/trm_bellman_iclr-confirmatory-repair.patch.gz`

SHA-256:

`eb26b8cfe4d98fc1b0c6053d37339f705a9a1137e1652cdf27a04388ea14c2ce`

Apply it to a clone containing base commit `6d5a241027fe72921d5fc039dd6a12434999088b`:

```bash
git switch -c iclr-confirmatory-repair 6d5a241027fe72921d5fc039dd6a12434999088b
gzip -dc trm_bellman_iclr-confirmatory-repair.patch.gz | git am
```

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
and finite-batch augmented-state diagnostic utilities.

The former multi-update exact-mode ambiguity is resolved by the explicit
`fixed_base_exact` protocol. It collects from a sealed base policy, freezes the
base recurrent map, fits only the value head, optimizes one candidate policy
head, and evaluates the exact probability-space mixture without recursively
promoting it. Legacy behavior remains available but is not labeled exact.

The authoritative partitioned Buck gate passed all 310 declared runtime cases:
296 cases across 30 targets and 14 logging/checkpoint cases in isolation. The
isolation avoids a retained TPX parallel-teardown failure in which the test body
reported `OK`. All six known type-check targets and `git diff --check` passed.
Every failed or interrupted attempt is retained and hashed in the code report.

## Open scientific and implementation work

- No end-to-end persistent checkpoint diagnostic runner exists. Current
  utilities summarize supplied tensors, while the historical episodic runner
  resets the latent and omits the remaining-budget clock.
- No learned checkpoint is present in either repository. Historical persistent
  theorem-facing diagnostics are `not verifiable from supplied evidence`.
- `configs/iclr_confirmatory/` does not exist. The registered unique
  1,024/256/512 hard train/validation/test split has not been materialized or
  locked. The lone local 450/50 trivial corpus has incomplete builder
  provenance and cannot substitute for it.
- Persistent checkpoint diagnostics, the one-factor bridge, equal-interaction
  UPI-TRM/PPO comparison, projection cross-design, and second domain remain
  missing experiments.
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
