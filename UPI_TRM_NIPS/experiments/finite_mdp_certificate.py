#!/usr/bin/env python3
"""
Finite-MDP certificate diagnostic for the UPI-TRM theory.

This script stays deliberately small and exact:

- finite discounted MDP with |S|=64 by default and |A|=4,
- exact dynamic programming for V^pi, Q^pi, A^pi, and eta(pi),
- exact K-step Bellman backups,
- exact contraction-style evaluator U_n with known truncation term,
- exact CPI surrogate and exact mixed-policy performance,
- reproducible PDF/PNG figures written via local gnuplot.

The diagnostic is not a task-scale benchmark. It is a finite-state certificate
check for the inequalities used in the paper.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


VALUE_TOL = 1e-10
CERT_TOL = 1e-8


Vector = List[float]
Matrix = List[List[float]]
Tensor3 = List[List[List[float]]]


@dataclass(frozen=True)
class FiniteMDP:
    num_states: int
    num_actions: int
    P: Tensor3
    R: Matrix
    rho: Vector
    pi: Matrix


@dataclass
class PolicyEvaluation:
    gamma: float
    P_pi: Matrix
    r_pi: Vector
    V_pi: Vector
    Q_pi: Matrix
    A_pi: Matrix
    d_pi: Vector
    eta_pi: float
    powers: Dict[int, Matrix]
    reward_prefix: Dict[int, Vector]

    def apply_k_step(self, U: Vector, K: int) -> Vector:
        return vector_add(
            self.reward_prefix[K],
            scalar_vec_mul(self.gamma**K, mat_vec_mul(self.powers[K], U)),
        )


@dataclass
class CandidateBundle:
    mode: str
    beta: float
    sigma_xi: float
    L_z: float
    n: int
    pi_cand: Matrix
    eps_A_cand: float
    eps_CPI: float
    metrics_by_alpha: List[Dict[str, float]]
    max_true_improvement: float
    certificates_hold: bool


def parse_float_list(text: str) -> List[float]:
    return [float(piece.strip()) for piece in text.split(",") if piece.strip()]


def parse_int_list(text: str) -> List[int]:
    return [int(piece.strip()) for piece in text.split(",") if piece.strip()]


def zeros(n: int) -> Vector:
    return [0.0 for _ in range(n)]


def zeros_matrix(rows: int, cols: int) -> Matrix:
    return [[0.0 for _ in range(cols)] for _ in range(rows)]


def eye(n: int) -> Matrix:
    mat = zeros_matrix(n, n)
    for i in range(n):
        mat[i][i] = 1.0
    return mat


def transpose(mat: Matrix) -> Matrix:
    return [list(col) for col in zip(*mat)]


def dot(u: Vector, v: Vector) -> float:
    return math.fsum(a * b for a, b in zip(u, v))


def mat_vec_mul(mat: Matrix, vec: Vector) -> Vector:
    return [dot(row, vec) for row in mat]


def mat_mat_mul(A: Matrix, B: Matrix) -> Matrix:
    B_t = transpose(B)
    return [[dot(row, col) for col in B_t] for row in A]


def vector_add(u: Vector, v: Vector) -> Vector:
    return [a + b for a, b in zip(u, v)]


def vector_sub(u: Vector, v: Vector) -> Vector:
    return [a - b for a, b in zip(u, v)]


def scalar_vec_mul(scale: float, vec: Vector) -> Vector:
    return [scale * value for value in vec]


def max_abs(vec: Vector) -> float:
    return max(abs(value) for value in vec)


def matrix_copy(mat: Matrix) -> Matrix:
    return [row[:] for row in mat]


def solve_linear_system(A: Matrix, b: Vector) -> Vector:
    n = len(A)
    aug = [A[row][:] + [float(b[row])] for row in range(n)]

    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("Singular linear system in finite-MDP diagnostic.")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]

        pivot_value = aug[col][col]
        inv_pivot = 1.0 / pivot_value
        for j in range(col, n + 1):
            aug[col][j] *= inv_pivot

        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if abs(factor) < 1e-16:
                continue
            for j in range(col, n + 1):
                aug[row][j] -= factor * aug[col][j]

    return [aug[row][n] for row in range(n)]


def assert_close(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def stable_softmax_rows(logits: Matrix) -> Matrix:
    out: Matrix = []
    for row in logits:
        row_max = max(row)
        exps = [math.exp(value - row_max) for value in row]
        total = math.fsum(exps)
        out.append([value / total for value in exps])
    return out


def grid_shape(num_states: int) -> Tuple[int, int]:
    if num_states == 64:
        return 8, 8
    if num_states == 128:
        return 8, 16
    for rows in range(int(math.sqrt(num_states)), 0, -1):
        if num_states % rows == 0:
            return rows, num_states // rows
    raise ValueError(f"Could not factor num_states={num_states} into a grid.")


def clip_unit(value: float) -> float:
    return max(-1.0, min(1.0, value))


def build_structured_grid_mdp(
    num_states: int,
    num_actions: int,
    rng: random.Random,
) -> FiniteMDP:
    if num_actions != 4:
        raise ValueError("The finite-MDP diagnostic uses exactly four actions.")

    rows, cols = grid_shape(num_states)
    goal = (rows - 1, cols - 1)
    traps = {(0, cols - 1), (rows - 1, 0)}
    max_distance = (rows - 1) + (cols - 1)

    def to_state(row: int, col: int) -> int:
        return row * cols + col

    def clamp(row: int, col: int) -> Tuple[int, int]:
        return min(max(row, 0), rows - 1), min(max(col, 0), cols - 1)

    def step_once(state: int, action: int) -> int:
        row, col = divmod(state, cols)
        delta = {
            0: (-1, 0),  # up
            1: (0, 1),   # right
            2: (1, 0),   # down
            3: (0, -1),  # left
        }[action]
        next_row, next_col = clamp(row + delta[0], col + delta[1])
        return to_state(next_row, next_col)

    state_reward = zeros(num_states)
    for state in range(num_states):
        row, col = divmod(state, cols)
        distance = abs(row - goal[0]) + abs(col - goal[1])
        potential = 1.0 - 2.0 * distance / max_distance
        reward = 0.20 * potential
        if (row, col) == goal:
            reward += 0.80
        if (row, col) in traps:
            reward -= 0.80
        state_reward[state] = clip_unit(reward)

    transition_weights = {
        0: ((0, 0.80), (3, 0.10), (1, 0.10)),
        1: ((1, 0.80), (0, 0.10), (2, 0.10)),
        2: ((2, 0.80), (1, 0.10), (3, 0.10)),
        3: ((3, 0.80), (2, 0.10), (0, 0.10)),
    }

    P: Tensor3 = [[zeros(num_states) for _ in range(num_actions)] for _ in range(num_states)]
    R: Matrix = zeros_matrix(num_states, num_actions)
    for state in range(num_states):
        row, col = divmod(state, cols)
        distance = abs(row - goal[0]) + abs(col - goal[1])
        for action in range(num_actions):
            for slip_action, prob in transition_weights[action]:
                next_state = step_once(state, slip_action)
                P[state][action][next_state] += prob
            expected_state_reward = dot(P[state][action], state_reward)
            intended_state = step_once(state, action)
            next_row, next_col = divmod(intended_state, cols)
            next_distance = abs(next_row - goal[0]) + abs(next_col - goal[1])
            if next_distance < distance:
                progress_bonus = 0.05
            elif next_distance > distance:
                progress_bonus = -0.03
            else:
                progress_bonus = 0.0
            action_tilt = 0.015 * math.sin(0.70 * state + 0.90 * action)
            R[state][action] = clip_unit(expected_state_reward - 0.02 + progress_bonus + action_tilt)

    rho = zeros(num_states)
    start_states = []
    for row in range(rows):
        for col in range(cols):
            if row + col <= max(2, rows // 2):
                start_states.append(to_state(row, col))
    for state in start_states:
        rho[state] = 1.0 / len(start_states)

    logits = zeros_matrix(num_states, num_actions)
    for state in range(num_states):
        row, col = divmod(state, cols)
        for action in range(num_actions):
            logits[state][action] = 0.25 * rng.gauss(0.0, 1.0)
        if row < goal[0]:
            logits[state][2] += 0.30
        if col < goal[1]:
            logits[state][1] += 0.30
        if row > goal[0]:
            logits[state][0] += 0.10
        if col > goal[1]:
            logits[state][3] += 0.10
    pi = stable_softmax_rows(logits)

    for state in range(num_states):
        for action in range(num_actions):
            assert_close(
                abs(math.fsum(P[state][action]) - 1.0) <= 1e-12,
                f"Transition probabilities do not sum to one at state={state}, action={action}.",
            )
        assert_close(
            abs(math.fsum(pi[state]) - 1.0) <= 1e-12,
            f"Policy probabilities do not sum to one at state={state}.",
        )
    assert_close(abs(math.fsum(rho) - 1.0) <= 1e-12, "Initial distribution does not sum to one.")

    return FiniteMDP(
        num_states=num_states,
        num_actions=num_actions,
        P=P,
        R=R,
        rho=rho,
        pi=pi,
    )


def exact_policy_evaluation(
    mdp: FiniteMDP,
    gamma: float,
    max_k: int,
) -> PolicyEvaluation:
    P_pi = zeros_matrix(mdp.num_states, mdp.num_states)
    r_pi = zeros(mdp.num_states)
    for state in range(mdp.num_states):
        r_pi[state] = math.fsum(mdp.pi[state][action] * mdp.R[state][action] for action in range(mdp.num_actions))
        for next_state in range(mdp.num_states):
            P_pi[state][next_state] = math.fsum(
                mdp.pi[state][action] * mdp.P[state][action][next_state]
                for action in range(mdp.num_actions)
            )

    system = matrix_copy(eye(mdp.num_states))
    for row in range(mdp.num_states):
        for col in range(mdp.num_states):
            system[row][col] -= gamma * P_pi[row][col]
    V_pi = solve_linear_system(system, r_pi)

    Q_pi = zeros_matrix(mdp.num_states, mdp.num_actions)
    A_pi = zeros_matrix(mdp.num_states, mdp.num_actions)
    for state in range(mdp.num_states):
        for action in range(mdp.num_actions):
            continuation = dot(mdp.P[state][action], V_pi)
            Q_pi[state][action] = mdp.R[state][action] + gamma * continuation
            A_pi[state][action] = Q_pi[state][action] - V_pi[state]

    P_pi_T = transpose(P_pi)
    occupancy_system = matrix_copy(eye(mdp.num_states))
    for row in range(mdp.num_states):
        for col in range(mdp.num_states):
            occupancy_system[row][col] -= gamma * P_pi_T[row][col]
    d_pi = scalar_vec_mul(1.0 - gamma, solve_linear_system(occupancy_system, mdp.rho))
    min_d = min(d_pi)
    assert_close(min_d >= -1e-8, f"Discounted occupancy has large negative entries: min={min_d}")
    d_pi = [max(0.0, value) for value in d_pi]
    total_d = math.fsum(d_pi)
    d_pi = [value / total_d for value in d_pi]

    eta_pi = dot(mdp.rho, V_pi)

    powers: Dict[int, Matrix] = {0: eye(mdp.num_states)}
    reward_prefix: Dict[int, Vector] = {0: zeros(mdp.num_states)}
    power = eye(mdp.num_states)
    prefix = zeros(mdp.num_states)
    discount = 1.0
    for step in range(1, max_k + 1):
        prefix = vector_add(prefix, scalar_vec_mul(discount, mat_vec_mul(power, r_pi)))
        power = mat_mat_mul(power, P_pi)
        powers[step] = power
        reward_prefix[step] = prefix[:]
        discount *= gamma

    return PolicyEvaluation(
        gamma=gamma,
        P_pi=P_pi,
        r_pi=r_pi,
        V_pi=V_pi,
        Q_pi=Q_pi,
        A_pi=A_pi,
        d_pi=d_pi,
        eta_pi=eta_pi,
        powers=powers,
        reward_prefix=reward_prefix,
    )


def make_evaluator(U_star: Vector, L_z: float, n: int) -> Tuple[Vector, float]:
    factor = L_z**n
    U_n = [(1.0 - factor) * value for value in U_star]
    C_z = max(abs((1.0 - L_z) * value) for value in U_star)
    return U_n, C_z


def exact_centered_advantage(
    mdp: FiniteMDP,
    gamma: float,
    U_n: Vector,
) -> Tuple[Matrix, Matrix, float]:
    Q_hat = zeros_matrix(mdp.num_states, mdp.num_actions)
    A_hat = zeros_matrix(mdp.num_states, mdp.num_actions)
    max_defect = 0.0
    for state in range(mdp.num_states):
        baseline = 0.0
        for action in range(mdp.num_actions):
            Q_hat[state][action] = mdp.R[state][action] + gamma * dot(mdp.P[state][action], U_n)
            baseline += mdp.pi[state][action] * Q_hat[state][action]
        for action in range(mdp.num_actions):
            A_hat[state][action] = Q_hat[state][action] - baseline
        centering_defect = abs(math.fsum(mdp.pi[state][action] * A_hat[state][action] for action in range(mdp.num_actions)))
        max_defect = max(max_defect, centering_defect)
    return Q_hat, A_hat, max_defect


def compute_eta(
    mdp: FiniteMDP,
    gamma: float,
    pi_policy: Matrix,
) -> float:
    P_policy = zeros_matrix(mdp.num_states, mdp.num_states)
    r_policy = zeros(mdp.num_states)
    for state in range(mdp.num_states):
        r_policy[state] = math.fsum(pi_policy[state][action] * mdp.R[state][action] for action in range(mdp.num_actions))
        for next_state in range(mdp.num_states):
            P_policy[state][next_state] = math.fsum(
                pi_policy[state][action] * mdp.P[state][action][next_state]
                for action in range(mdp.num_actions)
            )
    system = eye(mdp.num_states)
    for row in range(mdp.num_states):
        for col in range(mdp.num_states):
            system[row][col] -= gamma * P_policy[row][col]
    V_policy = solve_linear_system(system, r_policy)
    return dot(mdp.rho, V_policy)


def evaluate_candidate(
    mdp: FiniteMDP,
    evaluation: PolicyEvaluation,
    A_hat: Matrix,
    pi_cand: Matrix,
    beta: float,
    mode: str,
    sigma_xi: float,
    L_z: float,
    n: int,
    alphas: Sequence[float],
    decomp_bound: float,
) -> CandidateBundle:
    expectation_gap = zeros(mdp.num_states)
    expected_adv = zeros(mdp.num_states)
    for state in range(mdp.num_states):
        expectation_gap[state] = math.fsum(
            pi_cand[state][action] * (evaluation.A_pi[state][action] - A_hat[state][action])
            for action in range(mdp.num_actions)
        )
        expected_adv[state] = math.fsum(
            pi_cand[state][action] * evaluation.A_pi[state][action]
            for action in range(mdp.num_actions)
        )
    eps_A_cand = max_abs(expectation_gap)
    eps_CPI = max_abs(expected_adv)

    metrics_by_alpha: List[Dict[str, float]] = []
    max_true_improvement = -1e18
    certificates_hold = True
    for alpha in alphas:
        pi_alpha = zeros_matrix(mdp.num_states, mdp.num_actions)
        for state in range(mdp.num_states):
            for action in range(mdp.num_actions):
                pi_alpha[state][action] = (1.0 - alpha) * mdp.pi[state][action] + alpha * pi_cand[state][action]
        eta_pi_alpha = compute_eta(mdp, evaluation.gamma, pi_alpha)
        surrogate_expectation = math.fsum(
            evaluation.d_pi[state]
            * math.fsum(pi_alpha[state][action] * A_hat[state][action] for action in range(mdp.num_actions))
            for state in range(mdp.num_states)
        )
        Lhat_pi_alpha = evaluation.eta_pi + surrogate_expectation / (1.0 - evaluation.gamma)
        surrogate_gap = Lhat_pi_alpha - eta_pi_alpha
        penalty_decomp = (
            (2.0 * alpha * evaluation.gamma / (1.0 - evaluation.gamma)) * decomp_bound
            + (2.0 * eps_CPI * evaluation.gamma / ((1.0 - evaluation.gamma) ** 2)) * (alpha**2)
        )
        penalty_exact = (
            (alpha / (1.0 - evaluation.gamma)) * eps_A_cand
            + (2.0 * eps_CPI * evaluation.gamma / ((1.0 - evaluation.gamma) ** 2)) * (alpha**2)
        )
        hold_decomp = surrogate_gap <= penalty_decomp + CERT_TOL
        hold_exact = surrogate_gap <= penalty_exact + CERT_TOL
        certificates_hold = certificates_hold and hold_decomp and hold_exact
        max_true_improvement = max(max_true_improvement, eta_pi_alpha - evaluation.eta_pi)
        metrics_by_alpha.append(
            {
                "alpha": alpha,
                "eta_pi_alpha": eta_pi_alpha,
                "Lhat_pi_alpha": Lhat_pi_alpha,
                "penalty_decomp": penalty_decomp,
                "penalty_exact_A": penalty_exact,
                "certificate_holds_decomp": 1.0 if hold_decomp else 0.0,
                "certificate_holds_exact_A": 1.0 if hold_exact else 0.0,
            }
        )

    return CandidateBundle(
        mode=mode,
        beta=beta,
        sigma_xi=sigma_xi,
        L_z=L_z,
        n=n,
        pi_cand=pi_cand,
        eps_A_cand=eps_A_cand,
        eps_CPI=eps_CPI,
        metrics_by_alpha=metrics_by_alpha,
        max_true_improvement=max_true_improvement,
        certificates_hold=certificates_hold,
    )


def bundle_cpi_stats(bundle: CandidateBundle) -> Dict[str, float]:
    positive_alpha_rows = [row for row in bundle.metrics_by_alpha if row["alpha"] > 0.0]
    gaps = [row["Lhat_pi_alpha"] - row["eta_pi_alpha"] for row in positive_alpha_rows]
    penalties_decomp = [row["penalty_decomp"] for row in positive_alpha_rows]
    penalties_exact = [row["penalty_exact_A"] for row in positive_alpha_rows]
    exact_ratios = [
        gap / penalty
        for gap, penalty in zip(gaps, penalties_exact)
        if penalty > 0.0
    ]
    return {
        "min_gap": min(gaps) if gaps else 0.0,
        "max_gap": max(gaps) if gaps else 0.0,
        "max_penalty_decomp": max(penalties_decomp) if penalties_decomp else 0.0,
        "max_penalty_exact": max(penalties_exact) if penalties_exact else 0.0,
        "best_exact_ratio": max(exact_ratios) if exact_ratios else 0.0,
    }


def bundle_is_informative(bundle: CandidateBundle) -> bool:
    stats = bundle_cpi_stats(bundle)
    return (
        bundle.certificates_hold
        and stats["min_gap"] > 1e-8
        and bundle.max_true_improvement > 1e-6
    )


def bundle_score(bundle: CandidateBundle) -> Tuple[bool, bool, int, bool, float, float, float]:
    stats = bundle_cpi_stats(bundle)
    weak_positive_gap = stats["max_gap"] > 1e-8 and bundle.max_true_improvement > 1e-6
    return (
        bundle.certificates_hold,
        bundle_is_informative(bundle),
        1 if bundle.mode == "evaluator" else 0,
        weak_positive_gap,
        stats["best_exact_ratio"],
        -stats["max_penalty_exact"],
        stats["max_gap"],
    )


def select_cpi_slice(
    mdp: FiniteMDP,
    evaluation: PolicyEvaluation,
    K: int,
    sigma_values: Sequence[float],
    Lz_values: Sequence[float],
    n_candidates: Sequence[int],
    betas: Sequence[float],
    alphas: Sequence[float],
    base_noise: Vector,
) -> Tuple[Vector, float, float, int, float, float, Matrix, CandidateBundle]:
    preferred = [(0.10, 0.50, 4), (0.05, 0.50, 4), (0.05, 0.80, 8)]
    search_grid = list(preferred)
    for sigma_xi in sigma_values:
        for L_z in Lz_values:
            for n in n_candidates:
                triple = (sigma_xi, L_z, n)
                if triple not in search_grid:
                    search_grid.append(triple)

    def search_mode(mode: str) -> Tuple[Tuple[Vector, float, float, int, float, float, Matrix], CandidateBundle]:
        best_bundle: Optional[CandidateBundle] = None
        best_payload: Optional[Tuple[Vector, float, float, int, float, float, Matrix]] = None

        for sigma_xi, L_z, n in search_grid:
            xi = [sigma_xi * noise for noise in base_noise]
            U_star = [value + delta for value, delta in zip(evaluation.V_pi, xi)]
            U_n, C_z = make_evaluator(U_star, L_z=L_z, n=n)
            eps_res_star = max_abs(vector_sub(U_star, evaluation.apply_k_step(U_star, K)))
            decomp_bound = eps_res_star / (1.0 - evaluation.gamma**K) + (L_z**n / (1.0 - L_z)) * C_z
            _, A_hat, centering_defect = exact_centered_advantage(mdp, evaluation.gamma, U_n)
            assert_close(centering_defect <= VALUE_TOL, f"Centering defect too large in CPI search: {centering_defect}")
            source_advantage = A_hat if mode == "evaluator" else evaluation.A_pi

            for beta in betas:
                pi_cand = stable_softmax_rows([[beta * value for value in row] for row in source_advantage])
                bundle = evaluate_candidate(
                    mdp=mdp,
                    evaluation=evaluation,
                    A_hat=A_hat,
                    pi_cand=pi_cand,
                    beta=beta,
                    mode=mode,
                    sigma_xi=sigma_xi,
                    L_z=L_z,
                    n=n,
                    alphas=alphas,
                    decomp_bound=decomp_bound,
                )
                if best_bundle is None or bundle_score(bundle) > bundle_score(best_bundle):
                    best_bundle = bundle
                    best_payload = (U_n, eps_res_star, decomp_bound, n, sigma_xi, L_z, A_hat)

        assert best_bundle is not None and best_payload is not None
        return best_payload, best_bundle

    evaluator_payload, evaluator_bundle = search_mode("evaluator")
    if bundle_is_informative(evaluator_bundle):
        return (*evaluator_payload, evaluator_bundle)

    true_adv_payload, true_adv_bundle = search_mode("true_adv")
    if bundle_score(true_adv_bundle) > bundle_score(evaluator_bundle):
        return (*true_adv_payload, true_adv_bundle)
    return (*evaluator_payload, evaluator_bundle)


def write_csv(rows: List[Dict[str, object]], out_path: Path) -> None:
    fieldnames = [
        "record_type",
        "seed",
        "S",
        "A",
        "gamma",
        "K",
        "L_z",
        "n",
        "sigma_xi",
        "alpha",
        "beta",
        "candidate_mode",
        "value_error",
        "decomposition_bound",
        "finite_depth_residual",
        "finite_depth_residual_bound",
        "eps_res_star",
        "eps_res_n",
        "eps_A_cand",
        "eps_A_bound",
        "eta_pi",
        "eta_pi_alpha",
        "Lhat_pi_alpha",
        "eps_CPI",
        "penalty_decomp",
        "penalty_exact_A",
        "certificate_holds_decomp",
        "certificate_holds_exact_A",
    ]
    with out_path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_value_plot_data(
    path: Path,
    n_values: Sequence[int],
    lz_values: Sequence[float],
    value_error_curves: Dict[float, List[float]],
    decomp_bound_curves: Dict[float, List[float]],
) -> None:
    with path.open("w", encoding="ascii") as handle:
        header = ["n"]
        for L_z in lz_values:
            header.extend([f"err_{L_z:.2f}", f"bound_{L_z:.2f}"])
        handle.write("\t".join(header) + "\n")
        for idx, n in enumerate(n_values):
            row = [str(n)]
            for L_z in lz_values:
                row.append(f"{value_error_curves[L_z][idx]:.12g}")
                row.append(f"{decomp_bound_curves[L_z][idx]:.12g}")
            handle.write("\t".join(row) + "\n")


def write_cpi_plot_data(path: Path, cpi_rows: List[Dict[str, float]], positive_only: bool) -> None:
    with path.open("w", encoding="ascii") as handle:
        handle.write("alpha\tgap\tpenalty_decomp\tpenalty_exact\n")
        for row in cpi_rows:
            if positive_only and row["alpha"] <= 0.0:
                continue
            gap = row["Lhat_pi_alpha"] - row["eta_pi_alpha"]
            if positive_only:
                assert_close(gap > 0.0, "Positive-gap CPI plot requested but encountered a non-positive surrogate gap.")
                assert_close(
                    row["penalty_decomp"] > 0.0 and row["penalty_exact_A"] > 0.0,
                    "Positive-gap CPI plot requested but encountered a non-positive certificate value.",
                )
            handle.write(
                f"{row['alpha']:.12g}\t{gap:.12g}\t{row['penalty_decomp']:.12g}\t{row['penalty_exact_A']:.12g}\n"
            )


def run_gnuplot(script_text: str, script_path: Path) -> None:
    script_path.write_text(script_text, encoding="ascii")
    subprocess.run(["gnuplot", str(script_path)], check=True)


def write_value_gnuplot(
    data_path: Path,
    pdf_path: Path,
    png_path: Path,
    script_path: Path,
    lz_values: Sequence[float],
) -> None:
    colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]
    plot_terms = []
    column = 2
    for idx, L_z in enumerate(lz_values):
        color = colors[idx % len(colors)]
        plot_terms.append(
            f"'{data_path}' using 1:{column} with lines lc rgb '{color}' lw 2 title 'L_z={L_z:.2f} error'"
        )
        plot_terms.append(
            f"'{data_path}' using 1:{column + 1} with lines dt 2 lc rgb '{color}' lw 2 title 'L_z={L_z:.2f} bound'"
        )
        column += 2
    plot_body = ", \\\n+    ".join(plot_terms)
    script = f"""
