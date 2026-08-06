# GPT Pro prompt: independent theory and algorithm review

You are independently reviewing the canonical UPI--TRM ICLR theory paper after its latest revision. This is a new session. You have no access to earlier reviews or implementation discussions.

Read the following supplied files completely before forming conclusions:

- `main.tex`
- `main.pdf`
- `trm_rl.bib`

Treat the current source as authoritative. Use `main.pdf` to check the rendered artifact against the source. Do not invent missing repository context, line numbers, citations, experiments, or build results.

## Scope

Review only the paper's theory and algorithms. Do not review, request, design, or speculate about experiments, empirical validation, benchmarks, runtime behavior, or numerical results. Experiments will be considered later.

For algorithms and pseudocode, review mathematical correctness, inputs and outputs, state conventions, indexing, policy definitions, terminal handling, and consistency with the stated theorems. Do not treat pseudocode as evidence that runtime behavior or an empirical guarantee has been established.

The paper intentionally remains scoped to:

- one fixed MDP;
- one fixed current/candidate policy pair;
- one fixed parameter snapshot;
- one shared frozen recurrent map when both policies are analyzed in the same augmented MDP.

Do not recommend broadening that scope. Do not ask for experiments. Do not infer a theorem from diagnostics or finite-batch measurements.

## Review standard

Treat every possible defect as a hypothesis. Re-derive each result before reporting it. Default to rejecting speculative findings. A strong assumption is not an error when it is explicit and used correctly.

For every surviving finding, provide an auditable derivation or counterexample. Distinguish among:

1. blocking mathematical errors;
2. material but repairable errors;
3. minor precision or presentation issues;
4. optional theory improvements.

Do not propose changing an already-correct constant merely because a looser proof is easier. Do not produce stronger-looking claims that require assumptions so restrictive that the result becomes uninformative.

## Recent revisions to audit

The latest revision was intended to make these changes. Verify them against the source rather than assuming they are correct.

### Domain-relative recurrent contraction

The contraction premise should be relative to a declared nonabsorbing domain \(\mathcal D^\circ\). For \(s\in\mathcal D^\circ\), the input-specific map is

\[
T_s(z):=\widetilde f_\theta\bigl(z,y(s),x(s)\bigr).
\]

There should exist a closed invariant set \(\mathcal Z_{\mathrm{inv}}\) and \(L_z\in[0,1)\) such that, uniformly for every \(s\in\mathcal D^\circ\),

\[
T_s(\mathcal Z_{\mathrm{inv}})\subseteq\mathcal Z_{\mathrm{inv}}
\]

and

