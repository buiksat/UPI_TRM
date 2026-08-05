# Theory-Only Audit and Strengthening Report

## Audit scope and bundle integrity

I read `REVIEW_PROMPT.md`, `main.pdf`, `main.tex`, and `trm_rl.bib` completely, including the appendices, proofs, algorithms, captions, and limitations.

Bundle checks passed:

| File | Observed SHA-256 | Expected | Status |
|---|---|---|---|
| `main.tex` | `69f3eb3f3b1951780714fc82ec216476d2d724fc999229a415c46b9e12d4b625` | same | match |
| `main.pdf` | `f15d1c1d453477e56148bd24af34cdd6dd658d29558ac41d78dee735bc3ddce6` | same | match |
| `trm_rl.bib` | `2e420066b2f54d80e99a4e31f2e466ea36998e8583b4f1f4818ea16b4f86bdc9` | same | match |
| `main.pdf` page count | 29 | 29 | match |

The bundle therefore has no identity or hash mismatch. The rendered PDF and the supplied TeX agree on the theorem statements, equations, numbering, and appendices that can be inspected. The source contains `\input{figures/trm_to_mdp_bridge.tex}` at `main.tex:142–146`, but that local figure source is not supplied. Exact source recompilation is:

> not verifiable from supplied evidence

The actual runtime behavior, replay serialization, optimizer sequencing, checkpoint state, datasets, and implementation-level terminal masking are:

> not verifiable from supplied evidence

---

# 1. Blocking correctness findings

## 1.1 The recurrent-path supremum is formally undefined at the absorber

**Classification:** incomplete or ambiguous.

**Location:** `main.tex:257–301`, especially `main.tex:294–299`; proof at `main.tex:1758–1765`; PDF p. 5 and proof on PDF p. 23. The closure definition is at `main.tex:895–904`; PDF p. 14.

Definition 8.2 explicitly includes `s_abs` in
\(\mathcal R_{\pi,\pi_{\mathrm{cand}}}^{\mathrm{adv}}\). Equation (9) then writes

\[
\sup_{s\in\mathcal R_{\pi,\pi_{\mathrm{cand}}}^{\mathrm{adv}}}
\|z^{(j+1)}(s)-z^{(j)}(s)\|.
\]

No latent path \(z^{(j)}(s_{\mathrm{abs}})\) is defined. The theorem defines only a depth-independent scalar boundary \(U_j(s_{\mathrm{abs}})=b\). The proof implicitly repairs the issue by proving the latent inequality only “for every nonabsorbing \(s\)” and then observing that the scalar difference is zero at the absorber.

The smallest valid repair is to define

\[
\mathcal C^\circ
:=\mathcal R_{\pi,\pi_{\mathrm{cand}}}^{\mathrm{adv}}
\setminus\{s_{\mathrm{abs}}\}
\]

and take every recurrent-path supremum over \(\mathcal C^\circ\). There is no need to invent an absorbing latent. This correction also removes the redundant union with \(\{s_{\mathrm{abs}}\}\) at `main.tex:262–263` and `main.tex:352–353`, because Definition 8.2 already includes it.

A strictly stronger path inequality should be displayed before the current sum-of-suprema relaxation:

\[
\|U_n-U_m\|_\infty
\le
L_V\sup_{s\in\mathcal C^\circ}
\sum_{j=n}^{m-1}\|z^{(j+1)}(s)-z^{(j)}(s)\|
\le
L_V\sum_{j=n}^{m-1}
\sup_{s\in\mathcal C^\circ}
\|z^{(j+1)}(s)-z^{(j)}(s)\|.
\]

The first inequality can be strictly tighter when different states maximize different depth increments.

## 1.2 The stated general-kernel route does not close as an `L^∞(ν)` theorem

**Classification:** incomplete or ambiguous as an extension; the finite/countable theorems remain correct.

**Location:** scope statement at `main.tex:165–177`; general-kernel remark at `main.tex:935–938`; persistent-state scope at `main.tex:675–759`; PDF pp. 3, 12, and 14–15.

The paper correctly says that the measurable-space extension is not part of the formal claims. The proposed route through one common \(L^\infty(\nu)\) space is incomplete, however. Dominating all relevant transition laws is not enough to make every value and occupancy statement meaningful on \(\nu\)-equivalence classes. At minimum, an `L^∞(ν)` formulation also needs:

- the initial law \(\rho\ll\nu\), hence every occupancy law of interest dominated by \(\nu\);
- \(\nu\)-nonsingularity of the policy-induced kernel, so \(P_\pi(s,\cdot)\ll\nu\) on the declared domain and Bellman integration does not depend on the representative of an `L^∞(ν)` class;
- joint measurability of rewards, kernels, policies, and the integrated Bellman terms;
- a precise “for policy-almost every action” replacement for action support when no topology is assumed;
- a signed-measure total-variation formulation for CPI and deployment.

A cleaner theorem uses \(B_b(\mathcal C)\), the bounded measurable functions on a measurable invariant set \(\mathcal C\), with the ordinary pointwise supremum. A Markov kernel is automatically nonexpansive in this norm, and no dominating measure is needed. This directly covers continuous latent states in the persistent augmented MDP.

This is material because the persistent state is \((x,y,z,h)\) with \(z\in\mathbb R^d\). The formal finite/countable restriction can cover a deterministic finite reachable set, but it does not cover the general continuous-latent model described by the architecture. The theorem is not false; its present formal scope is narrower than the motivating model.

## 1.3 The central infinite-horizon CPI constant is valid but avoidably loose

**Classification:** correct but the constant is loose.

**Location:** Theorem 4.1 at `main.tex:466–498`; occupancy proof at `main.tex:1372–1469`; PDF pp. 7–8 and 19.

The manuscript bounds

\[
\|d_{\pi_\alpha}-d_\pi\|_1
\le \frac{2\gamma\alpha}{1-\gamma}
\]

by combining a generic occupancy perturbation lemma with
\(\|\pi_\alpha-\pi\|_1\le2\alpha\). For the exact mixture
\(\pi_\alpha=(1-\alpha)\pi+\alpha\pi_{\mathrm{cand}}\), the same coupling already used in the finite-horizon theorem gives the sharper exact-mixture bound

\[
\|d_{\pi_\alpha}-d_\pi\|_1
\le
2(1-\gamma)\sum_{t\ge0}\gamma^t
\bigl[1-(1-\alpha)^t\bigr]
=
\frac{2\gamma\alpha}{1-\gamma+\gamma\alpha}.
\]

Therefore the quadratic penalty can be replaced by

\[
\boxed{
\frac{2\varepsilon_{\mathrm{CPI}}\gamma\alpha^2}
{(1-\gamma)(1-\gamma+\gamma\alpha)}
}
\]

instead of

\[
\frac{2\varepsilon_{\mathrm{CPI}}\gamma\alpha^2}{(1-\gamma)^2}.
\]

Dominance is immediate because
\(1-\gamma+\gamma\alpha\ge1-\gamma\). The two constants are equal when \(\alpha=0\), \(\gamma=0\), or \(\varepsilon_{\mathrm{CPI}}=0\); otherwise the proposed constant is strictly smaller.

The bound is sharp under the manuscript’s scalar \(\varepsilon_{\mathrm{CPI}}\) assumption. Use states \(s_0,s_1\), initial state \(s_0\), and \(V^\pi\equiv0\). The current policy stays in either state with zero reward. At \(s_0\), the candidate receives reward \(+\varepsilon\) and moves to \(s_1\); at \(s_1\), it self-loops with reward \(-\varepsilon\). Then \(\delta(s_0)=\varepsilon\), \(\delta(s_1)=-\varepsilon\), and the gap between the current-state surrogate and the true mixture return equals the proposed penalty exactly.

Because the paper already proves the finite-horizon exact-mixture coupling at `main.tex:1199–1206`, retaining the looser infinite-horizon denominator creates an internal missed opportunity rather than a technical barrier.

## 1.4 The deployment theorem is correct but substantially looser than direct coupling

**Classification:** correct but the constant is loose.

**Location:** Theorem 9.3 and Corollary 9.4 at `main.tex:1222–1326`; PDF p. 18.

The current infinite-horizon deployment bound is

\[
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
\le
\frac{\Delta_r\delta}{(1-\gamma)^2}.
\]

Maximally couple the two policies while their states agree. The probability that reward \(r_t\) can differ is at most
\(1-(1-\delta)^{t+1}\). Hence

\[
\begin{aligned}
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
&\le
\Delta_r\sum_{t\ge0}\gamma^t
\bigl[1-(1-\delta)^{t+1}\bigr]\\
&=
\boxed{
\frac{\Delta_r\delta}
{(1-\gamma)(1-\gamma+\gamma\delta)}
}.
\end{aligned}
\]

The finite-horizon analogue is

\[
\boxed{
\Delta_r\Bigl[
G_H(\gamma)-(1-\delta)G_H(\gamma(1-\delta))
\Bigr].
}
\]

These dominate the current constants. Equality with the current infinite-horizon constant occurs at \(\delta=0\) or \(\gamma=0\); otherwise the coupling constant is strictly smaller.