set datafile separator '\\t'
set xlabel 'Evaluator depth n'
set ylabel 'Value error / certificate'
set title 'Finite-MDP value-error decomposition'
set key outside
set grid
set logscale y
set terminal pdfcairo enhanced color size 6.2in,3.8in font ',10'
set output '{pdf_path}'
plot {plot_body}
set terminal pngcairo size 1600,980 enhanced font ',10'
set output '{png_path}'
replot
"""
    run_gnuplot(script.strip() + "\n", script_path)


def write_cpi_gnuplot(
    data_path: Path,
    pdf_path: Path,
    png_path: Path,
    script_path: Path,
    logscale_y: bool,
) -> None:
    ylabel = "Positive surrogate gap / certificate" if logscale_y else "Surrogate gap / certificate"
    title = "Finite-MDP CPI certificate (log scale)" if logscale_y else "Finite-MDP CPI certificate"
    script = f"""
set datafile separator '\\t'
set xlabel 'Mixture weight alpha'
set ylabel '{ylabel}'
set title '{title}'
set key top left
set grid
{"set xrange [0.05:1.0]" if logscale_y else ""}
{"set logscale y" if logscale_y else ""}
set terminal pdfcairo enhanced color size 6.2in,3.8in font ',10'
set output '{pdf_path}'
plot '{data_path}' using 1:2 with linespoints lw 2 pt 7 lc rgb '#0f4c81' title 'Lhat - eta', \
     '{data_path}' using 1:3 with linespoints lw 2 pt 5 dt 2 lc rgb '#c0392b' title 'decomposition penalty', \
     '{data_path}' using 1:4 with linespoints lw 2 pt 9 dt 3 lc rgb '#2d8659' title 'exact A penalty'
