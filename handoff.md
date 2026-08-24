# UPI-TRM ICLR paper revision handoff

Date: 2026-08-23

## Repository revisions

Paper repository:

- path: `/home/buiksat/UPI_TRM`
- branch: `iclr-evidence-aligned-revision`
- expected starting SHA: `c40122a6865be964371f93b6d548f2ff9e6c4340`
- actual starting SHA: `c40122a6865be964371f93b6d548f2ff9e6c4340`
- starting worktree: clean
- intervening branch diff: none; the branch had not advanced beyond the
  expected SHA
- paper revision commit:
  `6bf794c01ddc3623522a5c4cdf4a1fe2f623af4d`
  (`Clarify finite-reference contribution and paper scope`)

Implementation reference:

- path: `/home/buiksat/trm_bellman`
- branch: `full-implementation`
- expected reference SHA: `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`
- actual reference SHA: `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`
- worktree before and after the paper revision: clean
- use in this task: read-only semantic reference; no implementation file was
  modified

This handoff update is documentation-only relative to paper revision commit
`6bf794c01ddc3623522a5c4cdf4a1fe2f623af4d`.

## Files changed in the paper revision

Added:

- `README.md`
- `UPI_TRM_ICLR/figures/persistent_depth_lanes.tex`
- `UPI_TRM_ICLR/verify_finite_mdp.py`

Materially changed:

- `UPI_TRM_ICLR/main.tex`
- `UPI_TRM_ICLR/main.pdf`
- `UPI_TRM_ICLR/Makefile`
- `UPI_TRM_ICLR/iclr2026_conference.sty`

Removed: none.

`UPI_TRM_ICLR/trm_rl.bib` was read and checked. No bibliography edit was
needed because the existing entries covered the primary sources used in the
new comparison table.

## Resolution of the eight requested issues

1. **Novelty claim.** The abstract, introduction, related work, contribution
   list, and conclusion now describe a domain-specific synthesis and semantic
   interface. They explicitly treat the triangle inequality, Bellman residual
   bound, Banach contraction, CPI, and occupancy coupling as standard tools.
   A related-work table compares classical approximate policy iteration, CPI,
   safe or monotone approximate policy improvement, recurrent reasoning
   models, and this finite-reference recurrent-evaluator setting.

2. **Finite-MDP nonvacuity.** Section 9 gives the concise calculation and Table
   6 gives the exact values. Appendix F enumerates the full three-state closure,
   including the shared absorber, and derives `V^pi`, the endpoint gap, the
   reference residual, the finite-reference upper bound, the actual value
   error, both occupancies, the exact mixture, candidate advantage and span,
   centering and candidate defects, the signed defect, the CPI lower bound, and
   the exact return. The example uses rational arithmetic, no learned
   parameters, and no sampling.

3. **Fixed-base scope.** The abstract, introduction, algorithm section,
   implementation discussion, and conclusion now state that the analyzed
   object is one proposal against one frozen base policy at one frozen
   parameter snapshot. They explicitly deny a recursively promoted CPI
   sequence. Algorithm 1 is captioned as one fixed-base proposal.

4. **Exact centering.** Table 2 distinguishes finite exact summation, exact
   integration or separately certified numerical error, and sampled or learned
   baselines. The main text states the cost of finite action enumeration,
   notes that the current Sudoku implementation can enumerate its masked action
   set, and routes approximate centering to the signed-defect theorem. No
   certified quadrature rule is claimed.

5. **Domains and dependencies.** Tables 4 and 5 map the Bellman,
   one-deviation, mixture, pair, deployment, and persistent augmented domains,
   their invariance requirements, path contents, alpha dependence, absorbing
   restrictions, and theorem uses. The dependency table separates Bellman-only
   results from assumptions involving head Lipschitzness, recurrent
   contraction, projection, invariant latent sets, slow drift, exact mixture
   realization, and deployment TV or KL control.

6. **Deployed depth versus comparison depth.** Figure 2 shows deployment and
   comparison lanes from the same stored pre-unroll latent. The comparison lane
   is labeled as endpoint evaluation only, with no action sampling or
   transition. Its caption states that changing `m` changes neither the stored
   state, deployed policy, `F_n`, transition kernel, nor replay trajectory.

7. **Theorem density.** The main narrative now follows finite-reference value
   control, the target-network population-residual bridge, signed exact-mixture
   CPI, persistent state and deployment realization, then the finite-MDP
   example. Repeated residual substitutions, fixed-point limits,
   projection-active specializations, slow-drift results, and boundary-case
   derivations remain available in the appendix. Existing theorem, equation,
   and proof labels were preserved; no old label was removed.

8. **Artifact documentation.** The new root `README.md` identifies the
   canonical paper directory and branch, semantic oracle, read-only
   implementation reference, Stage 0 systems-only boundary, absence of learned
   claims, clean PDF build commands, and deterministic finite-MDP verification
   command. The build files now retain the normal PDFTeX path when the official
   PSNFSS metrics exist and use an XeLaTeX/OpenType fallback on this host.

## Theorem and proof review

No existing theorem assumption was weakened and no conclusion was broadened.
The fixed MDP, fixed parameter snapshot, current policy, candidate policy,
domain invariance, absorbing boundary, exact-mixture, and shared recurrent-map
quantifiers remain explicit. The main-text persistent statement is the direct
finite-depth augmented-MDP specialization already proved in Appendix C.

The primary finite-reference result still uses only Bellman contraction and
finite endpoints. Recurrent contraction, projection, a recurrent fixed point,
and slow drift remain optional assumptions for separate specializations. The
target-network bridge still includes propagated target lag before reaching the
self-bootstrap Bellman residual. Terminal absorbing-tail accounting remains
single-counted.

No genuine error was found in the pre-existing theorem or proof semantics. The
new verification script uses `d_{pi_alpha}` for the signed CPI defect, matching
Theorem 7.3. Its final exact values agree with the paper.

## Final PDF

- path: `UPI_TRM_ICLR/main.pdf`
- pages: 45
- bytes: 367272
- SHA-256:
  `257d4fafd28ee9b32d4ff8272752d79cf225036efa0ab8fe3e046b198eb2cfc1`
- submission mode: anonymous ICLR review mode; `\iclrfinalcopy` remains disabled

## Build and validation

