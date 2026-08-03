# Theory extension derivation

Status: derivation complete and numerically unit-tested. No claim below uses a
finite batch as evidence for a uniform assumption.

This report develops three conditional results against the paper's current
clock and absorbing-state convention:

1. a finite-horizon, finite-reference residual bound;
2. finite-horizon CPI with exact statewise centering and an exact mixture;
3. a deployment perturbation bound for replacing the exact mixture by another
   policy.

The results are mathematically safe to include under the assumptions stated
here. They do not by themselves establish that any historical checkpoint
satisfies those assumptions.

## 1. Common finite-horizon convention

Let the nonabsorbing state at clock value $h\in\{1,\ldots,H\}$ be either
$s=(x,y,h)$ or the clock-complete persistent state

\[
\bar s=(x,y,z,h).
\]

The clock records the number of decisions remaining before the current
action. A terminal transition, STOP, solution, or budget exhaustion enters one
shared absorbing atom $s_{\mathrm{abs}}$. Write

\[
b:=V^\pi(s_{\mathrm{abs}})=-C_{\max}.
\]

Under the paper's shaping convention, the absorbing self-loop reward is

\[
r_{\mathrm{abs}}=(\gamma-1)C_{\max}=(1-\gamma)b,
\]

so $b=r_{\mathrm{abs}}+\gamma b$. This identity matters near the horizon. A
backup truncated when the clock reaches zero is exactly equal to a fixed
$K$-step backup padded with absorbing self-loops, provided every evaluator
uses the exact common boundary $b$.

Throughout, $0\le\gamma<1$. The derivations below assume a finite or countable
clock-complete policy-pair closure. The current and candidate policies act in
one fixed MDP. In the persistent case, they must share the same frozen
recurrent transition map that
updates the carried latent. The closure contains the current-policy reachable
states, the one-deviation successors for every action supported by either
policy, and every recursive current-policy successor needed by each stage of a
multi-step backup. In particular, it is recursively forward invariant under
the stage kernels used below. Rewards and the displayed functions are bounded.
The common reward interval includes the absorbing self-loop reward
$r_{\mathrm{abs}}$. All suprema are over the relevant stage of this recursive
policy-pair closure.

Every evaluator at every recurrent depth and clock stage uses the same
absorbing assignment:

\[
U_{h,q}(s_{\mathrm{abs}})=b
\qquad
\text{for all }h\in\{0,\ldots,H\}\text{ and every depth }q.
\]

This is an assumption, not a consequence of boundedness. Without it, the
terminal continuation error need not vanish.

## 2. Finite-horizon $K$-step residual bound

### 2.1 Stage operators

Let $V_h^\pi$ be the true value with $h$ decisions remaining and set
$V_0^\pi=b$. For $1\le \ell\le h$, let

\[
\mathcal T_{h:\ell}^\pi W
\]

denote the $\pi$ backup for $\ell$ transitions starting at clock $h$, with $W$
used at clock $h-\ell$ and $W(s_{\mathrm{abs}})=b$. Thus

\[
V_h^\pi=\mathcal T_{h:\ell}^\pi V_{h-\ell}^\pi.
\]

For the nominal backup length $K\ge1$, define

\[
\ell_h:=\min\{K,h\}.
\]

The final block is truncated when $h<K$. Because the boundary is a fixed
point of the absorbing self-loop, this truncated operator gives the same value
as running the remaining $K-h$ absorbing self-loops.

Let $U_{h,m}$ be the evaluator at recurrent reference depth $m$, with
$U_{0,m}=b$ and $U_{h,m}(s_{\mathrm{abs}})=b$ for every stage. Define the
stage residual and value error

\[
\epsilon_{h,m}
:=
\left\|
U_{h,m}-\mathcal T_{h:\ell_h}^\pi U_{h-\ell_h,m}
\right\|_{\infty,h},
\qquad
e_{h,m}:=\|U_{h,m}-V_h^\pi\|_{\infty,h},
\]

and $e_{0,m}=0$.

### 2.2 Stagewise recursion

The stage operator changes only its terminal function when comparing
$U_{h-\ell_h,m}$ with $V_{h-\ell_h}^\pi$. Therefore

