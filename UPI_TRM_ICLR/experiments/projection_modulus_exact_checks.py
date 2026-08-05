#!/usr/bin/env python3
"""Exact boundary checks for the radial-projection Lipschitz bound.

The construction uses a two-point metric space and ``fractions.Fraction``
throughout.  It checks cases where the composite modulus is below, equal to,
and above one without relying on floating-point tolerances.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


class ExactChecks:
    """Count exact assertions and fail with a named invariant."""

    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, invariant: str) -> None:
        self.count += 1
        if not condition:
            raise AssertionError(invariant)


def _ratio_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _radial_projection_1d(value: Fraction, radius: Fraction) -> Fraction:
    if abs(value) <= radius:
        return value
    return radius if value > 0 else -radius


def _classification(modulus: Fraction) -> str:
    if modulus < 1:
        return "strict_contraction"
    if modulus == 1:
        return "unit_modulus"
    return "superunit_modulus"


def _run_case(
    *,
    name: str,
    expected_pre_modulus: Fraction,
    expected_classification: str,
    radius: Fraction,
    exterior_radius: Fraction,
    checks: ExactChecks,
) -> dict[str, Any]:
    # For f(x_0)=-rho and f(x_1)=rho, choosing this input distance makes
    # Lip(f)=expected_pre_modulus exactly on the two-point domain.
    input_distance = 2 * exterior_radius / expected_pre_modulus
    pre_outputs = (-exterior_radius, exterior_radius)
    projected_outputs = tuple(
        _radial_projection_1d(value, radius) for value in pre_outputs
    )

    pre_output_distance = abs(pre_outputs[1] - pre_outputs[0])
    projected_output_distance = abs(projected_outputs[1] - projected_outputs[0])
    pre_modulus = pre_output_distance / input_distance
    projection_factor = projected_output_distance / pre_output_distance
    composite_modulus = projected_output_distance / input_distance
    theorem_product = (radius / exterior_radius) * pre_modulus
    classification = _classification(composite_modulus)

    checks.require(input_distance > 0, f"{name}: positive input distance")
    checks.require(
        abs(pre_outputs[0]) == exterior_radius,
        f"{name}: first output lies on exterior boundary",
    )
    checks.require(
        abs(pre_outputs[1]) == exterior_radius,
        f"{name}: second output lies on exterior boundary",
    )
    checks.require(
        min(abs(value) for value in pre_outputs) == exterior_radius,
        f"{name}: declared rho is the exact minimum norm",
    )
    checks.require(
        pre_output_distance == 2 * exterior_radius,
        f"{name}: exact pre-projection output distance",
    )
    checks.require(
        pre_modulus == expected_pre_modulus,
        f"{name}: exact pre-projection modulus",
    )
    checks.require(
        projected_outputs == (-radius, radius),
        f"{name}: exact radial projection",
    )
    checks.require(
        projected_output_distance == 2 * radius,
        f"{name}: exact projected output distance",
    )
    checks.require(
        projection_factor == radius / exterior_radius,
        f"{name}: exact radial-projection factor",
    )
    checks.require(
        composite_modulus == theorem_product,
        f"{name}: composite modulus equals theorem product",
    )
    checks.require(
        classification == expected_classification,
        f"{name}: boundary classification",
    )
    checks.require(
        ("contraction" in classification) == (composite_modulus < 1),
        f"{name}: contraction terminology is restricted to modulus below one",
    )

    return {
        "case": name,
        "input_distance": _ratio_text(input_distance),
        "pre_outputs": [_ratio_text(value) for value in pre_outputs],
        "minimum_pre_projection_norm": _ratio_text(exterior_radius),
        "pre_projection_output_distance": _ratio_text(pre_output_distance),
        "pre_projection_modulus": _ratio_text(pre_modulus),
        "projected_outputs": [_ratio_text(value) for value in projected_outputs],
        "projected_output_distance": _ratio_text(projected_output_distance),
        "radial_projection_factor": _ratio_text(projection_factor),
        "theorem_product": _ratio_text(theorem_product),
        "composite_modulus": _ratio_text(composite_modulus),
        "classification": classification,
        "passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/finite_mdp_certificate_validation/"
            "projection_modulus_exact_checks.json"
        ),
    )
    args = parser.parse_args()

    checks = ExactChecks()
    radius = Fraction(1)
    exterior_radius = Fraction(2)
    factor = radius / exterior_radius

    checks.require(radius > 0, "projection radius is positive")
    checks.require(exterior_radius > radius, "rho is strictly outside the ball")
    checks.require(factor == Fraction(1, 2), "declared projection factor")

    cases = [
        _run_case(
            name="below_one",
            expected_pre_modulus=Fraction(1),
            expected_classification="strict_contraction",
            radius=radius,
            exterior_radius=exterior_radius,
            checks=checks,
        ),
        _run_case(
            name="equal_to_one",
            expected_pre_modulus=Fraction(2),
            expected_classification="unit_modulus",
            radius=radius,
            exterior_radius=exterior_radius,
            checks=checks,
        ),
        _run_case(
            name="above_one",
            expected_pre_modulus=Fraction(4),
            expected_classification="superunit_modulus",
            radius=radius,
            exterior_radius=exterior_radius,
            checks=checks,
        ),
    ]

    checks.require(
        [case["composite_modulus"] for case in cases] == ["1/2", "1", "2"],
        "all three modulus decision regions are represented",
    )
    checks.require(
        sum(case["classification"] == "strict_contraction" for case in cases) == 1,
        "exactly one case is called a strict contraction",
    )

    payload = {
        "schema_version": 1,
        "arithmetic": "fractions.Fraction (exact rational arithmetic)",
        "construction": {
            "domain": "two-point metric space",
            "projection": "one-dimensional radial projection",
            "radius_R": _ratio_text(radius),
            "exterior_radius_rho_R": _ratio_text(exterior_radius),
            "theorem_factor_R_over_rho_R": _ratio_text(factor),
        },
        "formula_checked": (
            "Lip(Pi_R composed with f) = (R/rho_R) Lip(f) "
            "for the retained saturating pairs"
        ),
        "cases": cases,
        "assertions_checked": checks.count,
        "status": "PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
