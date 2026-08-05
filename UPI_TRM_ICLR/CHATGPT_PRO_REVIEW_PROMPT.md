# ChatGPT Pro review prompt

You are independently reviewing the revised canonical UPI--TRM ICLR theory paper. The attached archive contains:

- `main.tex`, the canonical source;
- `main.pdf`, the compiled paper;
- `trm_rl.bib`, the bibliography;
- `Makefile`, the canonical build path;
- `iclr2026_conference.sty` and `iclr2026_conference.bst`, the exact ICLR
  template files used by the paper;
- `algorithm.sty`, `algorithmic.sty`, and `fancyhdr.sty`, the local style
  dependencies selected by this source; and
- `figures/trm_to_mdp_bridge.tex`, the TikZ source included by `main.tex`.

Read `main.tex`, `main.pdf`, and `trm_rl.bib` completely. Inspect the build
and figure sources where relevant. Treat `main.tex` as the source of truth
and use `main.pdf` to audit the rendered artifact. Do not assume that a
theorem is correct because the prose says it is. Re-derive every material
claim before accepting or criticizing it.

From a fresh extraction with a standard TeX Live installation, reproduce the
paper by running `make pdf`. The archive contains every repository-local
source dependency used by that command; disposable build products are
intentionally excluded.

Review the paper as a mathematically demanding ICLR theory reviewer. Concentrate on:

1. theorem correctness, quantifiers, domains, measurability, boundedness, and policy dependence;
2. the absorber convention and the separation between value domains and nonabsorbing latent-path domains;
3. the measurable `B_b(C)` Bellman theorem and its continuous persistent-latent application;
4. exact probability-space mixing, the occupancy TV constant, the signed
   estimator-defect identity, and the advantage-span CPI penalty;
5. the distinction between the fixed-$\alpha$ mixture domain and the common
   $\pi$/$\pi_{\mathrm{cand}}$-invariant domain used by the safe-step interval,
   including all safe-step boundary cases;
6. every factor of two, sign, denominator, and `t` versus `t+1` index in TV and coupling arguments;
7. policy-overlap refinements, including the one-step and K-step factors;
8. finite-horizon residual blocks, stagewise spans, partial final blocks, terminal cancellation, and the `H=0`, `h=0`, `K>h`, and `gamma=0` cases;
9. the first-mismatch deployment theorem, standard-Borel coupling assumptions, Pinsker cap, combined CPI/deployment result, and claimed attainment example;
10. persistent state `(x,y,z,h)`, carried pre-unroll versus post-unroll latents, the shared frozen recurrent map, finite-path comparison, and the limits of recurrent-map discrepancy claims;
11. projection invariance, nonexpansiveness, strict-contraction conditions, `L_z=0`, and the state-dependent anchor result;
12. consistency of constants and assumptions across the abstract, main text, appendices, proofs, limitations, conclusion, algorithms, and notation table;
13. novelty and related-work wording, checking that established primitives are not claimed as new;
14. bibliography accuracy using only what can be verified from the supplied files; and
15. PDF quality, including equation rendering, page breaks, anonymous authorship, references, algorithms, and proof placement.

Check these identities and boundary cases independently:

```text
(1-gamma) sum_{t>=0} gamma^t [1-(1-alpha)^t]
  = gamma alpha / (1-gamma+gamma alpha)

sum_{t>=0} gamma^t [1-(1-delta)^(t+1)]
  = delta / ((1-gamma)(1-gamma+gamma delta))
```

Also compare every new constant with its older loose `(1-gamma)^(-2)` counterpart. Look for counterexamples before recommending stronger statements.

The paper is theory-only and intentionally scoped to a fixed MDP, fixed policy pair, fixed parameter snapshot, and shared recurrent map. Do not request experiments, fabricate empirical implications, or broaden this scope. Do not recommend new citations unless you can identify a verified primary source and state exactly which claim it supports.

## Required response

Return exactly two substantive sections.

### 1. Independent review

List only findings that survive adversarial verification. Classify each as blocking, material, or minor. For every finding:

- identify the theorem, equation, section, and quoted source phrase where possible;
- explain the mathematical or presentation problem precisely;
- give a derivation, counterexample, or concrete reason;
- state the smallest valid repair; and
- note downstream statements that must change.

Explicitly state what you checked and cleared. If a suspected issue is not real, omit it from the findings rather than presenting it as a concern. Distinguish mathematical errors from optional exposition improvements.

### 2. Ready-to-paste implementation prompt for Codex

Write a self-contained prompt that I can paste directly to Codex in the repository. It must instruct Codex to:

- edit the canonical files rather than return only recommendations;
- read the relevant source and re-derive each proposed change;
- preserve all correct scope distinctions and constants;
- implement only verified repairs and high-value improvements;
- propagate changes through theorem statements, proofs, prose, notation, and appendices;
- rebuild with the repository's standard build path until references stabilize;
- inspect the complete final PDF; and
- report files changed, mathematical changes, validation, build command, page count, warnings, and any rejected suggestion.

Make that implementation prompt specific enough to execute without another review pass. If the paper has no blocking or material defect, say so and make the prompt target only the justified minor improvements. Do not weaken assumptions or tests merely to make a proposed strengthening appear true.
