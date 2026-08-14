# UPI--TRM paper handoff

Date: 2026-08-13

## Resume point

- Repository: `https://github.com/buiksat/UPI_TRM.git`
- Branch: `iclr-evidence-aligned-revision`
- Synchronized implementation repository: `https://github.com/gopeshh/trm_bellman.git`
- Synchronized implementation branch: `full-implementation`
- Synchronized implementation source commit: `de013fd3fcaae8bc80d124c0c868c7c8611aeede` (`Close Phase 4 publication validation gaps`).
- Synchronized implementation parent: `12fa350951c31e8635ee51747f6de25295c07333` (`Authenticate Phase 4 publication runtimes`).
- Previous implementation behavior anchor: `980f6ede14717e87ad68ceb32acc111bdd7fca1b` (`Bind Phase 4 publication evidence`).
- Paper source anchor used by the implementation synchronization: `5253692fea5e77cfde3a130c50351183dc0268e3` (`Tighten finite-reference value premise`).
- Resolve and record the actual branch `HEAD` before review. Prompt and handoff maintenance may be newer than the paper-theory anchor.
- Canonical paper directory: `UPI_TRM_ICLR/`
- Current task state: the paper finite-reference theorem now states the
  bounded one-step reward premise needed to identify the block fixed point
  with the ordinary discounted policy value. The implementation has repaired
  the surviving Phase 4 metric-semantics, full-checkpoint, diagnostic-input,
  and evaluator-runtime provenance findings and committed the validated source
  state. Phase 4 now authenticates sealed runtime bytes before behavior imports,
  independently verifies training-producer source, and replays retained
  transitions through the registered environment during checkpoint audit. The
  paper source itself is unchanged.

On a new machine:

```bash
git clone https://github.com/buiksat/UPI_TRM.git
cd UPI_TRM
git switch iclr-evidence-aligned-revision
git pull --ff-only
```

Do not resume work from `main` or from an older archive.

## Canonical files

The active paper uses these files:

```text
UPI_TRM_ICLR/
├── .gitattributes
├── .gitignore
├── Makefile
├── algorithm.sty
├── algorithmic.sty
├── fancyhdr.sty
├── figures/
│   └── trm_to_mdp_bridge.tex
├── iclr2026_conference.bst
├── iclr2026_conference.sty
├── main.tex
├── main.pdf
└── trm_rl.bib
```

The current cross-repository review prompt lives in the implementation repository at `reports/CHATGPT_PRO_CODE_AND_PAPER_REVIEW_PROMPT.md`. It is intentionally outside the canonical paper source tree.

`main.tex`, `trm_rl.bib`, and the validated `main.pdf` are tracked. A fresh
clone contains the inspected PDF. After any paper-source edit, rebuild and
commit the updated PDF with the source rather than editing the PDF directly.

The other top-level paper directories, including `UPI_TRM_ICLR_RSI/`, `UPI_TRM_ICML/`, and `UPI_TRM_NIPS/`, are outside the current task. Do not edit them unless the user explicitly changes scope.

## Build and validation

Run the canonical build from the paper directory:

```bash
cd UPI_TRM_ICLR
make clean
make pdf
```

`make pdf` runs `pdflatex`, `bibtex`, and three additional `pdflatex` passes. The local style, bibliography style, algorithm styles, and TeX figure source are present, so the build does not depend on files elsewhere in the repository.

Last validated artifact before this handoff:

- page count: 38 pages;
- file size: 544,004 bytes;
- SHA-256: `de4fde697f7c835ef2827884569a5a44a12cca473758f91b4fd7dea6d298961d`;
- no missing inputs;
- no undefined references or citations;
- no duplicate labels;
- no LaTeX warnings in the final pass;
- anonymous authorship and submission-mode comments preserved;
- complete PDF inspected, including appendices, proofs, algorithms, figure, references, limitations, and final page.

