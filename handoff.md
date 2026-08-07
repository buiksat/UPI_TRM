# UPI--TRM paper handoff

Date: 2026-08-07

## Resume point

- Repository: `https://github.com/buiksat/UPI_TRM.git`
- Branch: `iclr-evidence-aligned-revision`
- Paper-theory anchor used by the implementation synchronization: `2107125 Tighten UPI-TRM theory and pseudocode`.
- Resolve and record the actual branch `HEAD` before review. Prompt and handoff maintenance may be newer than the paper-theory anchor.
- Canonical paper directory: `UPI_TRM_ICLR/`
- Current task state: the paper revision and repository cleanup are complete. The next step is an independent ChatGPT Pro review of both the canonical paper and the synchronized implementation, followed by a new Codex editing session only for independently verified repairs.

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

`main.tex` and `trm_rl.bib` are tracked. `main.pdf` is intentionally ignored by `UPI_TRM_ICLR/.gitignore`, so a fresh clone will not contain the current PDF. Rebuild it locally.

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
- file size: 561,399 bytes;
- SHA-256: `b5c639f0d01c4f0e8b10b801c610c632d1d4dd3c0ed6eb9590f1bd1157a8c805`;
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

## Latest paper changes

The current branch through `2107125` contains these important mathematical changes:

1. **Domain-relative recurrent contraction.** Assumption “Domain-relative forward-invariant contraction” now fixes a declared nonabsorbing domain `\(\mathcal D^\circ\)`. Invariance, contraction, initialization, and input-specific fixed-point claims use that same domain. A global condition over all input pairs is only a sufficient special case.
2. **Projection specialization.** “Projection-induced contraction on a saturated annulus” binds `\(x\)` and `\(y\)` through `\(s\in\mathcal C^\circ\)` and concludes contraction only on that domain. It preserves
   \[
   L_z\le \frac{R}{\rho_R}L_z^{\mathrm{pre}}(R).
   \]
3. **Target-network bridge.** The paper distinguishes the target-network population residual from the self-bootstrap Bellman residual and proves
   \[
   \|U_n-\mathcal T_K^\pi U_n\|_\infty
   \le
   \varepsilon_{\mathrm{targ},n}
   +\gamma^K\|\bar V-U_n\|_\infty.
   \]
   It explicitly says finite-batch or mean-square regression diagnostics do not establish the required sup-norm quantities.
4. **Safe exact-mixture step.** On the common policy-pair domain `\(\mathcal C_{\mathrm{pair}}\)`, the branch `\(\gamma>0\)` and `\(0<M<\gamma\Delta_g\)` now uses the nonredundant threshold
   \[
   \alpha\le
   \frac{M(1-\gamma)}{\gamma(\Delta_g-M)}.
   \]
5. **Repository cleanup.** Historical experiment outputs, reports, build snapshots, review archives, ZIP files, unused figures, scripts, and handoff bundles were removed. Do not restore them as part of the theory-paper work.

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

Use the tracked implementation file `reports/CHATGPT_PRO_CODE_AND_PAPER_REVIEW_PROMPT.md` for a new ChatGPT Pro session. It requires direct review of both repositories, an exact-source paper build, complete implementation dependency tracing, adversarial verification, and a written report. It keeps the work theory- and parity-focused and prohibits experiments.

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
2107125 Tighten UPI-TRM theory and pseudocode
1ff4624 Add cross-machine paper handoff
8165170 Add GPT Pro theory review prompt
e222885 update (removed the remaining historical handoff bundles)
c2168d2 Strengthen contraction theory and prune stale artifacts
6f58dda Fix safe-step domain and refresh GPT Pro review bundle
```

Next action:

1. Confirm both named branches are current and record their exact commit SHAs.
2. Start a new ChatGPT Pro session with direct access to both repositories and use `reports/CHATGPT_PRO_CODE_AND_PAPER_REVIEW_PROMPT.md` from the implementation repository.
3. Save ChatGPT Pro's complete report without editing either repository during review.
4. Independently verify every surviving finding.
5. Start a new Codex session only for verified repairs, then rerun the required paper and implementation validation.
