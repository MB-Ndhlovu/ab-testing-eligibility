"""Run the A/B experiment simulation."""

from src.data_generator import generate_data
from src.statistical import analyze_metric


def run():
    data = generate_data()
    a = data["group_a"]
    b = data["group_b"]

    results = {}

    results["approval_rate"] = analyze_metric(
        "approval_rate",
        n_a=a["n"], rate_a=a["approval_rate"],
        n_b=b["n"], rate_b=b["approval_rate"],
    )

    results["default_rate"] = analyze_metric(
        "default_rate",
        n_a=a["n"], rate_a=a["default_rate"],
        n_b=b["n"], rate_b=b["default_rate"],
    )

    return {
        "data": data,
        "stats": results,
    }