After any source edit, rebuild until references stabilize, inspect every page, then run:

```bash
git diff --check
git status --short
```

Inspect the complete diff before committing. Do not edit `main.pdf` directly.

The synchronized implementation source commit
`de013fd3fcaae8bc80d124c0c868c7c8611aeede` was validated with these gates:

- 15-target Buck runtime gate, including the expanded Phase 4 runtime,
  checkpoint, environment-replay, and source-identity regressions: 366 passed,
  0 failed;
- complete changed-surface type gate: 30 targets built successfully;
- built training PAR SHA-256: `cafabc3314730f09f6251144a2d2d06c329d7f93f5431a59f252f71f8b6e708e`;
- real launcher `--confirmatory --help`: exit 0, with no private unpack directory left behind;
- wrong-digest, uppercase-digest, malformed-digest, and direct-PAR confirmatory invocations failed closed;
- producer manifest matched all 80 behavior-source entries;
- rebuilt evaluator, audit, and figure PARs matched their complete committed
  Phase 4 source profiles after a stale pre-rebuild artifact was detected and
  rejected;
- 46 shell scripts passed `bash -n`;
- 625 JSON files and 96 YAML files parsed successfully;
- 251 tracked Python files passed source compilation;
- `git diff --check` passed.

The optional repository-wide Buck package pattern is not claimed green because
the prior diagnostic included unrelated historical type debt outside the
changed surface. The required changed-surface type gates above passed. The GPT
Pro review must rerun the required gates at the current branch heads rather
than treating these recorded results as current evidence.

## Latest paper changes

The current branch through `5253692` contains these important mathematical changes:

1. **Finite-reference policy value.** The theorem now assumes a uniformly
   bounded measurable one-step reward under the fixed policy. Its proof first
   constructs the ordinary discounted policy value by uniform convergence,
   then identifies that value as the unique fixed point of the `\(K\)`-step
   Bellman operator. This rules out conditionally cancelling block rewards
   whose ordinary discounted return diverges.
2. **Citation rendering.** Four maintained arXiv references now include stable
   URLs so the tracked bibliography style renders an external locator.
3. **Domain-relative recurrent contraction.** Assumption “Domain-relative forward-invariant contraction” now fixes a declared nonabsorbing domain `\(\mathcal D^\circ\)`. Invariance, contraction, initialization, and input-specific fixed-point claims use that same domain. A global condition over all input pairs is only a sufficient special case.
4. **Projection specialization.** “Projection-induced contraction on a saturated annulus” binds `\(x\)` and `\(y\)` through `\(s\in\mathcal C^\circ\)` and concludes contraction only on that domain. It preserves
   \[
   L_z\le \frac{R}{\rho_R}L_z^{\mathrm{pre}}(R).
   \]
5. **Target-network bridge.** The paper distinguishes the target-network population residual from the self-bootstrap Bellman residual and proves
   \[
   \|U_n-\mathcal T_K^\pi U_n\|_\infty
   \le
   \varepsilon_{\mathrm{targ},n}
   +\gamma^K\|\bar V-U_n\|_\infty.
   \]
   It explicitly says finite-batch or mean-square regression diagnostics do not establish the required sup-norm quantities.
6. **Safe exact-mixture step.** On the common policy-pair domain `\(\mathcal C_{\mathrm{pair}}\)`, the branch `\(\gamma>0\)` and `\(0<M<\gamma\Delta_g\)` now uses the nonredundant threshold
   \[
   \alpha\le
   \frac{M(1-\gamma)}{\gamma(\Delta_g-M)}.
   \]
7. **Repository cleanup.** Historical experiment outputs, reports, build snapshots, review archives, ZIP files, unused figures, scripts, and handoff bundles were removed. Do not restore them as part of the theory-paper work.

## Latest implementation synchronization

Commits `12fa350951c31e8635ee51747f6de25295c07333` and
`de013fd3fcaae8bc80d124c0c868c7c8611aeede` close the Phase 4 runtime and
producer-provenance findings plus the adversarial follow-up gaps:

