# Persistent diagnostics paper alignment report

Date: 2026-08-03

Paper branch: `iclr-evidence-aligned-revision`

Paper parent commit: `bd72f7a1377c8602f7b2b2eae4a68dc5ee3612cf`

Code branch: `iclr-confirmatory-repair`

Current implementation commit: `e4c924cc721e9f4f356789eba03a09f6c8ca1913`

## Code evidence incorporated

The implementation now contains a strict schema-v5 persistent-checkpoint
diagnostic runner and a registered fixed protocol. It retains clock-complete
augmented occurrences `(x,y,z,h)`, computes exact one-step and Monte Carlo
K-step operator residuals at `n` and registered reference depths, checks the
production exact-baseline and deployment-distribution callbacks, measures
finite-depth/path/carry/clock diagnostics, and emits deterministic finite-batch
artifacts with source and dataset provenance.

Validation through the current implementation commit is:

- all 33 declared runtime targets passed 397/397 tests;
- the focused source/registration/lock gate passed 57/57 tests;
- the preceding combined focused gate passed 198/198 tests;
- the packaged Buck CLI executed all eight debug cells;
- type checking is not green: 21 type targets in the last full-graph audit retain
  pre-existing debt, including nine pre-existing errors in the `rl` target.

The earlier runner-specific report is
`CODE_REPO/reports/PERSISTENT_CHECKPOINT_DIAGNOSTICS_REPORT.md`. The newer
registration, evaluator, accounting, and source-binding changes are identified
by implementation commit `e4c924c` and the staged artifacts below.

## Paper corrections

The implemented value head concatenates the latent representation, instance
embedding, and current-plan embedding. The manuscript and diagrams therefore
now define it as

`V_psi: Z x X x Y -> R`

and use `V_psi(z,x,y)` in finite-reference, persistent, finite-horizon,
projection-anchor, and slow-drift statements. The latent Lipschitz condition
holds `(x,y)` fixed and is uniform over relevant instance-plan pairs. The text
states that the current head does not consume `h` directly; the edit clock is
still required for Markov transitions, termination, rewards, and Bellman
targets.

The diagnostic table and C3 registry now distinguish:

- exact one-step residuals from Monte Carlo K-step operator estimates and from
  realized-path TD errors;
- reconstructed exact-summation/recentering from saved training-time
  centering;
- finite-depth candidate discrepancy from the theorem's uniform
  `epsilon_A,cand`;
- a retained-state production distribution-callback comparison from a uniform
  deployment bound or a full episode-loop test.

The claim ledger and review matrix record the runner as introduced at code
commit `ac624cd`, hardened to schema 5 at `6400959`, and integrated with the
fail-closed confirmatory execution path at `e4c924c`. They do not promote any
learned result.

## Recovery and artifact state

The retained ten-commit code recovery bundle is:

`handoff/trm_bellman_iclr-confirmatory-repair.bundle`

SHA-256:

`22299bf3b7efcfad8dd8cc474c2813fbfbf6d92536b7c288711ed3205de7ab60`

`git bundle verify` passes. A fetch into a detached worktree at base commit
`6d5a241027fe72921d5fc039dd6a12434999088b` reproduces tree
`400d42e3395b26cea2e98bc60620bb8a9c5348d7`, exactly matching `8d79ba7`.
The bundle stops at `8d79ba7`; it does not contain the later execution changes
through `e4c924c` and is not a complete recovery bundle for the current code.
A separate full recovery bundle now reaches `e4c924c` and verifies as complete,
but its Git history contains identity metadata and is not anonymous-release-ready.

The paper artifact inventory records this bundle as implementation provenance
only. It remains incomplete and not anonymous-release-ready.

Current `main.tex` SHA-256 at this report update:

`f1f7bb567578dbf1b4a3ab1d7c3db4cfdf3acee8b6e7fb9f818a8239550344e7`

## Debug execution evidence

The debug lock index is
`results/confirmatory_locks/debug_seed9001/index.json`, SHA-256
`3b130e9441561f6ade7ffeba19780933f9ce27f5331874117c8952db6e641a5e`.
It binds producer commit `e4c924c`, registry hash, exact configuration layers,
effective-configuration hashes, and individual lock hashes for eight cells:
`B0_I00`, `Bz_I10`, `Bd_I01`, `Bt`, `Bb`, `I11`, `UPI_TRM`, and `TRM_PPO`.

The staged evidence manifest is
`artifacts/debug_smoke/seed9001/MANIFEST.json`, SHA-256
`056b98f4163aec9fede0d0b734006055b9f7b4bce2f21ee5edb8e107c73c63ca`.
Every cell uses debug seed 9001, records exactly 80 training environment
interactions in its compute snapshot, and evaluates 256 distinct records from
the immutable validation split. Each run retains evaluation metadata, one
ordered per-instance row per record, a row-derived summary, compute counters,
checkpoint hashes, and log hashes. The lock index, execution index, every run,
and the staged manifest declare `excluded_from_confirmatory=true`.

These artifacts verify configuration routing, exact counters, evaluation
policy selection, noncycling evaluation, and immutable publication. Their
success rates, returns, and between-cell differences are debug outcomes. They
are not bridge evidence, not an interaction-matched UPI--TRM/PPO result, and
not evidence that a learned checkpoint satisfies a theorem assumption.

## Evidence boundary

No reconstructible successful persistent checkpoint or confirmatory endpoint
exists in the code or paper repository. Eight debug checkpoints after 80
training interactions are staged solely to validate execution mechanics. The
hard 1,024/256/512 train/validation/test split and immutable manifests are
materialized at `8d79ba7`; this supplies diagnostic inputs but no successful
learned endpoint. Consequently:

- persistent learned-checkpoint diagnostics: not verifiable from supplied evidence
- historical training-time centering: not verifiable from supplied evidence
- historical exact-mixture deployment gap: not verifiable from supplied evidence
- one-factor bridge outcome: not verifiable from supplied evidence
- equal-interaction UPI-TRM/PPO outcome: not verifiable from supplied evidence

The executable matrix and debug locks exist, but the matrix status remains
`registered_not_authorized`. No confirmatory run is authorized.

## Paper validation

`git diff --check` passes. `artifacts/MANIFEST.json` parses with `jq`. Static
searches find no remaining two-input `V_psi(z,x)` definition or emphasized
variant of the required unsupported-status label.

No `latexmk`, `pdflatex`, `xelatex`, `lualatex`, or `tectonic` binary is
available on this host. Current PDF syntax, page count, reference state, font
status, and visual layout are not verifiable from supplied evidence. The
restored PDF predates these source changes and must not be described as a
current build.

## Next execution dependency

Checkpoint schema 5 and the current runtime bind the producer commit, embedded
source manifest, training seed, run ID, effective configuration, runtime,
initialization, parent lineage, and complete live-resume state. Exact-budget
PPO, per-instance output retention, the executable bridge/matched matrix, and
debug publication mechanics are closed. The remaining blockers are
confirmatory authorization and execution, successful-checkpoint persistent
diagnostics, real-CUDA resume equivalence, separate distilled-policy
evaluation, and a deterministic anonymous supplement rebuild.

No result was fabricated or inferred from an unexecuted experiment.