A matching construction uses a common state in which the reference policy always receives \(r_{\min}\) and stays put, while the deployed policy chooses a mismatch action with probability \(\delta\), receives \(r_{\max}\), and enters an \(r_{\max}\)-absorbing state. The reward difference at time \(t\) then occurs exactly when a mismatch has happened by decision \(t\).

The KL corollary should use

\[
\bar\delta_\kappa:=\min\{1,\sqrt{\kappa/2}\}
\]

before substitution. Pinsker is valid in either displayed KL direction, but total variation never exceeds one.

## 1.5 The supplied source is not self-contained for recompilation

**Classification:** artifact/reproducibility limitation, not a mathematical error.

**Location:** `main.tex:142–146`; PDF p. 2.

The expected bundle intentionally contains four files and all expected hashes match, so this is not a bundle-integrity mismatch. The TeX nevertheless imports an unsupplied local figure file. Exact source-to-PDF regeneration is:

> not verifiable from supplied evidence

The repair is to include `figures/trm_to_mdp_bridge.tex` or inline the TikZ/PGF source.

**Bottom line on correctness:** I found no false central theorem. The main formal defect is the absorber in the recurrent-path supremum. The larger submission-level issue is that the clean continuous-state theorem needed by the persistent-latent model is not stated.

---

# 2. Verified results

## 2.1 Finite-reference-depth value decomposition

**Classification:** correct as stated after the absorber-domain repair; assumptions are stronger than necessary.

**Location:** `main.tex:247–301`, proof `main.tex:1742–1780`; PDF p. 5 and p. 23.

Let \(T=\mathcal T_K^\pi\), whose contraction modulus is \(\beta=\gamma^K\). Since \(V^\pi=TV^\pi\),

\[
\begin{aligned}
\|U_m-V^\pi\|_\infty
&\le
\|U_m-TU_m\|_\infty
+
\|TU_m-TV^\pi\|_\infty\\
&\le
\|U_m-TU_m\|_\infty
+
\beta\|U_m-V^\pi\|_\infty.
\end{aligned}
\]

Thus

\[
\|U_m-V^\pi\|_\infty
\le
\frac{\|U_m-TU_m\|_\infty}{1-\gamma^K}.
\]

Adding and subtracting \(U_m\) gives the displayed theorem.

The constant is worst-case sharp. In a one-state zero-reward self-loop, \(TU=\beta U\), \(V^\pi=0\). Take constants \(U_m=c\ge0\) and \(U_n=d\ge c\). Then

\[
\|U_n-V^\pi\|=d,
\quad
\|U_n-U_m\|=d-c,
\quad
\frac{\|U_m-TU_m\|}{1-\beta}=c,
\]

so equality holds.

The common recurrent map and initialization are not used in the residual decomposition. They are used only to interpret \(U_n,U_m\) as points on one recurrent path and to derive the path bound.

## 2.2 Recurrent path and contractive specialization

**Classification:** correct; the displayed sum of separate suprema is loose relative to the exact path supremum.

**Location:** `main.tex:292–326`; proof `main.tex:1758–1779`; PDF p. 5 and p. 23.

For each nonabsorbing state,

\[
|U_n(s)-U_m(s)|
\le
L_V\|z^{(n)}(s)-z^{(m)}(s)\|
\le
L_V\sum_{j=n}^{m-1}\|z^{(j+1)}(s)-z^{(j)}(s)\|.
\]

The exact supremum of this path sum is the strongest direct statement. Under a uniform contraction,

\[
\|z^{(j+1)}-z^{(j)}\|
\le L_z^j C_z,
\]

which yields

\[
L_V C_z\frac{L_z^n(1-L_z^{m-n})}{1-L_z}.
\]

Sending \(m\to\infty\) is valid because the recurrent iterates converge uniformly to \(U_*\) under the stated uniform conditions and

\[
\left|
\|U_m-TU_m\|-\|U_*-TU_*\|
\right|
\le(1+\gamma^K)\|U_m-U_*\|.
\]

The specialization can safely include \(L_z=0\); see Section 7.

## 2.3 Finite-depth residual certificate and countable-chain counterexample

**Classification:** correct as stated.

**Location:** `main.tex:348–406`; PDF pp. 6–7.

Setting the finite reference equal to the evaluated depth gives

\[
\|U_n-V^\pi\|_\infty
\le
\frac{\|U_n-\mathcal T_K^\pi U_n\|_\infty}{1-\gamma^K}.
\]

The bounded-function space is essential. On the deterministic chain
\(s_i\mapsto s_{i+1}\), with zero reward and
\(U(s_i)=\gamma^{-i}\),

\[
(\mathcal T_K^\pi U)(s_i)
=\gamma^K U(s_{i+K})
=\gamma^K\gamma^{-(i+K)}
=U(s_i),
\]

so the residual is zero, while \(V^\pi=0\) and
\(\sup_i|U(s_i)-V^\pi(s_i)|=\infty\). The manuscript’s requirement
\(U_n\in B(\mathcal C)\) excludes this example exactly. Determinism or pointwise computability alone does not.

## 2.4 One-step and K-step value-to-advantage bridge

**Classification:** correct; the uniform factor is worst-case sharp.

**Location:** `main.tex:410–435`, `main.tex:1579–1630`, proof `main.tex:1980–2001`; PDF pp. 7, 21, and 25.

With \(e=V-V^\pi\),