\[
\|T_s(z)-T_s(z')\|
\le L_z\|z-z'\|
\qquad
\text{for all }z,z'\in\mathcal Z_{\mathrm{inv}}.
\]

Initialization should be required on that same declared domain. Banach fixed-point existence and uniqueness should be asserted only for the input pairs represented there. A genuinely global condition over every mathematically possible \((x,y)\) may be described as a sufficient special case, but it must not be inferred from closure-restricted premises.

Audit every episodic, projection-aware, and persistent-latent use of this assumption. Confirm that each result instantiates the correct nonabsorbing domain and that no proof silently changes domains.

### Projection-induced contraction

Audit the projection-induced contraction proposition and all downstream uses. Its saturation premise should bind the inputs through the state:

\[
\|f_\theta(z,y(s),x(s))\|\ge \rho_R
\qquad
\text{for every }s\in\mathcal C^\circ,
\ z\in B_R,
\]

with \(\rho_R>R\). Its pre-projection modulus should use the same state domain. Re-derive the radial projection estimate

\[
\|\operatorname{Proj}_{B_R}(u)-\operatorname{Proj}_{B_R}(v)\|
\le \frac{R}{\rho_R}\|u-v\|
\]

under the stated saturation premises, and then verify

\[
L_z\le \frac{R}{\rho_R}L_z^{\mathrm{pre}}(R).
\]

The result should conclude only domain-relative contraction and forward invariance when

\[
\frac{R}{\rho_R}L_z^{\mathrm{pre}}(R)<1
\]

and the relevant initializations lie in \(B_R\). Check that the paper keeps projection-induced invariance, Euclidean-projection nonexpansiveness, a Lipschitz upper bound, and strict contraction as distinct claims. Check the conventions \(L_z^0=1\) and, when \(L_z=0\), \(L_z^n=0\) for every integer \(n\ge1\).

### Target-network residual bridge

The implementation discussion uses a \(K\)-step target network, whereas the certificate uses a self-bootstrap Bellman residual. Verify that the paper does not identify those two population operators.

For bounded measurable \(U_n\) and \(\bar V\) on the same invariant domain, it should define

\[
\varepsilon_{\mathrm{targ},n}
:=
\left\|
U_n-
\left(r_K^\pi+\gamma^K P_\pi^K\bar V\right)
\right\|_\infty
\]

and prove

\[
\begin{aligned}
\|U_n-\mathcal T_K^\pi U_n\|_\infty
&\le
\varepsilon_{\mathrm{targ},n}
+\gamma^K\|P_\pi^K(\bar V-U_n)\|_\infty\\
&\le
\varepsilon_{\mathrm{targ},n}
+\gamma^K\|\bar V-U_n\|_\infty.
\end{aligned}
\]

Check the invariant-domain, policy, boundedness, measurability, folded-terminal-reward, and absorbing-boundary conditions. Confirm that the source explicitly says empirical regression loss, finite-batch diagnostics, and \(L^2\) error do not establish either displayed sup-norm quantity.

### Safe exact-mixture step

Audit the safe-step result on the common \(\pi/\pi_{\mathrm{cand}}\)-invariant domain \(\mathcal C_{\mathrm{pair}}\). Interval guarantees must use \(M\), \(g\), and \(\Delta_g\) defined independently of \(\alpha\) on one common domain, not on an \(\alpha\)-specific occupancy domain.

For

\[
\gamma>0,
\qquad
0<M<\gamma\Delta_g,
\]

verify that the certified threshold is

\[
\alpha
\le
\frac{M(1-\gamma)}
{\gamma(\Delta_g-M)}.
\]

Prove that its denominator is positive and the threshold lies strictly between zero and one, so no redundant outer minimum with one is needed. Check all boundary cases:

- \(\alpha\in\{0,1\}\);
- \(\gamma=0\);
- \(M<0\);
- \(M=0\);
- \(\Delta_g=0\);
- \(M=\gamma\Delta_g\).

## Central results to re-derive

Independently verify the following results and their assumptions. These formulas should not change unless you find and demonstrate a genuine mathematical error.

### Measurable Bellman contraction

\[
\|\mathcal T_K^\pi V-\mathcal T_K^\pi W\|_\infty
\le
\gamma^K\|V-W\|_\infty.
\]

### Finite-reference residual certificate

\[
\|U_n-V^\pi\|_\infty
\le
\|U_n-U_m\|_\infty
+
\frac{
\|U_m-\mathcal T_K^\pi U_m\|_\infty
}{1-\gamma^K}.
\]

### Exact-mixture occupancy

\[
\operatorname{TV}(d_{\pi_\alpha},d_\pi)
\le
\frac{\gamma\alpha}{1-\gamma+\gamma\alpha}.
\]

For finite or countable state spaces, check

\[
\|d_{\pi_\alpha}-d_\pi\|_1
\le
\frac{2\gamma\alpha}{1-\gamma+\gamma\alpha}.
\]

### Signed estimator defect and CPI penalty

Verify the exact signed-defect identity and the span penalty

\[
\widehat L_\pi(\pi_\alpha)-L_\pi(\pi_\alpha)
=\frac{\Xi_\alpha}{1-\gamma}
\]

and

\[
\frac{\gamma\alpha^2\Delta_g}
{(1-\gamma)(1-\gamma+\gamma\alpha)}.
\]

Check the scalar specialization

\[
\frac{2\varepsilon_{\mathrm{CPI}}\gamma\alpha^2}
{(1-\gamma)(1-\gamma+\gamma\alpha)}.
\]

### Policy-overlap refinements

Verify the factors

\[
2\gamma\delta_V\tau(s)
\qquad\text{and}\qquad
2\gamma^K\delta_V\tau(s)
\]

for the estimators to which they are applied.

### Deployment perturbation

Verify

\[
\frac{\Delta_r\delta_{\mathrm{dep}}}
{(1-\gamma)(1-\gamma+\gamma\delta_{\mathrm{dep}})}.
\]

Check the time indices carefully. Exact-mixture state occupancy before decision \(t\) uses

\[
1-(1-\alpha)^t,
\]

whereas reward mismatch following deployment decision \(t\) uses

\[
1-(1-\delta_{\mathrm{dep}})^{t+1}.
\]

Do not introduce an extra factor of two into a span-versus-TV inequality. Confirm that \(\operatorname{TV}(p,q)=\tfrac12\|p-q\|_1\) whenever vector \(\ell_1\) notation is used for finite or countable spaces.

## Complete theory and algorithm audit

Check the entire paper, including every appendix and proof, for:

- measurable state and action spaces, stochastic-kernel quantifiers, invariance, and bounded measurability;
- separation between value domains containing the absorber and nonabsorbing latent-path domains;
- the carried pre-unroll latent and post-unroll latent convention;
- use of one shared frozen recurrent map for policies compared in the same augmented MDP;
- exact pointwise probability mixing versus parameter, logit, hidden-state interpolation, or distillation;
- the distinction between a value-function fixed point and a recurrent latent fixed point;
- finite-horizon indexing, stagewise spans, terminal cancellation, \(H=0\), \(h=0\), \(K>h\), and final partial blocks;
- signs of occupancy-averaged estimator defects;
- every factor of two introduced through total variation;
- theorem premises matching their proofs and downstream corollaries;
- algorithm pseudocode matching the formal state, policy, reward, bootstrap, and terminal conventions;
- unsupported uniform guarantees inferred from batch diagnostics;
- conservative novelty language and citations that are actually supported by the bibliography;
- stale equation, theorem, proposition, section, or appendix references;
- source/PDF disagreement, malformed equations, detached proofs, or material layout failures.

## Opportunities to improve the theory

Actively look for ways to improve the theory, not just errors. A proposed improvement must be:

- mathematically valid under explicit assumptions;
- within the fixed-MDP, fixed-policy-pair, fixed-parameter-snapshot scope;
- compatible with the measurable \(B_b(\mathcal C)\) formulation and the paper's state conventions;
- materially sharper, clearer, more general, or less assumption-heavy than the current result;
- supported by a derivation, proof outline, or counterexample showing why the change is valid;
- worth the theorem volume and complexity it adds.

For each proposal, state:

1. the current theorem or argument;
2. the proposed statement;
3. assumptions added, removed, or weakened;
4. a derivation or proof outline;
5. constants and downstream results affected;
6. whether it should be implemented now or deferred as future work.

Separate theory improvements into:

- high-value improvements recommended for this revision;
- correct but optional extensions;
- tempting strengthenings that fail or require uninformative assumptions.

Do not use experiments as justification for any theory improvement.

## Required response

Begin with exactly one verdict:

- `APPROVE`
- `APPROVE WITH MINOR REPAIRS`
- `MATERIAL REPAIRS REQUIRED`
- `BLOCKING ERROR`

Then provide the following sections.

### 1. Surviving findings

List findings in decreasing severity. For every finding include:

- the theorem, proposition, equation, algorithm, or section name;
- an exact source quotation or uniquely searchable source text;
- the mathematical derivation, counterexample, or consistency argument;
- the smallest correct repair;
- every downstream statement affected.

Do not report vague stylistic preferences as mathematical findings.

### 2. Theory improvements

Give the structured analysis requested above. Clearly identify which improvements should be implemented now.

### 3. Rejected candidate concerns

List plausible concerns you investigated and rejected. State the mathematical reason each one is not an error. This section should make clear that you adversarially checked the central results rather than merely accepting them.

### 4. Constant and boundary audit

Explicitly confirm each central constant above or give its corrected form with a complete derivation. Report the result of every listed boundary and indexing check.

### 5. Standalone implementation prompt for a new Codex session

Write a complete implementation prompt that can be copied directly into a brand-new Codex session. Assume that Codex has no access to this review, this conversation, or any prior session, but does have access to the repository.

The implementation prompt must:

- instruct Codex to edit the canonical paper directly rather than return only a review;
- identify every repository file that must be read completely before editing;
- contain all required correctness repairs that survived your review;
- include only the theory improvements you recommend implementing now;
- state every required formula, assumption, domain, quantifier, and boundary case explicitly;
- identify affected theorems, propositions, equations, proofs, algorithms, and sections through names or uniquely searchable text rather than unreliable line numbers;
- state which established constants and semantic distinctions must remain unchanged;
- require propagation through the abstract, introduction, contributions, main results, algorithms, appendices, limitations, conclusion, and notation wherever applicable;
- preserve the fixed-MDP, fixed-policy-pair, fixed-parameter-snapshot, shared-frozen-map scope;
- prohibit new experiments, experimental edits, empirical claims, unsupported novelty claims, and changes justified only by diagnostics;
- require a baseline build before editing and record its page count and warnings;
- require rebuilding `main.pdf` from `main.tex` through the repository's canonical build path;
- require full-source searches for stale statements and references;
- require independent mathematical and edge-case validation;
- require `git diff --check`, inspection of the complete diff, and inspection of every page of the rebuilt PDF;
- require a final report listing changed files, theorem-level changes, assumptions, preserved or changed constants, validation, the exact build command, final page count, and warnings.

The Codex prompt must be fully self-contained. Do not say “apply the findings above,” “as discussed,” or otherwise rely on context outside that prompt. Include every fact the new Codex session needs. State explicitly that the task is incomplete until the canonical source has been edited, `main.pdf` has been rebuilt, and the complete final PDF has been inspected.
