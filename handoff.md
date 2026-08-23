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