\[
\widehat Q_V(s,a)-Q^\pi(s,a)
=\gamma\mathbb E[e(S')\mid s,a].
\]

The centered baseline has the same \(\gamma\delta_V\) bound, so

\[
|\widehat A_V(s,a)-A^\pi(s,a)|
\le2\gamma\delta_V.
\]

The factor two is attainable when one action’s successor has error
\(+\delta_V\) and the current-policy baseline puts mass on a successor with error
\(-\delta_V\). For a \(K\)-step centered estimator, reward terms cancel and the corresponding constant is \(2\gamma^K\delta_V\).

For the candidate-policy *mean* error, the uniform factor can be sharpened using policy overlap; see Sections 3 and 5.

## 2.5 Infinite-horizon CPI with exact centering

**Classification:** correct but the policy-shift constant is loose.

**Location:** `main.tex:466–498`, proof `main.tex:2003–2052`; PDF pp. 7–8 and 25–26.

The exact centering identity is valid:

\[
\mathbb E_{a\sim\pi_\alpha}
[A^\pi-\widehat A]
=
\alpha
\mathbb E_{a\sim\pi_{\mathrm{cand}}}
[A^\pi-\widehat A].
\]

Therefore

\[
L_\pi(\pi_\alpha)
\ge
\widehat L_\pi(\pi_\alpha)
-rac{\alpha\varepsilon_{A,\mathrm{cand}}}{1-\gamma}.
\]

The current CPI shell is valid. It should be combined with the sharper exact-mixture occupancy constant from Section 1.3.

The one-step sufficient-improvement corollary and parameter-dependence corollary at `main.tex:514–558`, PDF p. 8, are algebraically correct and inherit the looseness of the CPI constant.

## 2.6 CPI with a centering defect

**Classification:** correct; pointwise uniform defects are stronger than necessary.

**Location:** `main.tex:1473–1533`; PDF p. 20.

Without exact centering,

\[
\mathbb E_{\pi_\alpha}[A^\pi-\widehat A]
=(1-\alpha)\mathbb E_\pi[A^\pi-\widehat A]
+
\alpha\mathbb E_{\pi_{\mathrm{cand}}}[A^\pi-\widehat A].
\]

Since \(\mathbb E_\pi A^\pi=0\), the stated penalty

\[
\frac{(1-\alpha)\varepsilon_{\mathrm{cent}}
+\alpha\varepsilon_{A,\mathrm{cand}}}{1-\gamma}
\]

is valid. Only the occupancy average of the signed combination is needed; the statewise suprema are transparent sufficient conditions.

## 2.7 Banach fixed-point and finite-unrolling proposition

**Classification:** correct but \(L_z>0\) is unnecessarily strict.

**Location:** Assumption at `main.tex:223–231`; Proposition at `main.tex:623–639`; proof `main.tex:1674–1693`; PDF pp. 4, 11, and 22.

The closed invariant set is complete, so Banach’s theorem applies. The a posteriori estimate

\[
\|z^{(n)}-z^*\|
\le
\sum_{k=n}^\infty \|z^{(k+1)}-z^{(k)}\|
\le
\frac{L_z^n}{1-L_z}\|z^{(1)}-z^{(0)}\|
\]

is correct. The proposition remains valid for \(L_z=0\) with the convention \(L_z^0=1\).

## 2.8 Direct persistent-latent certificate

**Classification:** correct under the declared fixed augmented MDP; assumptions are stronger than necessary because of the finite/countable restriction.

**Location:** `main.tex:675–759`; proof `main.tex:2054–2067`; PDF p. 12 and p. 26.

The state \(\bar s=(x,y,z,h)\) stores the pre-unroll carried latent; the policy uses \(F_n(x,y,z)\); a nonterminal successor carries that post-unroll latent. Both current and candidate policies use the same frozen \(F_n\), so they act in one MDP. The residual argument is then an ordinary \(\gamma^K\)-contraction proof on the augmented state space:

\[
\|\widetilde U_n-V^{\bar\pi}\|_\infty
\le
\frac{
\|\widetilde U_n-ar{\mathcal T}^{\bar\pi}_K\widetilde U_n\|_\infty
}{1-\gamma^K}.
\]

No latent fixed point, recurrent contraction, or slow drift is used. The value fixed point \(V^{\bar\pi}\) is still used. The paper is careful not to claim elimination of fixed points altogether.

Using different recurrent maps generally changes the transition kernel of the augmented MDP. Under the present assumptions, the shared-map requirement is necessary; see the counterexample in Section 5.6.

## 2.9 Slow-drift lemma and fixed-point comparison

**Classification:** correct; assumptions are stronger than necessary.

**Location:** `main.tex:769–848`; proof `main.tex:1695–1740`; PDF p. 13 and pp. 22–23.

The recursion

\[
e_{t+1}
\le
\kappa_n e_t+L_{z^*}\Delta y_{\max}
\]

is valid, and unrolling gives

\[
e_t
\le
\kappa_n^t e_0
+
L_{z^*}\Delta y_{\max}
\frac{1-\kappa_n^t}{1-\kappa_n}.
\]

The used post-unroll latent incurs one additional factor \(\kappa_n\), yielding the stated \(\mathcal C_{\mathrm{drift}}(n)\). The global fixed-point branch and uniform drift constants can be replaced by a finite-path reference sequence and local moduli; see Section 5.5.

## 2.10 Closure definitions

**Classification:** correct for finite/countable spaces, except for the absorber/path interaction in Section 1.1.

**Location:** `main.tex:890–933`; PDF p. 14.

The one-deviation set followed by the current-policy forward hull is exactly what is needed to evaluate current and candidate actions once and then continue under the current policy. The residual theorem alone does not need the candidate part of this closure; the advantage bridge does.

## 2.11 Finite-horizon residual theorem

**Classification:** correct; one boundary notation should be made uniform.

**Location:** `main.tex:990–1090`; PDF pp. 15–16.

Let
\(e_{h,m}=\|U_{h,m}-V_h^\pi\|_{\infty,h}\). Then

\[
e_{h,m}
\le
\epsilon_{h,m}
+
\gamma^{\ell_h}e_{h-\ell_h,m},
\qquad
\ell_h=\min\{K,h\}.
\]

Unrolling produces exactly the residuals at clocks
\(h,h-K,\ldots\) with weights \(1,\gamma^K,\ldots\). The final partial block terminates at \(e_{0,m}=0\). This handles:

- \(K>h\): one residual block, no bootstrap error;
- partial final blocks: the final error is multiplied by zero;
- \(h=0\): empty sum and zero error;
- \(\gamma=0\): only the first block can contribute.

The exact per-block sum is already preferable to the uniform maximum. The only notation repair is to define \(U_{0,q}\equiv b\) for every depth \(q\), not only \(U_{0,m}=b\) at `main.tex:1041`.

## 2.12 Finite-horizon CPI

**Classification:** correct; the range constant can be tightened.

**Location:** `main.tex:1102–1220`; PDF pp. 16–17.

The performance-difference identity and exact-mixture coupling are correct:

\[
\eta_H(\pi_\alpha)-\eta_H(\pi)
=
\alpha\sum_{t=0}^{H-1}\gamma^t
\mathbb E_{d_t^{\pi_\alpha}}[\delta_{H-t}],
\]

and

\[
\|d_t^{\pi_\alpha}-d_t^\pi\|_1
\le2[1-(1-\alpha)^t].
\]

The stated exact and quadratic forms follow. Since the two occupancy measures have equal total mass, the sharper signed-measure inequality uses the span of \(\delta_h\):

\[
\left|
\mathbb E_{d_t^{\pi_\alpha}}\delta_h
-
\mathbb E_{d_t^\pi}\delta_h
\right|
\le
\operatorname{span}(\delta_h)
[1-(1-\alpha)^t].
\]

Thus \(2\epsilon_{\mathrm{CPI},h}\) can be replaced by
\(\operatorname{span}(\delta_h)\), never larger and sometimes much smaller.

## 2.13 Deployment TV and KL results

**Classification:** correct but loose; either KL direction is valid.

**Location:** `main.tex:1222–1326`; PDF p. 18.

The proof based on
\(\operatorname{osc}_a Q^{\pi_\alpha}(s,a)\le\Delta_r/(1-\gamma)\)
and the performance-difference identity is valid. The reward *span*, rather than \(2R_{\max}\), is the right primitive; the manuscript already uses it first. The direct coupling improvement is given in Section 1.4.

Pinsker applies to either \(D_{\mathrm{KL}}(\widetilde\pi\|\pi_\alpha)\) or the reverse direction because total variation is symmetric. The support caveat is correct. The cap \(\min\{1,\sqrt{\kappa/2}\}\) should be explicit.

## 2.14 Projection lemmas and propositions

**Classification:** correct; the anchor restriction is stronger than necessary.

**Location:** interior lemma `main.tex:1658–1670`, PDF p. 22; saturated-annulus proposition `main.tex:1834–1888`, PDF p. 24; anchor proposition `main.tex:1890–1977`, PDF pp. 24–25.

- Interior projection: if \(z^*=\Pi_R(u)\) and \(\|z^*\|<R\), the radial branch cannot apply, so \(u=z^*\). Correct.
- Saturated annulus: the normalized-vector identity gives
  \[
  \|\Pi_R(u)-\Pi_R(v)\|
  \le (R/\rho_R)\|u-v\|,
  \]
  hence the product modulus. Correct. Projection alone is not claimed to imply contraction.
- Anchor residual: adding and subtracting \(B_{\mathrm{anc}}\) and applying Bellman contraction yields
  \[
  \varepsilon_{\mathrm{res}}^*
  \le
  \varepsilon_{\mathrm{anc}}
  +(1+\gamma^K)L_VD_{\mathrm{anc}}.
  \]
  Correct. The proof does not require the anchor to depend only on \(x\); any measurable state-dependent anchor in \(B_R\) works.

## 2.15 Absorbing boundary, shaping, and folded terminal accounting

**Classification:** mathematically consistent.

**Location:** setup `main.tex:165–177`; shaping convention `main.tex:941–975`; finite-horizon boundary `main.tex:978–1009`; implementation-facing description `main.tex:2086–2144`; PDF pp. 3, 15, and 26–28.

The formal absorber reward satisfies

\[
r_{\mathrm{abs}}=(1-\gamma)b,
\qquad
b=r_{\mathrm{abs}}+\gamma b.
\]

On a terminal transition, folding \(\gamma b\) into the final stored reward and then using zero terminal bootstrap accounts for the absorbing tail exactly once. Zero padding after termination adds no further reward. This is return-equivalent to the formal single absorber.

Whether a concrete codebase implements every branch exactly as written is:

> not verifiable from supplied evidence

---

# 3. Assumption-minimization table

| Result | Current assumption | Role in proof | Necessary or convenient | Valid weakening | Changed constant | Proof location |
|---|---|---|---|---|---|---|
| Finite-reference residual | Finite/countable \(\mathcal C\), bounded real functions, \(T_K:B(\mathcal C)\to B(\mathcal C)\) | Supplies a Banach space and \(\gamma^K\)-contraction | Finite/countable is convenient, not necessary | Any measurable invariant \(\mathcal C\) with \(B_b(\mathcal C)\); or weighted \(B_w\) with modulus \(\beta<1\) | \(1/(1-\gamma^K)\) on \(B_b\); \(1/(1-\beta)\) on \(B_w\) | `257–290`, `1745–1756`; PDF pp. 5, 23 |
| Bounded rewards, bounded \(V^\pi\), Bellman self-map | All are separately assumed | Ensures finite K-step rewards, self-map, fixed point | Partly redundant | Bounded rewards plus invariant Markov kernel imply \(T_K:B_b\to B_b\) and \(\|V^\pi\|_\infty\le R_{\max}/(1-\gamma)\) | none | `259–283`; PDF p. 5 |
| Bounded \(U_j\) for every \(j=n,\ldots,m\) | All intermediate depths bounded | Only endpoints enter residual decomposition; path term uses latent increments | Stronger than necessary | Require \(U_n,U_m\in B\); require finite path expression separately | none | `278–280`, `285–299`; PDF p. 5 |
| Same recurrent map and same initialization | Shared across all depths | Makes \(U_n,U_m\) one recurrent path | Necessary only for path interpretation | Residual decomposition holds for arbitrary \(U_n,U_m\); path theorem can allow nonstationary maps \(F_j\) | none for residual; local products for path | `270–278`, `292–299`; PDF p. 5 |
| Initialization ignores clock | \(z^{(0)}=z_{\mathrm{init}}(x,y)\) | Architecture restriction, not used by contraction proof | Convenient | Allow any measurable \(z^{(0)}(s)\), including \(h\) | none | `271–273`; PDF p. 5 |
| Full policy-pair advantage closure | Used by residual, advantage, CPI narrative | Ensures candidate one-step successors and subsequent \(\pi\) successors | Stronger than needed for pure residual | Residual: any \(\pi\)-invariant domain. Advantage: current reachable states plus one-step current/candidate successors and their \(\pi\)-hull. Deployment: separate hull under both deployed policies | none | `890–933`; PDF p. 14 |
| Common absorbing boundary | Imposed in infinite- and finite-horizon results | Makes terminal function difference zero | Convenient for infinite-horizon residual; necessary for zero terminal term in finite horizon | Infinite horizon: differing boundary is allowed if included in residual. Finite horizon: add \(\gamma^h\|U_0-b\|\) if boundaries differ | additional terminal mismatch if weakened | `361–363`, `1027–1046`; PDF pp. 6, 15 |
| Exact pointwise centering | \(E_\pi\widehat A=0\) at every current-reachable state | Removes the current-policy component exactly | Sufficient, not necessary | It suffices to control the signed occupancy average \(\Xi_\alpha\); state-dependent defects can be integrated against \(d_\pi\) | replaces pointwise sup by occupancy integral | `469–495`, `1473–1533`; PDF pp. 7, 20 |
| Uniform candidate bias | Supremum over states | Bounds surrogate estimation error | Sufficient, not necessary | Use \(|E_{d_\pi}b(s)|\), or \(E_{d_\pi}|b(s)|\); for value-derived advantages use TV overlap \(\tau(s)\) | can shrink by \(\tau(s)\) and occupancy weighting | `475–485`; PDF p. 7 |
| Exact pointwise mixture | \(\pi_\alpha=(1-\alpha)\pi+\alpha\pi_c\) | Gives exact linear advantage identity and exact-mixture coupling | Necessary for those exact formulas | Admit a deployed \(\widetilde\pi\) through an explicit TV/KL realization penalty | add deployment term | `468`, `748–755`, `1107–1111`; PDF pp. 7, 12, 16 |
| Same frozen recurrent map for persistent current/candidate | One \(F_n\) defines policy inputs and latent transition | Keeps both policies in one augmented MDP | Necessary under current regularity | Different maps require explicit reward/kernel mismatch assumptions; map norm alone is insufficient | simulation-lemma penalty if kernel mismatch is bounded | `688–695`; PDF p. 12 |
| Global contraction and global slow drift | Uniform \(L_z,L_{z^*},\Delta y_{\max}\) | Produces geometric fixed-point tracking | Convenient for optional comparison | Finite reference path \(\xi_t\), local moduli \(\kappa_t\), local defects \(d_t\) | products of local moduli | `769–823`; PDF p. 13 |
| \(L_z\in(0,1)\) | Strictly positive contraction modulus | Avoids \(0^0\) notation | Stronger than necessary | \(L_z\in[0,1)\), define \(L_z^0=1\), \(0^n=0\) for \(n\ge1\) | none | `223–231`, `623–639`; PDF pp. 4, 11 |
| Plan-independent projection anchor | \(z_{\mathrm{anc}}:\mathcal X\to B_R\) | Bounds \(U_*-B_{\mathrm{anc}}\) | Convenient | Any measurable \(z_{\mathrm{anc}}(s)\in B_R\) | none; potentially smaller \(D_{\mathrm{anc}}\) | `1890–1977`; PDF pp. 24–25 |
| `L^∞(ν)` domination route | Common \(\nu\) dominates transitions | Makes integration representative-independent | Incomplete as written | Prefer \(B_b(\mathcal C)\). If retaining `L^∞(ν)`, add \(\rho\ll\nu\), occupancy domination, kernel nonsingularity, and joint measurability | none | `935–938`; PDF pp. 14–15 |

---

# 4. Bound-tightening table

| Quantity | Current bound | Proposed bound | Relation | Equality / sharpness |
|---|---:|---:|---|---|
| Finite-reference value error | \(\|U_n-U_m\|+\|U_m-T_KU_m\|/(1-\gamma^K)\) | unchanged | Worst-case sharp | One-state zero-reward self-loop construction gives equality |
| Recurrent path | \(L_V\sum_j\sup_s\|\Delta z_j(s)\|\) | \(L_V\sup_s\sum_j\|\Delta z_j(s)\|\) | Proposed \(\le\) current | Equal when one state maximizes all increments; strict when maximizers differ |
| Weighted residual | not stated | \(\|U-V\|_w\le\|U-T_KU\|_w/(1-\beta)\), \(\beta=\gamma^K\lambda_K<1\) | Extends beyond bounded functions | Standard contraction residual constant; sharp for scalar contraction |
| One-step advantage, pointwise | \(2\gamma\delta_V\) | unchanged | Worst-case sharp | Opposite-sign successor errors attain factor two |
| Candidate-policy mean advantage error | \(2\gamma\delta_V\) via uniform error | \(2\gamma\tau\delta_V\), \(\tau=\sup_s\mathrm{TV}(\pi_c,\pi)\) | Proposed \(\le\) current | Sharp with two actions and TV distance \(\tau\) |
| Infinite-horizon exact-mixture occupancy | \(2\gamma\alpha/(1-\gamma)\) | \(2\gamma\alpha/(1-\gamma+\gamma\alpha)\) | Strictly smaller for \(\alpha,\gamma>0\) | Sharp under exact-mixture coupling |
| Infinite-horizon CPI penalty | \(2\epsilon\gamma\alpha^2/(1-\gamma)^2\) | \(2\epsilon\gamma\alpha^2/[(1-\gamma)(1-\gamma+\gamma\alpha)]\) | Proposed dominates | Two-state \(\delta=\pm\epsilon\) construction gives equality |
| CPI with advantage span | \(2\epsilon\)-based | \(\gamma\alpha^2\operatorname{span}(\delta)/[(1-\gamma)(1-\gamma+\gamma\alpha)]\) | Never larger because span \(\le2\epsilon\) | Equal when \(\delta\) attains \(\pm\epsilon\) |
| Centering/evaluation defect | Pointwise \([(1-\alpha)\epsilon_{cent}+\alpha\epsilon_{cand}]/(1-\gamma)\) | Signed occupancy term \(\Xi_\alpha/(1-\gamma)\), or its smallest established upper bound | Proposed can be much smaller | Pointwise result is a direct corollary |
| Finite-horizon CPI shift | \(2\alpha\sum_t\gamma^t\epsilon_h[1-(1-\alpha)^t]\) | \(\alpha\sum_t\gamma^t\operatorname{span}(\delta_h)[1-(1-\alpha)^t]\) | Proposed \(\le\) current | Equal when stage advantages attain symmetric extremes |
| Deployment, infinite horizon | \(\Delta_r\delta/(1-\gamma)^2\) | \(\Delta_r\delta/[(1-\gamma)(1-\gamma+\gamma\delta)]\) | Strictly smaller for \(\delta,\gamma>0\) | Absorbing high-reward mismatch construction gives equality |
| Deployment, finite horizon | \(\Delta_r\delta[G_H(\gamma)-H\gamma^H]/(1-\gamma)\) | \(\Delta_r[G_H(\gamma)-(1-\delta)G_H(\gamma(1-\delta))]\) | Proposed dominates | Same first-mismatch construction gives equality |
| KL deployment | substitute \(\sqrt{\kappa/2}\) | substitute \(\min\{1,\sqrt{\kappa/2}\}\) in sharper TV formula | Proposed never larger | Cap active for \(\kappa>2\) |
| Projection anchor | \((1+\gamma^K)L_V\sup\|z^*-z_{anc}(x)\|\) | same formula with state-dependent \(z_{anc}(s)\) | Same constant form, smaller feasible distance | No new assumption beyond measurability and boundedness |

---

# 5. Proposed stronger theorems

I recommend at most five additions. The first three are the highest-value revisions. The map-mismatch request is rejected under the current assumptions and replaced by a counterexample.

## 5.1 Measurable-space finite-reference theorem

**Status:** proved improvement; mathematically standard Bellman contraction, but essential for the motivating continuous latent state.

### Statement

Let \((\mathcal S,\Sigma_{\mathcal S})\) and
\((\mathcal A,\Sigma_{\mathcal A})\) be measurable spaces. Let
\(\mathcal C\in\Sigma_{\mathcal S}\) be a measurable set containing the relevant initial and one-deviation states. Let \(\pi\) be a stochastic kernel and suppose the policy-induced kernel satisfies

\[
P_\pi(\mathcal C\mid s)=1,
\qquad s\in\mathcal C.
\]

Assume the \(K\)-step expected reward

\[
r_K^\pi(s)
:=
\mathbb E_s^\pi\left[\sum_{i=0}^{K-1}\gamma^i r_i\right]
\]

is bounded and measurable on \(\mathcal C\). On
\(B_b(\mathcal C)\), define

\[
(\mathcal T_K^\pi V)(s)
=r_K^\pi(s)+\gamma^K(P_\pi^K V)(s).
\]

Then \(\mathcal T_K^\pi:B_b(\mathcal C)\to B_b(\mathcal C)\) is a
\(\gamma^K\)-contraction and has a unique fixed point \(V^\pi\). For any
\(U_n,U_m\in B_b(\mathcal C)\),

\[
\|U_n-V^\pi\|_\infty
\le
\|U_n-U_m\|_\infty
+
\frac{\|U_m-\mathcal T_K^\pi U_m\|_\infty}{1-\gamma^K}.
\]

### Proof

For bounded measurable \(V,W\), kernel integration preserves measurability and

\[
|P_\pi^K(V-W)(s)|
\le P_\pi^K|V-W|(s)
\le\|V-W\|_\infty.
\]

Therefore

\[
\|\mathcal T_K^\pi V-\mathcal T_K^\pi W\|_\infty
\le\gamma^K\|V-W\|_\infty.
\]

`B_b(C)` is complete, so Banach gives the fixed point. The residual and finite-reference inequalities follow exactly as in the current proof.

### Added assumptions

Only bounded measurability of \(r_K^\pi\), measurable kernels, and invariance of \(\mathcal C\). No common dominating measure is required.

For the advantage bridge, additionally require the reward and transition kernels to be jointly measurable in \((s,a)\), current and candidate policies to be stochastic kernels, and
\(P(\mathcal C\mid s,a)=1\) for current/candidate-policy almost every relevant action. For CPI, discounted occupancies are probability measures and all policy-shift arguments should use total variation.

### Positioning

Known theorem/core: standard measurable-space Bellman contraction. The paper’s contribution is the recurrent finite-reference specialization, not this extension. It should be formalized because it removes the artificial countability restriction from persistent \(z\).

## 5.2 Weighted-norm residual certificate and transversality alternative

**Status:** proved improvement; standard weighted-contraction theory.

### Statement

Let \(w:\mathcal C\to[1,\infty)\) be measurable and define

\[
B_w(\mathcal C)
=
\left\{f:\|f\|_w:=\sup_{s\in\mathcal C}rac{|f(s)|}{w(s)}<\infty\right\}.
\]

Assume \(r_K^\pi\in B_w(\mathcal C)\) and

\[
P_\pi^K w\le\lambda_K w,
\qquad
\beta:=\gamma^K\lambda_K<1.
\]

Then \(\mathcal T_K^\pi\) is a \(\beta\)-contraction on \(B_w\), has a unique fixed point \(V^\pi\in B_w\), and

\[
\boxed{
\|U_n-V^\pi\|_w
\le
\|U_n-U_m\|_w
+
\frac{\|U_m-\mathcal T_K^\pi U_m\|_w}{1-\beta}.
}
\]

### Proof

For \(f,g\in B_w\),

\[
\begin{aligned}
|P_\pi^K(f-g)(s)|
&\le
P_\pi^K|f-g|(s)\\
&\le
\|f-g\|_w P_\pi^K w(s)\\
&\le
\lambda_K\|f-g\|_w w(s).
\end{aligned}
\]

Thus the Bellman modulus is \(\beta\); Banach and the residual argument follow.

### Counterexample boundary

For the manuscript’s chain,
\(w(s_i)=\gamma^{-i}\) gives

\[
P_\pi^K w(s_i)=w(s_{i+K})=\gamma^{-K}w(s_i),
\]

so \(\lambda_K=\gamma^{-K}\) and \(\beta=1\). The weighted theorem correctly refuses to certify the zero-residual unbounded function.

### Transversality variant

Let \(d=U-\mathcal T_K^\pi U\). Iteration of
\(U-V^\pi=d+\gamma^K P_\pi^K(U-V^\pi)\) gives

\[
U-V^\pi
=
\sum_{j=0}^{N-1}\gamma^{jK}(P_\pi^K)^j d
+
\gamma^{NK}(P_\pi^K)^N(U-V^\pi).
\]

If the last term converges pointwise to zero and the residual series is absolutely finite, this identity gives a statewise certificate without a global sup norm. The chain counterexample fails the transversality condition because the tail remains \(U(s_i)\).

### Positioning

Weighted sup-norm contractions and residual bounds are established dynamic-programming results. This extension is useful but should not be presented as a new mathematical core.

## 5.3 Occupancy-aware exact-mixture CPI theorem

**Status:** proved improvement; synthesis of exact centering, signed occupancy error, exact-mixture coupling, and span control. The exact combined statement may be new in this application, but external novelty is not established.

### Statement

Let

\[
\pi_\alpha=(1-\alpha)\pi+\alpha\pi_c,
\qquad
\delta(s)=\mathbb E_{a\sim\pi_c}[A^\pi(s,a)].
\]

Define the signed evaluation defects

\[
c(s):=\mathbb E_{a\sim\pi}[\widehat A(s,a)],
\qquad
b(s):=\mathbb E_{a\sim\pi_c}
[\widehat A(s,a)-A^\pi(s,a)],
\]

and

\[
\Xi_\alpha
:=
\mathbb E_{s\sim d_\pi}
[(1-\alpha)c(s)+\alpha b(s)].
\]

Assume the displayed quantities are integrable. Then

\[
\boxed{
\eta(\pi_\alpha)
\ge
\widehat L_\pi(\pi_\alpha)
-
\frac{\Xi_\alpha}{1-\gamma}
-
\frac{\gamma\alpha^2\operatorname{span}(\delta)}
{(1-\gamma)(1-\gamma+\gamma\alpha)}.
}
\]

If only absolute upper bounds are available, replace \(\Xi_\alpha\) by any
\(B_\alpha\ge\Xi_\alpha\), for example

\[
B_\alpha
=(1-\alpha)\mathbb E_{d_\pi}|c(s)|
+
\alpha\mathbb E_{d_\pi}|b(s)|.
\]

Under exact centering and uniform candidate bias,

\[
\eta(\pi_\alpha)
\ge
\widehat L_\pi(\pi_\alpha)
-
\frac{\alpha\varepsilon_{A,c}}{1-\gamma}
-
\frac{2\varepsilon_{\mathrm{CPI}}\gamma\alpha^2}
{(1-\gamma)(1-\gamma+\gamma\alpha)}.
\]

### Proof

First, the surrogate relation is exact:

\[
\begin{aligned}
\widehat L_\pi(\pi_\alpha)-L_\pi(\pi_\alpha)
&=
\frac{1}{1-\gamma}
\mathbb E_{d_\pi,a\sim\pi_\alpha}
[\widehat A-A^\pi]\\
&=
\frac{\Xi_\alpha}{1-\gamma}.
\end{aligned}
\]

Second, couple \(\pi_\alpha\) and \(\pi\) by selecting the current-policy component with probability \(1-\alpha\) whenever the states agree. The state laws before decision \(t\) differ in total variation by at most
\(1-(1-\alpha)^t\). Thus

\[
\operatorname{TV}(d_{\pi_\alpha},d_\pi)
\le
(1-\gamma)\sum_{t\ge0}\gamma^t
[1-(1-\alpha)^t]
=
\frac{\gamma\alpha}{1-\gamma+\gamma\alpha}.
\]

The performance-difference identity gives

\[
\eta(\pi_\alpha)-L_\pi(\pi_\alpha)
=
\frac{\alpha}{1-\gamma}
\left(
\mathbb E_{d_{\pi_\alpha}}\delta
-
\mathbb E_{d_\pi}\delta
\right).
\]

For probability measures \(p,q\),

\[
|E_p f-E_q f|
\le\operatorname{span}(f)\operatorname{TV}(p,q).
\]

Substitution proves the theorem.

### Candidate-overlap corollary

If \(\widehat A=\widehat A_V\), set
\(e=V-V^\pi\) and
\(q_e(s,a)=\gamma E[e(S')\mid s,a]\). Then

\[
b(s)=E_{\pi_c}q_e-E_\pi q_e.
\]

Writing
\(\tau(s)=\operatorname{TV}(\pi_c(\cdot|s),\pi(\cdot|s))\),

\[
|b(s)|
\le
\operatorname{span}_a(q_e(s,a))\tau(s)
\le
2\gamma\delta_V\tau(s).
\]

Hence

\[
\varepsilon_{A,c}
\le2\gamma\delta_V\sup_s\tau(s),
\]

or, more sharply, use
\(2\gamma\delta_V E_{d_\pi}\tau(s)\) in the occupancy term.

### Equality and boundaries

The two-state construction in Section 1.3 attains the \(2\varepsilon_{\mathrm{CPI}}\) version exactly. The penalty is zero at \(\alpha=0\) or \(\gamma=0\). At \(\alpha=1\), it equals
\(2\varepsilon_{\mathrm{CPI}}\gamma/(1-\gamma)\), which is the correct worst-case contribution from all post-initial occupancies.

### Positioning

Occupancy-aware and span-based safe policy bounds are established in safe-policy-iteration work. The paper’s potentially distinctive element is the explicit composition with recurrent finite-reference residuals and exact centering. Claims should be framed as a synthesis unless a broader literature review establishes novelty.

## 5.4 Sharp deployment coupling and combined CPI/deployment theorem

**Status:** proved improvement.

### Statement

Let \(\pi_\alpha\) and \(\widetilde\pi\) act in the same fixed MDP, with rewards in
\([r_{\min},r_{\max}]\) and
\(\Delta_r=r_{\max}-r_{\min}\). If

\[
\sup_s\operatorname{TV}
(\widetilde\pi(\cdot|s),\pi_\alpha(\cdot|s))
\le\delta,
\]

then

\[
\boxed{
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
\le
\frac{\Delta_r\delta}
{(1-\gamma)(1-\gamma+\gamma\delta)}.
}
\]

For finite horizon \(H\),

\[
\boxed{
|\eta_H(\widetilde\pi)-\eta_H(\pi_\alpha)|
\le
\Delta_r
\left[
G_H(\gamma)-(1-\delta)G_H(\gamma(1-\delta))
\right].
}
\]

If either uniform KL direction is at most \(\kappa\), take

\[
\delta=\min\{1,\sqrt{\kappa/2}\}.
\]

Combining with Theorem 5.3 gives

\[
\begin{aligned}
\eta(\widetilde\pi)
\ge{}&
\widehat L_\pi(\pi_\alpha)
-
\frac{\Xi_\alpha}{1-\gamma}
-
\frac{\gamma\alpha^2\operatorname{span}(\delta_\pi)}
{(1-\gamma)(1-\gamma+\gamma\alpha)}\\
&-
\frac{\Delta_r\delta}
{(1-\gamma)(1-\gamma+\gamma\delta)}.
\end{aligned}
\]

Here \(\delta_\pi(s)=E_{\pi_c}A^\pi(s,a)\); the notation should distinguish it from the deployment TV radius.

### Proof

Maximally couple actions whenever the two states agree and use common transition/reward randomness after a matched action. The probability that rewards can differ at time \(t\) is at most
\(1-(1-\delta)^{t+1}\). Multiply by \(\Delta_r\gamma^t\) and sum. The closed forms follow from geometric series. The combined theorem follows from
\(\eta(\widetilde\pi)\ge\eta(\pi_\alpha)-D_{deploy}\).

### Positioning

This is a direct coupling/simulation-style bound. It is stronger and cleaner than the current theorem, but an external literature review is required before declaring the exact denominator novel.

## 5.5 Finite-path persistent-state comparison without a latent fixed point

**Status:** proved improvement; standard discrete Grönwall argument, relevant to the actual finite edit horizon.

### Statement

Consider a finite nonabsorbing path of maps \(F_t\) and actual carried latents

\[
z_{t+1}=F_t(z_t),
\qquad t=0,\ldots,T-1.
\]

Let \(\xi_0,\ldots,\xi_T\) be any reference latent path. Suppose local finite-path constants satisfy

\[
\|F_t(z)-F_t(\xi_t)\|
\le\kappa_t\|z-\xi_t\|
\]

for the relevant segment and define

\[
d_t:=\|F_t(\xi_t)-\xi_{t+1}\|.
\]

Then, with \(e_t=\|z_t-\xi_t\|\),

\[
e_{t+1}\le\kappa_t e_t+d_t
\]

and

\[
\boxed{
 e_t
\le
e_0\prod_{i=0}^{t-1}\kappa_i
+
\sum_{j=0}^{t-1}
 d_j\prod_{i=j+1}^{t-1}\kappa_i.
}
\]

If the value head at stage \(t\) is \(L_{V,t}\)-Lipschitz, then

\[
|V_\psi(z_t)-V_\psi(\xi_t)|
\le L_{V,t}e_t.
\]

For the corresponding evaluator functions \(U\) and \(U_\xi\), Bellman contraction gives

\[
\left|
\|U-T_KU\|_\infty
-
\|U_\xi-T_KU_\xi\|_\infty
\right|
\le
(1+\gamma^K)\|U-U_\xi\|_\infty.
\]

### Proof

The one-step inequality is the triangle inequality:

\[
\begin{aligned}
e_{t+1}
&=\|F_t(z_t)-\xi_{t+1}\|\\
&\le
\|F_t(z_t)-F_t(\xi_t)\|
+
\|F_t(\xi_t)-\xi_{t+1}\|\\
&\le\kappa_t e_t+d_t.
\end{aligned}
\]

Induction yields the product-sum expression. No fixed point, globally invariant contraction region, or differentiable plan embedding is required.

### Relation to the current slow-drift lemma

Take \(F_t=T_{x,y_t}^{\circ n}\),
\(\xi_t=z^*(x,y_t)\),
\(\kappa_t=L_z^n\), and
\(d_t\le L_{z^*}\Delta y_{\max}\). The current theorem is a uniform infinite-time corollary. The finite-path statement is stronger for a finite edit budget and local diagnostics.

### Positioning

The recursion is standard. Its value is conceptual: it supplies the fixed-point-free persistent comparison requested by the paper’s narrative.

## 5.6 Rejected stronger theorem: map distance alone cannot handle different recurrent maps

**Status:** rejected; counterexample.

Suppose the current policy uses recurrent map \(F\) and the candidate uses \(G\), with

\[
\sup_z\|F(z)-G(z)\|\le\varepsilon.
\]

No return penalty tending to zero with \(\varepsilon\) follows under the current assumptions. Let
\(F(z)=0\), \(G(z)=\varepsilon\), and let the policy head choose action \(a_0\) below threshold \(\varepsilon/2\) and \(a_1\) above it. The induced action distributions are disjoint although the map distance is \(\varepsilon\). Assign returns differing by order \(1/(1-\gamma)\).

There is a second obstruction: deterministic latent transitions
\(\delta_{F(z)}\) and \(\delta_{G(z)}\) have total-variation distance one whenever \(F(z)\ne G(z)\), no matter how small the Euclidean distance is.

A valid different-MDP result requires extra regularity stated directly at the kernel level. If two MDPs have reward-expectation gap at most \(\epsilon_r\) and transition-kernel TV gap at most \(\epsilon_P\), then for a fixed policy

\[
\|V_M^\pi-V_{\widetilde M}^\pi\|_\infty
\le
\frac{\epsilon_r}{1-\gamma}
+
\frac{\gamma\epsilon_P\Delta_r}{(1-\gamma)^2}.
\]

Connecting \(\|F-G\|\) to \(\epsilon_P\) would require stochastic smoothing or a Wasserstein/Lipschitz analysis. That is a research direction, not a theorem supported by the current assumptions.

---

# 6. Novelty and positioning assessment

## 6.1 Classification of the manuscript’s headline mathematical cores

| Manuscript result | Mathematical core | Assessment |
|---|---|---|
| Finite-reference-depth theorem | Contraction residual bound plus triangle inequality | Direct corollary; the paper explicitly disclaims novelty for the triangle inequality. The recurrent-depth interpretation is domain-specific. |
| Recurrent path bound | Lipschitz head plus telescoping latent path | Direct corollary; useful architecture-specific decomposition. |
| Contractive \(L_z^n\) specialization | Banach contraction and geometric series | Standard theorem specialized to the recurrent evaluator. |
| Finite-depth residual certificate | Standard fixed-point residual estimate | Known theorem; correctly scoped to a bounded Banach space. |
| Persistent augmented-state certificate | Markov state augmentation plus the same residual estimate | Domain-specific specialization/synthesis. |
| Finite-horizon residual recursion | Backward Bellman recursion with exact terminal boundary | Direct finite-horizon corollary; exact clock bookkeeping is useful but not a new contraction principle. |
| Centered CPI theorem | Standard CPI shell plus exact centering decomposition | Synthesis. The current occupancy constant is not tight. |
| Finite-horizon exact-mixture CPI | Performance-difference identity plus first-divergence coupling | Useful specialization; plausibly the strongest current theoretical component, but likely a direct consequence of standard tools. |
| Deployment theorem | Performance-difference/simulation-style perturbation | Standard type of result; current constant is loose. |
| Projection saturation result | Geometry of radial normalization plus pre-map Lipschitz bound | Straightforward but correct specialized proposition. |
| Projection anchor residual | Add/subtract anchor plus Bellman contraction | Direct corollary. |

## 6.2 Primary-source checks

The external primary-source audit supports the following positioning:

1. Weighted sup-norm Bellman contractions, multistep mappings, unique fixed points, and residual bounds of the form
   \(\|J_\mu-J\|\le\|T_\mu J-J\|/(1-\alpha)\)
   are established dynamic-programming results. A weighted extension would improve scope but is not a new core theorem.

2. Safe Policy Iteration already develops occupancy-aware policy differences and span-based performance bounds. The manuscript should cite and compare against the exact occupancy norm and span structure, not only the generic CPI shell.

3. The 2026 CRPI work in the supplied bibliography develops function-approximation-aware performance-difference lower bounds and per-step improvement guarantees under Bellman constraints. The present paper’s distinction is not “CPI with function approximation” in general. Its narrower distinction is the explicit finite recurrent-depth decomposition under fixed-snapshot sup-norm residual control.

4. TRM supplies the iterative tiny recurrent architecture, not a latent fixed-point design. The paper correctly treats contraction as optional.

## 6.3 Citation coverage gaps

The supplied bibliography includes Kakade–Langford, TRPO, Pirotta, Metelli et al., Eshwar et al., standard MDP references, and TRM/HRM work. It should add or explicitly discuss:

- weighted sup-norm contraction theory for dynamic programming;
- measurable-space Bellman contraction references if the `B_b` theorem is added;
- simulation/coupling perturbation results for policy or kernel mismatch;
- the exact relation between its occupancy bound and the span/occupancy formulations in safe-policy-iteration work.

## 6.4 Novelty conclusion

The present paper’s most defensible contribution is a **domain-specific synthesis**:

- finite recurrent depth \(n\) is separated from a finite reference depth \(m\);
- the reference error is certified by a Bellman residual;
- persistent latent state is made Markov by using \((x,y,z,h)\);
- exact centering and exact policy mixing connect evaluator error to one CPI step.

That synthesis is coherent. The mathematical primitives are mostly standard. As a theory-only ICLR submission, the paper needs at least one stronger integrated result rather than more corollaries. The best candidate is the occupancy-aware exact-mixture theorem with the sharp denominator, composed explicitly with finite-reference and deployment terms on a measurable augmented state space.

An exhaustive novelty determination would require a broader external literature review. The primary sources checked here are sufficient to reject claims that weighted residual theory, occupancy/span safe PI, or function-approximation CPI are new in isolation.

---

# 7. Exact manuscript edits

## 7.1 Repair the absorber domain and strengthen the path inequality

Replace the closure and path portion of Theorem 3.1 (`main.tex:261–299`) with:

```latex
Let
\[
\mathcal C:=\mathcal R_{\pi,\pi_{\mathrm{cand}}}^{\mathrm{adv}},
\qquad
\mathcal C^\circ:=\mathcal C\setminus\{s_{\mathrm{abs}}\}.
\]
By Definition~\ref{def:adv_closure}, $s_{\mathrm{abs}}\in\mathcal C$.
All value-function norms below are ordinary sup norms on $\mathcal C$;
all recurrent-latent suprema are taken on $\mathcal C^\circ$.
...
If the scalar head is $L_V$-Lipschitz in its latent argument uniformly
while $(x,y)$ is held fixed, then
\begin{align}
\|U_n-U_m\|_{\infty,\pi,\pi_{\mathrm{cand}}}^{\mathrm{adv}}
&\le
L_V\sup_{s\in\mathcal C^\circ}
\sum_{j=n}^{m-1}
\|z^{(j+1)}(s)-z^{(j)}(s)\|
\label{eq:finite_path_length_exact}\\
&\le
L_V\sum_{j=n}^{m-1}
\sup_{s\in\mathcal C^\circ}
\|z^{(j+1)}(s)-z^{(j)}(s)\|.
\label{eq:finite_path_length}
\end{align}
```

Use the same \(\mathcal C^\circ\) convention in every finite-horizon recurrent-path supremum.

## 7.2 Replace the general-kernel remark with a formal measurable-space theorem

Replace `main.tex:935–938` with:

```latex
\begin{theorem}[Measurable-space Bellman-domain extension]
\label{thm:measurable_extension}
Let $(\mathcal S,\Sigma_{\mathcal S})$ and
$(\mathcal A,\Sigma_{\mathcal A})$ be measurable spaces and let
$\mathcal C\in\Sigma_{\mathcal S}$ be measurable.  Let $\pi$ be a
stochastic kernel and suppose the induced kernel satisfies
$P_\pi(\mathcal C\mid s)=1$ for every $s\in\mathcal C$.
Assume the $K$-step expected reward
\[
r_K^\pi(s)
:=\mathbb E_s^\pi\!\left[\sum_{i=0}^{K-1}\gamma^i r_i\right]
\]
is bounded and measurable on $\mathcal C$.
On the Banach space $B_b(\mathcal C)$ of bounded measurable functions
with the ordinary sup norm, define
\[
(\mathcal T_K^\pi V)(s)
:=r_K^\pi(s)+\gamma^K(P_\pi^K V)(s).
\]
Then $\mathcal T_K^\pi$ is a $\gamma^K$-contraction, has a unique fixed
point $V^\pi\in B_b(\mathcal C)$, and for any
$U_n,U_m\in B_b(\mathcal C)$,
\[
\|U_n-V^\pi\|_\infty
\le
\|U_n-U_m\|_\infty
+
\frac{\|U_m-\mathcal T_K^\pi U_m\|_\infty}{1-\gamma^K}.
\]
The advantage and CPI extensions additionally require jointly measurable
reward/transition kernels, measurable current and candidate policy kernels,
and closure under current/candidate-policy-almost-every relevant action.
Discounted occupancies are probability measures and all policy-shift bounds
are stated in total variation.
\end{theorem}

\begin{remark}[Alternative $L^\infty(\nu)$ formulation]
If one instead works with equivalence classes in $L^\infty(\nu)$, one must
also require the initial and occupancy laws to be dominated by $\nu$ and the
relevant Markov kernels to be $\nu$-nonsingular, in addition to joint
measurability and action-almost-every closure conditions.
\end{remark}
```

## 7.3 Add the exact-mixture occupancy lemma

Insert before the current infinite-horizon CPI derivation:

```latex
\begin{lemma}[Exact-mixture occupancy coupling]
\label{lem:exact_mixture_occupancy}
Let $\pi_\alpha=(1-\alpha)\pi+\alpha\pi_{\mathrm{cand}}$ pointwise,
with $\alpha\in[0,1]$. Then
\[
\operatorname{TV}(d_{\pi_\alpha},d_\pi)
\le
\frac{\gamma\alpha}{1-\gamma+\gamma\alpha},
\qquad
\|d_{\pi_\alpha}-d_\pi\|_1
\le
\frac{2\gamma\alpha}{1-\gamma+\gamma\alpha}.
\]
\end{lemma}

\begin{proof}
Couple the two trajectories while their states agree. At each decision,
with probability $1-\alpha$ select the current-policy component of
$\pi_\alpha$ and use the same action and transition randomness. Hence the
state laws before decision $t$ differ in total variation by at most
$1-(1-\alpha)^t$. Therefore
\begin{align*}
\operatorname{TV}(d_{\pi_\alpha},d_\pi)
&\le
(1-\gamma)\sum_{t=0}^\infty
\gamma^t[1-(1-\alpha)^t]\\
&=
\frac{\gamma\alpha}{1-\gamma+\gamma\alpha}.
\end{align*}
\end{proof}
```

## 7.4 Replace Theorem 4.1 by the occupancy-aware sharp form

Replace `main.tex:466–498` with:

```latex
\begin{theorem}[Occupancy-aware CPI with centered evaluation error]
\label{thm:monotone_with_error}
Fix one discounted MDP with bounded rewards and let
$\pi_\alpha=(1-\alpha)\pi+\alpha\pi_{\mathrm{cand}}$ be the exact
pointwise mixture. Define
\[
\delta(s):=\mathbb E_{a\sim\pi_{\mathrm{cand}}(\cdot\mid s)}
[A^\pi(s,a)],
\qquad
\Delta_\delta:=\sup_s\delta(s)-\inf_s\delta(s),
\]
\[
c(s):=\mathbb E_{a\sim\pi(\cdot\mid s)}[\widehat A(s,a)],
\qquad
b(s):=\mathbb E_{a\sim\pi_{\mathrm{cand}}(\cdot\mid s)}
[\widehat A(s,a)-A^\pi(s,a)],
\]
and
\[
\Xi_\alpha
:=\mathbb E_{s\sim d_\pi}[(1-\alpha)c(s)+\alpha b(s)].
\]
Assume these quantities are finite. Then
\begin{equation}
\eta(\pi_\alpha)
\ge
\widehat L_\pi(\pi_\alpha)
-
\frac{\Xi_\alpha}{1-\gamma}
-
\frac{\gamma\alpha^2\Delta_\delta}
{(1-\gamma)(1-\gamma+\gamma\alpha)}.
\label{eq:main_theorem_occupancy}
\end{equation}
If $c(s)=0$ pointwise and
$|b(s)|\le\varepsilon_{A,\mathrm{cand}}$, then
\begin{equation}
\eta(\pi_\alpha)
\ge
\widehat L_\pi(\pi_\alpha)
-
\frac{\alpha\varepsilon_{A,\mathrm{cand}}}{1-\gamma}
-
\frac{2\varepsilon_{\mathrm{CPI}}\gamma\alpha^2}
{(1-\gamma)(1-\gamma+\gamma\alpha)}.
\label{eq:main_theorem}
\end{equation}
\end{theorem}
```

Proof text:

```latex
\begin{proof}
The surrogate difference is exact:
\[
\widehat L_\pi(\pi_\alpha)-L_\pi(\pi_\alpha)
=
\frac{\Xi_\alpha}{1-\gamma}.
\]
The performance-difference identity gives
\[
\eta(\pi_\alpha)-L_\pi(\pi_\alpha)
=
\frac{\alpha}{1-\gamma}
\left(
\mathbb E_{d_{\pi_\alpha}}\delta
-
\mathbb E_{d_\pi}\delta
\right).
\]
For probability measures $p,q$,
$|\mathbb E_p f-\mathbb E_q f|
\le\operatorname{span}(f)\operatorname{TV}(p,q)$.
Apply Lemma~\ref{lem:exact_mixture_occupancy}.  The uniform corollary uses
$\Delta_\delta\le2\varepsilon_{\mathrm{CPI}}$ and exact centering.
\end{proof}
```

Update every inherited infinite-horizon CPI formula, including
Eqs. corresponding to `main.tex:394`, `444`, `523`, `555`, `755`, `1493`, and `1826`.

## 7.5 Add policy-overlap control for candidate bias

Insert after Lemma 11.1 (`main.tex:1605–1613`):

```latex
\begin{corollary}[Candidate-policy bias with policy overlap]
\label{cor:candidate_overlap}
Let $\widehat A_V$ be the exactly centered one-step estimator and let
$\delta_V=\|V-V^\pi\|_\infty$.  Define
\[
\tau(s):=\operatorname{TV}
(\pi_{\mathrm{cand}}(\cdot\mid s),\pi(\cdot\mid s)),
\qquad
\tau:=\sup_s\tau(s).
\]
Then
\[
\left|
\mathbb E_{a\sim\pi_{\mathrm{cand}}}
[\widehat A_V(s,a)-A^\pi(s,a)]
\right|
\le2\gamma\delta_V\tau(s),
\]
and consequently
\[
\varepsilon_{A,\mathrm{cand}}
\le2\gamma\delta_V\tau.
\]
\end{corollary}

\begin{proof}
Let $e=V-V^\pi$ and
$q_e(s,a)=\gamma\mathbb E[e(S')\mid s,a]$.  Exact centering gives
\[
\mathbb E_{\pi_{\mathrm{cand}}}[\widehat A_V-A^\pi]
=
\mathbb E_{\pi_{\mathrm{cand}}}q_e-
\mathbb E_\pi q_e.
\]
Since $\operatorname{span}_a q_e(s,a)\le2\gamma\delta_V$, the
TV expectation inequality proves the claim.
\end{proof}
```

## 7.6 Tighten finite-horizon CPI by stagewise span

In Theorem 9.2, define

```latex
\Delta_h
:=
\sup_s\delta_h(s)-\inf_s\delta_h(s).
```

Replace the occupancy-shift term in Eq. (37) by

```latex
-\alpha\sum_{t=0}^{H-1}\gamma^t
\Delta_{H-t}[1-(1-\alpha)^t].
```

Retain the existing
\(-2\alpha\sum_t\gamma^t\epsilon_{\mathrm{CPI},H-t}[1-(1-\alpha)^t]\)
as a corollary using \(\Delta_h\le2\epsilon_{\mathrm{CPI},h}\).

For value-derived stage advantages, add:

```latex
\epsilon_{A,\mathrm{cand},h}
\le
2\gamma\tau_h E_{h-1},
\qquad
E_{h-1}:=\|U_{h-1}-V_{h-1}^\pi\|_{\infty,h-1},
```

with \(E_0=0\). Thus the stage-1 advantage error is exactly zero under the common terminal boundary.

## 7.7 Replace the deployment theorem by the sharp coupling form

Replace Eqs. corresponding to `main.tex:1247–1265` with:

```latex
\begin{align}
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
&\le
\frac{\Delta_r\delta}
{(1-\gamma)(1-\gamma+\gamma\delta)},
\label{eq:deployment_tv_bound}\\
|\eta_H(\widetilde\pi)-\eta_H(\pi_\alpha)|
&\le
\Delta_r\left[
G_H(\gamma)-(1-\delta)G_H(\gamma(1-\delta))
\right].
\label{eq:deployment_tv_finite_horizon}
\end{align}
```

Replace the proof by:

```latex
\begin{proof}
Maximally couple the two action kernels while the states agree and use the
same transition and reward randomness after a matched action.  The reward at
time $t$ can differ only if an action mismatch has occurred by decision $t$,
whose probability is at most $1-(1-\delta)^{t+1}$. Therefore
\[
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
\le
\Delta_r\sum_{t=0}^\infty
\gamma^t[1-(1-\delta)^{t+1}],
\]
which gives the infinite-horizon formula. Truncating the sum at $H-1$ gives
the finite-horizon formula.
\end{proof}
```

In the KL corollary, replace \(\delta\) by

```latex
\bar\delta_\kappa:=\min\left\{1,\sqrt{\kappa/2}\right\}.
```

Add the combined CPI/deployment lower bound immediately afterward.

## 7.8 Admit `L_z=0`

At `main.tex:223–231`, replace

```latex
$L_z\in(0,1)$
```

with

```latex
$L_z\in[0,1)$.  We use the convention $L_z^0=1$ for every
$L_z\in[0,1)$ and, when $L_z=0$, $L_z^n=0$ for every integer $n\ge1$.
```

No geometric denominator changes because \(1-L_z>0\). The claims at \(n=0\) remain as currently qualified.

## 7.9 Fix the finite-horizon boundary notation

At `main.tex:1041`, replace

```latex
where $U_{0,m}=b$.
```

with

```latex
where $U_{0,q}\equiv b$ for every finite depth $q\ge0$.
```

## 7.10 Generalize the projection anchor

In Proposition 12.2, replace

```latex
$z_{\mathrm{anc}}:\mathcal X\to B_R$ that depends only on $x$
```

with

```latex
a measurable state-dependent anchor
$z_{\mathrm{anc}}:\mathcal C^\circ\to B_R$.
```

Define

```latex
B_{\mathrm{anc}}(s)
:=V_\psi(z_{\mathrm{anc}}(s),x(s),y(s)),
```

and

```latex
D_{\mathrm{anc}}(R)
:=\sup_{s\in\mathcal C^\circ}
\|z^*(x(s),y(s))-z_{\mathrm{anc}}(s)\|_2.
```

The proof and constant are unchanged.

## 7.11 Add the different-map impossibility remark

Insert after `main.tex:694`:

```latex
\begin{remark}[Why the recurrent map is shared]
A small Euclidean discrepancy between two deterministic recurrent maps does
not imply a small policy or augmented-kernel discrepancy. For example,
$F(z)=0$ and $G(z)=\varepsilon$ can be separated by a threshold policy head,
producing disjoint action distributions for every $\varepsilon>0$. Moreover,
$\operatorname{TV}(\delta_{F(z)},\delta_{G(z)})=1$ whenever
$F(z)\ne G(z)$. Hence no return penalty that vanishes with
$\sup_z\|F(z)-G(z)\|$ follows without additional policy-head and transition
regularity. Different recurrent maps require a separate MDP-perturbation
theorem stated in terms of reward and kernel discrepancies.
\end{remark}
```

## 7.12 Make the source bundle self-contained

Include `figures/trm_to_mdp_bridge.tex` in the source artifact or inline its contents. Until then, exact recompilation remains:

> not verifiable from supplied evidence

---

# 8. Prioritized revision list

## Essential before submission

1. **Repair the absorber/path domain.** Define a nonabsorbing closure and use it in all latent suprema. This is the only direct formal ambiguity in a headline theorem.

2. **State the measurable-space `B_b` theorem.** The persistent augmented state contains a continuous latent. The current finite/countable scope is too narrow for the motivating architecture unless the reachable latent set is separately proved countable.

3. **Replace the infinite-horizon CPI constant with the exact-mixture denominator.** The finite-horizon section already contains the coupling idea. The sharper bound is proved, dominates the current one, has correct boundaries, and is sharp.

4. **Replace the deployment constant with the first-mismatch coupling bound and cap Pinsker.** This materially improves the deployment contribution and gives a clean combined CPI-plus-deployment theorem.

5. **Reframe novelty.** Present the work as a recurrent-evaluator/CPI synthesis. Do not position Bellman residual bounds, weighted contractions, occupancy-aware safe PI, or function-approximation CPI as new primitives.

6. **Include the missing figure source.** Exact source recompilation is otherwise not established.

## Strongly recommended theory strengthening

7. Add the occupancy-averaged centering master theorem. Keep pointwise centering and uniform candidate bias as readable corollaries.

8. Add the policy-overlap candidate-bias factor \(\tau(s)\). This connects the value error to the actual conservative step rather than a worst-case action pair.

9. Add the weighted-norm residual theorem and explicitly show why the countable-chain counterexample lands on the boundary \(\beta=1\).

10. Replace the global slow-drift comparison by, or precede it with, the finite-path local-modulus theorem. This is better aligned with a finite edit horizon and the claim that no latent fixed point is required by the primary analysis.

## Optional cleanup

11. Admit \(L_z=0\) with explicit power conventions.

12. Define \(U_{0,q}=b\) for every depth.

13. Generalize the projection anchor to a state-dependent measurable anchor.

14. Separate closure notation for residual, advantage, CPI, and deployment rather than reusing the largest policy-pair closure everywhere.

15. Add the exact path-supremum inequality before the sum of separate suprema.

---

# 9. ICLR verdict

## `borderline`

The paper is mathematically careful and I found no false central theorem. The finite-reference decomposition, finite-horizon terminal accounting, persistent-state Markovization, and exact-centering logic are correct. The authors also state limitations more honestly than is typical: the results are fixed-snapshot conditional statements, not training or learned-performance guarantees.

The theory-only contribution is presently below a clear acceptance bar for three reasons:

1. The main finite-reference result is a direct contraction-residual corollary plus a telescoping path inequality. Its novelty is primarily the recurrent-evaluator interpretation.
2. The formal finite/countable scope does not cleanly cover the continuous persistent latent state motivating the paper.
3. The two policy-shift results advertised as contributions use constants that can be materially and sharply improved by direct coupling.

The paper becomes materially stronger if it makes the measurable augmented-state theorem formal and replaces the current CPI/deployment shells with the sharp exact-mixture and first-mismatch bounds, ideally under the occupancy-averaged centering master theorem. Without those revisions, the work is coherent but too close to a domain-specific assembly of standard contraction and CPI tools for a theory-only ICLR submission.
