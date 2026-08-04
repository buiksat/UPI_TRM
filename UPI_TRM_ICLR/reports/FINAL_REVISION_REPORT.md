# Final revision report

Date: 2026-08-03, America/Los_Angeles

## Repositories

- Paper repository: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, audited evidence snapshot
  `5b475631d237cc53fc1c8b49a0a076ed140d4694`.
- Implementation repository: `/home/buiksat/trm_bellman`, branch
  `iclr-confirmatory-repair`, commit
  `e4c924cc721e9f4f356789eba03a09f6c8ca1913`.
- Protected NeurIPS path: `UPI_TRM_NIPS`, tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376`, tracked-content digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.
  Its path-scoped status is clean and it was not modified.

## Build and tests

- All 33 declared implementation runtime targets passed: 397/397, with zero
  failures, timeouts, infrastructure failures, or build failures. Buck trace:
  `ce53bee3-4ede-412f-a196-0e96d77d3b91`.
- The last full static audit retains 21 pre-existing failing type targets,
  including nine pre-existing `rl` errors. Static checking is not green.
- The final `main.tex` SHA-256 is
  `f1f7bb567578dbf1b4a3ab1d7c3db4cfdf3acee8b6e7fb9f818a8239550344e7`.
- The paper cannot be rebuilt on this host because no TeX engine is installed.
  `build/main_iclr_final.pdf` does not exist. Current page count, references,
  fonts, and rendered layout are `not verifiable from supplied evidence`.

## Correctness repairs

The paper and implementation now use the clock-complete persistent state
`(x,y,z,h)`, preserve pre/post-unroll latent carry order, handle terminal and
absorbing transitions explicitly, and retain complete replay/checkpoint state.
The evaluator paths implement exact terminal masking, exact baseline
summation, exact probability-space mixture evaluation, full-rollout PPO
budgets, record-local deterministic evaluation, complete interaction/compute
counters, and fail-closed source/config/data/run identity.

Projection language now distinguishes formal contraction from empirical
clamping. The finite-reference theorem is locally self-contained. CPI needs
exact centering, finite candidate-policy bias, an exact pointwise mixture, and
one fixed MDP; the stronger uniform advantage-error premise is used only for
its stated sufficient bound. The optional persistent slow-drift result now
requires `n>=1`, avoiding its former zero denominator.

Independent proof audit status: **PASS**, with no surviving mathematical
finding. Independent claim audit found no unsupported active manuscript claim.

## Executed evidence

Execution order:

1. Reproduced the 101-row finite-MDP theorem-pipeline CSV and both paper-visible
   figures byte for byte; all seven boundary groups passed.
2. Reproduced the 26,686-check finite-horizon suite and 261,814-check stress
   suite byte for byte.
3. Prepared and committed eight debug locks before outcomes were inspected.
4. Ran all six bridge cells and both matched-comparison cells at debug seed
   `9001`, exactly 80 training interactions per cell, with one pass over 256
   unique validation records.
5. Staged all 2,048 per-instance debug rows, metadata, summaries, compute
   snapshots, and the execution index.

Every debug run is marked `excluded_from_confirmatory`. All eight solved
0/256 at this deliberately tiny budget. This is a negative, uninformative
smoke outcome and is not performance evidence. No confirmatory seed was run.
The registered confirmatory matrix remains unauthorized: ten seeds per cell,
80,000 interactions, six bridge cells, and two UPI--TRM/PPO cells.

## Evidence disposition

- The historical 57.4% persistent result remains an in-sample historical
  record. It is absent from the abstract and active comparison narrative.
- Historical PPO/A2C/DQN, projection factorial, and inferential claims remain
  historical or archived because checkpoints, ordered populations, exact
  interactions, or raw provenance are incomplete.
- The historical episodic endpoint retains its zero-success record, but its
  evaluated policy identity is `not verifiable from supplied evidence`.
- Exploratory, single-seed, underpowered, redundant, and unsupported studies
  are triaged in `EXPERIMENT_TRIAGE.md` and `ARCHIVED_EXPERIMENTS.md`, not used
  as active method evidence.

## Artifacts

- Claim/evidence ledger: `reports/CLAIM_EVIDENCE_LEDGER.md`.
- Run registry: `results/RUN_REGISTRY.jsonl`.
- Working artifact inventory: `artifacts/MANIFEST.json`; it intentionally
  remains `complete=false` and `anonymous_release_ready=false`.
- Debug lock index SHA-256:
  `3b130e9441561f6ade7ffeba19780933f9ce27f5331874117c8952db6e641a5e`.
- Staged debug manifest SHA-256:
  `056b98f4163aec9fede0d0b734006055b9f7b4bce2f21ee5edb8e107c73c63ca`.
- Standalone current-code recovery bundle SHA-256:
  `5a357c0caa118907426da517aa0a7dc8df4f980fbe38ae9f8a13d0a6035e5ed4`.
  It reproduces code tree `c1eeed790105ca63e77e937db794cdfa305e92a5`
  but is not anonymous because Git history retains identity metadata.

## Remaining blockers

1. Run persistent finite-batch diagnostics on a reconstructible successful
   checkpoint. Historical theorem-facing values remain
   `not verifiable from supplied evidence`.
2. Authorize, lock, and execute all 80 confirmatory Sudoku runs. The planning
   range is 280 to 760 GPU-hours, or 5.8 to 15.8 ideal days on both local GPUs.
3. Run the projection train/evaluation cross-design and a predeclared second
   verifier-guided domain.
4. Fix the anonymous-archive scanner false positive, stage or explicitly
   exclude debug checkpoints/logs, and produce two byte-identical anonymous
   supplements.
5. Build and visually inspect the current PDF with an ICLR-compatible TeX
   toolchain.

## Decision

Estimated ICLR status: **below threshold**. The theory and implementation
correctness are materially stronger, but the reviewers' decision-changing
scientific evidence is still missing: successful-checkpoint diagnostics, the
confirmatory bridge, and the equal-interaction UPI--TRM/PPO comparison.

No result was fabricated, inferred from an unexecuted experiment, or promoted
from the debug tier. The protected NeurIPS path was not modified.
