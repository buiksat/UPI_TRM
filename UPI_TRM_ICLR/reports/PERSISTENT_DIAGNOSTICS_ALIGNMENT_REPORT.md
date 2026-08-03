# Persistent diagnostics paper alignment report

Date: 2026-08-03

Paper branch: `iclr-evidence-aligned-revision`

Paper parent commit: `bd72f7a1377c8602f7b2b2eae4a68dc5ee3612cf`

Code branch: `iclr-confirmatory-repair`

Code commit: `6400959bb7932095e6f82b84a3619a73539fe193`

## Code evidence incorporated

The implementation now contains a strict schema-v5 persistent-checkpoint
diagnostic runner and a registered fixed protocol. It retains clock-complete
augmented occurrences `(x,y,z,h)`, computes exact one-step and Monte Carlo
K-step operator residuals at `n` and registered reference depths, checks the
production exact-baseline and deployment-distribution callbacks, measures
finite-depth/path/carry/clock diagnostics, and emits deterministic finite-batch
artifacts with source and dataset provenance.

The final code validation after the schema-v5 hardening is:

- 322 unique runtime cases across 33 non-logging targets after an isolated
  rerun of two cases whose combined invocation lost TPX result files despite
  both unittest bodies reporting `OK`;
- 22 passing logging/checkpoint cases in isolation;
- 344 total unique runtime cases, zero assertion failures;
- 48 passing focused schema/diagnostic cases;
- packaged CLI build passed;
- the full `rl` typecheck reports nine pre-existing errors outside the new
  files and no persistent-diagnostic error.

The authoritative code report is
`CODE_REPO/reports/PERSISTENT_CHECKPOINT_DIAGNOSTICS_REPORT.md`.

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
commit `ac624cd` and hardened to schema 5 at `6400959`. They do not promote any
learned result.

## Recovery and artifact state

The exact eight-commit code recovery bundle is:

`handoff/trm_bellman_iclr-confirmatory-repair.bundle`

SHA-256:

`52547a3a7dfebd1521b917be9adbf8abbe218203d2bdbabf96c8c07f59b893bd`

`git bundle verify` passes. A fetch into a detached worktree at base commit
`6d5a241027fe72921d5fc039dd6a12434999088b` reproduces tree
`a001d2c13dcd024f87e4d44d7eb910405817cf5d`, exactly matching `6400959`.

The paper artifact inventory records this bundle as implementation provenance
only. It remains incomplete and not anonymous-release-ready.

Current `main.tex` SHA-256:

`76566fab5aef995a8bdd5581d30cc2d4da237128a6c0d22cc858f6bcece4a660`

## Evidence boundary

No learned checkpoint exists in the code or paper repository. The hard
1,024/256/512 train/validation/test split and immutable manifests have not been
materialized. Consequently:

- persistent learned-checkpoint diagnostics: not verifiable from supplied evidence
- historical training-time centering: not verifiable from supplied evidence
- historical exact-mixture deployment gap: not verifiable from supplied evidence
- one-factor bridge outcome: not verifiable from supplied evidence
- equal-interaction UPI-TRM/PPO outcome: not verifiable from supplied evidence

The registry remains draft and no confirmatory run is authorized.

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

Checkpoint schema 5 now binds the producer commit, source blobs, training
seed, run ID, effective configuration, runtime, initialization, parent
lineage, and complete live-resume state. The next blocker is to materialize and
hash the registered hard splits. Then finish the bridge and matched-PPO
configuration matrix, run debug-only smokes on the reserved debug seeds, and
execute persistent diagnostics, the one-factor bridge, and the
equal-interaction comparison in that order.

No result was fabricated or inferred from an unexecuted experiment.