The final clean build was run from the exact source committed as
`6bf794c01ddc3623522a5c4cdf4a1fe2f623af4d`:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_ICLR
make clean && make pdf
```

Result: exit 0. This host lacks `phvb.tfm` and `ptmr8t.tfm`, so the Makefile
selected XeLaTeX. The target ran XeLaTeX, BibTeX, then three more XeLaTeX
passes. The final pass produced 45 pages.

Log checks:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_ICLR
grep -nE 'LaTeX Warning:|Package natbib Warning:|Overfull \\hbox|multiply defined|undefined references|undefined citations' main.log || true
grep -nE 'Warning|error|Error' main.blg || true
```

Result: no matches. The remaining layout diagnostics are underfull boxes; no
overfull box damages readability.

Static label and citation check:

```bash
cd /home/buiksat/UPI_TRM
python3 - <<'PY'
import re
from collections import Counter
from pathlib import Path

tex = Path('UPI_TRM_ICLR/main.tex').read_text()
bib = Path('UPI_TRM_ICLR/trm_rl.bib').read_text()
labels = re.findall(r'\\label\{([^}]+)\}', tex)
refs = re.findall(r'\\(?:eq|page|auto|C|c)?ref\{([^}]+)\}', tex)
cites = sorted({k.strip() for group in re.findall(r'\\cite\w*\{([^}]+)\}', tex)
                for k in group.split(',')})
bibkeys = set(re.findall(r'@[^{]+\{\s*([^,\s]+)', bib))
dups = sorted(k for k, v in Counter(labels).items() if v > 1)
undef = sorted(set(refs) - set(labels))
missing = sorted(set(cites) - bibkeys)
print(f'labels={len(labels)} unique_labels={len(set(labels))} references={len(refs)} cited_keys={len(cites)}')
print(f'duplicate_labels={dups}')
print(f'undefined_refs={undef}')
print(f'missing_citations={missing}')
if dups or undef or missing:
    raise SystemExit(1)
PY
git diff --check
```

Result:

```text
labels=233 unique_labels=233 references=271 cited_keys=24
duplicate_labels=[]
undefined_refs=[]
missing_citations=[]
git diff --check: exit 0
```

