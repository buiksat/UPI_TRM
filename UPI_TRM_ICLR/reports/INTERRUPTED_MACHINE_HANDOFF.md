# ICLR repair handoff

Date: 2026-08-03

This report distinguishes committed implementation and paper work from missing
scientific evidence.

## Repositories and branches

- Paper: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, audited evidence snapshot
  `5b475631d237cc53fc1c8b49a0a076ed140d4694`. The closeout report follows
  without changing the audited manuscript.
- Code: `/home/buiksat/trm_bellman`, branch `iclr-confirmatory-repair`, commit
  `e4c924cc721e9f4f356789eba03a09f6c8ca1913`. Earlier milestones include
  protocol implementation `8109978`, persistent diagnostic runner `ac624cd`,
  schema-v5 identity hardening `6400959`, corpus builder `94a7199`, and
  materialized corpus `8d79ba7`.
- Protected NeurIPS tree: unchanged at tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376` with scoped tracked-file digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.

The paper repository contains an exact historical Git bundle for the ten code
commits ending at `8d79ba79917a7be8b14540bedb600f51076738c7` at:

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
matching code commit `8d79ba7`. This bundle does not contain the later code
work through `e4c924c`, including the exact-budget runner, registered cell
configs, source-identity checks, lock tooling, or debug executions. Do not use
it as recovery media for the current implementation. The older `.patch.gz`
file is retained only as the prior six-commit recovery artifact; it does not
contain the diagnostic runner or schema-v5 commit.

A separate standalone recovery bundle now contains the complete current code
history through `e4c924cc721e9f4f356789eba03a09f6c8ca1913`:

`handoff/trm_bellman_iclr-confirmatory-repair_e4c924c_full.bundle`

Its SHA-256 is
`5a357c0caa118907426da517aa0a7dc8df4f980fbe38ae9f8a13d0a6035e5ed4`
and its size is 91,779,510 bytes. `git bundle verify` reports complete history.
Fetching it into an empty repository reproduces commit `e4c924c` and tree
`c1eeed790105ca63e77e937db794cdfa305e92a5`. This is a recovery artifact, not
an anonymous supplement: Git history retains author, committer, email, and
host metadata. A release archive must use a history-free staged source tree or
an independently anonymized history.

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

Post-bundle implementation work now also provides:

- exact training-interaction budgets and exact optimizer/update counters;
- immutable schema-3 per-instance evaluation artifacts with semantic Sudoku
  validation and no implicit cycling;
- executable, fail-closed configs for every registered bridge and matched-PPO
  cell;
- deterministic held-out evaluation that restores Python, NumPy, Torch CPU,
  Torch CUDA, environment, and sampler RNG state;
- persistent exact-mixture evaluation, with the carried latent and remaining
  clock preserved between edits;
- a one-factor deployment bridge in which `B0` and `Bd` share the same
  pre-interpolation base/candidate snapshots and differ only in deployed
  policy evaluation;
- a registered-matrix validator that reconstructs the full effective config
  and rejects seed, run-ID, dataset, schedule, architecture, or config-layer
  drift;
- a producer-source manifest embedded in the Buck PAR and rechecked before
  and after artifact publication.

At the historical `8d79ba7` bundle boundary, the authoritative partitioned
Buck gate covered all 344 declared runtime cases: 322 cases across 33
non-logging targets and 22 logging/checkpoint cases in isolation. A combined
invocation recorded 320 passes and lost two TPX result files even though both
unittest bodies reported `OK`; the isolated target rerun passed all 31 cases.
The focused schema/diagnostic gate passed 48 cases. For the post-bundle work,
the latest invocation of all 33 declared runtime targets passed 397 of 397
tests. The focused source/registration/lock suite passed 57 of 57, and the
preceding combined focused suites passed 198 of 198. Twenty-one type targets
retain pre-existing debt in the last full-graph audit; the full `rl` typecheck
has the same nine pre-existing errors outside the changed files. No newly
introduced schema-v5 or policy-pair type error remains. See
`POST_REPAIR_RUNTIME_TEST_REPORT.md`. `git diff --check` passed. Every failed
or interrupted attempt is retained in the code reports.

## Debug matrix execution

The complete eight-cell seed-`9001` debug matrix passed preflight and executed
at code commit `e4c924cc721e9f4f356789eba03a09f6c8ca1913`:

`B0_I00`, `Bz_I10`, `Bd_I01`, `Bt`, `Bb`, `I11`, `UPI_TRM`, and `TRM_PPO`.

Each run used exactly 80 training environment interactions and evaluated the
same 256-record validation split once. Evaluation used 16 edits per record,
or 4,096 evaluation interactions per cell, outside the training budget. These
runs are debug-only pipeline smokes with seed `9001`; all are marked
`excluded_from_confirmatory`. All eight recorded zero solved validation
instances, which is expected to be uninformative at an 80-interaction training
budget and is not performance evidence.

The preflight lock index is:

`results/confirmatory_locks/debug_seed9001/index.json`

SHA-256:

`3b130e9441561f6ade7ffeba19780933f9ce27f5331874117c8952db6e641a5e`

The staged debug evidence manifest is:

`artifacts/debug_smoke/seed9001/MANIFEST.json`

SHA-256:

`056b98f4163aec9fede0d0b734006055b9f7b4bce2f21ee5edb8e107c73c63ca`

That manifest records every staged evaluation file hash plus the external log
and checkpoint hashes. The staged tree contains the execution index,
evaluation metadata, compute snapshots, 2,048 per-instance rows, and
summaries. The checkpoint and
log bytes remain outside this paper repository; only their hashes are retained
here, so the top-level artifact inventory remains incomplete and is not an
anonymous release bundle.

The code run matrix remains `registered_not_authorized`. No confirmatory seed
was trained, and no debug outcome may enter a confirmatory comparison.

## Open scientific and implementation work

- No reconstructible historical persistent checkpoint exists from which to
  produce a diagnostic bundle. The hard held-out manifest exists at
  `8d79ba7`, but historical persistent theorem-facing diagnostics remain
  `not verifiable from supplied evidence`.
- No learned checkpoint is tracked in either repository. The external
  80-interaction debug checkpoint hashes are retained in the staged manifest,
  but no theorem-facing diagnostic has been run on those pipeline-smoke
  checkpoints.
- `configs/iclr_confirmatory/persistent_diagnostics.json` registers the
  diagnostic protocol. The unique 1,024/256/512 hard train/validation/test
  split is materialized, byte-rebuilt, and locked by manifest hashes.
- Learned persistent diagnostic outputs, the confirmatory one-factor bridge,
  the confirmatory equal-interaction UPI-TRM/PPO comparison, projection
  cross-design, and second domain remain missing experiments.
- Checkpoint run identity, raw dataset materialization, exact-budget PPO,
  per-instance evaluation artifacts, executable cell configs, source binding,
  and debug lock execution are no longer implementation blockers.
- Confirmatory execution still requires an explicit registry authorization,
  complete pre-run locks at the final code commit, and sufficient compute.
  The current host exposes two NVIDIA GPUs, each with 81,920 MiB. No paid cloud
  allocation is authorized. The historical planning range for the 80-run
  registered Sudoku matrix is 280 to 760 GPU-hours.
- No repaired learned-model confirmatory run was started. The completed
  80-interaction jobs are debug smokes only.
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
