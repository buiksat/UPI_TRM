# ChatGPT Pro review prompt

You are independently reviewing the revised canonical UPI--TRM ICLR theory paper. The attached archive contains:

- `main.tex`, the canonical source;
- `main.pdf`, the compiled paper; and
- `trm_rl.bib`, the bibliography.

Read all three files completely. Treat `main.tex` as the source of truth and use `main.pdf` to audit the rendered artifact. Do not assume that a theorem is correct because the prose says it is. Re-derive every material claim before accepting or criticizing it.

Review the paper as a mathematically demanding ICLR theory reviewer. Concentrate on:

1. theorem correctness, quantifiers, domains, measurability, boundedness, and policy dependence;
2. the absorber convention and the separation between value domains and nonabsorbing latent-path domains;
3. the measurable `B_b(C)` Bellman theorem and its continuous persistent-latent application;
4. exact probability-space mixing, the occupancy TV constant, the signed estimator-defect identity, advantage-span CPI penalty, and safe-step cases;
5. every factor of two, sign, denominator, and `t` versus `t+1` index in TV and coupling arguments;
6. policy-overlap refinements, including the one-step and K-step factors;
7. finite-horizon residual blocks, stagewise spans, partial final blocks, terminal cancellation, and the `H=0`, `h=0`, `K>h`, and `gamma=0` cases;
8. the first-mismatch deployment theorem, standard-Borel coupling assumptions, Pinsker cap, combined CPI/deployment result, and claimed attainment example;
9. persistent state `(x,y,z,h)`, carried pre-unroll versus post-unroll latents, the shared frozen recurrent map, finite-path comparison, and the limits of recurrent-map discrepancy claims;
10. projection invariance, nonexpansiveness, strict-contraction conditions, `L_z=0`, and the state-dependent anchor result;
11. consistency of constants and assumptions across the abstract, main text, appendices, proofs, limitations, conclusion, algorithms, and notation table;
12. novelty and related-work wording, checking that established primitives are not claimed as new;
13. bibliography accuracy using only what can be verified from the supplied files; and
14. PDF quality, including equation rendering, page breaks, anonymous authorship, references, algorithms, and proof placement.

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