\[
\begin{aligned}
e_{h,m}
&\le
\epsilon_{h,m}
+
\left\|
\mathcal T_{h:\ell_h}^\pi U_{h-\ell_h,m}
-
\mathcal T_{h:\ell_h}^\pi V_{h-\ell_h}^\pi
\right\|_{\infty,h} \\
&\le
\epsilon_{h,m}+\gamma^{\ell_h}e_{h-\ell_h,m}.
\end{aligned}
\]

On trajectories that terminate before the end of the block, the terminal
function difference is zero because both functions equal (b). Bounding the
surviving paths by one gives the displayed coefficient. At $h\le K$, the
continuation term is exactly zero, not merely bounded by a geometric tail.

### 2.3 Exact unrolling and uniform specialization

Let

\[
J_h:=\left\lceil\frac{h}{K}\right\rceil,
\qquad J_0:=0.
\]

Repeated application of the recursion gives

\[
e_{h,m}
\le
\sum_{j=0}^{J_h-1}
\gamma^{jK}\epsilon_{h-jK,m}.
\tag{FH-residual}
\]

The last residual is evaluated at the positive clock
$h-(J_h-1)K\in\{1,\ldots,K\}$. The final partial block does not change the
weight on that residual. It only multiplies $e_{0,m}=0$.

If

\[
\epsilon_m:=\max_{1\le q\le h}\epsilon_{q,m},
\]

then

\[
e_{h,m}
\le
\frac{1-\gamma^{KJ_h}}{1-\gamma^K}\epsilon_m.
\tag{FH-uniform}
\]

This is the intended finite-horizon improvement over
$\epsilon_m/(1-\gamma^K)$. It approaches the infinite-horizon constant as
$h$ grows, but is exactly one when $1\le h\le K$.

### 2.4 Finite-reference depth

Fix one frozen recurrent map, one common initialization, one latent norm, and
one scalar head for every evaluator depth. More precisely, for each
nonabsorbing $s\in\mathcal R_h$, let

\[
z_h^{(0)}(s)=z_{\mathrm{init}}(s),
\qquad
z_h^{(q+1)}(s)=F(z_h^{(q)}(s),s),
\qquad
U_{h,q}(s)=V_\psi(z_h^{(q)}(s),x).
\]

The map $F$, initialization $z_{\mathrm{init}}$, latent norm, and head
$V_\psi$ are the same for every depth $q$. Only the number of applications of
$F$ changes. Together with the common boundary assignment above, this is the
evaluator construction assumed by the finite-reference and recurrent-path
bounds.

For evaluator depths $0\le n<m$, define

\[
D_{h;n,m}:=\|U_{h,n}-U_{h,m}\|_{\infty,h}.
\]

Adding and subtracting $U_{h,m}$, then applying `FH-residual`, gives

\[
\boxed{
\|U_{h,n}-V_h^\pi\|_{\infty,h}
\le
D_{h;n,m}
+
\sum_{j=0}^{J_h-1}\gamma^{jK}\epsilon_{h-jK,m}.
}
\tag{FH-finite-reference}
\]

The uniform form is

\[
\boxed{
\|U_{h,n}-V_h^\pi\|_{\infty,h}
\le
D_{h;n,m}
+
\frac{1-\gamma^{KJ_h}}{1-\gamma^K}\epsilon_m.
}
\]

If the scalar head is uniformly $L_V$-Lipschitz, the same finite recurrent
path argument as in the current paper gives

\[
D_{h;n,m}
\le
L_V\sum_{q=n}^{m-1}
\sup_{s\in\mathcal R_h}
\|z_h^{(q+1)}(s)-z_h^{(q)}(s)\|.
\]

No recurrent fixed point or recurrent contraction is needed.

### 2.5 Boundary audit

The formula survives the required edge cases:

| Case | Result |
| --- | --- |
| $h=0$ or absorbing start | $J_0=0$, the sum is empty, and the error is zero because the boundary is exact. |
| $1\le h\le K$ | $J_h=1$, so the residual multiplier is exactly one. |
| $K=1$ | The multiplier is $(1-\gamma^h)/(1-\gamma)$. |
| $\gamma=0$ | Every positive-horizon multiplier is one. |
| $h=qK$ | There are exactly $q$ full blocks and weights $1,\gamma^K,\ldots,\gamma^{(q-1)K}$. |
| $h=qK+r,\ 1\le r<K$ | There are $q+1$ residuals. The last is at clock $r$ with weight $\gamma^{qK}$. |
| $n=0$, $m=n+1$ | The finite-reference triangle and path bounds are unchanged. |

### 2.6 Inclusion decision

Safe to include. The theorem should be stated for the complete stage family and
the exact common absorbing boundary. A claim based only on a residual measured
at one clock value is not enough. A uniform empirical claim requires all stage
residuals on the complete closure, not a retained batch.

## 3. Finite-horizon CPI

### 3.1 Time-indexed setup

Start at clock $H$. Let $d_t^\pi$ be the probability law after $t$
transitions, before decision (t), including any mass already at the absorbing
atom. At that atom, define every advantage below to be zero. Let

\[
\pi_{\alpha,h}=(1-\alpha)\pi_h+\alpha\pi_{\mathrm{cand},h},
\qquad \alpha\in[0,1],
\]

be the exact pointwise probability-space mixture at every clock value. The two
policies must operate in the same fixed MDP. The recursive closure must contain
the complete time-indexed support of both $d_t^\pi$ and
$d_t^{\pi_\alpha}$ for every $t\in\{0,\ldots,H\}$.

Define the current-policy stage advantage and candidate advantage

\[
A_h^\pi(s,a)=Q_h^\pi(s,a)-V_h^\pi(s),
\qquad
\delta_h(s)=
\mathbb E_{a\sim\pi_{\mathrm{cand},h}(\cdot\mid s)}
[A_h^\pi(s,a)],
\]

with

\[
\epsilon_{\mathrm{CPI},h}:=\sup_s|\delta_h(s)|.
\]

The finite-horizon performance-difference identity is

\[
\eta_H(\pi_\alpha)-\eta_H(\pi)
=
\alpha\sum_{t=0}^{H-1}\gamma^t
\mathbb E_{s\sim d_t^{\pi_\alpha}}
[\delta_{H-t}(s)].
\tag{FH-PDL}
\]

It follows by telescoping the time-indexed Bellman equations. The terminal
term cancels because both policies use the same boundary (b).

Define the true finite-horizon surrogate

\[
L_{H,\pi}(\pi_\alpha)
:=
\eta_H(\pi)
+
\alpha\sum_{t=0}^{H-1}\gamma^t
\mathbb E_{s\sim d_t^\pi}[\delta_{H-t}(s)].
\]

### 3.2 Time-indexed occupancy shift

While two coupled trajectories occupy the same state, couple the exact mixture
to the current policy by selecting the current-policy component with
probability $1-\alpha$. Conditional on selecting that component, use the same
action and transition randomness. The probability that the trajectories have
diverged before time $t$ is at most $1-(1-\alpha)^t$. Hence

\[
\|d_t^{\pi_\alpha}-d_t^\pi\|_1
\le
2[1-(1-\alpha)^t]
\le 2\alpha t.
\tag{FH-occupancy}
\]

Combining `FH-PDL` and `FH-occupancy` gives the stage-specific bound

\[
\boxed{
\eta_H(\pi_\alpha)
\ge
L_{H,\pi}(\pi_\alpha)
-
2\alpha
\sum_{t=0}^{H-1}
\gamma^t\epsilon_{\mathrm{CPI},H-t}
[1-(1-\alpha)^t].
}
\tag{FH-CPI-exact-coupling}
\]

The label "exact-coupling" refers to retaining the nonlinear coupling
constant. It does not claim that the worst-case inequality is attained.

The simpler quadratic relaxation is

\[
\boxed{
\eta_H(\pi_\alpha)
\ge
L_{H,\pi}(\pi_\alpha)
-
2\alpha^2
\sum_{t=0}^{H-1}
t\gamma^t\epsilon_{\mathrm{CPI},H-t}.
}
\tag{FH-CPI-quadratic}
\]

