# UPI-TRM implementation and audit handoff

Date: 2026-08-17

## Repository heads

Paper repository:

- path: `/home/buiksat/UPI_TRM`
- branch: `iclr-evidence-aligned-revision`
- head before this handoff update:
  `265771ca48355e97b8e8611cc260d51e921ac691`
- only `handoff.md` changed; paper source and PDF were not edited

Implementation repository:

- path: `/home/buiksat/trm_bellman`
- branch: `full-implementation`
- head: `75a157cff500abce0f9afe142c33ff10d4775c48`
  (`Harden policy improvement evidence loading`)
- parent: `88e4cf1be1bd9ecceb0ec9ba19ae468851e69a0a`
  (`Add authenticated full run and theory bridge`)
- implementation worktree: clean
- tree: `b1c1e63d9e7e5b01429899ba1664b24eac4619f0`

The paper and implementation remain separate Git repositories. Do not move the
implementation into the paper repository during this evidence cycle. Source
authorization binds the implementation repository root and Git commit.

## Paper status

The paper source, PDF, theorem statements, algorithms, bibliography, and claims
were not changed.

- source: `UPI_TRM_ICLR/main.tex`
- PDF: `UPI_TRM_ICLR/main.pdf`
- PDF SHA-256:
  `9d59bc486b975c08a055e2393d057bbf11f9eb7b06826edfeeecbf1aed4857ae`

No Stage 1-3 outcome, learned-task result, or empirical claim was produced.

## Implementation history

Commit `88e4cf1` added the authenticated full-run backend, theory bridge,
pre-outcome amendment, non-smoke checkpoint resume and evaluation, immutable
publication, retry history, and owned Buck targets.

Commit `75a157c` adds the checkpoint evidence security boundary:

1. Authenticated checkpoint bytes are copied into write-sealed memfds only
   after the complete generation, result, manifest, model-state, validation,
   lineage, amendment, and `TEST_OPEN` metadata have authenticated.
2. Semantic validators receive sealed descriptors, not caller-controlled
   checkpoint paths.
3. Evidence checkpoint deserialization uses `torch.load(weights_only=True)`.
4. The dynamic Torch allowlist is isolated to eight reviewed entries during
   each load. The 74 ambient grants installed by `import torch` are removed for
   the load and restored afterward.
5. The compatibility loader supports the two first-party replay dataclasses and
   exact NumPy array/dtype constructors observed in the pre-cleanup checkpoint
   corpus.
6. Producer source manifests are versioned. Historical v1 manifests bind 92
   sources; current v2 manifests bind 93, including the checkpoint allowlist.
7. The launcher derives the highest inventory version satisfied by a clean Git
   tree and rejects manifest downgrades.
8. The general audit, full runtime, theory evaluator, PPO loader, and UPI loader
   share the same sealing and data-only deserialization boundary.

Commit statistics:

- 27 files changed
- 3,794 insertions, 374 deletions
- four new files:
  - `policy_improvement_checkpoint_allowlist.py`
  - `policy_improvement_sealed_evidence.py`
  - `tests/test_policy_improvement_checkpoint_allowlist_unittest.py`
  - `tests/test_policy_improvement_sealed_evidence_unittest.py`
- binary diff SHA-256 against `88e4cf1`:
  `7d16d37fc6b3ed7207fde87f77d03fc4606ee46c7edcb895b795c1ca5ae743b7`
- cumulative binary diff SHA-256 against `859f2ca`:
  `40c3efb02b3f776d10a1a4b3f7a1b035b7b12f8d025bc13cbcf99533b342df3e`

## Current-head validation

### Runtime gate

Command shape:

```bash
buck2 test --local-only @fbcode//mode/opt \
  fbcode//buiksat_trm:test_phase4_figure_publication \
  fbcode//buiksat_trm:test_phase4_reporting \
  fbcode//buiksat_trm:test_phase4_runtime_launcher \
  fbcode//buiksat_trm:test_policy_dataset_builder \
  fbcode//buiksat_trm:test_policy_improvement_audit \
  fbcode//buiksat_trm:test_policy_improvement_checkpoint_allowlist \
  fbcode//buiksat_trm:test_policy_improvement_checkpoint_validator \
  fbcode//buiksat_trm:test_policy_improvement_evidence \
  fbcode//buiksat_trm:test_policy_improvement_full_backend \
  fbcode//buiksat_trm:test_policy_improvement_full_runtime \
  fbcode//buiksat_trm:test_policy_improvement_sealed_evidence \
  fbcode//buiksat_trm:test_policy_improvement_smoke_checkpoint \
  fbcode//buiksat_trm:test_policy_improvement_smoke_runtime \
  fbcode//buiksat_trm:test_policy_improvement_theory_bridge \
  fbcode//buiksat_trm:test_policy_improvement_v1 \
  fbcode//buiksat_trm:test_run_identity \
  fbcode//buiksat_trm:test_upi_trm_logging_smoke \
  fbcode//buiksat_trm:test_upi_trm_trainer_smoke \
  -- --env UPI_TRM_HISTORICAL_CHECKPOINT_ROOT=<three pre-cleanup roots> \
  --env UPI_TRM_HISTORICAL_CHECKPOINT_COUNT=35
```

