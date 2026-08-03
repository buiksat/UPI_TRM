#!/usr/bin/env python3
"""Deterministic boundary checks for the finite-MDP theorem pipeline.

The primary generator intentionally retains its 101-row output contract.  This
separate numerical unit test exercises theorem boundaries that do not belong in
the plotting grid.  It uses only the Python standard library and writes a
machine-readable JSON result.

This is a theorem-pipeline unit test.  It is not empirical validation of a
learned recurrent evaluator.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import finite_mdp_certificate as certificate


TEST_TOL = 1e-8
ZERO_TOL = 1e-10


def max_vector_difference(left: Sequence[float], right: Sequence[float]) -> float:
    return max(abs(a - b) for a, b in zip(left, right))


def max_matrix_difference(
    left: Sequence[Sequence[float]],
    right: Sequence[Sequence[float]],
) -> float:
    return max(
        abs(a - b)
        for left_row, right_row in zip(left, right)
        for a, b in zip(left_row, right_row)
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_le(left: float, right: float, label: str, tolerance: float = TEST_TOL) -> None:
    if left > right + tolerance:
        raise AssertionError(
            f"{label}: left={left:.17g}, right={right:.17g}, tolerance={tolerance:.3g}"
        )


def require_close(left: float, right: float, label: str, tolerance: float = ZERO_TOL) -> None:
    if abs(left - right) > tolerance:
        raise AssertionError(
            f"{label}: left={left:.17g}, right={right:.17g}, tolerance={tolerance:.3g}"
        )


def build_reference_problem(
    *,
    gamma: float = 0.83,
    max_k: int = 7,
) -> tuple[certificate.FiniteMDP, certificate.PolicyEvaluation]:
    mdp = certificate.build_structured_grid_mdp(
        num_states=16,
        num_actions=4,
        rng=random.Random(1729),
    )
    evaluation = certificate.exact_policy_evaluation(mdp, gamma=gamma, max_k=max_k)
    return mdp, evaluation


def check_depth_boundaries() -> Dict[str, object]:
    """Check residual, finite-reference, and path bounds at depth boundaries."""

    _mdp, evaluation = build_reference_problem()
    rng = random.Random(2718)
    noise = [0.075 * rng.uniform(-1.0, 1.0) for _ in evaluation.V_pi]
    U_star = [value + delta for value, delta in zip(evaluation.V_pi, noise)]
    L_z = 0.6
    K = 3
    cases = [
        ("n_zero", 0, 4),
        ("m_equals_n_plus_one", 5, 6),
        ("large_m", 4, 128),
    ]

    worst_residual_margin = -math.inf
    worst_reference_margin = -math.inf
    worst_path_margin = -math.inf
    case_metrics: List[Dict[str, object]] = []

    for label, n, m in cases:
        U_n, C_z = certificate.make_evaluator(U_star, L_z=L_z, n=n)
        U_m, _ = certificate.make_evaluator(U_star, L_z=L_z, n=m)

        value_error_n = max_vector_difference(U_n, evaluation.V_pi)
        value_error_m = max_vector_difference(U_m, evaluation.V_pi)
        residual_n = max_vector_difference(U_n, evaluation.apply_k_step(U_n, K))
        residual_m = max_vector_difference(U_m, evaluation.apply_k_step(U_m, K))
        residual_bound_n = residual_n / (1.0 - evaluation.gamma**K)
        residual_bound_m = residual_m / (1.0 - evaluation.gamma**K)
        finite_reference_distance = max_vector_difference(U_n, U_m)
        finite_reference_bound = finite_reference_distance + residual_bound_m

        path_length = 0.0
        for depth in range(n, m):
            U_depth, _ = certificate.make_evaluator(U_star, L_z=L_z, n=depth)
            U_next, _ = certificate.make_evaluator(U_star, L_z=L_z, n=depth + 1)
            path_length += max_vector_difference(U_depth, U_next)
        geometric_path_bound = (
            (L_z**n) * (1.0 - L_z ** (m - n)) / (1.0 - L_z) * C_z
        )

        residual_margin = value_error_n - residual_bound_n
        reference_margin = value_error_n - finite_reference_bound
        path_margin = finite_reference_distance - path_length
        require_le(value_error_n, residual_bound_n, f"{label} residual-to-value")
        require_le(value_error_m, residual_bound_m, f"{label} reference residual-to-value")
        require_le(value_error_n, finite_reference_bound, f"{label} finite-reference")
        require_le(finite_reference_distance, path_length, f"{label} path length")
        require_le(path_length, geometric_path_bound, f"{label} geometric path length")

        if label == "n_zero":
            require(n == 0, "n=0 boundary case was not exercised")
            require_close(max(abs(value) for value in U_n), 0.0, "U_0 boundary")
        if label == "m_equals_n_plus_one":
            require(m == n + 1, "m=n+1 boundary case was not exercised")
        if label == "large_m":
            require(m >= 128, "large-m boundary case was not exercised")
            require_le(value_error_m, 0.08, "large-m reference approaches U_star residual scale")

        worst_residual_margin = max(worst_residual_margin, residual_margin)
        worst_reference_margin = max(worst_reference_margin, reference_margin)
        worst_path_margin = max(worst_path_margin, path_margin)
        case_metrics.append(
            {
                "case": label,
                "m": m,
                "n": n,
                "path_length": path_length,
                "residual_bound_n": residual_bound_n,
                "value_error_n": value_error_n,
            }
        )

    return {
        "boundaries": ["n=0", "m=n+1", "large m=128"],
        "cases": case_metrics,
        "K": K,
        "L_z": L_z,
        "worst_finite_reference_margin": worst_reference_margin,
        "worst_path_length_margin": worst_path_margin,
        "worst_residual_to_value_margin": worst_residual_margin,
    }


def check_one_step_and_zero_residual() -> Dict[str, object]:
    """Check K=1 and the exact fixed-point boundary."""

    _mdp, evaluation = build_reference_problem(max_k=5)
    U = [value + 0.2 * math.sin(index + 0.5) for index, value in enumerate(evaluation.V_pi)]
    value_error = max_vector_difference(U, evaluation.V_pi)
    residual = max_vector_difference(U, evaluation.apply_k_step(U, 1))
    residual_bound = residual / (1.0 - evaluation.gamma)
    require_le(value_error, residual_bound, "K=1 residual-to-value")

    zero_residual = max_vector_difference(
        evaluation.V_pi,
        evaluation.apply_k_step(evaluation.V_pi, 5),
    )
    zero_value_error = max_vector_difference(evaluation.V_pi, evaluation.V_pi)
    require_le(zero_residual, ZERO_TOL, "zero-residual fixed point", tolerance=0.0)
    require_close(zero_value_error, 0.0, "zero value error")

    return {
        "boundaries": ["K=1", "zero residual"],
        "K1_residual_bound": residual_bound,
        "K1_value_error": value_error,
        "zero_residual": zero_residual,
        "zero_value_error": zero_value_error,
    }


def check_advantage_candidate_and_cpi() -> Dict[str, object]:
    """Check value-to-advantage, candidate bias, centering, mixture, and CPI."""

    mdp, evaluation = build_reference_problem()
    rng = random.Random(31415)
    U_star = [
        value + 0.12 * rng.uniform(-1.0, 1.0)
        for value in evaluation.V_pi
    ]
    U_n, _ = certificate.make_evaluator(U_star, L_z=0.55, n=3)
    _Q_hat, A_hat, centering_defect = certificate.exact_centered_advantage(
        mdp,
        evaluation.gamma,
        U_n,
    )
    value_error = max_vector_difference(U_n, evaluation.V_pi)
    advantage_error = max_matrix_difference(A_hat, evaluation.A_pi)
    advantage_bound = 2.0 * evaluation.gamma * value_error
    require_le(centering_defect, ZERO_TOL, "exact statewise centering", tolerance=0.0)
    require_le(advantage_error, advantage_bound, "value-to-advantage")

    pi_cand = certificate.stable_softmax_rows(
        [[1.25 * advantage for advantage in row] for row in A_hat]
    )
    candidate_bias = max(
        abs(
            math.fsum(
                pi_cand[state][action]
                * (evaluation.A_pi[state][action] - A_hat[state][action])
                for action in range(mdp.num_actions)
            )
        )
        for state in range(mdp.num_states)
    )
    require_le(candidate_bias, advantage_error, "candidate-policy bias versus uniform advantage error")
    require_le(candidate_bias, advantage_bound, "candidate-policy bias versus value bound")

    alphas = [0.0, 0.35, 1.0]
    bundle = certificate.evaluate_candidate(
        mdp=mdp,
        evaluation=evaluation,
        A_hat=A_hat,
        pi_cand=pi_cand,
        beta=1.25,
        mode="boundary_test",
        sigma_xi=0.12,
        L_z=0.55,
        n=3,
        alphas=alphas,
        decomp_bound=value_error,
    )
    require(bundle.certificates_hold, "centered CPI inequalities failed")
    require_close(bundle.eps_A_cand, candidate_bias, "reported candidate bias")

    endpoint_errors: Dict[str, float] = {}
    worst_cpi_decomp_margin = -math.inf
    worst_cpi_exact_margin = -math.inf
    for row in bundle.metrics_by_alpha:
        alpha = row["alpha"]
        pi_alpha = [
            [
                (1.0 - alpha) * mdp.pi[state][action]
                + alpha * pi_cand[state][action]
                for action in range(mdp.num_actions)
            ]
            for state in range(mdp.num_states)
        ]
        for state, policy_row in enumerate(pi_alpha):
            require_close(math.fsum(policy_row), 1.0, f"mixture normalization state={state}")
        eta_recomputed = certificate.compute_eta(mdp, evaluation.gamma, pi_alpha)
        require_close(eta_recomputed, row["eta_pi_alpha"], f"mixture performance alpha={alpha}")

        surrogate_gap = row["Lhat_pi_alpha"] - row["eta_pi_alpha"]
        worst_cpi_decomp_margin = max(
            worst_cpi_decomp_margin,
            surrogate_gap - row["penalty_decomp"],
        )
        worst_cpi_exact_margin = max(
            worst_cpi_exact_margin,
            surrogate_gap - row["penalty_exact_A"],
        )
        require_le(surrogate_gap, row["penalty_decomp"], f"decomposition CPI alpha={alpha}")
        require_le(surrogate_gap, row["penalty_exact_A"], f"exact-bias CPI alpha={alpha}")

        if alpha == 0.0:
            endpoint_errors["alpha_0_policy_error"] = max_matrix_difference(pi_alpha, mdp.pi)
            endpoint_errors["alpha_0_eta_error"] = abs(eta_recomputed - evaluation.eta_pi)
        if alpha == 1.0:
            endpoint_errors["alpha_1_policy_error"] = max_matrix_difference(pi_alpha, pi_cand)
            endpoint_errors["alpha_1_eta_error"] = abs(
                eta_recomputed - certificate.compute_eta(mdp, evaluation.gamma, pi_cand)
            )

    require(set(endpoint_errors) == {
        "alpha_0_policy_error",
        "alpha_0_eta_error",
        "alpha_1_policy_error",
        "alpha_1_eta_error",
    }, "alpha endpoint checks are incomplete")
    for label, error in endpoint_errors.items():
        require_le(error, ZERO_TOL, label, tolerance=0.0)

    return {
        "boundaries": ["alpha=0", "alpha=1"],
        "advantage_bound": advantage_bound,
        "advantage_error": advantage_error,
        "candidate_policy_bias": candidate_bias,
        "centering_defect": centering_defect,
        "endpoint_errors": endpoint_errors,
        "worst_centered_cpi_decomposition_margin": worst_cpi_decomp_margin,
        "worst_centered_cpi_exact_bias_margin": worst_cpi_exact_margin,
    }


def check_zero_advantage_error() -> Dict[str, object]:
    """Check the zero advantage-error boundary without estimator drift."""

    mdp, evaluation = build_reference_problem()
    A_hat = [row[:] for row in evaluation.A_pi]
    advantage_error = max_matrix_difference(A_hat, evaluation.A_pi)
    require_close(advantage_error, 0.0, "zero advantage error")
    centering_defect = max(
        abs(
            math.fsum(
                mdp.pi[state][action] * A_hat[state][action]
                for action in range(mdp.num_actions)
            )
        )
        for state in range(mdp.num_states)
    )
    require_le(centering_defect, ZERO_TOL, "true-advantage centering", tolerance=0.0)

    pi_cand = certificate.stable_softmax_rows(
        [[advantage for advantage in row] for row in A_hat]
    )
    bundle = certificate.evaluate_candidate(
        mdp=mdp,
        evaluation=evaluation,
        A_hat=A_hat,
        pi_cand=pi_cand,
        beta=1.0,
        mode="zero_advantage_error",
        sigma_xi=0.0,
        L_z=0.0,
        n=0,
        alphas=[0.0, 1.0],
        decomp_bound=0.0,
    )
    require_close(bundle.eps_A_cand, 0.0, "zero candidate-policy bias")
    require(bundle.certificates_hold, "zero-advantage-error CPI boundary failed")

    return {
        "boundaries": ["zero advantage error"],
        "advantage_error": advantage_error,
        "candidate_policy_bias": bundle.eps_A_cand,
        "centering_defect": centering_defect,
    }


def check_gamma_zero() -> Dict[str, object]:
    """Check gamma=0, where the one-step backup discards continuation values."""

    mdp, evaluation = build_reference_problem(gamma=0.0, max_k=1)
    U = [0.3 * math.cos(index) for index in range(mdp.num_states)]
    backed_up = evaluation.apply_k_step(U, 1)
    value_error = max_vector_difference(U, evaluation.V_pi)
    residual = max_vector_difference(U, backed_up)
    require_close(value_error, residual, "gamma=0 residual identity")
    require_le(value_error, residual, "gamma=0 residual-to-value")
    require_close(
        max_vector_difference(backed_up, evaluation.r_pi),
        0.0,
        "gamma=0 backup equals immediate reward",
    )

    _Q_hat, A_hat, centering_defect = certificate.exact_centered_advantage(mdp, 0.0, U)
    advantage_error = max_matrix_difference(A_hat, evaluation.A_pi)
    require_le(centering_defect, ZERO_TOL, "gamma=0 centering", tolerance=0.0)
    require_le(advantage_error, ZERO_TOL, "gamma=0 advantage error", tolerance=0.0)

    pi_cand = certificate.stable_softmax_rows(A_hat)
    bundle = certificate.evaluate_candidate(
        mdp=mdp,
        evaluation=evaluation,
        A_hat=A_hat,
        pi_cand=pi_cand,
        beta=1.0,
        mode="gamma_zero",
        sigma_xi=0.0,
        L_z=0.5,
        n=2,
        alphas=[0.0, 1.0],
        decomp_bound=value_error,
    )
    require(bundle.certificates_hold, "gamma=0 centered CPI boundary failed")

    return {
        "boundaries": ["gamma=0", "K=1"],
        "advantage_error": advantage_error,
        "centering_defect": centering_defect,
        "residual": residual,
        "value_error": value_error,
    }


def build_clock_chain_mdp() -> certificate.FiniteMDP:
    """Build a three-step clock-complete MDP plus a zero-value absorber."""

    num_states = 4
    num_actions = 2
    P = [
        [certificate.zeros(num_states) for _ in range(num_actions)]
        for _ in range(num_states)
    ]
    for state in range(3):
        for action in range(num_actions):
            P[state][action][state + 1] = 1.0
    for action in range(num_actions):
        P[3][action][3] = 1.0

    rewards = [
        [1.0, -0.5],
        [0.25, 0.75],
        [-0.2, 0.4],
        [0.0, 0.0],
    ]
    policy = [
        [0.25, 0.75],
        [0.60, 0.40],
        [0.30, 0.70],
        [0.50, 0.50],
    ]
    return certificate.FiniteMDP(
        num_states=num_states,
        num_actions=num_actions,
        P=P,
        R=rewards,
        rho=[0.0, 0.0, 0.0, 1.0],
        pi=policy,
    )


def check_terminal_and_absorbing_boundaries() -> Dict[str, object]:
    """Check clock exhaustion, K beyond horizon, and absorbing initialization."""

    mdp = build_clock_chain_mdp()
    gamma = 0.9
    evaluation = certificate.exact_policy_evaluation(mdp, gamma=gamma, max_k=5)
    expected_rewards = [
        math.fsum(mdp.pi[state][action] * mdp.R[state][action] for action in range(2))
        for state in range(4)
    ]
    manual_value = [
        expected_rewards[0] + gamma * expected_rewards[1] + gamma**2 * expected_rewards[2],
        expected_rewards[1] + gamma * expected_rewards[2],
        expected_rewards[2],
        0.0,
    ]
    require_le(
        max_vector_difference(evaluation.V_pi, manual_value),
        ZERO_TOL,
        "manual finite-horizon value",
        tolerance=0.0,
    )
    require_close(evaluation.eta_pi, 0.0, "absorbing initial-state return")
    require_close(evaluation.V_pi[3], 0.0, "absorbing-state value")

    boundary_U = [7.0, -5.0, 3.0, 0.0]
    K_beyond_horizon = 5
    long_backup = evaluation.apply_k_step(boundary_U, K_beyond_horizon)
    require_le(
        max_vector_difference(long_backup, evaluation.V_pi),
        ZERO_TOL,
        "K beyond remaining horizon",
        tolerance=0.0,
    )
    for action in range(mdp.num_actions):
        require_close(
            evaluation.Q_pi[2][action],
            mdp.R[2][action],
            f"terminal action value action={action}",
        )
    require_close(
        evaluation.apply_k_step(boundary_U, 1)[2],
        expected_rewards[2],
        "terminal backup has no continuation leakage",
    )
    require_close(
        evaluation.apply_k_step(boundary_U, K_beyond_horizon)[3],
        0.0,
        "absorbing K-step backup",
    )

    bad_absorbing_value = [0.0, 0.0, 0.0, 1.0]
    bad_absorbing_backup = evaluation.apply_k_step(
        bad_absorbing_value,
        K_beyond_horizon,
    )
    absorbing_residual = abs(
        bad_absorbing_value[3] - bad_absorbing_backup[3]
    )
    absorbing_error = abs(bad_absorbing_value[3] - evaluation.V_pi[3])
    absorbing_residual_bound = absorbing_residual / (1.0 - gamma**K_beyond_horizon)
    require_close(
        absorbing_error,
        absorbing_residual_bound,
        "absorbing boundary residual certificate",
    )
    global_residual = max_vector_difference(
        bad_absorbing_value,
        bad_absorbing_backup,
    )
    global_error = max_vector_difference(bad_absorbing_value, evaluation.V_pi)
    require_le(
        global_error,
        global_residual / (1.0 - gamma**K_beyond_horizon),
        "global residual certificate with incorrect absorbing value",
    )

    return {
        "boundaries": [
            "K beyond remaining finite horizon",
            "absorbing initial state",
            "absorbing boundary",
            "terminal boundary",
        ],
        "K": K_beyond_horizon,
        "absorbing_initial_eta": evaluation.eta_pi,
        "absorbing_residual_bound": absorbing_residual_bound,
        "global_residual_bound_with_bad_absorber": global_residual
        / (1.0 - gamma**K_beyond_horizon),
        "manual_value_max_error": max_vector_difference(evaluation.V_pi, manual_value),
        "terminal_backup_error": abs(
            evaluation.apply_k_step(boundary_U, 1)[2] - expected_rewards[2]
        ),
    }


def check_primary_csv(csv_path: Path) -> Dict[str, object]:
    """Verify the retained 80+21 row artifact and its displayed inequalities."""

    payload = csv_path.read_bytes()
    with csv_path.open("r", encoding="ascii", newline="") as handle:
        rows = list(csv.DictReader(handle))
    value_rows = [row for row in rows if row["record_type"] == "value_curve"]
    cpi_rows = [row for row in rows if row["record_type"] == "cpi_curve"]
    require(len(rows) == 101, f"primary CSV row count changed: {len(rows)}")
    require(len(value_rows) == 80, f"value row count changed: {len(value_rows)}")
    require(len(cpi_rows) == 21, f"CPI row count changed: {len(cpi_rows)}")

    worst_decomposition_margin = -math.inf
    worst_residual_margin = -math.inf
    worst_advantage_margin = -math.inf
    worst_cpi_decomposition_margin = -math.inf
    worst_cpi_exact_margin = -math.inf
    for row in rows:
        value_error = float(row["value_error"])
        decomposition_bound = float(row["decomposition_bound"])
        residual_bound = float(row["finite_depth_residual_bound"])
        worst_decomposition_margin = max(
            worst_decomposition_margin,
            value_error - decomposition_bound,
        )
        worst_residual_margin = max(worst_residual_margin, value_error - residual_bound)
        require_le(value_error, decomposition_bound, "CSV finite-reference decomposition")
        require_le(value_error, residual_bound, "CSV residual-to-value")
        require(row["certificate_holds_decomp"] == "1", "CSV decomposition flag is false")
        require(row["certificate_holds_exact_A"] == "1", "CSV exact-A flag is false")

        if row["record_type"] == "cpi_curve":
            advantage_margin = float(row["eps_A_cand"]) - float(row["eps_A_bound"])
            surrogate_gap = float(row["Lhat_pi_alpha"]) - float(row["eta_pi_alpha"])
            cpi_decomposition_margin = surrogate_gap - float(row["penalty_decomp"])
            cpi_exact_margin = surrogate_gap - float(row["penalty_exact_A"])
            worst_advantage_margin = max(worst_advantage_margin, advantage_margin)
            worst_cpi_decomposition_margin = max(
                worst_cpi_decomposition_margin,
                cpi_decomposition_margin,
            )
            worst_cpi_exact_margin = max(worst_cpi_exact_margin, cpi_exact_margin)
            require_le(float(row["eps_A_cand"]), float(row["eps_A_bound"]), "CSV candidate bias")
            require_le(surrogate_gap, float(row["penalty_decomp"]), "CSV centered CPI decomposition")
            require_le(surrogate_gap, float(row["penalty_exact_A"]), "CSV centered CPI exact bias")

    alpha_values = sorted(float(row["alpha"]) for row in cpi_rows)
    require_close(alpha_values[0], 0.0, "CSV alpha=0 boundary")
    require_close(alpha_values[-1], 1.0, "CSV alpha=1 boundary")

    return {
        "boundaries": ["alpha=0", "alpha=1"],
        "cpi_rows": len(cpi_rows),
        "csv_sha256": hashlib.sha256(payload).hexdigest(),
        "total_rows": len(rows),
        "value_rows": len(value_rows),
        "worst_advantage_margin": worst_advantage_margin,
        "worst_centered_cpi_decomposition_margin": worst_cpi_decomposition_margin,
        "worst_centered_cpi_exact_bias_margin": worst_cpi_exact_margin,
        "worst_finite_reference_margin": worst_decomposition_margin,
        "worst_residual_to_value_margin": worst_residual_margin,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--primary-csv",
        type=Path,
        default=Path("results/finite_mdp_certificate_validation/finite_mdp_summary.csv"),
        help="The retained 101-row primary artifact.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Machine-readable JSON output path.",
    )
    args = parser.parse_args()

    checks: Mapping[str, Callable[[], Dict[str, object]]] = {
        "advantage_candidate_centered_cpi_and_exact_mixture": check_advantage_candidate_and_cpi,
        "depth_boundaries": check_depth_boundaries,
        "gamma_zero": check_gamma_zero,
        "one_step_and_zero_residual": check_one_step_and_zero_residual,
        "primary_101_row_contract": lambda: check_primary_csv(args.primary_csv),
        "terminal_and_absorbing_boundaries": check_terminal_and_absorbing_boundaries,
        "zero_advantage_error": check_zero_advantage_error,
    }
    results: List[Dict[str, object]] = []
    for name in sorted(checks):
        try:
            metrics = checks[name]()
            results.append({"name": name, "status": "passed", "metrics": metrics})
            print(f"PASS {name}")
        except Exception as error:  # Retain every failure in the machine-readable result.
            results.append(
                {
                    "name": name,
                    "status": "failed",
                    "error_type": type(error).__name__,
                    "error": str(error),
                }
            )
            print(f"FAIL {name}: {type(error).__name__}: {error}")

    failed = [result for result in results if result["status"] != "passed"]
    output = {
        "all_passed": not failed,
        "check_count": len(results),
        "failed_count": len(failed),
        "results": results,
        "schema_version": 1,
        "suite": "finite_mdp_theorem_pipeline_boundary_checks",
        "tolerances": {
            "inequality": TEST_TOL,
            "numerical_zero": ZERO_TOL,
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print(
        f"RESULT checks={len(results)} passed={len(results) - len(failed)} "
        f"failed={len(failed)} output={args.out}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