### 3.3 Exact centering and estimated advantage

Let $\widehat A_h$ satisfy exact statewise centering

\[
\mathbb E_{a\sim\pi_h(\cdot\mid s)}[\widehat A_h(s,a)]=0
\quad\text{for every }(h,s),
\]

and define the stagewise candidate bias

\[
\epsilon_{A,\mathrm{cand},h}
:=
\sup_s
\left|
\mathbb E_{a\sim\pi_{\mathrm{cand},h}(\cdot\mid s)}
[\widehat A_h(s,a)-A_h^\pi(s,a)]
\right|.
\]

Define

\[
\widehat L_{H,\pi}(\pi_\alpha)
:=
\eta_H(\pi)
+
\sum_{t=0}^{H-1}\gamma^t
\mathbb E_{s\sim d_t^\pi,
a\sim\pi_{\alpha,H-t}(\cdot\mid s)}
[\widehat A_{H-t}(s,a)].
\]

Exact centering removes the current-policy component pointwise, giving

\[
L_{H,\pi}(\pi_\alpha)
\ge
\widehat L_{H,\pi}(\pi_\alpha)
-
\alpha\sum_{t=0}^{H-1}
\gamma^t\epsilon_{A,\mathrm{cand},H-t}.
\]

Therefore

\[
\boxed{
\begin{aligned}
\eta_H(\pi_\alpha)
\ge{}&
\widehat L_{H,\pi}(\pi_\alpha)
-
\alpha\sum_{t=0}^{H-1}
\gamma^t\epsilon_{A,\mathrm{cand},H-t} \\
&-
2\alpha\sum_{t=0}^{H-1}
\gamma^t\epsilon_{\mathrm{CPI},H-t}
[1-(1-\alpha)^t].
\end{aligned}
}
\tag{FH-CPI-centered}
\]

The quadratic version replaces the last line by

\[
-2\alpha^2\sum_{t=0}^{H-1}
t\gamma^t\epsilon_{\mathrm{CPI},H-t}.
\]

### 3.4 Uniform constants

Let

\[
G_H(q):=\sum_{t=0}^{H-1}q^t=\frac{1-q^H}{1-q},
\]

and

\[
S_H(\gamma):=\sum_{t=0}^{H-1}t\gamma^t
=
\frac{\gamma-H\gamma^H+(H-1)\gamma^{H+1}}
{(1-\gamma)^2}.
\]

For uniform stage bounds

\[
\epsilon_{A,\mathrm{cand},h}\le\epsilon_{A,\mathrm{cand}},
\qquad
\epsilon_{\mathrm{CPI},h}\le\epsilon_{\mathrm{CPI}},
\]

`FH-CPI-centered` becomes

\[
\boxed{
\begin{aligned}
\eta_H(\pi_\alpha)
\ge{}&
\widehat L_{H,\pi}(\pi_\alpha)
-\alpha\epsilon_{A,\mathrm{cand}}G_H(\gamma)\\
&-2\alpha\epsilon_{\mathrm{CPI}}
\left[G_H(\gamma)-G_H(\gamma(1-\alpha))\right].
\end{aligned}
}
\tag{FH-CPI-uniform}
\]

A simpler bound is

\[
\boxed{
\eta_H(\pi_\alpha)
\ge
\widehat L_{H,\pi}(\pi_\alpha)
-\alpha\epsilon_{A,\mathrm{cand}}G_H(\gamma)
-2\alpha^2\epsilon_{\mathrm{CPI}}S_H(\gamma).
}
\tag{FH-CPI-uniform-quadratic}
\]

As $H\to\infty$, the nonlinear distribution penalty approaches

\[
\frac{2\gamma\alpha^2\epsilon_{\mathrm{CPI}}}
{(1-\gamma)(1-\gamma+\gamma\alpha)},
\]

which is no larger than the paper's standard

\[
\frac{2\gamma\alpha^2\epsilon_{\mathrm{CPI}}}{(1-\gamma)^2}.
\]

The quadratic finite-horizon constant approaches the standard constant
exactly because $S_H(\gamma)\to\gamma/(1-\gamma)^2$.

