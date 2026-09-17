#!/usr/bin/env python3
"""Verify the exact two-nonabsorbing-state certificate example in main.tex.

The calculation uses only fractions. It is a deterministic theorem check, not
an experiment and not evidence about a learned policy.
"""

from fractions import Fraction
import json


ACTIVE_STATES = ("s0", "s1")
STATES = ACTIVE_STATES + ("s_abs",)
# "a" and "b" are the actions written a_0 and a_1 in main.tex.
ACTIONS = ("a", "b")
GAMMA = Fraction(1, 2)
ALPHA = Fraction(1, 2)
K = 1
N = 1
M = 2

RHO = (Fraction(1), Fraction(0), Fraction(0))
PI = {
    "s0": {"a": Fraction(1), "b": Fraction(0)},
    "s1": {"a": Fraction(1), "b": Fraction(0)},
    "s_abs": {"a": Fraction(1), "b": Fraction(0)},
}
PI_CAND = {
    "s0": {"a": Fraction(0), "b": Fraction(1)},
    "s1": {"a": Fraction(0), "b": Fraction(1)},
    "s_abs": {"a": Fraction(0), "b": Fraction(1)},
}

# Deterministic (reward, successor) pairs.
MODEL = {
    ("s0", "a"): (Fraction(0), "s0"),
    ("s0", "b"): (Fraction(1), "s1"),
    ("s1", "a"): (Fraction(0), "s0"),
    ("s1", "b"): (Fraction(0), "s1"),
    ("s_abs", "a"): (Fraction(0), "s_abs"),
    ("s_abs", "b"): (Fraction(0), "s_abs"),
}


def _solve_2x2(a, b, c, d, u, v):
    det = a * d - b * c
    assert det != 0
    return ((u * d - b * v) / det, (a * v - u * c) / det)


def _kernel_and_reward(policy):
    transition = [[Fraction(0) for _ in STATES] for _ in STATES]
    reward = [Fraction(0) for _ in STATES]
    for i, state in enumerate(STATES):
        for action in ACTIONS:
            probability = policy[state][action]
            immediate_reward, successor = MODEL[(state, action)]
            reward[i] += probability * immediate_reward
            transition[i][STATES.index(successor)] += probability
    return transition, reward


def _value(policy):
    transition, reward = _kernel_and_reward(policy)
    active_value = _solve_2x2(
        1 - GAMMA * transition[0][0],
        -GAMMA * transition[0][1],
        -GAMMA * transition[1][0],
        1 - GAMMA * transition[1][1],
        reward[0],
        reward[1],
    )
    return active_value + (Fraction(0),)


def _occupancy(policy):
    transition, _ = _kernel_and_reward(policy)
    # Solve d = (1-gamma) rho + gamma d P by transposing the linear system.
    active_occupancy = _solve_2x2(
        1 - GAMMA * transition[0][0],
        -GAMMA * transition[1][0],
        -GAMMA * transition[0][1],
        1 - GAMMA * transition[1][1],
        (1 - GAMMA) * RHO[0],
        (1 - GAMMA) * RHO[1],
    )
    return active_occupancy + (Fraction(0),)


def _mixture():
    return {
        state: {
            action: (1 - ALPHA) * PI[state][action]
            + ALPHA * PI_CAND[state][action]
            for action in ACTIONS
        }
        for state in STATES
    }


def _q(value, state, action):
    reward, successor = MODEL[(state, action)]
    return reward + GAMMA * value[STATES.index(successor)]


def _self_bootstrap_residual(value):
    return tuple(
        value[i] - sum(
            PI[state][action] * _q(value, state, action) for action in ACTIONS
        )
        for i, state in enumerate(STATES)
    )


