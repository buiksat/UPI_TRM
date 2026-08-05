#!/usr/bin/env python3
"""Independent exact-arithmetic checks for the finite-depth residual chain.

This regression uses only the Python standard library.  It does not import the
finite-MDP implementation used to generate the manuscript figures.  Rational
arithmetic pins the residual, value, advantage, candidate-bias, and CPI
constants without numerical tolerances.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Callable, Sequence


Scalar = Fraction
Vector = list[Scalar]
Matrix = list[Vector]
Tensor3 = list[Matrix]


def _fraction_text(value: Scalar) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _vector_text(values: Sequence[Scalar]) -> list[str]:
    return [_fraction_text(value) for value in values]


def _matrix_text(values: Sequence[Sequence[Scalar]]) -> list[list[str]]:
    return [_vector_text(row) for row in values]


@dataclass
class CheckBook:
    count: int = 0

    def require(self, condition: bool, message: str) -> None:
        self.count += 1
        if not condition:
            raise AssertionError(message)

    def equal(self, actual: object, expected: object, message: str) -> None:
        self.require(actual == expected, f"{message}: actual={actual!r}, expected={expected!r}")

    def less(self, left: Scalar, right: Scalar, message: str) -> None:
        self.require(left < right, f"{message}: left={left}, right={right}")

    def less_equal(self, left: Scalar, right: Scalar, message: str) -> None:
        self.require(left <= right, f"{message}: left={left}, right={right}")


@dataclass(frozen=True)
class ExactMDP:
    states: tuple[str, ...]
    num_actions: int
    transition: Tensor3
    reward: Matrix
    initial: Vector

    def validate(self, checks: CheckBook) -> None:
        checks.equal(len(self.transition), len(self.states), "transition state count")
        checks.equal(len(self.reward), len(self.states), "reward state count")
        checks.equal(len(self.initial), len(self.states), "initial state count")
        checks.equal(sum(self.initial), Fraction(1), "initial distribution normalization")
        for state, action_rows in enumerate(self.transition):
            checks.equal(len(action_rows), self.num_actions, f"action count at state {state}")
            checks.equal(len(self.reward[state]), self.num_actions, f"reward action count at state {state}")
            for action, row in enumerate(action_rows):
                checks.equal(len(row), len(self.states), f"successor count at ({state}, {action})")
                checks.equal(sum(row), Fraction(1), f"transition normalization at ({state}, {action})")


def _zero_matrix(rows: int, columns: int) -> Matrix:
    return [[Fraction(0) for _ in range(columns)] for _ in range(rows)]


def _solve_linear_exact(matrix: Matrix, rhs: Vector) -> Vector:
    """Solve a nonsingular linear system by exact Gauss-Jordan elimination."""

    size = len(rhs)
    augmented = [matrix[row][:] + [rhs[row]] for row in range(size)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column] != 0),
            None,
        )
        if pivot is None:
            raise ValueError("singular exact linear system")
        if pivot != column:
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]

        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            augmented[row] = [
                current - factor * pivot_entry
                for current, pivot_entry in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(size)]


def _policy_dynamics(mdp: ExactMDP, policy: Matrix) -> tuple[Matrix, Vector]:
    size = len(mdp.states)
    transition = _zero_matrix(size, size)
    reward = [Fraction(0) for _ in range(size)]
    for state in range(size):
        for action in range(mdp.num_actions):
            probability = policy[state][action]
            reward[state] += probability * mdp.reward[state][action]
            for successor in range(size):
                transition[state][successor] += (
                    probability * mdp.transition[state][action][successor]
                )
    return transition, reward


def _policy_evaluation(
    mdp: ExactMDP,
    policy: Matrix,
    gamma: Scalar,
) -> tuple[Vector, Matrix, Matrix, Scalar]:
    transition, reward = _policy_dynamics(mdp, policy)
    size = len(mdp.states)
    system = [
        [
            (Fraction(1) if row == column else Fraction(0))
            - gamma * transition[row][column]
            for column in range(size)
        ]
        for row in range(size)
    ]
    value = _solve_linear_exact(system, reward)
    action_value = _zero_matrix(size, mdp.num_actions)
    advantage = _zero_matrix(size, mdp.num_actions)
    for state in range(size):
        for action in range(mdp.num_actions):
            continuation = sum(
                probability * value[successor]
                for successor, probability in enumerate(
                    mdp.transition[state][action]
                )
            )
            action_value[state][action] = mdp.reward[state][action] + gamma * continuation
            advantage[state][action] = action_value[state][action] - value[state]
    performance = sum(
        probability * value[state]
        for state, probability in enumerate(mdp.initial)
    )
    return value, action_value, advantage, performance


def _discounted_occupancy(mdp: ExactMDP, policy: Matrix, gamma: Scalar) -> Vector:
    transition, _reward = _policy_dynamics(mdp, policy)
    size = len(mdp.states)
    system = [
        [
            (Fraction(1) if row == column else Fraction(0))
            - gamma * transition[column][row]
            for column in range(size)
        ]
        for row in range(size)
    ]
    rhs = [(Fraction(1) - gamma) * probability for probability in mdp.initial]
    return _solve_linear_exact(system, rhs)


def _bellman_backup(
    mdp: ExactMDP,
    policy: Matrix,
    gamma: Scalar,
    value: Vector,
) -> Vector:
    transition, reward = _policy_dynamics(mdp, policy)
    return [
        reward[state]
        + gamma
        * sum(
            transition[state][successor] * value[successor]
            for successor in range(len(mdp.states))
        )
        for state in range(len(mdp.states))
    ]


def _k_step_bellman_backup(
    mdp: ExactMDP,
    policy: Matrix,
    gamma: Scalar,
    value: Vector,
    steps: int,
) -> Vector:
    backed_up = value[:]
    for _ in range(steps):
        backed_up = _bellman_backup(mdp, policy, gamma, backed_up)
    return backed_up


def _centered_advantage(
    mdp: ExactMDP,
    policy: Matrix,
    gamma: Scalar,
    evaluator: Vector,
) -> tuple[Matrix, Matrix]:
    q_hat = _zero_matrix(len(mdp.states), mdp.num_actions)
    advantage_hat = _zero_matrix(len(mdp.states), mdp.num_actions)
    for state in range(len(mdp.states)):
        for action in range(mdp.num_actions):
            continuation = sum(
                probability * evaluator[successor]
                for successor, probability in enumerate(
                    mdp.transition[state][action]
                )
            )
            q_hat[state][action] = mdp.reward[state][action] + gamma * continuation
        baseline = sum(
            policy[state][action] * q_hat[state][action]
            for action in range(mdp.num_actions)
        )
        advantage_hat[state] = [value - baseline for value in q_hat[state]]
    return q_hat, advantage_hat


def _sup_abs(values: Sequence[Scalar]) -> Scalar:
    return max(abs(value) for value in values)


def _matrix_sup_abs(values: Sequence[Sequence[Scalar]]) -> Scalar:
    return max(abs(value) for row in values for value in row)


def _mix_policy(base: Matrix, candidate: Matrix, alpha: Scalar) -> Matrix:
    return [
        [
            (Fraction(1) - alpha) * base_probability
            + alpha * candidate_probability
            for base_probability, candidate_probability in zip(base_row, candidate_row)
        ]
        for base_row, candidate_row in zip(base, candidate)
    ]


def _build_candidate_successor_mdp() -> tuple[ExactMDP, Matrix, Matrix]:
    # State 0 is retained forever by the base policy.  Candidate action 1
    # reaches state 1, so state 1 belongs to the advantage-evaluation closure
    # even though it is absent from the ordinary base reachable set.  State 2
    # is the shared zero-valued absorber.
    states = ("base", "candidate_only", "absorbing")
    transition: Tensor3 = [
        [
            [Fraction(1), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0)],
        ],
        [
            [Fraction(0), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0)],
        ],
        [
            [Fraction(0), Fraction(0), Fraction(1)],
            [Fraction(0), Fraction(0), Fraction(1)],
        ],
    ]
    reward = _zero_matrix(len(states), 2)
    mdp = ExactMDP(
        states=states,
        num_actions=2,
        transition=transition,
        reward=reward,
        initial=[Fraction(1), Fraction(0), Fraction(0)],
    )
    base = [
        [Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0)],
    ]
    candidate = [
        [Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0)],
    ]
    return mdp, base, candidate


def _check_unbounded_countable_counterexample(checks: CheckBook) -> dict[str, object]:
    gamma = Fraction(1, 2)
    tested_k = (1, 2, 3, 5, 8)
    sampled_indices = tuple(range(7))
    rows: list[dict[str, object]] = []
    for steps in tested_k:
        residuals: list[Scalar] = []
        for index in sampled_indices:
            value = Fraction(2**index)
            backed_up = gamma**steps * Fraction(2 ** (index + steps))
            checks.equal(backed_up, value, f"unbounded chain fixed point K={steps}, i={index}")
            residuals.append(abs(value - backed_up))
        checks.equal(_sup_abs(residuals), Fraction(0), f"unbounded residual K={steps}")
        rows.append(
            {
                "K": steps,
                "sampled_residual_sup": _fraction_text(_sup_abs(residuals)),
                "operator_identity": "gamma^K U(s_{i+K}) = U(s_i)",
            }
        )
    checks.equal(Fraction(2 ** (sampled_indices[-1] + 1)), 2 * Fraction(2**sampled_indices[-1]), "unbounded geometric growth")
    return {
        "name": "unbounded_countable_chain_counterexample",
        "gamma": _fraction_text(gamma),
        "tested_K": list(tested_k),
        "sampled_indices": list(sampled_indices),
        "rows": rows,
        "residual_sup": "0",
        "value_error_sup": "infinity",
        "absorbing_atom": "unreachable zero-reward atom with U=V=0",
        "bounded_function_space_member": False,
        "disposition": "excluded by the bounded-evaluator premise",
    }


def _check_tight_one_state_certificate(checks: CheckBook) -> dict[str, object]:
    gamma = Fraction(1, 2)
    evaluator = Fraction(7, 3)
    tested_k = (1, 2, 4, 7)
    rows: list[dict[str, object]] = []
    for steps in tested_k:
        backed_up = gamma**steps * evaluator
        residual = abs(evaluator - backed_up)
        certificate = residual / (Fraction(1) - gamma**steps)
        checks.equal(certificate, abs(evaluator), f"tight one-state certificate K={steps}")
        rows.append(
            {
                "K": steps,
                "residual": _fraction_text(residual),
                "value_error": _fraction_text(abs(evaluator)),
                "certificate": _fraction_text(certificate),
                "equality": True,
            }
        )
    return {
        "name": "bounded_one_state_tight_residual_certificate",
        "gamma": _fraction_text(gamma),
        "evaluator": _fraction_text(evaluator),
        "rows": rows,
    }


def _check_bounded_countable_chain(checks: CheckBook) -> dict[str, object]:
    gamma = Fraction(1, 2)
    tested_k = (1, 2, 3, 4, 7, 8)
    sampled_indices = tuple(range(8))
    rows: list[dict[str, object]] = []
    for steps in tested_k:
        residuals: list[Scalar] = []
        for index in sampled_indices:
            evaluator = Fraction(-1 if index % 2 else 1)
            successor = Fraction(-1 if (index + steps) % 2 else 1)
            backed_up = gamma**steps * successor
            residuals.append(abs(evaluator - backed_up))
        analytic_residual = abs(Fraction(1) - Fraction((-1) ** steps) * gamma**steps)
        checks.equal(_sup_abs(residuals), analytic_residual, f"bounded chain residual K={steps}")
        certificate = analytic_residual / (Fraction(1) - gamma**steps)
        checks.less_equal(Fraction(1), certificate, f"bounded countable certificate K={steps}")
        if steps % 2 == 0:
            checks.equal(certificate, Fraction(1), f"bounded countable equality K={steps}")
        else:
            checks.less(Fraction(1), certificate, f"bounded countable strictness K={steps}")
        rows.append(
            {
                "K": steps,
                "residual_sup": _fraction_text(analytic_residual),
                "value_error_sup": "1",
                "certificate": _fraction_text(certificate),
                "relation": "equality" if steps % 2 == 0 else "strict",
            }
        )
    return {
        "name": "bounded_countable_chain_confirmation",
        "gamma": _fraction_text(gamma),
        "evaluator": "U(s_i)=(-1)^i",
        "bounded_function_space_member": True,
        "rows": rows,
    }


def _check_fraction_exact_oracle(checks: CheckBook) -> dict[str, object]:
    gamma = Fraction(1, 2)
    mdp, base, candidate = _build_candidate_successor_mdp()
    mdp.validate(checks)

    value, action_value, advantage, eta_base = _policy_evaluation(mdp, base, gamma)
    checks.equal(value, [Fraction(0)] * 3, "exact base value")
    checks.equal(action_value, _zero_matrix(3, 2), "exact action value")
    checks.equal(advantage, _zero_matrix(3, 2), "exact advantage")
    checks.equal(eta_base, Fraction(0), "exact base performance")

    evaluator = [Fraction(0), Fraction(2), Fraction(0)]
    backed_up = _k_step_bellman_backup(mdp, base, gamma, evaluator, 1)
    residual_by_state = [abs(left - right) for left, right in zip(evaluator, backed_up)]
    error_by_state = [abs(left - right) for left, right in zip(evaluator, value)]
    full_residual = _sup_abs(residual_by_state)
    full_value_error = _sup_abs(error_by_state)
    residual_certificate = full_residual / (Fraction(1) - gamma)
    residual_advantage_bound = 2 * gamma * residual_certificate
    checks.equal(full_residual, Fraction(1), "full-closure residual")
    checks.equal(full_value_error, Fraction(2), "full-closure value error")
    checks.equal(residual_certificate, full_value_error, "full-closure tight certificate")

    # The candidate-only successor is absent from R_pi but is required by the
    # one-deviation advantage closure.  Omitting it makes the restricted
    # residual zero even though the candidate action reads its evaluator error.
    base_and_absorber = (0, 2)
    restricted_residual = max(residual_by_state[state] for state in base_and_absorber)
    checks.equal(restricted_residual, Fraction(0), "base-only restricted residual")
    checks.require(
        mdp.transition[0][1][1] > 0 and base[0][1] == 0 and candidate[0][1] == 1,
        "state 1 must be a candidate-only one-step successor",
    )

    q_hat, advantage_hat = _centered_advantage(mdp, base, gamma, evaluator)
    for state in range(len(mdp.states)):
        centering = sum(
            base[state][action] * advantage_hat[state][action]
            for action in range(mdp.num_actions)
        )
        checks.equal(centering, Fraction(0), f"exact centering at state {state}")
    advantage_error = _matrix_sup_abs(
        [
            [
                advantage_hat[state][action] - advantage[state][action]
                for action in range(mdp.num_actions)
            ]
            for state in range(len(mdp.states))
        ]
    )
    checks.equal(q_hat[0][1], Fraction(1), "candidate-only successor Q estimate")
    checks.equal(advantage_hat[0][1], Fraction(1), "candidate-only successor advantage estimate")
    checks.equal(advantage_error, Fraction(1), "uniform advantage error")
    checks.less_equal(
        advantage_error,
        2 * gamma * full_value_error,
        "value-to-advantage bound",
    )
    checks.less_equal(
        advantage_error,
        residual_advantage_bound,
        "residual-derived advantage bound",
    )

    candidate_bias_by_state = [
        abs(
            sum(
                candidate[state][action]
                * (advantage_hat[state][action] - advantage[state][action])
                for action in range(mdp.num_actions)
            )
        )
        for state in range(len(mdp.states))
    ]
    candidate_bias = _sup_abs(candidate_bias_by_state)
    epsilon_cpi = max(
        abs(
            sum(
                candidate[state][action] * advantage[state][action]
                for action in range(mdp.num_actions)
            )
        )
        for state in range(len(mdp.states))
    )
    checks.equal(candidate_bias, Fraction(1), "candidate-policy bias")
    checks.equal(epsilon_cpi, Fraction(0), "CPI distribution-shift constant")

    occupancy = _discounted_occupancy(mdp, base, gamma)
    checks.equal(occupancy, [Fraction(1), Fraction(0), Fraction(0)], "base discounted occupancy")

    alpha_rows: list[dict[str, object]] = []
    for alpha in (Fraction(0), Fraction(1, 3), Fraction(1)):
        mixture = _mix_policy(base, candidate, alpha)
        for state, row in enumerate(mixture):
            checks.equal(sum(row), Fraction(1), f"mixture normalization alpha={alpha}, state={state}")
        _mixed_value, _mixed_q, _mixed_advantage, eta_mixture = _policy_evaluation(
            mdp, mixture, gamma
        )
        surrogate_expectation = sum(
            occupancy[state]
            * sum(
                mixture[state][action] * advantage_hat[state][action]
                for action in range(mdp.num_actions)
            )
            for state in range(len(mdp.states))
        )
        estimated_surrogate = eta_base + surrogate_expectation / (Fraction(1) - gamma)
        linear_penalty = alpha * candidate_bias / (Fraction(1) - gamma)
        quadratic_penalty = (
            2
            * epsilon_cpi
            * gamma
            * alpha**2
            / (Fraction(1) - gamma) ** 2
        )
        lower_bound = estimated_surrogate - linear_penalty - quadratic_penalty
        residual_linear_penalty = (
            alpha * residual_advantage_bound / (Fraction(1) - gamma)
        )
        residual_lower_bound = (
            estimated_surrogate - residual_linear_penalty - quadratic_penalty
        )
        checks.equal(eta_mixture, Fraction(0), f"exact mixture performance alpha={alpha}")
        checks.equal(estimated_surrogate, 2 * alpha, f"estimated surrogate alpha={alpha}")
        checks.equal(linear_penalty, 2 * alpha, f"linear CPI penalty alpha={alpha}")
        checks.equal(quadratic_penalty, Fraction(0), f"quadratic CPI penalty alpha={alpha}")
        checks.equal(lower_bound, eta_mixture, f"tight CPI lower bound alpha={alpha}")
        checks.equal(
            residual_linear_penalty,
            4 * alpha,
            f"residual-derived CPI penalty alpha={alpha}",
        )
        checks.less_equal(
            residual_lower_bound,
            eta_mixture,
            f"residual-derived CPI lower bound alpha={alpha}",
        )

        tightened_error = alpha * candidate_bias
        checks.less_equal(tightened_error, advantage_error, f"alpha tightening alpha={alpha}")
        relation = "equality" if alpha == 1 else "strict"
        if relation == "equality":
            checks.equal(tightened_error, advantage_error, "alpha=1 tightening equality")
        else:
            checks.less(tightened_error, advantage_error, f"alpha tightening strictness alpha={alpha}")
        residual_relation = "equality" if alpha == 0 else "strict"
        if residual_relation == "equality":
            checks.equal(residual_lower_bound, eta_mixture, "residual CPI equality at alpha=0")
        else:
            checks.less(residual_lower_bound, eta_mixture, f"residual CPI strictness alpha={alpha}")
        alpha_rows.append(
            {
                "alpha": _fraction_text(alpha),
                "policy_at_base_state": _vector_text(mixture[0]),
                "eta": _fraction_text(eta_mixture),
                "estimated_surrogate": _fraction_text(estimated_surrogate),
                "linear_penalty": _fraction_text(linear_penalty),
                "quadratic_penalty": _fraction_text(quadratic_penalty),
                "lower_bound": _fraction_text(lower_bound),
                "cpi_relation": "equality",
                "residual_derived_linear_penalty": _fraction_text(
                    residual_linear_penalty
                ),
                "residual_derived_lower_bound": _fraction_text(
                    residual_lower_bound
                ),
                "residual_derived_cpi_relation": residual_relation,
                "alpha_candidate_bias_vs_uniform_error": relation,
            }
        )

    # A cancellation case makes candidate bias strictly smaller than the
    # uniform error without changing the pointwise centering requirement.
    cancellation_errors = (Fraction(1), Fraction(-1))
    cancellation_candidate = (Fraction(1, 2), Fraction(1, 2))
    cancellation_bias = abs(
        sum(
            probability * error
            for probability, error in zip(cancellation_candidate, cancellation_errors)
        )
    )
    cancellation_uniform_error = max(abs(error) for error in cancellation_errors)
    checks.equal(cancellation_bias, Fraction(0), "candidate-bias cancellation")
    checks.less(cancellation_bias, cancellation_uniform_error, "strict candidate-bias tightening")

    return {
        "name": "fraction_exact_residual_advantage_candidate_bias_and_cpi_oracle",
        "gamma": _fraction_text(gamma),
        "states": list(mdp.states),
        "base_policy": _matrix_text(base),
        "candidate_policy": _matrix_text(candidate),
        "evaluator": _vector_text(evaluator),
        "true_value": _vector_text(value),
        "one_step_backup": _vector_text(backed_up),
        "residual_by_state": _vector_text(residual_by_state),
        "value_error_by_state": _vector_text(error_by_state),
        "full_closure_residual": _fraction_text(full_residual),
        "base_only_residual": _fraction_text(restricted_residual),
        "full_closure_value_error": _fraction_text(full_value_error),
        "residual_certificate": _fraction_text(residual_certificate),
        "advantage_hat": _matrix_text(advantage_hat),
        "uniform_advantage_error": _fraction_text(advantage_error),
        "value_derived_advantage_bound": _fraction_text(2 * gamma * full_value_error),
        "residual_derived_advantage_bound": _fraction_text(
            residual_advantage_bound
        ),
        "candidate_policy_bias": _fraction_text(candidate_bias),
        "epsilon_cpi": _fraction_text(epsilon_cpi),
        "candidate_only_successor": "candidate_only",
        "alpha_rows": alpha_rows,
        "cancellation_strictness_case": {
            "uniform_error": _fraction_text(cancellation_uniform_error),
            "candidate_bias": _fraction_text(cancellation_bias),
            "relation": "strict",
        },
    }


def run() -> dict[str, object]:
    checks = CheckBook()
    case_builders: tuple[Callable[[CheckBook], dict[str, object]], ...] = (
        _check_unbounded_countable_counterexample,
        _check_tight_one_state_certificate,
        _check_bounded_countable_chain,
        _check_fraction_exact_oracle,
    )
    cases = [builder(checks) for builder in case_builders]
    return {
        "schema_version": 1,
        "suite": "corollary_6_2_independent_exact_regression",
        "arithmetic": "fractions.Fraction",
        "all_passed": True,
        "check_count": checks.count,
        "case_count": len(cases),
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for deterministic JSON output.",
    )
    args = parser.parse_args()
    payload = run()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="ascii")
    print(
        f"PASS {payload['suite']}: {payload['check_count']} exact checks; "
        f"output={args.output}"
    )


if __name__ == "__main__":
    main()
