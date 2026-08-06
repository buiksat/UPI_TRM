# UPI--TRM paper handoff

Date: 2026-08-06

## Resume point

- Repository: `https://github.com/buiksat/UPI_TRM.git`
- Branch: `iclr-evidence-aligned-revision`
- Last substantive commit: `8165170 Add GPT Pro theory review prompt`
- At handoff creation, local `HEAD` and `origin/iclr-evidence-aligned-revision` both pointed to `8165170` and the worktree was clean.
- Canonical paper directory: `UPI_TRM_ICLR/`
- Current task state: the paper revision and repository cleanup are complete. The next step is an independent GPT Pro theory and algorithm review, followed by a new Codex editing session only if that review finds verified repairs or worthwhile theory improvements.

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
├── GPT_PRO_THEORY_REVIEW_PROMPT.md
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

- page count: 34 pages;
- file size: 536,967 bytes;
- SHA-256: `b1e07cc67aef054ecad140a56f624b1858a05fd1ae3e5516a3ebb25b9bcd6ac0`;
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

Commit `c2168d2` revised `main.tex` and removed stale artifacts. The important mathematical changes are:

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

## GPT Pro review workflow

The tracked file `UPI_TRM_ICLR/GPT_PRO_THEORY_REVIEW_PROMPT.md` is the final prompt for a new GPT Pro session. It tells GPT Pro to:

- read `main.tex`, `main.pdf`, and `trm_rl.bib` completely;
- review only theory and algorithms, not experiments;
- adversarially re-derive the central results;
- look for valid, useful theory improvements;
- separate required repairs from optional future extensions;
- produce a complete standalone implementation prompt for a brand-new Codex session.

For the GPT Pro session, provide exactly these four files unless the user asks for a different package:

```text
main.tex
main.pdf
trm_rl.bib
GPT_PRO_THEORY_REVIEW_PROMPT.md
```

Do not include styles, figures, logs, build intermediates, old prompts, reports, or unrelated files in the review ZIP. GPT Pro is reviewing the supplied source and PDF, not reproducing the LaTeX build.

When GPT Pro returns its review, do not implement findings mechanically. Re-derive each proposed repair against the current repository. Implement only verified corrections and high-value improvements that fit the established scope. Preserve every central constant unless a complete derivation proves it wrong.

## Git history and next action

Relevant commits, newest first:

```text
8165170 Add GPT Pro theory review prompt
e222885 update (removed the remaining historical handoff bundles)
c2168d2 Strengthen contraction theory and prune stale artifacts
6f58dda Fix safe-step domain and refresh GPT Pro review bundle
```

Next action:

1. Rebuild `main.pdf` on the new machine.
2. Send the four-file set above to a new GPT Pro session with `GPT_PRO_THEORY_REVIEW_PROMPT.md` as the prompt.
3. Save GPT Pro's complete response.
4. Start a new Codex session using the standalone implementation prompt generated by GPT Pro.
5. Let Codex edit and rebuild the paper only after independently confirming the proposed mathematics.