PDF integrity and metadata checks:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_ICLR
gs -q -dNOSAFER -dBATCH -dNOPAUSE -sDEVICE=nullpage main.pdf
gs -q -dNOSAFER -dNODISPLAY -c '(/home/buiksat/UPI_TRM/UPI_TRM_ICLR/main.pdf) (r) file runpdfbegin pdfpagecount = quit'
stat -c '%s' main.pdf
sha256sum main.pdf
```

Result: PDF parse exit 0, 45 pages, 367272 bytes, and the SHA-256 shown above.

The final PDF pages containing the title, related-work table, depth-lane
diagram, algorithm and centering table, domain and dependency maps,
persistent/deployment statements, finite-MDP summary, full finite-MDP
derivation, and final page were rendered with Ghostscript at 110 dpi and
visually inspected. No clipping, stale reference, figure collision, or
material readability defect was found.

## Deterministic finite-MDP verification

Command:

```bash
cd /home/buiksat/UPI_TRM
python3 UPI_TRM_ICLR/verify_finite_mdp.py
```

Result: exit 0. The script asserted and emitted:

```text
V^pi                         = (0, 0, 0)
||U_1-U_2||_infinity         = 1/8
||U_2-T^pi_1 U_2||_infinity = 3/16
finite-reference bound       = 1/2
actual ||U_1-V^pi||          = 1/4
d_pi                         = (1, 0, 0)
d_pi_alpha                   = (3/4, 1/4, 0)
g                            = (1, 0, 0)
span(g)                      = 1
c                            = (0, 0, 0)
b                            = (-1/4, -1/4, 0)
Xi_alpha                     = -1/8
estimated surrogate          = 3/4
signed CPI lower bound       = 2/3
eta(pi_alpha)                = 3/4
```

The script SHA-256 is
`e4bf4a3c77ae57738cbd9de37931cfd9600919b17bde1ca0bf4094cbc5409d85`.

## Evidence and claim boundary

- No learned experiment was run.
- No learned-task performance result or empirical comparison was added.
- No deleted historical result, checkpoint, metric, path, or reconstructed
  artifact was used.
- Finite-batch and local diagnostics remain labeled as diagnostics, not
  population certificates.
- Stage 0 remains systems-only and is not paper evidence.

## Remaining paper limitations

- The result certifies one fixed-base proposal at one frozen snapshot, not a
  recursively promoted policy sequence or an optimization trajectory.
- The theorem requires population suprema on declared invariant domains.
  Finite datasets and regression losses do not establish those quantities.
- Exact statewise centering requires exact finite-action summation or exact
  integration. The signed-defect theorem is required when centering is
  approximate.
- The exact CPI statement applies only to the explicit pointwise
  probability-space mixture. Distillation and parameter, logit, hidden-state,
  or network interpolation require a separately established deployment gap.
- Persistent-state comparisons require the current and candidate policies to
  share one frozen recurrent transition map.
- The finite-reference and CPI bounds can be loose or vacuous when residuals,
  defects, spans, endpoint gaps, or discount denominators are unfavorable.
- No bridge from training dynamics to the theorem's uniform premises is proved.

## Remaining implementation blockers

### Stage 0: systems-only

- No fresh Stage 0 package exists for implementation commit
  `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`.
- A new runtime authorization and frozen runtime/source identities must bind
  that exact commit before the registered Stage 0 rows are run and audited.
- Stage 0 must use only its registered training records. The test split remains
  unauthorized, and Stage 0 output must not be cited as paper evidence.

### Stage 1 and later learned work

- The v2 protocol leaves `base_policy_artifact` unavailable. Stage 1 must fail
  closed until an authenticated competent train-only base artifact is bound, or
  the user explicitly chooses the random-base stress-test interpretation.
- Any theorem-facing run must use `training_protocol: fixed_base_exact` and the
  exact pointwise mixture. It still cannot establish the paper's uniform
  residual, invariance, overlap, centering-defect, or deployment premises from
  finite data alone.
- Stage 2 and Stage 3 additionally require their registered prerequisites and a
  separately authenticated `TEST_OPEN` transaction. None was created or used
  in this paper-only task.

## Final state before the handoff commit

- paper revision: committed at
  `6bf794c01ddc3623522a5c4cdf4a1fe2f623af4d`
- implementation reference: unchanged at
  `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`
- paper PDF: built and validated at the paper revision commit
- this handoff change: documentation only

# Authenticated protocol-v2 Stage 0 execution attempt

Date: 2026-08-23

Execution window: `2026-08-23T19:26:31Z` to `2026-08-23T19:55:40Z`

## Frozen identities

- Paper repository: `/home/buiksat/UPI_TRM`
- Paper branch: `iclr-evidence-aligned-revision`
- Starting paper HEAD: `977c7a61d1febeff60429f334fc823fa460af1ac`
- Frozen paper source and PDF revision at the stop point:
  `977c7a61d1febeff60429f334fc823fa460af1ac`
- Implementation repository: `/home/buiksat/trm_bellman`
- Implementation branch: `full-implementation`
- Implementation HEAD: `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`
- Both worktrees were clean at the start. The implementation worktree remained
  clean through the stop point. `git replace -l` was empty.
- Frozen PDF:
  `/home/buiksat/UPI_TRM/UPI_TRM_ICLR/main.pdf`
- Frozen PDF SHA-256:
  `257d4fafd28ee9b32d4ff8272752d79cf225036efa0ab8fe3e046b198eb2cfc1`
- No paper source or PDF file changed. This handoff update is documentation-only
  relative to the starting paper commit.

## Execution root and host

- External execution root:
  `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl`
- Root mode: `0700`
- Filesystem: `btrfs` on
  `/dev/vda3[/var/localhome/devenvusera2d2]`
- Host: `devvm8504.hil0.facebook.com`
- Python: `3.12.13+meta`
- Buck2: `267acfd7b674f035b00ce9414afaf824027eafe6`
- CUDA-visible hardware: two NVIDIA A100-PG509-200 devices, 40,960 MiB each,
  driver `580.126.09`
- Environment metadata:
  `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/metadata/environment_preflight.json`

## Dataset preflight

The preflight authenticated the registered train content and only metadata for
validation and test. It did not deserialize validation or test arrays.

- Dataset root:
  `/home/buiksat/trm_bellman/data/policy-improvement-v1-owner/policy-improvement-hard-4x4-v1`
- Dataset manifest SHA-256:
  `2572bb79faeec976dc83cb75b8520e59691a7c9dc3f8fe252554fc29bfe90ccd`
- Train manifest SHA-256:
  `05146037857b1adb42520e80a0c2ab250053a517196c8b8ac95e002aa40c6f74`
- Train ordered-record SHA-256:
  `73110263bb388e0f6e0976156d03f499b83541a58d07c39b8b634e94a98ad446`
- Train count: `1024`
- Validation manifest SHA-256, metadata only:
  `a4b1bffb92f9c7c1ebe7baf9dcaaed83191f9c6249bec0887ed8ff7fb6b4a937`
- Test manifest SHA-256, metadata only:
  `bf14acfc94e580bb3678102729f88432fda599610b2ca2578949f8c4cbc775bd`
- Stage 0 indices: `[749, 910, 352, 318, 877, 605, 148, 280]`
- Stage 0 ordered-record SHA-256:
  `522a60c5f0b4276c5a66743005ff430800ad0085e020cd4a7403a0f303456033`
- Stage 0 ordered-input SHA-256:
  `903e3155d6a728e55dccd3f49e07a3797e0013e2c3cc979d17ba7eaefee584b2`
- Stage 0 binding SHA-256:
  `c6350d61eb7c2d3f2b04114bf83017c764172512506477b156b21941ff9ef656`
- `validation_select` and `validation_bridge` were verified from manifest
  metadata as disjoint and exhaustive 128-record partitions.
- Dataset preflight record:
  `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/metadata/dataset_preflight.json`
  with SHA-256
  `7dc3aef8882f23ae3c34ddcd3532cba754ddbd4f22e6e4f597a02df7babe3b9c`.

## Current-SHA gates

Focused test command:

```bash
cd /data/repos/fbsource
buck2 test --local-only @fbcode//mode/opt \
  fbcode//buiksat_trm:test_phase4_runtime_launcher \
  fbcode//buiksat_trm:test_policy_improvement_v1 \
  fbcode//buiksat_trm:test_policy_improvement_v2 \
  fbcode//buiksat_trm:test_policy_improvement_runtime_authorization \
  fbcode//buiksat_trm:test_policy_improvement_audit \
  fbcode//buiksat_trm:test_policy_improvement_checkpoint_allowlist \
  fbcode//buiksat_trm:test_policy_improvement_sealed_evidence \
  fbcode//buiksat_trm:test_policy_improvement_evidence \
  fbcode//buiksat_trm:test_policy_improvement_full_runtime \
  fbcode//buiksat_trm:test_policy_improvement_full_backend \
  fbcode//buiksat_trm:test_policy_improvement_throughput \
  fbcode//buiksat_trm:test_policy_improvement_theory_bridge_v2 \
  fbcode//buiksat_trm:test_policy_improvement_smoke_checkpoint \
  fbcode//buiksat_trm:test_policy_improvement_smoke_runtime \
  fbcode//buiksat_trm:test_policy_improvement_checkpoint_validator \
  fbcode//buiksat_trm:test_run_identity \
  fbcode//buiksat_trm:test_upi_trm_trainer_smoke \
  fbcode//buiksat_trm:test_algorithm2_boundary_contract \
  fbcode//buiksat_trm:test_cpi_mixture_policy_smoke \
  fbcode//buiksat_trm:test_rl_k_step_targets \
  fbcode//buiksat_trm:test_theory_exact_components \
  fbcode//buiksat_trm:test_plan_edit_env \
  fbcode//buiksat_trm:test_rl_k_step_value_update_trainer \
  fbcode//buiksat_trm:test_config_integrity
```

Result: 24 targets listed successfully; 477 tests passed, 0 failed, 0 timed
out, 0 fatal, 1 skipped, 0 omitted, 0 infrastructure failures, and 0 build
failures. The raw Buck exit code was `64` because
`test_real_historical_checkpoints_load_data_only` skipped when
`UPI_TRM_HISTORICAL_CHECKPOINT_ROOT` was absent. That variable was deliberately
not set because this cycle forbids historical evidence. No test failed.

- Test stdout SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Test stderr SHA-256:
  `922983de2b27df57a55c423035017fc872c320c83c013347fa94e77368981064`
- Test window: `2026-08-23T19:34:07Z` to `2026-08-23T19:46:02Z`

Generated type-check command:

```bash
cd /data/repos/fbsource
buck2 build --local-only @fbcode//mode/opt \
  fbcode//buiksat_trm:policy_improvement_runtime_authorization-type-checking \
  fbcode//buiksat_trm:policy_improvement_throughput-type-checking \
  fbcode//buiksat_trm:test_policy_improvement_runtime_authorization-library-type-checking \
  fbcode//buiksat_trm:test_policy_improvement_throughput-library-type-checking