### 3.5 Boundary audit

* $H=0$: all sums are empty and policies have identical performance.
* $H=1$: the occupancy-shift penalty is zero. Both policies are evaluated
  on the same initial distribution, so the surrogate has no state-distribution
  error.
* $\gamma=0$: only the initial decision contributes. The occupancy-shift
  penalty is zero.
* $\alpha=0$: the policy is unchanged and both penalties vanish.
* $\alpha=1$: the coupling penalty is
  $2\sum_{t=1}^{H-1}\gamma^t\epsilon_{\mathrm{CPI},H-t}$, which is finite.
* Absorption before (H): absorbed mass contributes zero advantage, so the
  proof and constants remain valid.

### 3.6 Inclusion decision

Safe to include as a finite-horizon specialization. It is still a CPI shell,
not a training-convergence theorem. It requires exact pointwise mixture
deployment, exact centering at every clock-complete state, and one shared MDP.
In a persistent model, changing the recurrent transition map between policies
invalidates the argument.

## 4. Deployment perturbation bound

### 4.1 Infinite discounted horizon

Let

\[
\pi_\alpha=(1-\alpha)\pi+\alpha\pi_{\mathrm{cand}}
\]

be the exact mixture and let $\widetilde\pi$ be the deployed policy. Both
must be policies in the same fixed MDP. Let $\mathcal D$ be either the full
state space or a closure containing the initial-law support that is recursively
forward invariant under both $\pi_\alpha$ and $\widetilde\pi$. For every
$s\in\mathcal D$, define the union of deployed and exact-mixture supports

\[
\mathcal A_{\mathcal D}(s)
:=
\operatorname{supp}\pi_\alpha(\cdot\mid s)
\cup
\operatorname{supp}\widetilde\pi(\cdot\mid s),
\]

and require $\mathcal D$ to contain the one-step successors of every action in
$\mathcal A_{\mathcal D}(s)$, including successors and later states reachable
only through deployed-policy support. Assume the uniform statewise bound on
this complete domain:

\[
\sup_{s\in\mathcal D}
\operatorname{TV}
(\widetilde\pi(\cdot\mid s),\pi_\alpha(\cdot\mid s))
\le\delta.
\tag{uniform-TV}
\]

Suppose every reward on transitions from this union of action supports,
including the absorbing self-loop reward, lies in a common interval
$[r_{\min},r_{\max}]$ and write

\[
\Delta_r:=r_{\max}-r_{\min}.
\]

For the exact-mixture action value,

\[
\operatorname{osc}_{a\in\mathcal A_{\mathcal D}(s)}
Q^{\pi_\alpha}(s,a)
\le\frac{\Delta_r}{1-\gamma}.
\]

The total-variation expectation inequality gives

\[
\left|
\mathbb E_{a\sim\widetilde\pi}A^{\pi_\alpha}(s,a)
\right|
=
\left|
\mathbb E_{a\sim\widetilde\pi}Q^{\pi_\alpha}(s,a)
-
\mathbb E_{a\sim\pi_\alpha}Q^{\pi_\alpha}(s,a)
\right|
\le
\delta\frac{\Delta_r}{1-\gamma}.
\]

Applying the performance-difference identity yields

\[
\boxed{
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
\le
\frac{\Delta_r\,\delta}{(1-\gamma)^2}.
}
\tag{deployment-TV}
\]

Under the paper's assumption $|r|\le R_{\max}$, use
$\Delta_r\le2R_{\max}$:

\[
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
\le
\frac{2R_{\max}\delta}{(1-\gamma)^2}.
\]

This bound includes the immediate-reward effect. There is no extra leading
factor of γ.

### 4.2 Finite-horizon sharpening

For the finite-horizon version, use stage-indexed domains $\mathcal D_h$ with
the same recursive invariance under both policies and the same union-of-support
successor requirement. With $h$ decisions remaining and a fixed common
terminal boundary,

\[
\operatorname{osc}_a Q_h^{\pi_\alpha}(s,a)
\le
\Delta_r G_h(\gamma).
\]

Therefore