1. A standard-library launcher authenticates the complete training, evaluator,
   audit, or figure PAR before behavior imports, copies it to a sealed memfd,
   and executes that descriptor. The entrypoint rechecks digest, seals, role,
   module origin, and descriptor-bound unpack directory before importing the
   behavior modules.
2. Audit and figure consumers independently resolve the authorized producer
   commit and manifest. Each of the 12 records binds one externally authorized
   training-PAR SHA-256, and all records must use the same runtime.
3. Strict schema-4 checkpoint loading reconstructs the exact model, optimizers,
   schedulers, RNG, counters, replay, collector, environment, dataset, and
   diagnostic identities. Missing, unexpected, swapped, or fabricated state
   fails closed.
4. Every retained replay transition is run through the exact registered
   `PlanEditEnv`. The audit checks the production action mask, successor state,
   reward, terminal flag, and terminal reason, so impossible replay cannot be
   accepted as resumable evidence.
5. The authenticated consumer source closure includes every imported
   `dataset/*.py` file as well as model, RL, utility, root, and Phase 4 sources.
   Tampered source and bytecode fail before execution.
6. Figure outputs are staged privately, identities are revalidated, and only
   then are publication files replaced. Launcher-owned options cannot be
   overridden by child arguments or `--name=value` aliases.
7. The registered dummy-data builder supplies a deterministic editable cell
   and clue for every Phase 4 record. Training checks action support before the
   first update, and audit regenerates the exact seeded records.

The earlier `L_preproj`, masked policy stability, and complete checkpoint/data
identity repairs from `980f6ede` remain in place.

The prior raw/effective ZIP-name, checkpoint-schema, CleanRL dispatcher,
stochastic replay-readiness, and bibliography repairs from `f86bddb` remain in
place.

The commit retains the descriptor-bound unpack root, sealed complete-runtime
authentication, canonical archive-path checks, environment sanitization, and
runtime-digest evidence binding from `d9ccad7` and `e4edcb2`.

Review these as claims to challenge, not accepted facts. In particular, test
raw versus effective ZIP names, path replacement, same-inode mutation, archive
duplication, unsafe members, bytecode injection, environment override hooks,
descriptor tampering, child startup failure, evidence-schema downgrade, and
cleanup.

The launcher is not a sandbox against the external trust root. The operating
system, host namespace, other same-UID processes, launcher executable, and
initial launcher environment remain trusted. Cleanup is best effort if that
trusted namespace mutates after descriptor acquisition.

The following central constants were intentionally preserved:

\[
\operatorname{TV}(d_{\pi_\alpha},d_\pi)
\le
\frac{\gamma\alpha}{1-\gamma+\gamma\alpha},
\]

\[
\frac{\gamma\alpha^2\Delta_g}
{(1-\gamma)(1-\gamma+\gamma\alpha)},
\qquad
\frac{2\varepsilon_{\mathrm{CPI}}\gamma\alpha^2}
{(1-\gamma)(1-\gamma+\gamma\alpha)},
\]

\[
2\gamma\delta_V\tau(s),
\qquad
2\gamma^K\delta_V\tau(s),
\]

and

\[
\frac{\Delta_r\delta_{\mathrm{dep}}}
{(1-\gamma)(1-\gamma+\gamma\delta_{\mathrm{dep}})}.
\]

Do not restore either older loose `\((1-\gamma)^{-2}\)` penalty.

## Theory scope and semantic constraints

Preserve these points in every future revision:

- The work is theory-only. Experiments are deferred to a later task.
- Review algorithms for mathematical correctness, but do not add experiments or empirical claims.
- The scope remains one fixed MDP, one fixed current/candidate policy pair, one fixed parameter snapshot, and one shared frozen recurrent map when both policies are compared in the same augmented MDP.
- Persistent state is `\((x,y,z,h)\)`, where `\(z\)` is the carried pre-unroll latent. The post-unroll latent is carried after a nonterminal transition.
- Exact mixing is the pointwise probability mixture
  \[
  \pi_\alpha=(1-\alpha)\pi+\alpha\pi_{\mathrm{cand}}.
  \]
  Parameter, logit, hidden-state interpolation, and distillation are different policies unless a deployment discrepancy is proved.
- Value domains include the absorber. Latent-path suprema use nonabsorbing domains and do not invent an absorbing latent.
- Bellman arguments use the value-function fixed point `\(V^\pi\)`. The primary finite-reference argument does not require a recurrent latent fixed point. Do not call the full analysis “fixed-point-free.”
- Projection gives forward invariance and nonexpansiveness. It gives strict contraction only when the proved product modulus is below one.
- Uniform theorem premises are not consequences of finite-batch diagnostics.
- Folded terminal rewards, zero or common terminal bootstrap, and the absorbing boundary must count the terminal contribution exactly once.
- Exact-mixture occupancy uses `\(1-(1-\alpha)^t\)` because occupancy is measured before decision `\(t\)`. Deployment reward mismatch uses `\(1-(1-\delta_{\mathrm{dep}})^{t+1}\)` because reward `\(r_t\)` follows decision `\(t\)`.
- Preserve `\(\operatorname{TV}(p,q)=\tfrac12\|p-q\|_1\)` in finite or countable settings and do not add an extra factor of two to span-TV inequalities.
- Keep novelty claims conservative. The contribution is a domain-specific synthesis and composition, not priority claims for standard Bellman, Banach, occupancy, or coupling tools.

## ChatGPT Pro cross-repository review workflow

Use the implementation's tracked file
`reports/CHATGPT_PRO_CODE_AND_PAPER_REVIEW_PROMPT.md` at the current
implementation branch head for a new ChatGPT Pro session. The frozen behavior
source anchor is `de013fd3fcaae8bc80d124c0c868c7c8611aeede`; later commits may update
only `README.md`, `reports/**`, or other handoff documentation. The prompt
requires direct review of both
repositories, an exact-source paper build, complete implementation dependency
tracing, sealed-runtime adversarial checks, and a written report. It keeps the
work theory- and parity-focused and prohibits experiments.

Give ChatGPT Pro direct read access to these branches:

```text
/home/buiksat/trm_bellman  branch full-implementation
/home/buiksat/UPI_TRM     branch iclr-evidence-aligned-revision
```

If the review environment cannot access those paths, clone the two remotes into a temporary directory and check out the named branches. If only file uploads are available, export both exact commits outside either repository and upload the complete clean trees plus the new prompt. Do not commit generated ZIP files or review bundles.

The prompt requires a blind pass before ChatGPT Pro reads prior review reports. Treat every prior finding and verdict as a hypothesis. When ChatGPT Pro returns its report, re-derive each proposed repair against the current repositories before editing anything.

## Git history and next action

Relevant commits, newest first:

```text
5253692 Tighten finite-reference value premise
bb11de7 Replace paper-only review prompts
2107125 Tighten UPI-TRM theory and pseudocode
1ff4624 Add cross-machine paper handoff
8165170 Add GPT Pro theory review prompt
e222885 update (removed the remaining historical handoff bundles)
c2168d2 Strengthen contraction theory and prune stale artifacts
6f58dda Fix safe-step domain and refresh GPT Pro review bundle
```

Next action:

1. Confirm both named branches are current and record their exact commit SHAs.
2. Start a new ChatGPT Pro session with direct access to both repositories and
   use `reports/CHATGPT_PRO_CODE_AND_PAPER_REVIEW_PROMPT.md` from the
   implementation repository.
3. Save ChatGPT Pro's complete report without editing either repository during
   review.
4. Independently verify every surviving finding before starting another repair.