```

Result: exit `0`, four targets. Type-check stdout SHA-256 was the empty-file
digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
stderr SHA-256 was
`44aff66aef62489e6bbd26273fbe495a1a665fb84d2f3c4a8ba4b3f412c4fbcf`.

`git -C /home/buiksat/trm_bellman diff --check` exited `0` with empty stdout
and stderr.

## Runtime build

Build command:

```bash
cd /data/repos/fbsource
buck2 build --local-only @fbcode//mode/opt --show-full-output \
  fbcode//buiksat_trm:phase4_runtime_launcher \
  fbcode//buiksat_trm:upi_trm_train \
  fbcode//buiksat_trm:policy_improvement_full \
  fbcode//buiksat_trm:policy_improvement_theory_bridge \
  fbcode//buiksat_trm:policy_improvement_audit \
  fbcode//buiksat_trm:policy_improvement_analysis \
  fbcode//buiksat_trm:generate_policy_improvement_runtime_authorization \
  fbcode//buiksat_trm:policy_improvement_smoke_plan
```

Result: exit `0`, eight targets, from `2026-08-23T19:47:53Z` to
`2026-08-23T19:51:00Z`. Build stdout SHA-256 was
`6a772da5e16ba6799843dd97561db6abbe2d3574806f09bc3381ae048cf64082`;
stderr SHA-256 was
`53f40b9ae6f9b06287031f77dcb4003873e2d04377e010f48197c970afa1463c`.

The Buck outputs were copied as separate read-only files into the external
execution root before hashing and authorization.

| Target | Frozen path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `phase4_runtime_launcher` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/phase4_runtime_launcher.par` | 840475 | `5f38ddfc12d7d604b8d0f19a635f23e2cf9ed6b6c17687814c7a92a434c7f15f` |
| `upi_trm_train` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/upi_trm_train.par` | 1460660834 | `5cc289cc9fb7106ea8d0aa82175d171f283a07298e534afa587baae55faf1e1e` |
| `policy_improvement_full` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_full.par` | 1460748258 | `b518cbdf837807f6e0c25ac8c7ba0907f102598476ddceb743f9210760817c84` |
| `policy_improvement_theory_bridge` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_theory_bridge.par` | 1460852689 | `5710ce96abff7f0ec05354a879aed1b6ef5b6802fd6c350ca2465f1ec7c0ebaf` |
| `policy_improvement_audit` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_audit.par` | 1460812190 | `0750924c583036f1d1217123acee563a6a1be46f4c1a5ed6395ebb164b7ca6df` |
| `policy_improvement_analysis` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_analysis.par` | 1460815829 | `9a0c7ecfc19aa28cdb2f4f7b43061df98eb2d69cfa77d326d10fbcd93b013d5e` |
| `generate_policy_improvement_runtime_authorization` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/generate_policy_improvement_runtime_authorization.par` | 1187891 | `6156434628253c16f85a0640bb40e20014411e1276c677d7c7f48b86299839bb` |
| `policy_improvement_smoke_plan` | `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_smoke_plan.par` | 1135384 | `adc00bbf7661ea4b6a5fbbd47981f4fb2f1c976e4d0eade2f8d3f7133df639ba` |

The complete artifact manifest is
`/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/metadata/build_artifacts.json`
with SHA-256
`a63259f537ca32675abce5307ff32f898d39441d6937ed5031ad749b67a5f9c6`.

## Fail-closed stop at runtime authorization

Authorization command:

```bash
/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/generate_policy_improvement_runtime_authorization.par \
  --project-root /home/buiksat/trm_bellman \
  --expected-git-commit 3ceddf42baa073f23ea7026e24e11f1f72fdbf2a \
  --authorization-id stage0-v2-3ceddf42-20260823T195343Z \
  --created-at-utc 2026-08-23T19:53:43Z \
  --launcher /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/phase4_runtime_launcher.par \
  --training-runtime /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/upi_trm_train.par \
  --full-runtime /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_full.par \
  --theory-runtime /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_theory_bridge.par \
  --audit-runtime /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_audit.par \
  --analysis-runtime /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/build/policy_improvement_analysis.par \
  --owner-directory /home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/authorization \
  --output-name runtime_authorization_v3.json
```

Result: exit `1`. No authorization file was published at
`/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/authorization/runtime_authorization_v3.json`.
The requested ID was `stage0-v2-3ceddf42-20260823T195343Z`, and the expected
schema was `policy_improvement_runtime_authorization_v3`, version `3`.

The exact error was:

```text
RuntimeAuthorizationGenerationError: Launcher PAR native runtime support differs.
```

The launcher member inventory and executable prefix matched the frozen checks.
The native-support manifest did not:

- expected native-support manifest SHA-256:
  `4f2d213fe8530f0bbf048de5fc62fd49b8dd1f1dee46cd9d37943440ab29b4ee`
- actual native-support manifest SHA-256:
  `974e9a793a853aead172bb80c899ad6004cd57985a8d81e6dc911fd0232f24a9`
- expected and actual executable prefix: 8215 bytes, SHA-256
  `87e71b36ae3f0dff3321a09ad2d09f1255ababea6f2e3577419c7f01c8e50f05`
- native-main member SHA-256:
  `ae045fa3a8eca8e17289ff5d54bb02997d2d1cde3f2ce2ca6d90f777efef54dc`
- allocator-preload member SHA-256:
  `9da817f06e846faa4c8b371b39deebd55f025e20b9093245a88667250526b9a3`
- Authorization stderr SHA-256:
  `0265497a49125543fdde2af8c0049a72d5e46c211db4c18999a677a4319edd25`
- Authorization stdout was empty, SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

This is consistent with Buck native-runtime support drift relative to the
source-pinned launcher identity. The smallest safe resolution is to use the
reviewed Buck bootstrap that reproduces the pinned native-support digest, or to
review the two changed native members and update the pin in a new implementation
commit. The latter changes the reviewed source SHA and requires a new review,
rebuild, source profile, and runtime authorization.

## Unexecuted phases and evidence boundary

- The Stage 0 plan was not rendered.
- No prepare or resume process started.
- No checkpoint, result, per-instance record, compute-accounting artifact, or
  failed-attempt manifest was created.
