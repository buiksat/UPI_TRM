#!/usr/bin/env python3
"""Fixed exact bridge from evaluator residuals to policy improvement.

The explicit case registry below is evaluated in full.  It includes
positive, null, negative, non-vacuous, and vacuous outcomes.  All calculations
use fractions.Fraction through an exact finite-MDP oracle; no case is selected
or removed by the script after evaluation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from corollary_6_2_exact_checks import (
    CheckBook,
    ExactMDP,
    _bellman_backup,
    _centered_advantage,
    _discounted_occupancy,
    _fraction_text,
    _matrix_sup_abs,
    _matrix_text,
    _mix_policy,
    _policy_evaluation,
    _sup_abs,
    _vector_text,
    _zero_matrix,
)


GAMMA = Fraction(1, 2)
K_STEPS = 1
BASE_CORRECT_EDIT_PROBABILITY = Fraction(1, 4)
TERMINAL_SUCCESS_REWARD = Fraction(4)


@dataclass(frozen=True)
class BridgeCase:
    name: str
    alpha: Fraction
    evaluator_error: Fraction
    candidate_correct_edit_probability: Fraction
    expected_pipeline_status: str
    expected_actual_outcome: str


# This is the current hand-constructed case registry.  Expected outcome labels
# are encoded here, and every listed case is emitted after evaluation.
CASES: tuple[BridgeCase, ...] = (
    BridgeCase(
        name="zero_residual_positive",
        alpha=Fraction(1, 20),
        evaluator_error=Fraction(0),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="positive",
        expected_actual_outcome="positive",
    ),
    BridgeCase(
        name="small_residual_positive",
        alpha=Fraction(1, 100),
        evaluator_error=Fraction(1, 100),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="positive",
        expected_actual_outcome="positive",
    ),
    BridgeCase(
        name="moderate_residual_positive",
        alpha=Fraction(1, 100),
        evaluator_error=Fraction(1, 10),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="positive",
        expected_actual_outcome="positive",
    ),
    BridgeCase(
        name="residual_bridge_vacuous_exact_bias_positive",
        alpha=Fraction(1, 100),
        evaluator_error=Fraction(1, 2),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="vacuous",
        expected_actual_outcome="positive",
    ),
    BridgeCase(
        name="large_alpha_boundary_vacuous",
        alpha=Fraction(1, 4),
        evaluator_error=Fraction(0),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="vacuous",
        expected_actual_outcome="positive",
    ),
    BridgeCase(
        name="smaller_candidate_bias_positive",
        alpha=Fraction(1, 100),
        evaluator_error=Fraction(1, 100),
        candidate_correct_edit_probability=Fraction(1, 2),
        expected_pipeline_status="positive",
        expected_actual_outcome="positive",
    ),
    BridgeCase(
        name="null_candidate_with_residual",
        alpha=Fraction(1, 2),
        evaluator_error=Fraction(1, 2),
        candidate_correct_edit_probability=Fraction(1, 4),
        expected_pipeline_status="vacuous",
        expected_actual_outcome="null",
    ),
    BridgeCase(
        name="unfavorable_candidate_retained",
        alpha=Fraction(1, 10),
        evaluator_error=Fraction(1, 10),
        candidate_correct_edit_probability=Fraction(0),
        expected_pipeline_status="vacuous",
        expected_actual_outcome="negative",
    ),
    BridgeCase(
        name="alpha_zero_control",
        alpha=Fraction(0),
        evaluator_error=Fraction(1),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="vacuous",
        expected_actual_outcome="null",
    ),
    BridgeCase(
        name="large_residual_positive_but_pipeline_vacuous",
        alpha=Fraction(1, 100),
        evaluator_error=Fraction(2),
        candidate_correct_edit_probability=Fraction(3, 4),
        expected_pipeline_status="vacuous",
        expected_actual_outcome="positive",
    ),
)


def _case_registry_payload() -> list[dict[str, object]]:
    return [
        {
            "name": case.name,
            "alpha": _fraction_text(case.alpha),
            "evaluator_error": _fraction_text(case.evaluator_error),
            "candidate_correct_edit_probability": _fraction_text(
                case.candidate_correct_edit_probability
            ),
            "expected_pipeline_status": case.expected_pipeline_status,
            "expected_actual_outcome": case.expected_actual_outcome,
        }
        for case in CASES
    ]


def _case_registry_sha256() -> str:
    encoded = json.dumps(
        _case_registry_payload(), sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _build_plan_edit_mdp() -> ExactMDP:
    # The clock is explicit in each nonabsorbing state name.  At h=2, action 1
    # makes the correct edit and action 0 leaves the plan unsolved.  At h=1,
    # either action terminates in the same absorber; only the correctly edited
    # state receives the terminal checker reward.
    states = ("start_h2", "correct_h1", "unsolved_h1", "absorbing_h0")
    transition = [
        [
            [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
        ],
        [
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
        ],
        [
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
        ],
        [
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
        ],
    ]
    reward = _zero_matrix(len(states), 2)
    reward[1] = [TERMINAL_SUCCESS_REWARD, TERMINAL_SUCCESS_REWARD]
    return ExactMDP(
        states=states,
        num_actions=2,
        transition=transition,
        reward=reward,
        initial=[Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
    )


def _stage_policy(correct_edit_probability: Fraction) -> list[list[Fraction]]:
    return [
        [Fraction(1) - correct_edit_probability, correct_edit_probability],
        [Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0)],
    ]


def _outcome(change: Fraction) -> str:
    if change > 0:
        return "positive"
    if change < 0:
        return "negative"
    return "null"


def _candidate_bias(
    candidate: Sequence[Sequence[Fraction]],
    estimated_advantage: Sequence[Sequence[Fraction]],
    true_advantage: Sequence[Sequence[Fraction]],
) -> Fraction:
    return max(
        abs(
            sum(
                candidate[state][action]
                * (
                    estimated_advantage[state][action]
                    - true_advantage[state][action]
                )
                for action in range(len(candidate[state]))
            )
        )
        for state in range(len(candidate))
    )


def _epsilon_cpi(
    candidate: Sequence[Sequence[Fraction]],
    true_advantage: Sequence[Sequence[Fraction]],
) -> Fraction:
    return max(
        abs(
            sum(
                candidate[state][action] * true_advantage[state][action]
                for action in range(len(candidate[state]))
            )
        )
        for state in range(len(candidate))
    )


def _evaluate_case(
    checks: CheckBook,
    mdp: ExactMDP,
    base: list[list[Fraction]],
    base_value: list[Fraction],
    base_advantage: list[list[Fraction]],
    eta_base: Fraction,
    base_occupancy: list[Fraction],
    case: BridgeCase,
) -> dict[str, object]:
    candidate = _stage_policy(case.candidate_correct_edit_probability)
    mixture = _mix_policy(base, candidate, case.alpha)
    for state, row in enumerate(mixture):
        checks.equal(sum(row), Fraction(1), f"{case.name}: mixture state {state}")
        checks.require(
            all(probability >= 0 for probability in row),
            f"{case.name}: negative mixture probability at state {state}",
        )

    # Choose U(start_h2) to satisfy its base-policy Bellman equation.  The only
    # evaluator error is at correct_h1, so its magnitude is also the exact
    # full-closure one-step residual.
    evaluator = [
        GAMMA
        * BASE_CORRECT_EDIT_PROBABILITY
        * (TERMINAL_SUCCESS_REWARD + case.evaluator_error),
        TERMINAL_SUCCESS_REWARD + case.evaluator_error,
        Fraction(0),
        Fraction(0),
    ]
    backed_up = _bellman_backup(mdp, base, GAMMA, evaluator)
    residual_by_state = [
        abs(left - right) for left, right in zip(evaluator, backed_up)
    ]
    value_error_by_state = [
        abs(left - right) for left, right in zip(evaluator, base_value)
    ]
    residual = _sup_abs(residual_by_state)
    value_error = _sup_abs(value_error_by_state)
    value_certificate = residual / (Fraction(1) - GAMMA**K_STEPS)
    checks.equal(residual, case.evaluator_error, f"{case.name}: residual magnitude")
    checks.equal(value_error, case.evaluator_error, f"{case.name}: value error")
    checks.less_equal(value_error, value_certificate, f"{case.name}: value certificate")

    _q_hat, estimated_advantage = _centered_advantage(
        mdp, base, GAMMA, evaluator
    )
    for state in range(len(mdp.states)):
        centering = sum(
            base[state][action] * estimated_advantage[state][action]
            for action in range(mdp.num_actions)
        )
        checks.equal(centering, Fraction(0), f"{case.name}: centering state {state}")
    advantage_error_matrix = [
        [
            estimated_advantage[state][action]
            - base_advantage[state][action]
            for action in range(mdp.num_actions)
        ]
        for state in range(len(mdp.states))
    ]
    advantage_error = _matrix_sup_abs(advantage_error_matrix)
    advantage_bound_from_value = 2 * GAMMA * value_error
    advantage_bound_from_residual = 2 * GAMMA * value_certificate
    checks.less_equal(
        advantage_error,
        advantage_bound_from_value,
        f"{case.name}: value-to-advantage bound",
    )
    checks.less_equal(
        advantage_error,
        advantage_bound_from_residual,
        f"{case.name}: residual-to-advantage bound",
    )

    candidate_bias = _candidate_bias(
        candidate, estimated_advantage, base_advantage
    )
    epsilon_cpi = _epsilon_cpi(candidate, base_advantage)
    checks.less_equal(
        candidate_bias,
        advantage_error,
        f"{case.name}: candidate bias versus uniform error",
    )
    checks.less_equal(
        candidate_bias,
        advantage_bound_from_residual,
        f"{case.name}: candidate bias versus residual bound",
    )

    _mixed_value, _mixed_q, _mixed_advantage, eta_mixture = _policy_evaluation(
        mdp, mixture, GAMMA
    )
    actual_change = eta_mixture - eta_base
    estimated_expectation = sum(
        base_occupancy[state]
        * sum(
            mixture[state][action] * estimated_advantage[state][action]
            for action in range(mdp.num_actions)
        )
        for state in range(len(mdp.states))
    )
    estimated_surrogate = (
        eta_base + estimated_expectation / (Fraction(1) - GAMMA)
    )
    quadratic_penalty = (
        2
        * epsilon_cpi
        * GAMMA
        * case.alpha**2
        / (Fraction(1) - GAMMA) ** 2
    )
    exact_bias_linear_penalty = (
        case.alpha * candidate_bias / (Fraction(1) - GAMMA)
    )
    residual_linear_penalty = (
        case.alpha * advantage_bound_from_residual / (Fraction(1) - GAMMA)
    )
    exact_bias_lower_bound = (
        estimated_surrogate - exact_bias_linear_penalty - quadratic_penalty
    )
    residual_pipeline_lower_bound = (
        estimated_surrogate - residual_linear_penalty - quadratic_penalty
    )
    exact_bias_slack = eta_mixture - exact_bias_lower_bound
    residual_pipeline_slack = eta_mixture - residual_pipeline_lower_bound
    checks.less_equal(
        exact_bias_lower_bound,
        eta_mixture,
        f"{case.name}: exact-bias CPI bound",
    )
    checks.less_equal(
        residual_pipeline_lower_bound,
        eta_mixture,
        f"{case.name}: residual-pipeline CPI bound",
    )
    checks.require(exact_bias_slack >= 0, f"{case.name}: exact-bias slack")
    checks.require(
        residual_pipeline_slack >= 0,
        f"{case.name}: residual-pipeline slack",
    )

    pipeline_status = (
        "positive" if residual_pipeline_lower_bound > eta_base else "vacuous"
    )
    exact_bias_status = (
        "positive" if exact_bias_lower_bound > eta_base else "vacuous"
    )
    actual_outcome = _outcome(actual_change)
    checks.equal(
        pipeline_status,
        case.expected_pipeline_status,
        f"{case.name}: expected pipeline status",
    )
    checks.equal(
        actual_outcome,
        case.expected_actual_outcome,
        f"{case.name}: expected actual outcome",
    )

    return {
        "name": case.name,
        "included_in_explicit_case_registry": True,
        "alpha": _fraction_text(case.alpha),
        "evaluator_error_parameter": _fraction_text(case.evaluator_error),
        "candidate_correct_edit_probability": _fraction_text(
            case.candidate_correct_edit_probability
        ),
        "base_value": _vector_text(base_value),
        "base_advantage": _matrix_text(base_advantage),
        "evaluator": _vector_text(evaluator),
        "bellman_backup": _vector_text(backed_up),
        "evaluator_residual_by_state": _vector_text(residual_by_state),
        "evaluator_residual_sup": _fraction_text(residual),
        "actual_value_error_by_state": _vector_text(value_error_by_state),
        "actual_value_error_sup": _fraction_text(value_error),
        "residual_value_certificate": _fraction_text(value_certificate),
        "estimated_advantage": _matrix_text(estimated_advantage),
        "advantage_error": _matrix_text(advantage_error_matrix),
        "actual_advantage_error_sup": _fraction_text(advantage_error),
        "value_derived_advantage_bound": _fraction_text(
            advantage_bound_from_value
        ),
        "residual_derived_advantage_bound": _fraction_text(
            advantage_bound_from_residual
        ),
        "candidate_bias": _fraction_text(candidate_bias),
        "epsilon_cpi": _fraction_text(epsilon_cpi),
        "exact_pointwise_mixture": _matrix_text(mixture),
        "base_performance": _fraction_text(eta_base),
        "mixture_performance": _fraction_text(eta_mixture),
        "actual_performance_change": _fraction_text(actual_change),
        "actual_outcome": actual_outcome,
        "estimated_surrogate": _fraction_text(estimated_surrogate),
        "estimated_surrogate_change": _fraction_text(
            estimated_surrogate - eta_base
        ),
        "quadratic_cpi_penalty": _fraction_text(quadratic_penalty),
        "exact_candidate_bias_linear_penalty": _fraction_text(
            exact_bias_linear_penalty
        ),
        "exact_candidate_bias_cpi_lower_bound": _fraction_text(
            exact_bias_lower_bound
        ),
        "exact_candidate_bias_cpi_lower_bound_change": _fraction_text(
            exact_bias_lower_bound - eta_base
        ),
        "exact_candidate_bias_certificate_status": exact_bias_status,
        "exact_candidate_bias_slack": _fraction_text(exact_bias_slack),
        "residual_pipeline_linear_penalty": _fraction_text(
            residual_linear_penalty
        ),
        "cpi_lower_bound": _fraction_text(residual_pipeline_lower_bound),
        "cpi_lower_bound_change": _fraction_text(
            residual_pipeline_lower_bound - eta_base
        ),
        "certificate_positive": pipeline_status == "positive",
        "certificate_vacuous": pipeline_status == "vacuous",
        "certificate_status": pipeline_status,
        "certificate_slack": _fraction_text(residual_pipeline_slack),
        "unfavorable_or_null_retained": actual_outcome in {"negative", "null"},
    }


def run() -> dict[str, object]:
    checks = CheckBook()
    mdp = _build_plan_edit_mdp()
    mdp.validate(checks)
    base = _stage_policy(BASE_CORRECT_EDIT_PROBABILITY)
    base_value, _base_q, base_advantage, eta_base = _policy_evaluation(
        mdp, base, GAMMA
    )
    base_occupancy = _discounted_occupancy(mdp, base, GAMMA)

    checks.equal(
        base_value,
        [Fraction(1, 2), Fraction(4), Fraction(0), Fraction(0)],
        "base value oracle",
    )
    checks.equal(eta_base, Fraction(1, 2), "base performance oracle")
    checks.equal(sum(base_occupancy), Fraction(1), "discounted occupancy normalization")

    results = [
        _evaluate_case(
            checks,
            mdp,
            base,
            base_value,
            base_advantage,
            eta_base,
            base_occupancy,
            case,
        )
        for case in CASES
    ]
    positive_certificates = sum(
        result["certificate_status"] == "positive" for result in results
    )
    vacuous_certificates = sum(
        result["certificate_status"] == "vacuous" for result in results
    )
    actual_counts = {
        outcome: sum(result["actual_outcome"] == outcome for result in results)
        for outcome in ("positive", "null", "negative")
    }
    checks.require(positive_certificates > 0, "missing non-vacuous certificate")
    checks.require(vacuous_certificates > 0, "missing vacuous certificate")
    checks.require(actual_counts["null"] > 0, "missing retained null outcome")
    checks.require(actual_counts["negative"] > 0, "missing retained negative outcome")

    return {
        "schema_version": 1,
        "suite": "fixed_exact_finite_plan_edit_theory_outcome_bridge",
        "arithmetic": "fractions.Fraction",
        "selection_rule": (
            "current hand-constructed source registry; every listed case evaluated; "
            "expected outcome labels encoded in source"
        ),
        "case_registry_sha256": _case_registry_sha256(),
        "case_registry": _case_registry_payload(),
        "all_passed": True,
        "check_count": checks.count,
        "case_count": len(results),
        "positive_certificate_count": positive_certificates,
        "vacuous_certificate_count": vacuous_certificates,
        "actual_outcome_counts": actual_counts,
        "mdp": {
            "states": list(mdp.states),
            "actions": ["leave_unsolved_or_stop", "make_correct_edit_or_stop"],
            "gamma": _fraction_text(GAMMA),
            "K": K_STEPS,
            "base_correct_edit_probability": _fraction_text(
                BASE_CORRECT_EDIT_PROBABILITY
            ),
            "terminal_success_reward": _fraction_text(TERMINAL_SUCCESS_REWARD),
            "base_policy": _matrix_text(base),
            "base_discounted_occupancy": _vector_text(base_occupancy),
            "absorbing_boundary": "shared zero-valued absorbing_h0 state",
        },
        "cases": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = run()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="ascii")
    print(
        f"PASS {payload['suite']}: {payload['check_count']} exact checks, "
        f"{payload['positive_certificate_count']} positive certificates, "
        f"{payload['vacuous_certificate_count']} vacuous; output={args.output}"
    )


if __name__ == "__main__":
    main()
