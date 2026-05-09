"""Run the A/B experiment simulation and compute treatment effects."""

from src.data_generator import generate_data, summarize
from src.statistical import two_proportion_ztest, compute_power


def run_simulation():
    # Generate data
    df = generate_data()
    summary = summarize(df)

    n_a = summary["A"]["n_total"]
    n_b = summary["B"]["n_total"]
    n_approved_a = summary["A"]["n_approved"]
    n_approved_b = summary["B"]["n_approved"]
    n_defaulted_a = int(summary["A"]["default_rate"] * n_approved_a)
    n_defaulted_b = int(summary["B"]["default_rate"] * n_approved_b)

    # Approval rate test
    approval_test = two_proportion_ztest(n_approved_a, n_a, n_approved_b, n_b)

    # Default rate test (among approved)
    default_test = two_proportion_ztest(n_defaulted_a, n_approved_a, n_defaulted_b, n_approved_b)

    # Power
    approval_power = compute_power(n_a, n_b, summary["A"]["approval_rate"], summary["B"]["approval_rate"])
    default_power = compute_power(n_approved_a, n_approved_b, summary["A"]["default_rate"], summary["B"]["default_rate"])

    return {
        "summary": summary,
        "approval_rate_test": approval_test,
        "default_rate_test": default_test,
        "approval_power": approval_power,
        "default_power": default_power,
    }


if __name__ == "__main__":
    results = run_simulation()
    import json
    print(json.dumps(results, indent=2))