def _fraction(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    value_pi = _value(PI)
    mixture = _mixture()
    value_mix = _value(mixture)
    d_pi = _occupancy(PI)
    d_mix = _occupancy(mixture)

    # z^(0)=0, T_s(z)=u_s-z/2, and V_psi(z,s)=z.
    u = (Fraction(1, 4), Fraction(-1, 4), Fraction(0))
    u_n = tuple(u_i for u_i in u)
    u_m = tuple(u_i - u_i / 2 for u_i in u)
    endpoint_gap = max(abs(x - y) for x, y in zip(u_n, u_m))
    residual = tuple(
        u_m[i] - _q(u_m, state, "a") for i, state in enumerate(STATES)
    )
    residual_norm = max(abs(x) for x in residual)
    finite_reference_bound = endpoint_gap + residual_norm / (1 - GAMMA**K)
    actual_value_error = max(abs(x - y) for x, y in zip(u_n, value_pi))

    # Compare the same deployed U_1 with its own residual, the optional
    # contractive limit, and deeper finite references. No policy changes.
    eps_res_1 = max(abs(x) for x in _self_bootstrap_residual(u_n))
    direct_bound = eps_res_1 / (1 - GAMMA)
    l_z = Fraction(1, 2)
    l_v = Fraction(1)
    c_z = max(abs(x) for x in u)  # First increment from z^(0)=0.
    invariant_interval = (Fraction(-1, 2), Fraction(1, 2))
    # Each map is affine; interval endpoint images verify invariance.
    assert all(
        invariant_interval[0] <= u_i - l_z * z <= invariant_interval[1]
        for u_i in u[:len(ACTIVE_STATES)] for z in invariant_interval
    )
    u_star = tuple(u_i / (1 + l_z) for u_i in u)
    assert all(u_i - l_z * z == z for u_i, z in zip(u, u_star))
    eps_star = max(abs(x) for x in _self_bootstrap_residual(u_star))
    geometric_path_bound = l_v * l_z**N * c_z / (1 - l_z)
    fixed_point_bound = eps_star / (1 - GAMMA) + geometric_path_bound

    u_3 = tuple(u_i - l_z * z for u_i, z in zip(u, u_m))
    u_4 = tuple(u_i - l_z * z for u_i, z in zip(u, u_3))
    gap_3 = max(abs(x - y) for x, y in zip(u_n, u_3))
    gap_4 = max(abs(x - y) for x, y in zip(u_n, u_4))
    eps_3 = max(abs(x) for x in _self_bootstrap_residual(u_3))
    eps_4 = max(abs(x) for x in _self_bootstrap_residual(u_4))
    reference_bound_3 = gap_3 + eps_3 / (1 - GAMMA)
    reference_bound_4 = gap_4 + eps_4 / (1 - GAMMA)

    advantage = {
        state: {
            action: _q(value_pi, state, action) - value_pi[i]
            for action in ACTIONS
        }
        for i, state in enumerate(STATES)
    }
    g = tuple(advantage[state]["b"] for state in STATES)
    span_g = max(g) - min(g)

    q_u_n = {
        state: {action: _q(u_n, state, action) for action in ACTIONS}
        for state in STATES
    }
    baseline = tuple(q_u_n[state]["a"] for state in STATES)
    a_hat = {
        state: {
            action: q_u_n[state][action] - baseline[i]
            for action in ACTIONS
        }
        for i, state in enumerate(STATES)
    }
    centering_defect = tuple(a_hat[state]["a"] for state in STATES)
    candidate_defect = tuple(
        a_hat[state]["b"] - advantage[state]["b"] for state in STATES
    )
    xi_alpha = sum(
        d_pi[i]
        * ((1 - ALPHA) * centering_defect[i] + ALPHA * candidate_defect[i])
        for i in range(len(STATES))
    )
    estimated_surrogate = sum(
        RHO[i] * value_pi[i] for i in range(len(STATES))
    ) + sum(
        d_pi[i]
        * sum(mixture[state][action] * a_hat[state][action] for action in ACTIONS)
        for i, state in enumerate(STATES)
    ) / (1 - GAMMA)
    occupancy_penalty = (
        GAMMA * ALPHA**2 * span_g
        / ((1 - GAMMA) * (1 - GAMMA + GAMMA * ALPHA))
    )
    signed_cpi_lower_bound = (
        estimated_surrogate - xi_alpha / (1 - GAMMA) - occupancy_penalty
    )
    eta_mix = sum(RHO[i] * value_mix[i] for i in range(len(STATES)))
    candidate_bias = max(abs(x) for x in candidate_defect)
    epsilon_cpi = max(abs(x) for x in g)
    absolute_evaluation_penalty = ALPHA * candidate_bias / (1 - GAMMA)
    absolute_occupancy_penalty = (
        2 * epsilon_cpi * GAMMA * ALPHA**2
        / ((1 - GAMMA) * (1 - GAMMA + GAMMA * ALPHA))
    )
    absolute_cpi_lower_bound = (
        estimated_surrogate - absolute_evaluation_penalty
        - absolute_occupancy_penalty
    )

    assert value_pi == (0, 0, 0)
    assert u_n == (Fraction(1, 4), Fraction(-1, 4), Fraction(0))
    assert u_m == (Fraction(1, 8), Fraction(-1, 8), Fraction(0))
    assert endpoint_gap == Fraction(1, 8)
    assert residual == (Fraction(1, 16), Fraction(-3, 16), Fraction(0))
    assert residual_norm == Fraction(3, 16)
    assert finite_reference_bound == Fraction(1, 2)
    assert actual_value_error == Fraction(1, 4)
    assert d_pi == (Fraction(1), Fraction(0), Fraction(0))
    assert d_mix == (Fraction(3, 4), Fraction(1, 4), Fraction(0))
    assert value_mix == (Fraction(3, 4), Fraction(1, 4), Fraction(0))
    assert g == (Fraction(1), Fraction(0), Fraction(0))
    assert span_g == 1
    assert centering_defect == (0, 0, 0)
    assert candidate_defect == (
        Fraction(-1, 4),
        Fraction(-1, 4),
        Fraction(0),
    )
    assert xi_alpha == Fraction(-1, 8)
    assert estimated_surrogate == Fraction(3, 4)
    assert occupancy_penalty == Fraction(1, 3)
    assert signed_cpi_lower_bound == Fraction(2, 3)
    assert eta_mix == Fraction(3, 4)

    assert eps_res_1 == Fraction(3, 8)
    assert direct_bound == Fraction(3, 4)
    assert u_star == (Fraction(1, 6), Fraction(-1, 6), Fraction(0))
    assert eps_star == Fraction(1, 4)
    assert c_z == Fraction(1, 4)
    assert geometric_path_bound == Fraction(1, 4)
    assert fixed_point_bound == Fraction(3, 4)
    assert u_3 == (Fraction(3, 16), Fraction(-3, 16), Fraction(0))
    assert u_4 == (Fraction(5, 32), Fraction(-5, 32), Fraction(0))
    assert gap_3 == Fraction(1, 16)
    assert gap_4 == Fraction(3, 32)
    assert eps_3 == Fraction(9, 32)
    assert eps_4 == Fraction(15, 64)
    assert reference_bound_3 == Fraction(5, 8)
    assert reference_bound_4 == Fraction(9, 16)
    assert absolute_evaluation_penalty == Fraction(1, 4)
    assert absolute_occupancy_penalty == Fraction(2, 3)
    assert absolute_cpi_lower_bound == Fraction(-1, 6)

    result = {
        "certificate": {
            "actual_value_error": _fraction(actual_value_error),
            "endpoint_gap": _fraction(endpoint_gap),
            "finite_reference_upper_bound": _fraction(finite_reference_bound),
            "reference_residual": _fraction(residual_norm),
            "direct_depth_1": {
                "residual": _fraction(eps_res_1),
                "upper_bound": _fraction(direct_bound),
            },
            "fixed_point": {
                "value": [_fraction(x) for x in u_star],
                "residual": _fraction(eps_star),
                "invariant_interval": [_fraction(x) for x in invariant_interval],
                "L_z": _fraction(l_z),
                "L_V": _fraction(l_v),
                "C_z": _fraction(c_z),
                "geometric_path_bound": _fraction(geometric_path_bound),
                "upper_bound": _fraction(fixed_point_bound),
            },
            "deeper_finite_references": {
                "3": {
                    "value": [_fraction(x) for x in u_3],
                    "endpoint_gap": _fraction(gap_3),
                    "residual": _fraction(eps_3),
                    "upper_bound": _fraction(reference_bound_3),
                },
                "4": {
                    "value": [_fraction(x) for x in u_4],
                    "endpoint_gap": _fraction(gap_4),
                    "residual": _fraction(eps_4),
                    "upper_bound": _fraction(reference_bound_4),
                },
            },
        },
        "cpi": {
            "candidate_defect": [_fraction(x) for x in candidate_defect],
            "candidate_expected_advantage": [_fraction(x) for x in g],
            "centering_defect": [_fraction(x) for x in centering_defect],
            "d_pi": [_fraction(x) for x in d_pi],
            "d_pi_alpha": [_fraction(x) for x in d_mix],
            "eta_pi_alpha": _fraction(eta_mix),
            "estimated_surrogate": _fraction(estimated_surrogate),
            "signed_cpi_lower_bound": _fraction(signed_cpi_lower_bound),
            "absolute_cpi_lower_bound": _fraction(absolute_cpi_lower_bound),
            "absolute_evaluation_penalty": _fraction(absolute_evaluation_penalty),
            "absolute_occupancy_penalty": _fraction(absolute_occupancy_penalty),
            "span": _fraction(span_g),
            "xi_alpha": _fraction(xi_alpha),
        },
        "parameters": {
            "K": K,
            "alpha": _fraction(ALPHA),
            "gamma": _fraction(GAMMA),
            "m": M,
            "n": N,
        },
        "value_pi": [_fraction(x) for x in value_pi],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