- The Stage 0 audit was not run.
- The theory smoke was not run.
- Throughput calibration was not run. The 4096 tier was neither authorized nor
  executed.
- Stage 1, Stage 2, Stage 3, validation selection, validation bridge, and test
  evaluation were not run.
- No validation or test content was opened.
- No `TEST_OPEN` record was created.
- No deleted or historical experiment evidence was inspected or used.
- No task-performance result or claim was generated.
- Stage 0 and theory-smoke outputs, had they existed, would not be paper
  evidence. None exists from this attempt.
- No implementation source or configuration file was modified.

The canonical external execution manifest is
`/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl/metadata/stage0_execution_manifest.json`
with SHA-256
`fb6ff938247d2e0bf9122a01eed93f12d6d69eb09665e52ed7fe94ddbd55c9e8`.

## Remaining blockers after this attempt

### Stage 0

- Runtime authorization is blocked by the launcher native-support digest
  mismatch above. No authenticated Stage 0 package exists at the frozen
  implementation SHA.

### Stage 1

- Stage 1 remains blocked by the unavailable authenticated train-only
  `base_policy_artifact` and its continuation contract.

### Stage 2 and Stage 3

- Both remain unauthorized. No test-opening capability was created.

# Approximate-DP positioning revision handoff

Date: 2026-08-24

## Repository revisions

Paper repository:

- path: `/home/buiksat/UPI_TRM`
- branch: `iclr-evidence-aligned-revision`
- last known SHA supplied for this task:
  `977c7a61d1febeff60429f334fc823fa460af1ac`
- actual starting SHA:
  `500837dc1e2e01a0ece600c1c4fe0c6c9230ca82`
- starting worktree: clean
- intervening change: commit `500837dc1e2e01a0ece600c1c4fe0c6c9230ca82`
  added only the preceding authenticated Stage 0 handoff record; the diff from
  `977c7a61d1febeff60429f334fc823fa460af1ac` changed only `handoff.md`
- paper revision commit:
  `1c482f1c444f0aca9c983431abce2b604ea2cbf0`
  (`Position finite-reference bounds against approximate DP`)

Implementation reference:

- path: `/home/buiksat/trm_bellman`
- branch: `full-implementation`
- expected and actual SHA:
  `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`
- worktree before and after the revision: clean
- use in this task: read-only terminology and semantic verification

This handoff update is documentation-only relative to paper revision commit
`1c482f1c444f0aca9c983431abce2b604ea2cbf0`.

## Materially changed files

- `UPI_TRM_ICLR/main.tex`
- `UPI_TRM_ICLR/trm_rl.bib`
- `UPI_TRM_ICLR/verify_finite_mdp.py`
- `UPI_TRM_ICLR/main.pdf`
- `handoff.md` in this separate documentation commit

No implementation file, conference style file, Makefile, README, figure source,
or learned-result artifact was changed.

## Primary literature checked

The comparative claims were checked against these primary sources:

1. R\'emi Munos, "Error Bounds for Approximate Policy Iteration," ICML 2003,
   pages 560-567. The official AAAI paper page and linked paper were used:
   `https://aaai.org/papers/icml03-074-error-bounds-for-approximate-policy-iteration/`.
2. R\'emi Munos and Csaba Szepesv\'ari, "Finite-Time Bounds for Fitted Value
   Iteration," JMLR 9 (2008), pages 815-857. The official JMLR page and PDF
   were used: `https://www.jmlr.org/papers/volume9/munos08a/munos08a.pdf`.
3. Sham Kakade and John Langford, "Approximately Optimal Approximate
   Reinforcement Learning," ICML 2002, pages 267-274. The authors' primary
   LaTeX source was checked at
   `https://www.cs.cmu.edu/~jcl/papers/aoarl/Final.tex_back`.
4. Sham Machandranath Kakade, *On the Sample Complexity of Reinforcement
   Learning*, University College London doctoral thesis, 2003. The author's
   thesis PDF was checked at
   `https://homes.cs.washington.edu/~sham/papers/thesis/sham_thesis.pdf`.

Direct shell downloads were unavailable in this environment, so the primary
documents were loaded into a private research corpus for inspection. Text
extraction from the older PDFs did not expose every theorem body reliably.
The paper therefore makes narrow object-level comparisons and adds no theorem
numbers, constants, or source-specific concentrability formulas that could not
be checked directly. The unrelated arXiv record `cs/0105027` was explicitly
excluded after identity checking showed that it is not the Kakade-Langford CPI
paper.

## Gap audit and resolved points

| Requested point | Starting status | Resolution |
| --- | --- | --- |
| Generic Bellman-residual ancestry | Needed clarification | The abstract, introduction, related work, theorem commentary, contribution list, and conclusion now state that the abstract inequality is the standard fixed-policy a posteriori residual bound followed by a triangle transfer. No new generic AVI/API mechanism is claimed. |
| Strongest reviewer objection | Missing in explicit form | Related work now concedes that recurrence is irrelevant once the endpoints are arbitrary bounded measurable functions, then identifies where the objection stops: intra-state depth, one-MDP persistent semantics, shared-map ownership, endpoint-only `m`, and logically separate CPI composition. |
| Munos-style weighted-norm positioning | Materially incomplete | A source-checked comparison paragraph and compact table distinguish recursive API/FVI update sequences, weighted norms, coverage or concentrability terms, inherent Bellman residuals, finite-sample terms, and final policy loss from this paper's conditional one-snapshot sup-norm result. |
| Content without recurrent contraction | Partly present | New Remark `rem:noncontractive_endpoints` states that the main theorem and finite-path bound survive without a usable global recurrent modulus or with `L_z >= 1`. It records the limits of `D_{n,m}`, gives an oscillatory `F(z)=-z` illustration, and states the assumptions behind three crude endpoint-gap bounds. |
| Forms of nonstationarity | Needed clarification | New Remark `rem:frozen_schedule_scope` separates a frozen depth-indexed map schedule, an observed clock or mode that belongs in the Markov state, and parameter changes that invalidate the fixed-snapshot theorem. |
| Weighted `L_p` restatement | Needed a new formal statement | Appendix Proposition `prop:weighted_finite_reference` gives a complete fixed-policy proof with explicit domination, integrability, and density-ratio assumptions. |
| Learned-operator terminology | Already mostly correct | The new appendix text makes the ownership explicit: `T_K^pi` and `P_pi^K` generate the contraction and resolvent. The learned recurrence determines endpoint functions and, in persistent mode, enters the frozen augmented transition kernel. |
| Persistent-latent concentrability | Missing | The weighted-result discussion explains graph-supported augmented occupancies, possible singularity relative to product Lebesgue references, the analytical but non-operational choice `mu=d_rho^{pi,K}`, and why finite-population diagnostics do not establish a continuous-state density ratio. |
| Projection and certification limits | Needed strengthening | The conclusion now states that compactness does not compute a useful supremum, projection need not bound external state, whole-ball interval bounds and global norm products may be vacuous, and residual certification must cover rewards, policies, masks, successors, terminals, and expectations. |
| Credible future certification route | Needed clarification | The conclusion proposes finite external enumeration, state- or clock-dependent reachable latent enclosures, relational endpoint bounds, direct residual certification, and branch-and-bound or abstract interpretation. It is labeled proposed methodology, not an established verifier. |
| Kakade distribution mismatch | Needed clarification | Text after the exact-mixture occupancy lemma now states that its coefficient is local to one current-policy mixture. It does not provide comparator-policy coverage, global convergence, or near-optimality. |