Result:

- exit code: 0
- targets: 18
- passed tests: 464
- failures, timeouts, fatal errors, skips, infrastructure failures, and build
  failures: 0
- test run:
  `https://www.internalfb.com/intern/testinfra/testrun/14073749025919558`
- log: `/tmp/codex_final_runtime_gate_rerun2.log`
- log SHA-256:
  `55be5ab39757673fc30df4eb8bd62d2b99e4cd6d18246ca66c96e9d167c70ba0`

Before the obsolete evidence directories were deleted, the gate data-only
loaded all 35 checkpoints that were present across those roots. That was a
loader-compatibility check only. Those checkpoints came from experiments the
user has since declared invalid and are no longer retained.

### Type, manifest, and static gates

- affected type gate: 56 targets, exit 0
- target inventory: `/tmp/upitrm_type_gate_targets.txt`
- type log: `/tmp/codex_final_type_gate.log`
- type log SHA-256:
  `c1dfa8a0c67372dac0403496eeb3328bc223399c5fa7805524457c3330b3a0d1`
- producer-manifest regeneration: byte-identical after commit, 93 sources
- `git diff --check`: exit 0 before commit
- focused Python compilation for the launcher authorization fix: exit 0
- clean synthetic v1 launcher authorization: exit 0
- clean synthetic v1 audit source authentication: exit 0
- clean committed v2 launcher authorization: exit 0
- direct v1-on-v2 downgrade regression: rejected as required

### Optimized PARs

All six optimized PAR builds exited 0. Build log:
`/tmp/codex_final_par_build.log`, SHA-256
`a638cd4420ca6122e4b1146e2eb9efb35241f35b6409764a95031e6c3805b9c0`.

```text
launcher  d1dffbdf7c64ab07ca3f55b5514e3d40ad14db09c2edb9ae17f0caa9f8004baa
training  dccc93b577fde350a26071613124ec884bbffc550cfabf760e1759462e3cdb31
full      97f238bec61ef32cf7421fba27bf8fca2dd475e3f2130309f8c70cfd744fb9ea
theory    d2ef328fd5f1190b3467fcb244ad3119b248420d07fec8832256e69ffd1cb715
audit     b6c6464dfebbc8b649868023b62360d005462c59acad9387d14769de9905977a
analysis  518ead315392db7bdbc872e66fbf17f530bc4be068ef039c9269964ebc191501
```

## Current source identities

Producer manifest:

- schema: v2
- sources: 93
- raw/authenticated SHA-256:
  `6a1aef8e48d6ff4e0cfae243bb108a389bee0228f1d7266492983af275400c5f`

Source profiles:

```text
full      127347cdb8257a414ab12953687625ca85c28805f197060f2b2f176e5b63a97a  100 paths
theory    6b77831569d87786a923f5abd1407e8f6917ea57aa5d57995c5fdd976dcfbf24  102 paths
audit     27f845bcacc0c8166e3772cce8736f87e0a24a78a5f0d46c4722566052af671f  105 paths
analysis  4055d6e6b78a67ca84f3e8967fdb304528dfd152175845c6d40a8238fa0a0fc7  106 paths
```

Canonical registered identities remain:

```text
protocol          583e99828d877f9a33503e84af58f1ccb8aa643f7ecc5baa826d6662de6a48b2
base registry     6f618e6f3db0b60079ffc41d37982b781a9ff22a2ddab512c36e44db84a162f6
theory amendment  6127ec9cdf5a774bd5b05248d2804cbecc6c847c851d339ea593ca5f3d40bd6c
```

Every previous current-head runtime authorization is obsolete because the Git
commit, producer manifest, source profiles, and PAR hashes changed. No new
authorization directory was created during this final fix.

## Experiment evidence status

The paper changed, and the user declared the old experiments incorrect and no
longer relevant. Their producer checkouts, authorizations, evidence packages,
reconstructed audit package, and old logs were therefore removed. They must not
be cited, audited, or used as a baseline for the revised paper.

No canonical Stage 0 package exists for the revised experiment. The next
experiment cycle must start from commit `75a157c`, a new runtime authorization,
and newly generated Stage 0 smoke evidence.

## Removed external directories

The following eight obsolete directories were permanently deleted at the
user's request. They are not recoverable from Trash.