\[
\boxed{
|\eta_H(\widetilde\pi)-\eta_H(\pi_\alpha)|
\le
\Delta_r\delta
\sum_{t=0}^{H-1}\gamma^tG_{H-t}(\gamma)
=
\frac{\Delta_r\delta}{1-\gamma}
\left[G_H(\gamma)-H\gamma^H\right].
}
\tag{deployment-TV-FH}
\]

The terminal boundary cancels between policies. At $H=1$, the constant is
$\Delta_r\delta$. At $H=0$, it is zero. As $H\to\infty$, it approaches
`deployment-TV`.

### 4.3 Uniform KL corollary

If either one fixed KL direction satisfies a uniform bound, for example

\[
\sup_{s\in\mathcal D}
D_{\mathrm{KL}}
(\widetilde\pi(\cdot\mid s)\|\pi_\alpha(\cdot\mid s))
\le\kappa,
\]

then Pinsker's inequality gives

\[
\delta\le\sqrt{\kappa/2}.
\]

Hence

\[
\boxed{
|\eta(\widetilde\pi)-\eta(\pi_\alpha)|
\le
\frac{\Delta_r}{(1-\gamma)^2}\sqrt{\frac{\kappa}{2}}.
}
\tag{deployment-KL}
\]

The reverse KL direction also implies the same Pinsker conversion when that
reverse KL is the quantity bounded uniformly. The direction must be stated.
Finite KL also carries its usual support requirement.

If the chosen KL direction is infinite because the deployed policy assigns
positive mass outside the exact mixture's support, Pinsker remains formally
true but supplies only an infinite, uninformative upper bound. The finite-KL
corollary is then inapplicable. The TV theorem can still be used when a uniform
TV bound is available.

### 4.4 Combination with CPI

Any valid lower bound $B_{\mathrm{CPI}}$ on the exact mixture can be lifted
to the deployed policy as

\[
\boxed{
\eta(\widetilde\pi)
\ge
B_{\mathrm{CPI}}
-
\frac{\Delta_r\delta}{(1-\gamma)^2}.
}
\]

For example, $B_{\mathrm{CPI}}$ may be the current infinite-horizon centered
CPI bound or `FH-CPI-centered` with the finite-horizon deployment constant
substituted.

### 4.5 Scope restriction for persistent latents

The deployment result compares action kernels in one fixed MDP. It applies to
a distilled policy head evaluated on the same clock-complete augmented state
when the frozen recurrent map and latent-carry transition remain unchanged. It
does not cover interpolation or distillation that changes the recurrent map,
because that changes the augmented transition kernel. Such a case needs an
additional model-mismatch bound.

### 4.6 Uniform assumptions versus retained diagnostics

The theorem assumptions are uniform. None of the following is sufficient on
its own:

* replay-batch mean KL;
* replay-batch maximum KL;
* a finite held-out maximum TV;
* agreement on sampled actions;
* a local finite-difference proxy.

Those quantities may be reported only as finite-batch diagnostics. They do not
instantiate `uniform-TV` or `deployment-KL`. If the historical action kernels,
states, or checkpoints are absent, the deployment discrepancy is exactly:

> not verifiable from supplied evidence

### 4.7 Inclusion decision

Safe to include as a conditional theorem and directly relevant to the paper's
exact-mixture versus deployed-policy gap. Do not state that the historical
deployment is covered unless a genuine uniform TV or KL bound is available and
the recurrent transition map is shared.

## 5. Deterministic numerical unit test

Script:

`experiments/finite_horizon_theory_checks.py`

Command:

```text
python3 experiments/finite_horizon_theory_checks.py \
  --seed 20260803 --random-cases 200
```

The script uses only the Python standard library. It constructs random finite
MDPs with a nonzero shared absorbing boundary and directly solves every
quantity. It directly checks the finite-horizon performance-difference
identity, the nonlinear uniform $G_H$ closed form and its dominance relations,
every time-indexed occupancy inequality, and every statewise centering
identity. It also includes a positive-horizon initial law concentrated on the
absorbing atom and deterministic policies with TV distance one, disjoint
supports, and infinite KL.

Reproducibility hashes:

```text
dbb19311ccca6c18e3d2ab3dfa61c9bc2740f6ebc019c8ff3ff0a1f392f9eb15  experiments/finite_horizon_theory_checks.py
2bcd3fadd5ad7094b397e492b711d524f65c52d7fe6efea6062922e105a0d8e6  official stdout JSON
d2d4b47d08cde84536053fb06aa3c4180a2ea239dd7daa60deb3248f1d0d2da4  stress stdout JSON
```

Result:

```json
{
  "boundary_coverage": [
    "H=0",
    "H=1",
    "K=1",
    "K=H",
    "K>H",
    "gamma=0",
    "alpha=0",
    "alpha=1",
    "n=0",
    "m=n+1",
    "absorbing initial state",
    "shared nonzero absorbing boundary",
    "TV delta=1",
    "incompatible policy supports",
    "infinite KL with Pinsker finite-bound marked inapplicable"
  ],
  "checks": {
    "finite_horizon_cpi_checks": 5535,
    "finite_horizon_deployment_checks": 205,
    "incompatible_support_checks": 7,
    "infinite_horizon_deployment_checks": 410,
    "positive_horizon_absorbing_initial_checks": 11,
    "residual_reference_checks": 20500,
    "zero_horizon_and_absorbing_checks": 18
  },
  "finite_horizon_case_count": 205,
  "finite_horizon_cpi_check_breakdown": {
    "centering_assertions": 2460,
    "closed_form_assertions": 820,
    "cpi_bound_assertions": 1230,
    "occupancy_assertions": 820,
    "performance_difference_assertions": 205
  },
  "incompatible_support_case": {
    "forward_kl": "infinity",
    "pinsker_finite_bound_applicable": false,
    "reverse_kl": "infinity",
    "tv_delta": 1.0
  },
  "maximum_centering_defect": 1.8735013540549517e-16,
  "maximum_occupancy_bound_violation": 0.0,
  "maximum_performance_difference_error": 1.1102230246251565e-16,
  "maximum_residual_uniform_bound_ratio": 1.0000000000000002,
  "minimum_numerical_slack": -4.440892098500626e-16,
  "positive_horizon_absorbing_initial_law": {
    "horizon": 4,
    "maximum_law_error": 0.0
  },
  "random_cases": 200,
  "seed": 20260803,
  "status": "PASS",
  "total_checks": 26686
}
```

The negative minimum slack is floating-point roundoff and is below the test
tolerance. The test covers $H=0$, $H=1$, $K=1$, $K=H$, $K>H$,
$\gamma=0$, $\alpha=0$, $\alpha=1$, $n=0$, $m=n+1$, an absorbing
initial law at positive horizon, the nonzero shared absorbing boundary,
TV distance one, disjoint policy supports, and an infinite-KL case for which
the finite Pinsker corollary is correctly marked inapplicable.

An independent stress rerun used seed 9,173,551 and 2,000 random cases. It
passed 261,814 checks. Its minimum numerical slack was
$-8.882\times10^{-16}$, its maximum centering defect was
$2.220\times10^{-16}$, its maximum performance-difference identity error was
$3.331\times10^{-16}$, and its maximum occupancy-bound violation was zero.

Random finite-MDP checks are not a proof. They are regression tests for signs,
constants, indexing, terminal handling, and boundary normalization. The proofs
above are the basis for inclusion.

## 6. Final inclusion assessment

| Result | Mathematical status | Paper recommendation |
| --- | --- | --- |
| Finite-horizon residual plus finite reference | Derived, boundary-audited, 20,500 numerical checks | Include. It directly matches the finite edit budget and strengthens the primary theorem without adding a fixed-point assumption. |
| Finite-horizon CPI | Derived from time-indexed occupancies, 5,535 explicitly counted checks | Safe for an appendix or compact corollary. Present it as a standard finite-horizon CPI specialization, not the main novelty. |
| TV/KL deployment perturbation | Derived with reward-range constants, 622 checks including TV=1 and infinite KL | Include. It addresses the exact-mixture deployment gap. Keep the uniform assumption visibly separate from finite-batch diagnostics. |
