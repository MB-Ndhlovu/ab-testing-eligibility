"""Run A/B experiment simulation."""

from src.data_generator import generate_data
from src.statistical import two_proportion_z_test, confidence_interval


ALPHA = 0.05


def run_simulation():
    """Run the full experiment simulation."""
    data = generate_data()

    results = {}
    for metric in ["approval_rate", "default_rate"]:
        p_a = data["group_a"]["metrics"][metric]
        p_b = data["group_b"]["metrics"][metric]
        n_a = data["group_a"]["n"]
        n_b = data["group_b"]["n"]

        z_test = two_proportion_z_test(n_a, p_a, n_b, p_b)
        ci = confidence_interval(p_a, p_b, n_a, n_b)

        results[metric] = {
            "group_a": float(round(p_a, 4)),
            "group_b": float(round(p_b, 4)),
            "z_statistic": float(round(z_test["z"], 4)),
            "p_value": float(round(z_test["p_value"], 6)),
            "ci_95_lower": float(round(ci[0], 4)),
            "ci_95_upper": float(round(ci[1], 4)),
            "significant": bool(z_test["p_value"] < ALPHA),
            "mde": float(round(abs(p_b - p_a), 4)),
        }

    return results