```text
/home/buiksat/upi-trm-policy-audit-859f2ca.myImeqnx
/home/buiksat/upi-trm-policy-auth-2d43263f.MjSzspvD
/home/buiksat/upi-trm-policy-auth-5e8801b1.bAjbAlMP
/home/buiksat/upi-trm-policy-authorizations
/home/buiksat/upi-trm-policy-evidence-2d43263f.Erh9bSVz
/home/buiksat/upi-trm-policy-evidence-owner
/home/buiksat/upi-trm-producer-2d43263
/home/buiksat/upi-trm-producer-c67bea28
```

Approximately 2.7 GB was reclaimed. `/home/buiksat/UPI_TRM` and
`/home/buiksat/trm_bellman` were not deleted or moved.

## Test-split disclosure

An old, now-retired audit attempt eagerly opened local test arrays before
`TEST_OPEN`. No values were manually inspected or reported. That evidence was
deleted with the invalid experiment artifacts.

Current code authenticates test metadata without opening files below the test
directory until an authenticated `TEST_OPEN` record exists. Do not claim the
entire repair session avoided opening the test split. Do claim only that the
committed implementation prevents the premature open.

## Remaining blockers and debt

1. Generate a new runtime authorization for commit `75a157c` before launching
   any policy role for the revised experiment.
2. Generate fresh Stage 0 smoke evidence under the selected current runtime.
   Do not reconstruct or reuse the deleted experiments.
3. The eight-entry data-only allowlist remains a standing compatibility grant.
   A malicious data-only payload can also request excessive tensor or array
   allocation. File sealing bounds bytes, not expanded memory.
4. `TEST_OPEN` remains an owner-writable singleton rather than an append-only or
   WORM ledger. Deletion can erase evidence of an earlier open.
5. A crash or `SIGKILL` before failed-attempt publication remains
   indistinguishable from no attempt without an external append-only ledger.

## Required next actions

1. Push or transfer implementation commit `75a157c`.
2. Generate one runtime authorization naming `75a157c` and the hashes above.
3. Run a new Stage 0 smoke cycle for the revised experiment. Do not run Stage
   1-3 or open the test split.
4. Audit the new Stage 0 package. Require stdout to contain exactly one
   canonical JSON document, then verify
   4 expected rows, 4 complete rows, 0 failed rows, 10 per-instance artifacts,
   8 semantic checkpoint validations, and `test_open=false`.
5. Do not run Stage 1-3 until that audit is green and the pre-outcome amendment
   remains committed.

## Claude review prompt

```text
Review implementation commit 75a157cff500abce0f9afe142c33ff10d4775c48
in /home/buiksat/trm_bellman against parent
88e4cf1be1bd9ecceb0ec9ba19ae468851e69a0a. Also inspect the cumulative
implementation from 859f2cab5e89f30a7a70f1ff4b18567f55cb3252 when needed.

Read /home/buiksat/UPI_TRM/handoff.md. Treat all paper source and PDF files as
read-only. Do not run Stage 1-3, open the test split, train a learned run, edit
the paper, or make empirical claims. Review only unless explicitly asked to fix
a verified blocker.

Use adversarial default-reject verification. Reproduce each candidate and
report only survivors with file:line anchors. Focus on:

1. Sealed-descriptor ownership and cleanup across every success and exception
   path.
2. Complete-generation authentication before any checkpoint loader runs.
3. Exact isolation and restoration of Torch dynamic safe globals.
4. Safety and necessity of all eight allowlisted globals, including NumPy
   object-dtype and resource-expansion cases.
5. Producer manifest v1/v2 anti-downgrade behavior through the real
   authorize_phase4_training_source path, not only selector helpers.
6. Manifest v1 regression compatibility and current v2 source completeness.
7. Evidence deserialization closure, including import aliases and indirect
   loader references.
8. Preservation of runtime authorization, amendment, TEST_OPEN, immutable
   publication, retry-history, and no-source-fallback contracts.

Validation evidence:

- runtime gate: 18 targets, 464 passed, exit 0;
- type gate: 56 targets, exit 0;
- pre-cleanup checkpoint loader compatibility: 35/35;
- optimized launcher/training/full/theory/audit/analysis PAR builds: exit 0;
- implementation diff SHA-256 against 88e4cf1:
  7d16d37fc6b3ed7207fde87f77d03fc4606ee46c7edcb895b795c1ca5ae743b7.

The old experiment evidence was deleted after the user declared it invalid.
Review the implementation only. Do not quote any old row, artifact, or metric
counts as evidence for the revised paper.

Return blocking findings first, then concerns checked and cleared, additional
smoke-only tests, and the safest path forward. Include no experiment results or
paper claims.
```

## Current status

- implementation security fix: committed at `75a157c`
- implementation worktree: clean
- full learned backend: connected and smoke-tested; no full learned run executed
- theory bridge: implemented and smoke-tested; no scientific evaluation run
- pre-outcome amendment: committed
- Stage 1-3: not run
- paper claims: unchanged
- runtime/type gates: green
- revised-experiment Stage 0: not run
- experiment status: incomplete