The paper required material positioning revisions, but the primary
finite-reference theorem itself did not require a semantic weakening or a
change to its bound.

## New weighted-Lp proposition

For one fixed current policy on the invariant Bellman domain, let
`beta = gamma^K`, `P = P_pi^K`, and
`r_m = U_m - T_K^pi U_m`. For probability measures `rho` and `mu`, bounded
measurable endpoints, and `1 <= p < infinity`, define

```text
d_rho^{pi,K} = (1-beta) sum_{t>=0} beta^t rho P^t.
```

If `d_rho^{pi,K} << mu` and

```text
C_{rho,mu}^{pi,K}
  = || d d_rho^{pi,K} / d mu ||_{infinity,mu} < infinity,
```

then Proposition `prop:weighted_finite_reference` proves

```text
||U_n - V^pi||_{p,rho}
  <= ||U_n-U_m||_{p,rho}
   + (C_{rho,mu}^{pi,K})^(1/p) / (1-gamma^K)
     ||U_m - T_K^pi U_m||_{p,mu}.
```

If also `rho << mu` with finite
`C_{rho,mu}^{(0)} = ||d rho/d mu||_{infinity,mu}`, the first endpoint term may
be replaced by
`(C_{rho,mu}^{(0)})^(1/p) ||U_n-U_m||_{p,mu}`.

The proof uses the resolvent identity
`e_m = r_m + beta P e_m`, positivity of the fixed Markov kernel, Jensen's
inequality, and change of measure. This is an a posteriori one-policy result.
It has no policy-sequence supremum, function-class inherent Bellman error,
sampling term, or regression-to-population guarantee.

## Other theorem-facing changes

- The central theorem's assumptions, quantifiers, domains, factors of
  `gamma^K`, and conclusion are unchanged.
- The new noncontractive remark makes clear that a small endpoint gap alone is
  insufficient and that no monotonicity in recurrent depth follows.
- The new frozen-schedule remark does not broaden the result to SGD, TD, BPTT,
  or adaptive training dynamics.
- The exact-mixture occupancy bound is explicitly limited to one local
  fixed-base comparison.
- The conclusion removes an unproved suggestion of a Wasserstein analysis and
  retains only the requirement for explicit kernel and reward discrepancies
  plus sufficient propagation regularity.
- `verify_finite_mdp.py` previously evaluated the signed theorem defect
  `Xi_alpha` under `d_{pi_alpha}`. The theorem defines it under `d_pi`, so the
  script now uses `d_pi`. In this enumerated example the per-state candidate
  defect is constant on the active states, so the exact reported value remains
  `-1/8`; no table value or claimed bound changed.

## Build and validation

The final source revision was validated with:

```bash
cd /home/buiksat/UPI_TRM/UPI_TRM_ICLR
python3 verify_finite_mdp.py \
  > /tmp/upi-trm-adp-audit.wFMPLwtR/verify-final.json
make clean
make pdf
```

Results:

- deterministic verifier exit: `0`
- exact finite-reference values: endpoint gap `1/8`, reference residual
  `3/16`, upper bound `1/2`, actual error `1/4`
- exact signed CPI values: `Xi_alpha=-1/8`, lower bound `2/3`, exact mixture
  return `3/4`
- clean PDF build exit: `0`
- build sequence: XeLaTeX, BibTeX, and stabilizing XeLaTeX passes through the
  repository Makefile
- anonymous mode: `\commentsfalse`; no `\iclrfinalcopy`

Additional checks:

```bash
cd /home/buiksat/UPI_TRM
git diff --check

cd /home/buiksat/UPI_TRM/UPI_TRM_ICLR
rg -n 'LaTeX Warning:|Package natbib Warning:|Overfull \\hbox|multiply defined|undefined references|undefined citations' main.log
rg -n 'Warning|warning|Error|error' main.blg
gs -q -dNOSAFER -dBATCH -dNOPAUSE -sDEVICE=nullpage main.pdf
```

Results:

- `git diff --check`: exit `0`
- LaTeX warning scan: no matches
- BibTeX result: `warning$ -- 0`; no errors
- static source audit: 248 labels, 248 unique labels, 281 references, 27
  cited keys, and 47 bibliography keys; no duplicate labels, undefined
  references, missing citations, or duplicate bibliography keys
- Ghostscript full-PDF parse: exit `0`
- visual inspection covered the abstract, revised related-work table,
  noncontractive discussion, weighted proposition and proof, conclusion,
  references, and final appendix page; no clipping or malformed table was
  found
- material overfull boxes: none
- implementation checkout after validation: exact reference SHA and clean

Verifier identities:

- `UPI_TRM_ICLR/verify_finite_mdp.py` SHA-256:
  `6a9ef3d0ad7bdd85589d6deecfaef53b81815d4140d13363bc801aa2f74e9e73`
- canonical verifier output SHA-256:
  `468f85c23efd6e5f72bfb02da749110a6b975646bf69925bd082ea285b063b39`

## Final PDF

- path: `/home/buiksat/UPI_TRM/UPI_TRM_ICLR/main.pdf`
- pages: 47
- bytes: 384275
- SHA-256:
  `a4f77b4eded395f4ca25df7203ce350132f5c69e43b0cd351831fbde3d5b0733`

## Remaining limitations and evidence boundary

- The primary result remains conditional on population suprema. It does not
  turn finite batches or regression loss into a certificate.
