"""Run the A/B experiment simulation and compute treatment effects."""

import json
import numpy as np
from src.data_generator import generate_applicants, assign_outcomes, compute_summary
from src.statistical import two_proportion_ztest, compute_power, minimum_detectable_effect


def make_json_safe(obj):
    """Convert numpy types to native Python for JSON serialization."""
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(v) for v in obj]
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    return obj


def run_experiment(n: int = 5000, seed: int = 42) -> dict:
    """
    Execute the full A/B experiment pipeline.
    """
    df = generate_applicants(n)
    df = assign_outcomes(df)
    summary = compute_summary(df)

    results = {}

    for metric in ["approval_rate", "default_rate"]:
        grp_a = summary["A"]
        grp_b = summary["B"]

        if metric == "approval_rate":
            conv_a = int(grp_a["approval_rate"] * grp_a["n"])
            conv_b = int(grp_b["approval_rate"] * grp_b["n"])
            n_a = grp_a["n"]
            n_b = grp_b["n"]
        else:
            n_approved_a = int(grp_a["approval_rate"] * grp_a["n"])
            n_approved_b = int(grp_b["approval_rate"] * grp_b["n"])
            conv_a = int(grp_a["default_rate"] * n_approved_a)
            conv_b = int(grp_b["default_rate"] * n_approved_b)
            n_a = n_approved_a
            n_b = n_approved_b

        z_result = two_proportion_ztest(
            n_treatment=n_b,
            n_control=n_a,
            conversions_treatment=conv_b,
            conversions_control=conv_a,
            alpha=0.05,
            alternative="two-sided",
        )

        results[metric] = {
            "group_A": {
                "rate": round(float(grp_a[metric]), 4),
                "n": n_a,
                "conversions": conv_a,
            },
            "group_B": {
                "rate": round(float(grp_b[metric]), 4),
                "n": n_b,
                "conversions": conv_b,
            },
            "treatment_effect": float(z_result.point_estimate),
            "z_statistic": float(z_result.z_statistic),
            "p_value": float(z_result.p_value),
            "ci_lower": float(z_result.ci_lower),
            "ci_upper": float(z_result.ci_upper),
            "significant": bool(z_result.significant),
        }

    # Power analysis
    p_approval_a = summary["A"]["approval_rate"]
    p_approval_b = summary["B"]["approval_rate"]
    mde_approval = abs(p_approval_b - p_approval_a)

    power_approval = compute_power(n, float(p_approval_a), float(mde_approval), alpha=0.05)
    mde_required  = minimum_detectable_effect(n, float(p_approval_a), alpha=0.05, power=0.80)

    def safe_float(v):
        return round(float(v), 4)

    results["_meta"] = {
        "n_total": n,
        "power_approval_test": float(power_approval),
        "mde_observed": safe_float(mde_approval),
        "mde_required_for_80_power": safe_float(mde_required),
        "group_a_summary": {k: safe_float(v) if isinstance(v, float) else v
                            for k, v in summary["A"].items()},
        "group_b_summary": {k: safe_float(v) if isinstance(v, float) else v
                            for k, v in summary["B"].items()},
    }

    return make_json_safe(results)


if __name__ == "__main__":
    results = run_experiment()
    print(json.dumps(results, indent=2))