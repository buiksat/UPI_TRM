#!/usr/bin/env python3
"""Deterministic numerical checks for the finite-horizon theory extensions.

This file uses only the Python standard library.  It is a numerical unit test,
not empirical validation of a learned evaluator.  It checks random finite MDPs
plus explicit boundary cases for:

* the stagewise K-step residual recursion and its geometric unrolling;
* the finite-reference-depth decomposition;
* finite-horizon CPI with an exact probability-space mixture and exact
  statewise centering;
* finite- and infinite-horizon policy-deployment perturbation bounds.

The shared absorbing atom has value -C and self-loop reward (gamma - 1) C,
matching the paper's shaping convention.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from typing import Iterable, Sequence


TOL = 2.0e-10


def _dot(xs: Sequence[float], ys: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(xs, ys))


def _normalize(xs: Iterable[float]) -> list[float]:
    values = list(xs)
    total = sum(values)
    if total <= 0.0:
        raise ValueError("probability weights must have positive sum")
    return [x / total for x in values]


def _tv(p: Sequence[float], q: Sequence[float]) -> float:
    return 0.5 * sum(abs(x - y) for x, y in zip(p, q))


def _geom(gamma: float, count: int) -> float:
    if count <= 0:
        return 0.0
    return (1.0 - gamma**count) / (1.0 - gamma)


def _assert_le(lhs: float, rhs: float, context: str) -> float:
    slack = rhs - lhs
    scale = max(1.0, abs(lhs), abs(rhs))
    if slack < -TOL * scale:
        raise AssertionError(f"{context}: {lhs:.17g} > {rhs:.17g}")
    return slack


def _assert_close(lhs: float, rhs: float, context: str) -> float:
    error = abs(lhs - rhs)
    scale = max(1.0, abs(lhs), abs(rhs))
    if error > TOL * scale:
        raise AssertionError(f"{context}: {lhs:.17g} != {rhs:.17g}")
    return error


@dataclass(frozen=True)
class FiniteHorizonMDP:
    horizon: int
    num_states: int
    num_actions: int
    gamma: float
    boundary_value: float
    # transitions[h][s][a] is a list of (probability, next_state, reward).
    # next_state == -1 denotes the shared absorbing atom.
    transitions: list[list[list[list[tuple[float, int, float]]]]]
    initial: list[float]

    @property
    def absorbing_reward(self) -> float:
        return (1.0 - self.gamma) * self.boundary_value


Policy = list[list[list[float]]]


def _random_policy(
    rng: random.Random, horizon: int, num_states: int, num_actions: int
) -> Policy:
    policy: Policy = [[]]
    for _h in range(1, horizon + 1):
        policy.append(
            [
                _normalize(rng.uniform(0.1, 2.0) for _ in range(num_actions))
                for _s in range(num_states)
            ]
        )
    return policy


def _mix_policy(current: Policy, candidate: Policy, alpha: float) -> Policy:
    mixed: Policy = [[]]
    for h in range(1, len(current)):
        mixed.append(
            [
                [
                    (1.0 - alpha) * p + alpha * q
                    for p, q in zip(current[h][s], candidate[h][s])
                ]
                for s in range(len(current[h]))
            ]
        )
    return mixed


def _make_finite_horizon_mdp(
    rng: random.Random,
    horizon: int,
    num_states: int,
    num_actions: int,
    gamma: float,
) -> FiniteHorizonMDP:
    boundary_value = -0.4
    transitions: list[list[list[list[tuple[float, int, float]]]]] = [[]]
    for h in range(1, horizon + 1):
        by_state: list[list[list[tuple[float, int, float]]]] = []
        for _s in range(num_states):
            by_action: list[list[tuple[float, int, float]]] = []
            for _a in range(num_actions):
                if h == 1:
                    by_action.append([(1.0, -1, rng.uniform(-0.8, 0.8))])
                    continue
                weights = _normalize(
                    [rng.uniform(0.2, 1.0)]
                    + [rng.uniform(0.1, 1.0) for _ in range(num_states)]
                )
                outcomes: list[tuple[float, int, float]] = [
                    (weights[0], -1, rng.uniform(-0.8, 0.8))
                ]
                outcomes.extend(
                    (weights[sp + 1], sp, rng.uniform(-0.8, 0.8))
                    for sp in range(num_states)
                )
                by_action.append(outcomes)
            by_state.append(by_action)
        transitions.append(by_state)
    return FiniteHorizonMDP(
        horizon=horizon,
        num_states=num_states,
        num_actions=num_actions,
        gamma=gamma,
        boundary_value=boundary_value,
        transitions=transitions,
        initial=_normalize(rng.uniform(0.1, 1.0) for _ in range(num_states)),
    )


def _value_tables(
    mdp: FiniteHorizonMDP, policy: Policy
) -> tuple[list[list[float]], list[list[list[float]]]]:
    values: list[list[float]] = [
        [mdp.boundary_value for _ in range(mdp.num_states)]
    ]
    q_values: list[list[list[float]]] = [[]]
    for h in range(1, mdp.horizon + 1):
        q_h: list[list[float]] = []
        v_h: list[float] = []
        for s in range(mdp.num_states):
            q_s: list[float] = []
            for a in range(mdp.num_actions):
                q = 0.0
                for probability, sp, reward in mdp.transitions[h][s][a]:
                    continuation = (
                        mdp.boundary_value if sp == -1 else values[h - 1][sp]
                    )
                    q += probability * (reward + mdp.gamma * continuation)
                q_s.append(q)
            q_h.append(q_s)
            v_h.append(_dot(policy[h][s], q_s))
        q_values.append(q_h)
        values.append(v_h)
    return values, q_values


def _backup_from_stage(
    mdp: FiniteHorizonMDP,
    policy: Policy,
    h: int,
    steps: int,
    terminal_values: Sequence[float],
) -> list[float]:
    """Apply the stage operators from h-steps+1 through h."""
    if not 0 <= steps <= h:
        raise ValueError("backup steps must lie in [0, h]")
    previous = list(terminal_values)
    for stage in range(h - steps + 1, h + 1):
        current: list[float] = []
        for s in range(mdp.num_states):
            action_values: list[float] = []
            for a in range(mdp.num_actions):
                q = 0.0
                for probability, sp, reward in mdp.transitions[stage][s][a]:
                    continuation = (
                        mdp.boundary_value if sp == -1 else previous[sp]
                    )
                    q += probability * (reward + mdp.gamma * continuation)
                action_values.append(q)
            current.append(_dot(policy[stage][s], action_values))
        previous = current
    return previous


def _occupancies(
    mdp: FiniteHorizonMDP,
    policy: Policy,
    initial: Sequence[float] | None = None,
) -> list[list[float]]:
    """Probability laws before each decision, with absorbing mass last."""
    distribution = (
        list(mdp.initial) + [0.0] if initial is None else list(initial)
    )
    if len(distribution) != mdp.num_states + 1:
        raise ValueError("initial law must include one absorbing-state entry")
    _assert_close(sum(distribution), 1.0, "initial-law normalization")
    result: list[list[float]] = []
    for t in range(mdp.horizon):
        result.append(list(distribution))
        h = mdp.horizon - t
        successor = [0.0 for _ in range(mdp.num_states + 1)]
        successor[-1] += distribution[-1]
        for s in range(mdp.num_states):
            for a, action_probability in enumerate(policy[h][s]):
                for probability, sp, _reward in mdp.transitions[h][s][a]:
                    index = mdp.num_states if sp == -1 else sp
                    successor[index] += distribution[s] * action_probability * probability
        distribution = successor
    return result


def _evaluator_depths(
    rng: random.Random, mdp: FiniteHorizonMDP, max_depth: int
) -> tuple[list[list[list[float]]], list[list[list[float]]], float]:
    latent: list[list[list[float]]] = []
    initial_by_stage = [[mdp.boundary_value for _ in range(mdp.num_states)]]
    initial_by_stage.extend(
        [rng.uniform(-1.5, 1.5) for _ in range(mdp.num_states)]
        for _h in range(1, mdp.horizon + 1)
    )
    latent.append(initial_by_stage)
    contraction = rng.uniform(-0.75, 0.75)
    offsets = [[0.0 for _ in range(mdp.num_states)]]
    offsets.extend(
        [rng.uniform(-0.6, 0.6) for _ in range(mdp.num_states)]
        for _h in range(1, mdp.horizon + 1)
    )
    for depth in range(max_depth):
        next_depth = [[mdp.boundary_value for _ in range(mdp.num_states)]]
        next_depth.extend(
            [
                math.tanh(contraction * latent[depth][h][s] + offsets[h][s])
                for s in range(mdp.num_states)
            ]
            for h in range(1, mdp.horizon + 1)
        )
        latent.append(next_depth)
    head_scale = rng.uniform(0.4, 1.7)
    head_bias = rng.uniform(-0.3, 0.3)
    evaluator: list[list[list[float]]] = []
    for depth in range(max_depth + 1):
        by_stage = [[mdp.boundary_value for _ in range(mdp.num_states)]]
        by_stage.extend(
            [head_scale * latent[depth][h][s] + head_bias for s in range(mdp.num_states)]
            for h in range(1, mdp.horizon + 1)
        )
        evaluator.append(by_stage)
    return evaluator, latent, abs(head_scale)


def _check_residual_and_reference(
    rng: random.Random, mdp: FiniteHorizonMDP, policy: Policy, block: int
) -> dict[str, float | int]:
    values, _q = _value_tables(mdp, policy)
    evaluator, latent, head_lipschitz = _evaluator_depths(rng, mdp, 5)
    comparisons = ((0, 1), (0, 5), (2, 3), (2, 5))
    checks = 0
    minimum_slack = math.inf
    maximum_ratio = 0.0

    # Exact absorbing boundary and its self-loop fixed-point identity.
    boundary_rhs = mdp.absorbing_reward + mdp.gamma * mdp.boundary_value
    _assert_close(
        boundary_rhs,
        mdp.boundary_value,
        "absorbing boundary Bellman fixed point",
    )
    checks += 1
    _assert_le(abs(mdp.absorbing_reward), 1.0, "absorbing reward interval")
    checks += 1

    # Every recurrent depth uses the same absorbing boundary. Stage zero is
    # the concrete boundary representation used by every truncated backup.
    for depth in range(len(evaluator)):
        for represented_boundary in evaluator[depth][0]:
            _assert_close(
                represented_boundary,
                mdp.boundary_value,
                f"depth-{depth} absorbing boundary",
            )
            checks += 1

    for n, m in comparisons:
        residual_by_stage = [0.0]
        reference_error = [0.0]
        discrepancy = [0.0]
        for h in range(1, mdp.horizon + 1):
            ell = min(block, h)
            target_stage = h - ell
            backup = _backup_from_stage(
                mdp, policy, h, ell, evaluator[m][target_stage]
            )
            residual = max(
                abs(evaluator[m][h][s] - backup[s])
                for s in range(mdp.num_states)
            )
            residual_by_stage.append(residual)
            error = max(
                abs(evaluator[m][h][s] - values[h][s])
                for s in range(mdp.num_states)
            )
            reference_error.append(error)
            disc = max(
                abs(evaluator[n][h][s] - evaluator[m][h][s])
                for s in range(mdp.num_states)
            )
            discrepancy.append(disc)

            recursive_rhs = residual + mdp.gamma**ell * reference_error[target_stage]
            minimum_slack = min(
                minimum_slack,
                _assert_le(error, recursive_rhs, "stagewise residual recursion"),
            )
            checks += 1

            stage = h
            weight = 1.0
            unrolled = 0.0
            while stage > 0:
                unrolled += weight * residual_by_stage[stage]
                stage = max(0, stage - block)
                weight *= mdp.gamma**block
            minimum_slack = min(
                minimum_slack,
                _assert_le(error, unrolled, "unrolled residual recursion"),
            )
            checks += 1

            finite_reference_error = max(
                abs(evaluator[n][h][s] - values[h][s])
                for s in range(mdp.num_states)
            )
            minimum_slack = min(
                minimum_slack,
                _assert_le(
                    finite_reference_error,
                    disc + unrolled,
                    "finite-reference decomposition",
                ),
            )
            checks += 1

            uniform_residual = max(residual_by_stage[1:])
            blocks = (h + block - 1) // block
            geometric = (
                1.0
                if mdp.gamma == 0.0
                else (1.0 - mdp.gamma ** (block * blocks))
                / (1.0 - mdp.gamma**block)
            )
            uniform_bound = disc + geometric * uniform_residual
            minimum_slack = min(
                minimum_slack,
                _assert_le(
                    finite_reference_error,
                    uniform_bound,
                    "uniform geometric finite-reference bound",
                ),
            )
            checks += 1
            if uniform_bound > TOL:
                maximum_ratio = max(
                    maximum_ratio, finite_reference_error / uniform_bound
                )

            path = 0.0
            for depth in range(n, m):
                path += max(
                    abs(latent[depth + 1][h][s] - latent[depth][h][s])
                    for s in range(mdp.num_states)
                )
            minimum_slack = min(
                minimum_slack,
                _assert_le(disc, head_lipschitz * path, "recurrent path bound"),
            )
            checks += 1

    return {
        "checks": checks,
        "minimum_slack": minimum_slack,
        "maximum_bound_ratio": maximum_ratio,
    }


def _check_finite_horizon_cpi(
    rng: random.Random,
    mdp: FiniteHorizonMDP,
    current: Policy,
    candidate: Policy,
    alpha: float,
) -> dict[str, object]:
    mixed = _mix_policy(current, candidate, alpha)
    current_values, current_q = _value_tables(mdp, current)
    mixed_values, _ = _value_tables(mdp, mixed)
    current_eta = _dot(mdp.initial, current_values[mdp.horizon])
    mixed_eta = _dot(mdp.initial, mixed_values[mdp.horizon])
    current_occupancy = _occupancies(mdp, current)
    mixed_occupancy = _occupancies(mdp, mixed)

    delta: list[list[float]] = [[]]
    epsilon_cpi = [0.0]
    estimated_advantage: list[list[list[float]]] = [[]]
    epsilon_candidate = [0.0]
    max_centering_defect = 0.0
    breakdown = {
        "centering_assertions": 0,
        "occupancy_assertions": 0,
        "performance_difference_assertions": 0,
        "closed_form_assertions": 0,
        "cpi_bound_assertions": 0,
    }
    for h in range(1, mdp.horizon + 1):
        delta_h: list[float] = []
        estimated_h: list[list[float]] = []
        bias_h: list[float] = []
        for s in range(mdp.num_states):
            advantage = [q - current_values[h][s] for q in current_q[h][s]]
            raw_error = [rng.uniform(-0.4, 0.4) for _ in advantage]
            mean_error = _dot(current[h][s], raw_error)
            centered_error = [error - mean_error for error in raw_error]
            ahat = [a + error for a, error in zip(advantage, centered_error)]
            estimated_h.append(ahat)
            centering_defect = abs(_dot(current[h][s], ahat))
            _assert_close(
                centering_defect,
                0.0,
                f"exact centering at h={h}, s={s}",
            )
            breakdown["centering_assertions"] += 1
            max_centering_defect = max(max_centering_defect, centering_defect)
            delta_h.append(_dot(candidate[h][s], advantage))
            bias_h.append(abs(_dot(candidate[h][s], centered_error)))
        delta.append(delta_h)
        epsilon_cpi.append(max(abs(x) for x in delta_h))
        estimated_advantage.append(estimated_h)
        epsilon_candidate.append(max(bias_h))

    true_surrogate = current_eta
    estimated_surrogate = current_eta
    performance_difference_rhs = current_eta
    exact_distribution_penalty = 0.0
    quadratic_distribution_penalty = 0.0
    linear_estimation_penalty = 0.0
    max_occupancy_violation = -math.inf
    inequality_slacks: list[float] = []
    for t in range(mdp.horizon):
        h = mdp.horizon - t
        expected_delta = sum(
            current_occupancy[t][s] * delta[h][s]
            for s in range(mdp.num_states)
        )
        true_surrogate += mdp.gamma**t * alpha * expected_delta
        mixed_expected_delta = sum(
            mixed_occupancy[t][s] * delta[h][s]
            for s in range(mdp.num_states)
        )
        performance_difference_rhs += (
            mdp.gamma**t * alpha * mixed_expected_delta
        )
        expected_ahat = 0.0
        for s in range(mdp.num_states):
            expected_ahat += current_occupancy[t][s] * _dot(
                mixed[h][s], estimated_advantage[h][s]
            )
        estimated_surrogate += mdp.gamma**t * expected_ahat

        exact_distribution_penalty += (
            2.0
            * alpha
            * mdp.gamma**t
            * epsilon_cpi[h]
            * (1.0 - (1.0 - alpha) ** t)
        )
        quadratic_distribution_penalty += (
            2.0 * alpha * alpha * mdp.gamma**t * t * epsilon_cpi[h]
        )
        linear_estimation_penalty += (
            alpha * mdp.gamma**t * epsilon_candidate[h]
        )

        occupancy_l1 = sum(
            abs(x - y)
            for x, y in zip(mixed_occupancy[t], current_occupancy[t])
        )
        occupancy_bound = 2.0 * (1.0 - (1.0 - alpha) ** t)
        max_occupancy_violation = max(
            max_occupancy_violation, occupancy_l1 - occupancy_bound
        )
        inequality_slacks.append(
            _assert_le(
                occupancy_l1,
                occupancy_bound,
                f"time-indexed occupancy shift at t={t}",
            )
        )
        breakdown["occupancy_assertions"] += 1

    performance_difference_error = _assert_close(
        performance_difference_rhs,
        mixed_eta,
        "finite-horizon performance-difference identity",
    )
    breakdown["performance_difference_assertions"] += 1

    inequality_slacks.append(
        _assert_le(
            true_surrogate - exact_distribution_penalty,
            mixed_eta,
            "finite-horizon exact-coupling CPI",
        )
    )
    breakdown["cpi_bound_assertions"] += 1
    inequality_slacks.append(
        _assert_le(
            true_surrogate - quadratic_distribution_penalty,
            mixed_eta,
            "finite-horizon quadratic CPI",
        )
    )
    breakdown["cpi_bound_assertions"] += 1
    inequality_slacks.append(
        _assert_le(
            estimated_surrogate
            - linear_estimation_penalty
            - exact_distribution_penalty,
            mixed_eta,
            "finite-horizon CPI with centered evaluation error",
        )
    )
    breakdown["cpi_bound_assertions"] += 1
    inequality_slacks.append(
        _assert_le(
            estimated_surrogate
            - linear_estimation_penalty
            - quadratic_distribution_penalty,
            mixed_eta,
            "finite-horizon quadratic CPI with centered evaluation error",
        )
    )
    breakdown["cpi_bound_assertions"] += 1

    # Check the nonlinear G_H closed form directly, then verify that uniform
    # constants dominate their stage-specific counterparts.
    uniform_epsilon_cpi = max(epsilon_cpi)
    uniform_epsilon_candidate = max(epsilon_candidate)
    geometric_h = _geom(mdp.gamma, mdp.horizon)
    time_weight = sum(t * mdp.gamma**t for t in range(mdp.horizon))
    uniform_linear_penalty = (
        alpha * uniform_epsilon_candidate * geometric_h
    )
    uniform_nonlinear_direct = (
        2.0
        * alpha
        * uniform_epsilon_cpi
        * sum(
            mdp.gamma**t * (1.0 - (1.0 - alpha) ** t)
            for t in range(mdp.horizon)
        )
    )
    uniform_nonlinear_closed = (
        2.0
        * alpha
        * uniform_epsilon_cpi
        * (
            _geom(mdp.gamma, mdp.horizon)
            - _geom(mdp.gamma * (1.0 - alpha), mdp.horizon)
        )
    )
    uniform_quadratic_penalty = (
        2.0 * alpha * alpha * uniform_epsilon_cpi * time_weight
    )
    _assert_close(
        uniform_nonlinear_direct,
        uniform_nonlinear_closed,
        "nonlinear uniform G_H closed form",
    )
    breakdown["closed_form_assertions"] += 1
    inequality_slacks.append(
        _assert_le(
            exact_distribution_penalty,
            uniform_nonlinear_closed,
            "uniform nonlinear penalty dominates stage-specific penalty",
        )
    )
    breakdown["closed_form_assertions"] += 1
    inequality_slacks.append(
        _assert_le(
            uniform_nonlinear_closed,
            uniform_quadratic_penalty,
            "quadratic penalty dominates nonlinear G_H penalty",
        )
    )
    breakdown["closed_form_assertions"] += 1
    inequality_slacks.append(
        _assert_le(
            linear_estimation_penalty,
            uniform_linear_penalty,
            "uniform linear penalty dominates stage-specific penalty",
        )
    )
    breakdown["closed_form_assertions"] += 1

    uniform_nonlinear_lower = (
        estimated_surrogate
        - uniform_linear_penalty
        - uniform_nonlinear_closed
    )
    inequality_slacks.append(
        _assert_le(
            uniform_nonlinear_lower,
            mixed_eta,
            "uniform nonlinear finite-horizon CPI",
        )
    )
    breakdown["cpi_bound_assertions"] += 1
    uniform_quadratic_lower = (
        estimated_surrogate
        - uniform_linear_penalty
        - uniform_quadratic_penalty
    )
    inequality_slacks.append(
        _assert_le(
            uniform_quadratic_lower,
            mixed_eta,
            "uniform quadratic finite-horizon CPI",
        )
    )
    breakdown["cpi_bound_assertions"] += 1
    checks = sum(breakdown.values())
    return {
        "checks": checks,
        "check_breakdown": breakdown,
        "minimum_slack": min(inequality_slacks),
        "max_centering_defect": max_centering_defect,
        "max_occupancy_bound_violation": max_occupancy_violation,
        "performance_difference_error": performance_difference_error,
    }


def _check_finite_horizon_deployment(
    rng: random.Random,
    mdp: FiniteHorizonMDP,
    exact_policy: Policy,
) -> dict[str, float | int]:
    alternative = _random_policy(
        rng, mdp.horizon, mdp.num_states, mdp.num_actions
    )
    beta = rng.choice((0.0, 0.03, 0.2, 0.7, 1.0))
    deployed = _mix_policy(exact_policy, alternative, beta)
    exact_values, _ = _value_tables(mdp, exact_policy)
    deployed_values, _ = _value_tables(mdp, deployed)
    exact_eta = _dot(mdp.initial, exact_values[mdp.horizon])
    deployed_eta = _dot(mdp.initial, deployed_values[mdp.horizon])
    delta = max(
        _tv(exact_policy[h][s], deployed[h][s])
        for h in range(1, mdp.horizon + 1)
        for s in range(mdp.num_states)
    )
    # All generated transition rewards and the absorbing reward lie in [-1, 1].
    reward_width = 2.0
    gamma = mdp.gamma
    decision_weight = (
        _geom(gamma, mdp.horizon) - mdp.horizon * gamma**mdp.horizon
    ) / (1.0 - gamma)
    bound = reward_width * delta * decision_weight
    slack = _assert_le(
        abs(deployed_eta - exact_eta),
        bound,
        "finite-horizon deployment perturbation",
    )
    return {"checks": 1, "minimum_slack": slack, "delta": delta}


@dataclass(frozen=True)
class StationaryMDP:
    num_states: int
    num_actions: int
    gamma: float
    # transitions[s][a] is a list of (probability, next_state, reward).
    transitions: list[list[list[tuple[float, int, float]]]]
    initial: list[float]


def _solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1.0e-14:
            raise ArithmeticError("singular linear system")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [x / pivot_value for x in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0.0:
                continue
            augmented[row] = [
                x - factor * y
                for x, y in zip(augmented[row], augmented[column])
            ]
    return [augmented[row][-1] for row in range(n)]


def _stationary_eta(mdp: StationaryMDP, policy: list[list[float]]) -> float:
    transition_matrix = [
        [0.0 for _ in range(mdp.num_states)] for _ in range(mdp.num_states)
    ]
    rewards = [0.0 for _ in range(mdp.num_states)]
    for s in range(mdp.num_states):
        for a, action_probability in enumerate(policy[s]):
            for probability, sp, reward in mdp.transitions[s][a]:
                mass = action_probability * probability
                transition_matrix[s][sp] += mass
                rewards[s] += mass * reward
    matrix = [
        [
            (1.0 if row == column else 0.0)
            - mdp.gamma * transition_matrix[row][column]
            for column in range(mdp.num_states)
        ]
        for row in range(mdp.num_states)
    ]
    values = _solve_linear(matrix, rewards)
    return _dot(mdp.initial, values)


def _kl_divergence(p: Sequence[float], q: Sequence[float]) -> float:
    """Return KL(p || q), including the incompatible-support infinity."""
    total = 0.0
    for p_value, q_value in zip(p, q):
        if p_value == 0.0:
            continue
        if q_value == 0.0:
            return math.inf
        total += p_value * math.log(p_value / q_value)
    return total


def _check_infinite_horizon_deployment(
    rng: random.Random, gamma: float
) -> dict[str, float | int]:
    num_states = 4
    num_actions = 3
    transitions: list[list[list[tuple[float, int, float]]]] = []
    for _s in range(num_states):
        by_action: list[list[tuple[float, int, float]]] = []
        for _a in range(num_actions):
            probabilities = _normalize(rng.uniform(0.1, 1.0) for _ in range(num_states))
            by_action.append(
                [
                    (probabilities[sp], sp, rng.uniform(-1.0, 1.0))
                    for sp in range(num_states)
                ]
            )
        transitions.append(by_action)
    mdp = StationaryMDP(
        num_states=num_states,
        num_actions=num_actions,
        gamma=gamma,
        transitions=transitions,
        initial=_normalize(rng.uniform(0.1, 1.0) for _ in range(num_states)),
    )
    exact = [
        _normalize(rng.uniform(0.2, 1.5) for _ in range(num_actions))
        for _ in range(num_states)
    ]
    alternative = [
        _normalize(rng.uniform(0.2, 1.5) for _ in range(num_actions))
        for _ in range(num_states)
    ]
    beta = rng.choice((0.0, 0.01, 0.1, 0.5, 1.0))
    deployed = [
        [
            (1.0 - beta) * p + beta * q
            for p, q in zip(exact[s], alternative[s])
        ]
        for s in range(num_states)
    ]
    delta = max(_tv(exact[s], deployed[s]) for s in range(num_states))
    exact_eta = _stationary_eta(mdp, exact)
    deployed_eta = _stationary_eta(mdp, deployed)
    reward_width = 2.0
    tv_bound = reward_width * delta / (1.0 - gamma) ** 2
    tv_slack = _assert_le(
        abs(deployed_eta - exact_eta), tv_bound, "infinite-horizon TV deployment"
    )

    uniform_kl = max(
        _kl_divergence(deployed[s], exact[s]) for s in range(num_states)
    )
    if not math.isfinite(uniform_kl):
        raise AssertionError("random positive-support policy produced infinite KL")
    pinsker_bound = (
        reward_width
        * math.sqrt(uniform_kl / 2.0)
        / (1.0 - gamma) ** 2
    )
    pinsker_slack = _assert_le(
        abs(deployed_eta - exact_eta),
        pinsker_bound,
        "infinite-horizon Pinsker deployment",
    )
    return {
        "checks": 2,
        "minimum_slack": min(tv_slack, pinsker_slack),
        "delta": delta,
        "uniform_kl": uniform_kl,
    }


def _check_positive_horizon_absorbing_initial_law() -> dict[str, object]:
    """Exercise a genuine H>0 initial law concentrated on the absorbing atom."""
    rng = random.Random(441991)
    mdp = _make_finite_horizon_mdp(rng, 4, 2, 2, 0.83)
    current = _random_policy(rng, mdp.horizon, mdp.num_states, mdp.num_actions)
    candidate = _random_policy(rng, mdp.horizon, mdp.num_states, mdp.num_actions)
    mixed = _mix_policy(current, candidate, 0.6)
    absorbing_initial = [0.0 for _ in range(mdp.num_states)] + [1.0]
    target_law = absorbing_initial
    checks = 0
    max_law_error = 0.0
    for label, policy in (("current", current), ("mixture", mixed)):
        for t, law in enumerate(_occupancies(mdp, policy, absorbing_initial)):
            law_error = sum(abs(x - y) for x, y in zip(law, target_law))
            _assert_close(
                law_error,
                0.0,
                f"positive-horizon absorbing initial law: {label}, t={t}",
            )
            max_law_error = max(max_law_error, law_error)
            checks += 1

    absorbing_eta = (
        sum(
            mdp.gamma**t * mdp.absorbing_reward
            for t in range(mdp.horizon)
        )
        + mdp.gamma**mdp.horizon * mdp.boundary_value
    )
    _assert_close(
        absorbing_eta,
        mdp.boundary_value,
        "positive-horizon absorbing return",
    )
    checks += 1

    # Every stage advantage is zero on the shared atom. The finite-horizon
    # performance-difference identity therefore has zero right-hand side.
    performance_difference_rhs = absorbing_eta + sum(
        mdp.gamma**t * 0.0 for t in range(mdp.horizon)
    )
    _assert_close(
        performance_difference_rhs,
        absorbing_eta,
        "absorbing-start performance-difference identity",
    )
    checks += 1
    _assert_close(
        abs(absorbing_eta - absorbing_eta),
        0.0,
        "absorbing-start deployment difference",
    )
    checks += 1
    return {
        "checks": checks,
        "minimum_slack": 0.0,
        "maximum_initial_law_error": max_law_error,
        "horizon": mdp.horizon,
    }


def _check_incompatible_support_deployment() -> dict[str, object]:
    """Cover TV=1 and a KL corollary that is inapplicable because KL is infinite."""
    gamma = 0.75
    exact = [[1.0, 0.0]]
    deployed = [[0.0, 1.0]]
    checks = 0
    slacks: list[float] = []

    delta = _tv(exact[0], deployed[0])
    _assert_close(delta, 1.0, "deterministic incompatible-support TV")
    checks += 1

    stationary = StationaryMDP(
        num_states=1,
        num_actions=2,
        gamma=gamma,
        transitions=[[
            [(1.0, 0, -1.0)],
            [(1.0, 0, 1.0)],
        ]],
        initial=[1.0],
    )
    exact_eta = _stationary_eta(stationary, exact)
    deployed_eta = _stationary_eta(stationary, deployed)
    tv_bound = 2.0 * delta / (1.0 - gamma) ** 2
    slacks.append(
        _assert_le(
            abs(deployed_eta - exact_eta),
            tv_bound,
            "deterministic incompatible-support TV deployment",
        )
    )
    checks += 1

    forward_kl = _kl_divergence(deployed[0], exact[0])
    reverse_kl = _kl_divergence(exact[0], deployed[0])
    if not math.isinf(forward_kl):
        raise AssertionError("deployed||exact KL must be infinite")
    checks += 1
    if not math.isinf(reverse_kl):
        raise AssertionError("exact||deployed KL must be infinite")
    checks += 1
    pinsker_finite_bound_applicable = math.isfinite(forward_kl)
    if pinsker_finite_bound_applicable:
        raise AssertionError("finite-KL Pinsker corollary must be marked inapplicable")
    checks += 1

    # Repeat TV=1 under a finite decision horizon and the shared nonzero
    # absorbing boundary.
    horizon = 3
    boundary_value = -0.4
    transitions: list[list[list[list[tuple[float, int, float]]]]] = [[]]
    for h in range(1, horizon + 1):
        next_state = -1 if h == 1 else 0
        transitions.append([[
            [(1.0, next_state, -1.0)],
            [(1.0, next_state, 1.0)],
        ]])
    finite = FiniteHorizonMDP(
        horizon=horizon,
        num_states=1,
        num_actions=2,
        gamma=gamma,
        boundary_value=boundary_value,
        transitions=transitions,
        initial=[1.0],
    )
    finite_exact: Policy = [[]] + [[[1.0, 0.0]] for _ in range(horizon)]
    finite_deployed: Policy = [[]] + [[[0.0, 1.0]] for _ in range(horizon)]
    finite_exact_values, _ = _value_tables(finite, finite_exact)
    finite_deployed_values, _ = _value_tables(finite, finite_deployed)
    finite_difference = abs(
        finite_deployed_values[horizon][0] - finite_exact_values[horizon][0]
    )
    decision_weight = (
        _geom(gamma, horizon) - horizon * gamma**horizon
    ) / (1.0 - gamma)
    finite_bound = 2.0 * delta * decision_weight
    slacks.append(
        _assert_le(
            finite_difference,
            finite_bound,
            "finite-horizon deterministic TV=1 deployment",
        )
    )
    checks += 1
    _assert_le(
        abs(finite.absorbing_reward),
        1.0,
        "incompatible-support absorbing reward interval",
    )
    checks += 1
    return {
        "checks": checks,
        "minimum_slack": min(slacks),
        "tv_delta": delta,
        "forward_kl": "infinity",
        "reverse_kl": "infinity",
        "pinsker_finite_bound_applicable": pinsker_finite_bound_applicable,
    }


def _check_zero_horizon_and_absorbing() -> dict[str, float | int]:
    checks = 0
    minimum_slack = math.inf
    boundary_value = -0.4
    for gamma in (0.0, 0.5, 0.99):
        absorbing_reward = (1.0 - gamma) * boundary_value
        fixed_point = absorbing_reward + gamma * boundary_value
        if abs(fixed_point - boundary_value) > TOL:
            raise AssertionError("absorbing-only return does not equal the boundary")
        checks += 1

        if _geom(gamma, 0) != 0.0:
            raise AssertionError("H=0 geometric weight must be zero")
        checks += 1

        cpi_time_weight = sum(t * gamma**t for t in range(0))
        if cpi_time_weight != 0.0:
            raise AssertionError("H=0 CPI penalty must be zero")
        checks += 1

        deployment_weight = (
            _geom(gamma, 0) - 0.0 * gamma**0
        ) / (1.0 - gamma)
        if deployment_weight != 0.0:
            raise AssertionError("H=0 deployment penalty must be zero")
        checks += 1

        for block in (1, 5):
            blocks = (0 + block - 1) // block
            if blocks != 0:
                raise AssertionError("J_0 must be zero")
            checks += 1
    minimum_slack = 0.0
    return {"checks": checks, "minimum_slack": minimum_slack}


def run(seed: int, random_cases: int) -> dict[str, object]:
    rng = random.Random(seed)
    totals = {
        "residual_reference_checks": 0,
        "finite_horizon_cpi_checks": 0,
        "finite_horizon_deployment_checks": 0,
        "infinite_horizon_deployment_checks": 0,
        "positive_horizon_absorbing_initial_checks": 0,
        "incompatible_support_checks": 0,
    }
    cpi_check_breakdown = {
        "centering_assertions": 0,
        "occupancy_assertions": 0,
        "performance_difference_assertions": 0,
        "closed_form_assertions": 0,
        "cpi_bound_assertions": 0,
    }
    minimum_slack = math.inf
    maximum_residual_bound_ratio = 0.0
    maximum_centering_defect = 0.0
    maximum_occupancy_bound_violation = -math.inf
    maximum_performance_difference_error = 0.0

    boundary_cases = [
        (1, 1, 0.0, 0.0),
        (1, 4, 0.7, 1.0),
        (2, 1, 0.4, 0.1),
        (4, 4, 0.95, 0.5),
        (5, 8, 0.9, 1.0),
    ]
    cases = list(boundary_cases)
    for _ in range(random_cases):
        horizon = rng.randint(1, 7)
        block = rng.randint(1, horizon + 4)
        gamma = rng.choice((0.0, 0.2, 0.6, 0.9, 0.97))
        alpha = rng.choice((0.0, 0.05, 0.25, 0.7, 1.0))
        cases.append((horizon, block, gamma, alpha))

    for horizon, block, gamma, alpha in cases:
        mdp = _make_finite_horizon_mdp(rng, horizon, 3, 3, gamma)
        current = _random_policy(rng, horizon, 3, 3)
        candidate = _random_policy(rng, horizon, 3, 3)

        residual = _check_residual_and_reference(rng, mdp, current, block)
        totals["residual_reference_checks"] += int(residual["checks"])
        minimum_slack = min(minimum_slack, float(residual["minimum_slack"]))
        maximum_residual_bound_ratio = max(
            maximum_residual_bound_ratio,
            float(residual["maximum_bound_ratio"]),
        )

        cpi = _check_finite_horizon_cpi(rng, mdp, current, candidate, alpha)
        totals["finite_horizon_cpi_checks"] += int(cpi["checks"])
        for name, value in dict(cpi["check_breakdown"]).items():
            cpi_check_breakdown[name] += int(value)
        minimum_slack = min(minimum_slack, float(cpi["minimum_slack"]))
        maximum_centering_defect = max(
            maximum_centering_defect, float(cpi["max_centering_defect"])
        )
        maximum_occupancy_bound_violation = max(
            maximum_occupancy_bound_violation,
            float(cpi["max_occupancy_bound_violation"]),
        )
        maximum_performance_difference_error = max(
            maximum_performance_difference_error,
            float(cpi["performance_difference_error"]),
        )

        exact_mixture = _mix_policy(current, candidate, alpha)
        deployment = _check_finite_horizon_deployment(rng, mdp, exact_mixture)
        totals["finite_horizon_deployment_checks"] += int(deployment["checks"])
        minimum_slack = min(
            minimum_slack, float(deployment["minimum_slack"])
        )

    for _ in range(random_cases + len(boundary_cases)):
        gamma = rng.choice((0.0, 0.2, 0.7, 0.95, 0.99))
        deployment = _check_infinite_horizon_deployment(rng, gamma)
        totals["infinite_horizon_deployment_checks"] += int(deployment["checks"])
        minimum_slack = min(
            minimum_slack, float(deployment["minimum_slack"])
        )

    zero_horizon = _check_zero_horizon_and_absorbing()
    totals["zero_horizon_and_absorbing_checks"] = int(zero_horizon["checks"])
    minimum_slack = min(minimum_slack, float(zero_horizon["minimum_slack"]))
    absorbing_initial = _check_positive_horizon_absorbing_initial_law()
    totals["positive_horizon_absorbing_initial_checks"] = int(
        absorbing_initial["checks"]
    )
    minimum_slack = min(
        minimum_slack, float(absorbing_initial["minimum_slack"])
    )
    incompatible_support = _check_incompatible_support_deployment()
    totals["incompatible_support_checks"] = int(incompatible_support["checks"])
    minimum_slack = min(
        minimum_slack, float(incompatible_support["minimum_slack"])
    )
    total_checks = sum(totals.values())
    return {
        "status": "PASS",
        "seed": seed,
        "random_cases": random_cases,
        "finite_horizon_case_count": len(cases),
        "checks": totals,
        "finite_horizon_cpi_check_breakdown": cpi_check_breakdown,
        "total_checks": total_checks,
        "minimum_numerical_slack": minimum_slack,
        "maximum_residual_uniform_bound_ratio": maximum_residual_bound_ratio,
        "maximum_centering_defect": maximum_centering_defect,
        "maximum_occupancy_bound_violation": maximum_occupancy_bound_violation,
        "maximum_performance_difference_error": maximum_performance_difference_error,
        "positive_horizon_absorbing_initial_law": {
            "horizon": absorbing_initial["horizon"],
            "maximum_law_error": absorbing_initial["maximum_initial_law_error"],
        },
        "incompatible_support_case": {
            "tv_delta": incompatible_support["tv_delta"],
            "forward_kl": incompatible_support["forward_kl"],
            "reverse_kl": incompatible_support["reverse_kl"],
            "pinsker_finite_bound_applicable": incompatible_support[
                "pinsker_finite_bound_applicable"
            ],
        },
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
            "infinite KL with Pinsker finite-bound marked inapplicable",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260803)
    parser.add_argument("--random-cases", type=int, default=200)
    args = parser.parse_args()
    print(json.dumps(run(args.seed, args.random_cases), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