- The weighted result can be vacuous or inapplicable when the chosen reference
  measure does not dominate the persistent augmented occupancy.
- Projection and compactness do not by themselves provide computable endpoint
  or Bellman-residual suprema.
- The paper gives no global convergence, comparator-policy coverage,
  near-optimality, training-dynamics, or learned-task result.
- No learned experiment was run, no empirical claim was added, and no Stage 0
  artifact was used as paper evidence.
- No deleted or historical experiment evidence was inspected or used.
- No implementation file was changed.

# Launcher runtime-authorization repair audit, stopped fail-closed

Date: 2026-08-24

Window: `2026-08-24T17:37:11Z` to `2026-08-24T18:14:21Z`

This cycle was an implementation-only repair audit of the launcher
runtime-authorization blocker recorded in the preceding authenticated Stage 0
attempt. It stopped fail-closed during the repair phase. No implementation
source or configuration file was changed, and no Stage 0 process ran.

## Starting state

- Implementation repository: `/home/buiksat/trm_bellman`, branch
  `full-implementation`, HEAD `3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`,
  worktree clean with `--untracked-files=all`, `git replace -l` empty. No
  tracked file has been modified since `2026-08-21T01:06:10Z`, well before the
  prior failure at `2026-08-23T19:53:43Z`.
- Paper repository at the start of this cycle: branch
  `iclr-evidence-aligned-revision`, HEAD
  `500837dc1e2e01a0ece600c1c4fe0c6c9230ca82`, worktree clean, PDF SHA-256
  `257d4fafd28ee9b32d4ff8272752d79cf225036efa0ab8fe3e046b198eb2cfc1`. All
  starting invariants held.
- The paper branch then advanced during this cycle through the concurrent
  approximate-DP positioning revision recorded above
  (`1c482f1c444f0aca9c983431abce2b604ea2cbf0` and
  `bdf8d18772999984ee97049300cd84a32f27be31`). That work is preserved. This
  cycle did not build, modify, or revert any paper source or PDF file, and the
  current PDF SHA-256 `a4f77b4eded395f4ca25df7203ce350132f5c69e43b0cd351831fbde3d5b0733`
  is the product of that separate paper revision, not of this cycle.
- Host: `devvm8504.hil0.facebook.com`, Python `3.12.13+meta`, Buck2
  `267acfd7b674f035b00ce9414afaf824027eafe6`, fbsource checkout `9c664fadec8d`
  dated `2026-08-21 06:00 -0700`, two NVIDIA A100-PG509-200 devices.
- Private diagnostic root, created with `umask 077` and mode `0700`:
  `/home/buiksat/upi-trm-stage0-v3-diag.gotJM0D7`. The prior root
  `/home/buiksat/upi-trm-stage0-v2-3ceddf42.iAmSeUUl` was read only and is
  preserved unmodified; its manifest still hashes to
  `fb6ff938247d2e0bf9122a01eed93f12d6d69eb09665e52ed7fe94ddbd55c9e8`.

## Reproducibility of the launcher artifact

The launcher PAR was rebuilt twice from the unchanged starting SHA:

```bash
cd /data/repos/fbsource
buck2 build --local-only @fbcode//mode/opt --show-full-output \
  fbcode//buiksat_trm:phase4_runtime_launcher

buck2 --isolation-dir=upitrm-diag-cold build --local-only @fbcode//mode/opt \
  --show-full-output fbcode//buiksat_trm:phase4_runtime_launcher
```

The second build used a separate isolation directory, a cold daemon, and a
separate `buck-out`, so it re-executed the packaging action rather than
rematerializing a cached one. Both fresh artifacts and the preserved
`2026-08-23` artifact are byte-identical:

- size: 840475 bytes
- SHA-256:
  `5f38ddfc12d7d604b8d0f19a635f23e2cf9ed6b6c17687814c7a92a434c7f15f`
- 65 members, identical across every per-member ZIP field, including
  compression method, CRC, timestamp, external attributes, header offset, and
  content digest

The mismatch is therefore not nondeterministic Buck output.

## Root cause

Five distinct checks in the checked-in launcher identity boundary disagree with
the artifact that the repository's own documented Buck command produces. Only
the first of the five was reached in the prior cycle, because the validator
short-circuits.

| Check | Result | Reached on 2026-08-23 |
| --- | --- | --- |
| executable prefix, 8215 bytes | pass | yes |
| `BUILDSTAMP` archive binding | pass | yes |
| `runtime/` member inventory | pass | yes |
| native-support manifest digest | fail | yes, this stopped the prior cycle |
| pinned-support manifest digest | fail | no |
| startup-loader normalized digest | fail | no |
| pinned startup-function set | fail | no |
| pinned target-label pattern | fail | no |
| pinned executable closure | fail | no |

Two of the failures are stale digests with an accounted-for Meta-owned cause.

- Native support. The normalized identity is the canonical JSON object mapping
  `runtime/bin/phase4_runtime_launcher#native-main#platform-runtime#python#py_version_3_12`
  to `ae045fa3a8eca8e17289ff5d54bb02997d2d1cde3f2ce2ca6d90f777efef54dc` and
  `runtime/lib/__python_generated_allocator_preload` to
  `9da817f06e846faa4c8b371b39deebd55f025e20b9093245a88667250526b9a3`, which
  hashes to `974e9a793a853aead172bb80c899ad6004cd57985a8d81e6dc911fd0232f24a9`
  against the pinned `4f2d213fe8530f0bbf048de5fc62fd49b8dd1f1dee46cd9d37943440ab29b4ee`.
  Both members are ELF artifacts that Buck links for platform010: the native
  CPython 3.12 main and the Buck-generated
  `fbcode//buiksat_trm:phase4_runtime_launcher-allocator-preload`. fbsource
  updated `llvm-fb/21/platform010` at `2026-08-20 15:22 -0700` and
  `llvm-fb/19/platform010` at `2026-08-20 15:53 -0700`, roughly two hours after
  the pins were committed at `2026-08-20 12:53` to `13:05 -0700`. Relinking
  under the new toolchain changes both member digests.
- Pinned support. Seven of the 44 pinned members were modified upstream before
  the current checkout revision: `fbvscode/bootstrapping.py`
  (`39b94855953d`, `2026-08-18`), `clifoundation/lib/py/error/typing.py`
  (`12642c219533`, `2026-08-18`), and the five `python/debuggers` modules
  (`e48eb0cde99d`, `2026-08-19`). All 44 members are Meta-owned: 33 are
  byte-identical to checked-in fbsource sources, 9 are empty namespace
  `__init__.py` files, and 2 are generated by the Meta buck2 prelude
  `make_par` tooling. None is unaccounted for.

