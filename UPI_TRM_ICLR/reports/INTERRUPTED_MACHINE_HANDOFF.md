# Interrupted machine handoff

Date: 2026-08-03

The machine was scheduled for removal before the full requested workflow could
finish. This report distinguishes committed work from missing work.

## Repositories and branches

- Paper: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, current pre-handoff commit `5c5d687`.
- Code: `/home/buiksat/trm_bellman`, branch `iclr-confirmatory-repair`, commit
  `5377a396a6d5f00f1d3b8248e1f9c40206482f24`.
- Protected NeurIPS tree: unchanged at tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376` with scoped tracked-file digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.

The paper repository contains a recovery copy of the three code commits at:

`handoff/trm_bellman_iclr-confirmatory-repair.patch.gz`

SHA-256:

`a8a31f5fe76ed29931be4253ec858029eb5c195bbf65713e35837f00cfeae01c`

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
- Current clean PDF build: 31 pages, SHA-256
  `f769d3abd252cc6b5518b0b7390ae41bf432e2594902226bd95acf9eb72cad74`.
  It had zero undefined citations, undefined references, fatal errors, or
  overfull boxes, and no detected Type 3 font object.

## Code work completed

See the code repository's `reports/ICLR_REPAIR_HANDOFF.md`. The implementation
now contains clock-complete replay, persistent exact centering, fixed-K segment
validation, exact live interaction budgets, schema-v3 resume, complete dataset
provenance, held-out CleanRL evaluation, PPO/DQN boundary fixes, seeded dataset
builders, and finite-batch augmented-state diagnostic utilities.

Static compilation and diff checks pass. The combined post-repair Buck batch
was interrupted before results were available. Do not describe the repair as
fully tested until the next machine runs the command in that report.

## Open scientific and implementation work

- An adversarial audit found that `is_theory_exact()` still overstates a
  multi-update training path. The fixed-snapshot theorem is conditional after
  the value update, but replay/value-policy identity across repeated exact-mode
  updates needs a deliberate design. The code handoff lists the two valid
  options. The paper must not call multi-step training theorem aligned before
  this is resolved.
- Persistent checkpoint diagnostics, the one-factor bridge, equal-interaction
  UPI-TRM/PPO comparison, projection cross-design, and second domain remain
  missing experiments.
- The registered minimum Sudoku matrix is at least 245 serial GPU-hours. No
  repaired learned-model run was started.
- Final proof/evidence/reproducibility reports, anonymous review bundle, GPT Pro
  review prompt, and final PDF copy were not completed after the code repair.

## Push status

Both GitHub pushes failed because this host could not resolve `github.com`.
Retry these commands from a networked machine:

```bash
git -C /home/buiksat/trm_bellman push -u origin iclr-confirmatory-repair
git -C /home/buiksat/UPI_TRM push -u origin iclr-evidence-aligned-revision
```

No result was fabricated or inferred from an unexecuted experiment.
