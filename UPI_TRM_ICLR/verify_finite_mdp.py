#!/usr/bin/env python3
"""Verify the exact two-nonabsorbing-state certificate example in main.tex.

The calculation uses only fractions. It is a deterministic theorem check, not
an experiment and not evidence about a learned policy.
"""

from fractions import Fraction
import json


ACTIVE_STATES = ("s0", "s1")
STATES = ACTIVE_STATES + ("s_abs",)
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
        d_mix[i]
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

    result = {
        "certificate": {
            "actual_value_error": _fraction(actual_value_error),
            "endpoint_gap": _fraction(endpoint_gap),
            "finite_reference_upper_bound": _fraction(finite_reference_bound),
            "reference_residual": _fraction(residual_norm),
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
