# Interrupted machine handoff

Date: 2026-08-03

The machine was scheduled for removal before the full requested workflow could
finish. This report distinguishes committed work from missing work.

## Repositories and branches

- Paper: `/home/buiksat/UPI_TRM`, branch
  `iclr-evidence-aligned-revision`, current pre-handoff commit `5c5d687`.
- Code: `/home/buiksat/trm_bellman`, branch `iclr-confirmatory-repair`, commit
  `111e3a96655d1b3414ba15801a3ebfa393e8e394`.
- Protected NeurIPS tree: unchanged at tree
  `8dc95739b9830a75409af3d89ba86ac174ae1376` with scoped tracked-file digest
  `32e7967b973bffe2858d340fa793177c298796937790d17ca1463ce7b636cdab`.

The paper repository contains a recovery copy of the four code commits at:

`handoff/trm_bellman_iclr-confirmatory-repair.patch.gz`

SHA-256:

`e73a2e6d38df9204f25f07fe5e628a9b89407a50ab28839ee5d7fc0b02e6b071`

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

Static compilation and diff checks pass. The final focused Buck set passed 120
of 121 tests, exposed one PPO boundary-check `NameError`, and then passed the
complete 12-test CleanRL target after that fix. No focused failure remains.
The next machine still needs to rerun all declared targets before calling the
repair fully validated.

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
