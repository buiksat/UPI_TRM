# UPI-TRM machine-transfer handoff

Date: 2026-08-16

## Current repository heads

Paper:

- path: `/home/buiksat/UPI_TRM`
- branch: `iclr-evidence-aligned-revision`
- source/PDF commit: `a539e6f75e6da1ca7a09deade2e014f9d2d253b5`
  (`Keep deployment proof QED with final display`)
- this handoff will be the next documentation-only commit

Implementation:

- path: `/home/buiksat/trm_bellman`
- branch: `full-implementation`
- current head: `859f2ca` (`Keep policy audit output canonical`)
- parent: `5e8801b` (`Preserve GPU kernels in policy audit runtimes`)
- smoke producer commit: `2d43263f394e98c62a2167bde0a3e55e217898d0`
  (`Bind successful retries to authenticated failure history`)

Both branches contain local commits that were not pushed during this session.
Push them or transfer the repositories before discarding this machine.

## Completed repair commits

Implementation commits created during this repair:

1. `2bd5615` - atomic Phase 4 generation-directory publication and tests.
2. `a3ca1ca` - exact float64 finite-MDP sanity suite.
3. `7317d7011c31ac622c0723d22cf9f4bb0571bdf1` - registered
   `policy_improvement_v1` protocol, schemas, registry, smoke and fail-closed
   full-runtime infrastructure.
4. `74d5b4932501c266ab69ddd74015e3124885914e` - frozen dataset identities.
5. `3fbba51e3525d74503591af17ab5d23e07b6c740` - fixed Stage 0 trainer
   identity serialization.
6. `c67bea28b16b8260925e979ff2f6fd9d5d00129c` - bound the Stage 0 exact
   baseline checker.
7. `2d43263f394e98c62a2167bde0a3e55e217898d0` - bound successful retries
   to authenticated failed-attempt history and closed Git replacement-ref
   substitution.
8. `5e8801b1fe546fdc1c33b1d066cedde212fddfa8` - retained CUDA kernel
   sections in the audit and analysis PARs.
9. `859f2ca` - suppressed checkpoint progress output during audit restores so
   the audit emits one canonical JSON document on stdout.

Paper commit:

- `a539e6f75e6da1ca7a09deade2e014f9d2d253b5` - adds `\qedhere` to the
  final Theorem F.5 display and regenerates the tracked PDF.

The theorem text, constants, domains, Algorithms 1-2, checkpoint semantics,
replay semantics, and exact-mixture semantics were not changed.

## Canonical paper artifact

- source: `UPI_TRM_ICLR/main.tex`
- PDF: `UPI_TRM_ICLR/main.pdf`
- pages: 38
- bytes: 544,294
- PDF SHA-256:
  `9d59bc486b975c08a055e2393d057bbf11f9eb7b06826edfeeecbf1aed4857ae`
- `main.tex` Git blob: `9fcaa6aa199223708e91b39a89d62c137f072a95`
- `trm_rl.bib` Git blob: `38c36ecc9021c5d072a9723acb0c247460c4ea9c`
- `main.pdf` Git blob: `c6a55aa7500ded84972e9599dbca05cd527804bd`

The QED marker is attached to the final display on page 26. Page 27 starts
with Remark F.6. The paper still makes no learned-task performance claim.

## Deterministic validation already completed

- exact finite-MDP suite: 212/212 checks passed;
  maximum numerical violation `2.6645352591003757e-15`.
- retry/provenance focused Python tests: 32/32 passed.
- affected Buck regression gate after the replacement-ref repair: 143 passed,
  0 failed, 0 timed out, 0 fatal, 0 infrastructure failures, 0 build failures.
- expanded policy-improvement type gate: 25/25 targets passed.
- stdout-suppression regression at implementation head `859f2ca`: 1 passed,
  0 failed.
- replacement-ref attack and hostile inherited `GIT_*` variants were rejected.
- current implementation producer manifest SHA-256 at `859f2ca`:
  `c1a37a92dba62139fca75bfdc6d0ac4667d091b7093ff0383a40b1c7851eeaaf`.

The complete final runtime/type/static gate must be rerun at `859f2ca`. Do not
quote the earlier counts as current final evidence.

## Registered experiment identities

- protocol ID: `policy-improvement-v1-20260814`
- canonical protocol SHA-256:
  `583e99828d877f9a33503e84af58f1ccb8aa643f7ecc5baa826d6662de6a48b2`
- raw protocol SHA-256:
  `be986854e39776513e3cd6891ced583efd361a79ce5f1f194f5cc8af7c3c87c3`
- registry raw SHA-256:
  `db8d4198409c94fda3174faffe56ba0d37b9b01f98319f217127342658be3ed4`
- registry rows: 157 total, 4 smoke and 153 full.
- dataset top manifest:
  `2572bb79faeec976dc83cb75b8520e59691a7c9dc3f8fe252554fc29bfe90ccd`
- records: 1,024 train, 256 validation, 512 test.

`RUN_UPITRM_FULL_EXPERIMENTS` was unset. No Stage 1-3 run was launched. The
full runtime remains intentionally fail-closed because the production
non-smoke backend is not connected.

## Fresh authenticated Stage 0 smoke

The four-method smoke completed successfully at producer commit `2d43263`.
Every method used seed `1257297357`, validation records 0-7, and the registered
16/32 interaction prepare/resume schedule. The test split was never opened.

Durations:

| Method | Prepare | Resume |
| --- | ---: | ---: |
| fixed-base exact persistent-z | 503.065 s | 849.867 s |
| fixed-base exact episodic-z | 474.176 s | 855.066 s |
| legacy parameter interpolation | 661.621 s | 1,218.135 s |
| matched PPO | 294.813 s | 329.632 s |

Smoke runtime identities:

- launcher SHA-256:
  `8e73d60512934705f8a295fb67845f5a90b8c6f3006e1ea6ebcb373881c76d6a`
- training PAR SHA-256:
  `8c0bed3e3e8230f1b5294938a7523b6ec3c9dcd17be3da752e8c0b780255d28b`
- producer manifest SHA-256 at `2d43263`:
  `8da0a8be7e2728d900c105e5e36009598c65419dce0681b6010c3cc2f82d1163`
- runtime authorization SHA-256:
  `04ba5dd28509e1c7c51a2b6a49e4d8814c8f162a95560376671ad79071e76e75`
- smoke-plan SHA-256:
  `2037cb53e8f0825f7bc10a48ee221e81e223ebedf0d117e2459d1cada5446ad8`

Each final segment is schema 2 and commits its exact
`prior_failed_attempts` inventory. The new evidence root contains no failed
attempts. Persistent-z was independently checked byte-for-byte: exact file
inventories, hashes, checkpoint lineage, authorization, source identity, and
test isolation all passed.

## External artifacts that are not in Git

Copy these directories before changing machines if the smoke evidence should
be retained:

```text
/home/buiksat/upi-trm-policy-evidence-2d43263f.Erh9bSVz/
/home/buiksat/upi-trm-policy-auth-2d43263f.MjSzspvD/
/home/buiksat/upi-trm-policy-auth-5e8801b1.bAjbAlMP/
```

The detached producer checkout can be recreated, but its current path is:

```text
/home/buiksat/upi-trm-producer-2d43263/
```

It is clean at `2d43263` and contains an exact copy of the frozen dataset.

Do not commit the smoke evidence or authorization directories to either source
repository.

## Audit history and current resume point

1. The first authenticated audit used an audit PAR without retained GPU
   sections. It failed at PPO optimizer validation with
   `cudaErrorInvalidKernelImage`.
2. Commit `5e8801b` adds `keep_gpu_sections = True` to the audit and analysis
   PARs.
3. The next retry correctly rejected reconstruction from the wrong checkout.
   A clean detached `2d43263` producer checkout was then supplied.
4. The repaired audit semantically passed:
   - schema `policy_improvement_audit_v5`;
   - 4 expected and 4 complete rows;
   - 0 failed rows;
   - 10 per-instance artifacts;
   - 8 semantic checkpoint validations;
   - test-open verification `false`.
5. That audit stdout also contained 12 checkpoint progress lines before the
   canonical JSON. It is not a publishable JSON artifact. Commit `859f2ca`
   suppresses those messages for audit restores, and its focused Buck test
   passed.

The noncanonical semantic-pass file is retained only for debugging:

```text
/home/buiksat/upi-trm-policy-auth-5e8801b1.bAjbAlMP/stage0-audit.json
SHA-256: 54b9b96f37253e29cbbb5a121efe91adef96e3bb35945d56641a06aa0757f22b
```

Do not publish or treat that file as canonical JSON.

## First actions on the new machine

1. Materialize both repositories at the exact committed heads and confirm
   clean worktrees.
2. Restore the three external evidence/authorization directories, or rerun the
   Stage 0 smoke if they were not transferred.
3. Recreate a clean detached checkout at `2d43263` and copy the frozen dataset
   under its registered relative path.
4. From `/data/users/buiksat/fbsource`, confirm
   `fbcode/buiksat_trm` resolves to the implementation repository.
5. Run `buck2 kill` before building because the repository is symlinked into
   the Buck workspace.
6. Build and hash at `859f2ca`:

```bash
buck2 build --local-only @fbcode//mode/opt --show-output \
  fbcode//buiksat_trm:phase4_runtime_launcher \
  fbcode//buiksat_trm:upi_trm_train \
  fbcode//buiksat_trm:policy_improvement_audit \
  fbcode//buiksat_trm:policy_improvement_analysis
```

7. Create a new runtime authorization for `859f2ca` using the new artifact
   hashes. Keep the `2d43263` authorization as a historical authorization.
8. Rerun the Stage 0 audit through `phase4_runtime_launcher` with:
   - current audit source/authorization at `859f2ca`;
   - `--historical-runtime-authorization` naming the `2d43263` authorization;
   - child `--project-root` and `--dataset-root` pointing at the clean detached
     `2d43263` checkout;
   - the four final result paths and ten per-instance paths from the external
     evidence root.
9. Require stdout to parse as one JSON document with no prefix lines and the
   semantic counts listed above.
10. Run the complete user-prescribed Buck runtime gate, type gate, launcher
    negatives, manifest/static gates, paper build, and visual inspection.
11. Create
    `reports/CODEX_REPAIR_AND_EXPERIMENT_REPORT.md` and refresh both GPT Pro
    review prompts. These documentation deliverables were not completed before
    the machine transfer.

## Final status at transfer

- repair source status: implemented and committed;
- Stage 0 smoke: complete;
- semantic audit: passed once, but canonical-output rerun still required at
  `859f2ca`;
- full learned experiments: not authorized and not executable;
- paper learned-task claims: unchanged, none added;
- final repair verdict: `REPAIRS INCOMPLETE` until the canonical audit rerun
  and full final validation gates pass;
- experiment status: `INCOMPLETE`.