set terminal pngcairo size 1600,980 enhanced font ',10'
set output '{png_path}'
replot
"""
    run_gnuplot(script.strip() + "\n", script_path)


def write_summary_table(
    out_path: Path,
    lz_values: Sequence[float],
    n_summary: int,
    summary_rows: Dict[float, Dict[str, float]],
    cpi_bundle: CandidateBundle,
) -> None:
    lines = [
        "% Auto-generated by experiments/finite_mdp_certificate.py",
        "\\begin{table}[t]",
        "\\centering",
        "\\small",
        "\\caption{Finite-MDP certificate diagnostic summary for the plotting slice.}",
        "\\label{tab:finite_mdp_certificate_summary}",
        "\\begin{tabular}{lcccc}",
        "\\toprule",
        "$L_z$ & $n$ & $\\|U_n - V^\\pi\\|_\\infty$ & Decomp. bound & Residual bound \\\\",
        "\\midrule",
    ]
    for L_z in lz_values:
        row = summary_rows[L_z]
        lines.append(
            f"{L_z:.2f} & {n_summary} & {row['value_error']:.4f} & "
            f"{row['decomposition_bound']:.4f} & {row['finite_depth_residual_bound']:.4f} \\\\"
        )
    lines.extend(
        [
            "\\midrule",
            "\\multicolumn{5}{l}{\\emph{Selected CPI slice:} "
            f"$\\sigma_\\xi={cpi_bundle.sigma_xi:.2f}$, "
            f"$L_z={cpi_bundle.L_z:.2f}$, $n={cpi_bundle.n}$, "
            f"{cpi_bundle.mode} candidate, $\\beta={cpi_bundle.beta:.1f}$}} \\\\",
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{table}",
            "",
        ]
    )
    out_path.write_text("\n".join(lines), encoding="ascii")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0, help="Random seed.")
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("results/finite_mdp_certificate"),
        help="Output directory for figures and tables.",
    )
    parser.add_argument("--num-states", type=int, default=64, help="Number of states (64 or 128).")
    parser.add_argument("--num-actions", type=int, default=4, help="Number of actions. Must be 4.")
    parser.add_argument("--gamma", type=float, default=0.9, help="Discount factor for the main diagnostic.")
    parser.add_argument("--K", type=int, default=3, help="Exact K-step Bellman horizon for the main diagnostic.")
    parser.add_argument("--lz-values", default="0.2,0.5,0.8,0.95", help="Comma-separated L_z values.")
    parser.add_argument("--n-max", type=int, default=20, help="Maximum evaluator depth for the value plot.")
    parser.add_argument(
        "--sigma-xi-values",
        default="0.0,0.01,0.05,0.1",
        help="Comma-separated perturbation scales used when searching the CPI slice.",
    )
    parser.add_argument("--decomposition-sigma", type=float, default=0.05, help="Perturbation scale for the value plot.")
    parser.add_argument(
        "--betas",
        default="0.1,0.25,0.5,1,2,5,10",
        help="Comma-separated candidate inverse temperatures.",
    )
    parser.add_argument(
        "--candidate-n-values",
        default="4,8,12,16",
        help="Comma-separated n values to search when selecting the CPI slice.",
    )
    args = parser.parse_args()

    outdir = args.outdir.resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    lz_values = parse_float_list(args.lz_values)
    sigma_values = parse_float_list(args.sigma_xi_values)
    betas = parse_float_list(args.betas)
    candidate_n_values = parse_int_list(args.candidate_n_values)
    n_values = list(range(1, args.n_max + 1))
    alphas = [index / 20.0 for index in range(21)]
    n_summary = 8 if 8 in n_values else n_values[-1]

    rng = random.Random(args.seed)
    mdp = build_structured_grid_mdp(args.num_states, args.num_actions, rng)
    evaluation = exact_policy_evaluation(mdp, gamma=args.gamma, max_k=max(args.K, 5))
    base_noise = [rng.gauss(0.0, 1.0) for _ in range(args.num_states)]

    csv_rows: List[Dict[str, object]] = []
    value_error_curves: Dict[float, List[float]] = {}
    decomp_bound_curves: Dict[float, List[float]] = {}
    summary_rows: Dict[float, Dict[str, float]] = {}
    decomposition_gaps: List[float] = []
    residual_gaps: List[float] = []

    xi_decomp = [args.decomposition_sigma * noise for noise in base_noise]
    U_star_decomp = [value + delta for value, delta in zip(evaluation.V_pi, xi_decomp)]
    eps_res_star_decomp = max_abs(vector_sub(U_star_decomp, evaluation.apply_k_step(U_star_decomp, args.K)))

    for L_z in lz_values:
        value_error_curves[L_z] = []
        decomp_bound_curves[L_z] = []
        for n in n_values:
            U_n, C_z = make_evaluator(U_star_decomp, L_z=L_z, n=n)
            value_error = max_abs(vector_sub(U_n, evaluation.V_pi))
            truncation_term = (L_z**n / (1.0 - L_z)) * C_z
            decomposition_bound = eps_res_star_decomp / (1.0 - args.gamma**args.K) + truncation_term
            eps_res_n = max_abs(vector_sub(U_n, evaluation.apply_k_step(U_n, args.K)))
            finite_depth_residual_bound = eps_res_n / (1.0 - args.gamma**args.K)

            decomposition_gap = value_error - decomposition_bound
            residual_gap = value_error - finite_depth_residual_bound
            assert_close(
                decomposition_gap <= CERT_TOL,
                f"Value-error decomposition violated at L_z={L_z}, n={n}: gap={decomposition_gap}",
            )
            assert_close(
                residual_gap <= CERT_TOL,
                f"Finite-depth residual certificate violated at L_z={L_z}, n={n}: gap={residual_gap}",
            )
            decomposition_gaps.append(decomposition_gap)
            residual_gaps.append(residual_gap)

            value_error_curves[L_z].append(value_error)
            decomp_bound_curves[L_z].append(decomposition_bound)
            csv_rows.append(
                {
                    "record_type": "value_curve",
                    "seed": args.seed,
                    "S": args.num_states,
                    "A": args.num_actions,
                    "gamma": args.gamma,
                    "K": args.K,
                    "L_z": L_z,
                    "n": n,
                    "sigma_xi": args.decomposition_sigma,
                    "alpha": 0.0,
                    "beta": 0.0,
                    "candidate_mode": "none",
                    "value_error": value_error,
                    "decomposition_bound": decomposition_bound,
                    "finite_depth_residual": eps_res_n,
                    "finite_depth_residual_bound": finite_depth_residual_bound,
                    "eps_res_star": eps_res_star_decomp,
                    "eps_res_n": eps_res_n,
                    "eps_A_cand": 0.0,
                    "eps_A_bound": 0.0,
                    "eta_pi": evaluation.eta_pi,
                    "eta_pi_alpha": evaluation.eta_pi,
                    "Lhat_pi_alpha": evaluation.eta_pi,
                    "eps_CPI": 0.0,
                    "penalty_decomp": 0.0,
                    "penalty_exact_A": 0.0,
                    "certificate_holds_decomp": 1,
                    "certificate_holds_exact_A": 1,
                }
            )
            if n == n_summary:
                summary_rows[L_z] = {
                    "value_error": value_error,
                    "decomposition_bound": decomposition_bound,
                    "finite_depth_residual_bound": finite_depth_residual_bound,
                }

    U_n_cpi, eps_res_star_cpi, decomp_bound_cpi, n_cpi, sigma_cpi, Lz_cpi, A_hat_cpi, cpi_bundle = select_cpi_slice(
        mdp=mdp,
        evaluation=evaluation,
        K=args.K,
        sigma_values=sigma_values,
        Lz_values=lz_values,
        n_candidates=candidate_n_values,
        betas=betas,
        alphas=alphas,
        base_noise=base_noise,
    )

    value_error_cpi = max_abs(vector_sub(U_n_cpi, evaluation.V_pi))
    eps_res_n_cpi = max_abs(vector_sub(U_n_cpi, evaluation.apply_k_step(U_n_cpi, args.K)))
    finite_depth_residual_bound_cpi = eps_res_n_cpi / (1.0 - args.gamma**args.K)
    eps_A_bound_cpi = 2.0 * args.gamma * decomp_bound_cpi
    advantage_gap = cpi_bundle.eps_A_cand - eps_A_bound_cpi
    assert_close(
        advantage_gap <= CERT_TOL,
        f"Advantage certificate violated on CPI slice: gap={advantage_gap}",
    )

    cpi_rows_for_plot: List[Dict[str, float]] = []
    cpi_decomp_gaps: List[float] = []
    cpi_exact_gaps: List[float] = []
    for row in cpi_bundle.metrics_by_alpha:
        surrogate_gap = row["Lhat_pi_alpha"] - row["eta_pi_alpha"]
        cpi_decomp_gap = surrogate_gap - row["penalty_decomp"]
        cpi_exact_gap = surrogate_gap - row["penalty_exact_A"]
        assert_close(
            cpi_decomp_gap <= CERT_TOL,
            f"CPI decomposition certificate violated at alpha={row['alpha']}: gap={cpi_decomp_gap}",
        )
        assert_close(
            cpi_exact_gap <= CERT_TOL,
            f"CPI exact-A certificate violated at alpha={row['alpha']}: gap={cpi_exact_gap}",
        )
        cpi_decomp_gaps.append(cpi_decomp_gap)
        cpi_exact_gaps.append(cpi_exact_gap)
        cpi_rows_for_plot.append(row)
        csv_rows.append(
            {
                "record_type": "cpi_curve",
                "seed": args.seed,
                "S": args.num_states,
                "A": args.num_actions,
                "gamma": args.gamma,
                "K": args.K,
                "L_z": Lz_cpi,
                "n": n_cpi,
                "sigma_xi": sigma_cpi,
                "alpha": row["alpha"],
                "beta": cpi_bundle.beta,
                "candidate_mode": cpi_bundle.mode,
                "value_error": value_error_cpi,
                "decomposition_bound": decomp_bound_cpi,
                "finite_depth_residual": eps_res_n_cpi,
                "finite_depth_residual_bound": finite_depth_residual_bound_cpi,
                "eps_res_star": eps_res_star_cpi,
                "eps_res_n": eps_res_n_cpi,
                "eps_A_cand": cpi_bundle.eps_A_cand,
                "eps_A_bound": eps_A_bound_cpi,
                "eta_pi": evaluation.eta_pi,
                "eta_pi_alpha": row["eta_pi_alpha"],
                "Lhat_pi_alpha": row["Lhat_pi_alpha"],
                "eps_CPI": cpi_bundle.eps_CPI,
                "penalty_decomp": row["penalty_decomp"],
                "penalty_exact_A": row["penalty_exact_A"],
                "certificate_holds_decomp": int(row["certificate_holds_decomp"]),
                "certificate_holds_exact_A": int(row["certificate_holds_exact_A"]),
            }
        )

    write_csv(csv_rows, outdir / "finite_mdp_summary.csv")

    value_data_path = outdir / "fig_value_decomposition.dat"
    cpi_data_path = outdir / "fig_cpi_certificate.dat"
    write_value_plot_data(value_data_path, n_values, lz_values, value_error_curves, decomp_bound_curves)
    cpi_plot_positive_only = bundle_cpi_stats(cpi_bundle)["min_gap"] > 1e-8
    write_cpi_plot_data(cpi_data_path, cpi_rows_for_plot, positive_only=cpi_plot_positive_only)
    write_value_gnuplot(
        data_path=value_data_path,
        pdf_path=outdir / "fig_value_decomposition.pdf",
        png_path=outdir / "fig_value_decomposition.png",
        script_path=outdir / "fig_value_decomposition.gp",
        lz_values=lz_values,
    )
    write_cpi_gnuplot(
        data_path=cpi_data_path,
        pdf_path=outdir / "fig_cpi_certificate.pdf",
        png_path=outdir / "fig_cpi_certificate.png",
        script_path=outdir / "fig_cpi_certificate.gp",
        logscale_y=cpi_plot_positive_only,
    )
    write_summary_table(
        out_path=outdir / "finite_mdp_summary.tex",
        lz_values=lz_values,
        n_summary=n_summary,
        summary_rows=summary_rows,
        cpi_bundle=cpi_bundle,
    )

    print(f"Wrote figures and tables to {outdir}")
    print(
        "Worst margins: "
        f"decomposition={max(decomposition_gaps):.3e}, "
        f"residual={max(residual_gaps):.3e}, "
        f"advantage={advantage_gap:.3e}, "
        f"cpi_decomp={max(cpi_decomp_gaps):.3e}, "
        f"cpi_exact={max(cpi_exact_gaps):.3e}"
    )
    print(
        "Selected CPI slice: "
        f"sigma_xi={sigma_cpi:.2f}, L_z={Lz_cpi:.2f}, n={n_cpi}, "
        f"beta={cpi_bundle.beta:.1f}, mode={cpi_bundle.mode}, "
        f"max_true_improvement={cpi_bundle.max_true_improvement:.4f}, "
        f"min_positive_gap={bundle_cpi_stats(cpi_bundle)['min_gap']:.4e}"
    )


if __name__ == "__main__":
    main()