The remaining three failures are not drift. They are properties of the fbcode
Python macro layer that predate the pins, so the checked-in boundary was never
satisfiable by a launcher built with this repository's documented command.

- The PAR carries ten executable members the pinned closure does not admit:
  `python/imports_monitor/{__init__,check_jk,imports_monitor,monitor_base,scribe_cat,scuba,scubadata}.py`
  and `cli/py/{__init__,usage/__init__}.py` plus `cli/__init__.py`. They enter
  through `fbcode//python/imports_monitor:imports_monitor`, which
  `tools/build_defs/fbcode_macros/build_defs/lib/python_common.bzl` adds by
  default to every fbcode Linux `python_binary`. That default has been in place
  since `2025-08-04`, with the current install form since `2026-05-14`.
- The executable manifest declares three startup functions, not the single
  pinned `00_STATIC_EXTENSION_FINDER`. The extra
  `00_MULTIPROCESSING_FORK_DEFAULT` hook comes from
  `python.set_multiprocessing_fork_default(enabled = True)` in `fbcode/PACKAGE`,
  in effect since `2026-03-03`. The extra `01_PYTHON_IMPORTS_MONITOR` hook runs
  `python.imports_monitor.imports_monitor:install(...)` at interpreter startup.
  Because the startup-loader digest is taken over the loader body with only the
  `VARS` line normalized away, the extra hooks also change that digest.
- The pinned label pattern requires a configuration name ending in `-no-san`.
  The built target is configured as
  `opt-linux-x86_64-fbcode-platform010-clang21-no-san-opt-by-default#8b1a31e17a6261c4`.
  The `opt-by-default` python modifier has applied since `2025-04-09`.

## Why no repair was committed

Refreshing the native-support digest alone does not unblock authorization; it
moves the failure to the next check. Making the whole boundary pass requires
admitting those ten Meta-owned members and the two additional startup hooks
into the launcher's pre-authentication trusted closure and relaxing the target
label pattern. The launcher's contract is that nothing but the pinned support,
the two dynamic support members, and the authorized profile sources executes
inside the launcher PAR before the runtime is authenticated. Widening that set
by ten members, one of which installs import-time telemetry before
`phase4_runtime_launcher.main` runs, is a reviewed security-boundary decision
rather than a minimal identity refresh, and this cycle is not authorized to
weaken authentication to make the run pass. No source change was made, no
commit was created, and the implementation SHA remains
`3ceddf42baa073f23ea7026e24e11f1f72fdbf2a`.

The current tests do not catch this. Every launcher pin is replaced with
`mock.patch.object` in
`tests/test_policy_improvement_runtime_authorization_unittest.py`, and the test
PARs are synthesized in-process, so no test compares the checked-in identity
against a real Buck artifact.

## Smallest safe next step

The implementation owner needs to choose the launcher closure policy, and then
one reviewed cycle should implement that choice.

- Option A: accept the standard fbcode `python_binary` surface. Regenerate all
  five launcher identity values from a freshly built launcher, pin the exact
  three startup functions and the exact configuration label, and add a test
  that derives the identity from a real Buck artifact instead of mocking it.
  This records that the imports monitor and the fork-default hook run inside
  the authenticated launcher.
- Option B: keep the narrow closure. Set `imports_monitor = False` on the
  `phase4_runtime_launcher` target, which removes all ten extra members using
  existing Meta-owned Buck metadata. The `00_MULTIPROCESSING_FORK_DEFAULT` hook
  and the `-opt-by-default` label suffix still require explicit pin updates.

Either option must also regenerate the pinned-support and native-support
digests from the freshly built launcher and record in the reviewed commit that
the identity was rebound at the current fbsource toolchain.

## Gates and phases in this cycle

- Freeze and inspect: complete, all invariants held.
- Native-support diagnosis: complete.
- Reviewed repair: stopped fail-closed. No source change.
- Fresh static, test, type-check, and build gate: not run. There is no repaired
  commit to run it at, so no test, type-check, or build result in this document
  is claimed for any revision.
- Dataset preflight: not run. The registered dataset identities are unchanged
  from the preceding attempt and were not re-verified in this cycle.
- Runtime authorization, Stage 0 plan, prepare and resume execution, evidence
  inventory, audit, theory smoke, and throughput calibration: not run. No
  execution root, authorization file, plan, checkpoint, result, per-instance
  record, compute-accounting artifact, theory request, theory result, or
  throughput document was created.
- Failed-attempt inventory: zero. No learned execution was attempted.

## Evidence boundary

- No validation content was opened.
- No test content was opened.
- No `TEST_OPEN` was created.
- No historical experiment evidence, result, or checkpoint was inspected,
  reconstructed, or used.
- Stage 0 and theory-smoke outputs are not paper evidence. None exists from
  this cycle.
- Throughput calibration is an engineering measurement only. It was not run,
  and the 4096-interaction tier was neither authorized nor executed.
- No task-performance result or claim was generated.
- No Python library was compiled or installed. No `pip`, `uv`, Poetry, Conda,
  `setup.py`, wheel, virtual environment, or third-party build path was used.
  Every build used Buck2 from the Meta checkout, and every dependency in the
  launcher graph resolves to an existing Meta-owned Buck target.
- No implementation source or configuration file was modified. Both worktrees
  are clean.

The canonical external manifest for this cycle is
`/home/buiksat/upi-trm-stage0-v3-diag.gotJM0D7/metadata/stage0_execution_manifest.json`
with SHA-256
`30d5f426be5262079f606c6ec361d1fabfc431ccfef62c21a89084da2b115578`.

## Remaining blockers after this cycle

### Stage 0

- Runtime authorization remains blocked. The launcher identity boundary in
  `scripts/policy_improvement_runtime_authorization.py` does not describe the
  artifact that `fbcode//buiksat_trm:phase4_runtime_launcher` produces, and
  rebinding it requires the reviewed closure decision above. No authenticated
  Stage 0 package exists at any implementation SHA.

### Stage 1

- Stage 1 remains blocked by the unavailable authenticated train-only
  `base_policy_artifact` and its continuation contract.

### Stage 2 and Stage 3

- Both remain unauthorized. No test-opening capability was created.
