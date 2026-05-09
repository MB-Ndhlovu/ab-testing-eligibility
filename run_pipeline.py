"""Execute the full A/B testing pipeline."""

import json
import numpy as np
from src.simulate import run_experiment, interpret_results
from src.report import generate_report

np.random.seed(42)


def main():
    print("Running A/B Test Experiment...")
    print("-" * 40)

    # Run experiment
    results = run_experiment(n_samples=5000, alpha=0.05)

    # Generate and print report
    report = generate_report(results)
    print(report)

    # Prepare JSON-serializable summary
    summary = {
        "group_a": {
            "n": int(results["group_a"]["n"]),
            "approval_rate": round(results["group_a"]["approval_rate"], 6),
            "default_rate": round(results["group_a"]["default_rate"], 6),
            "avg_loan_size": round(results["group_a"]["avg_loan_size"], 4),
            "avg_processing_time": round(results["group_a"]["avg_processing_time"], 4),
        },
        "group_b": {
            "n": int(results["group_b"]["n"]),
            "approval_rate": round(results["group_b"]["approval_rate"], 6),
            "default_rate": round(results["group_b"]["default_rate"], 6),
            "avg_loan_size": round(results["group_b"]["avg_loan_size"], 4),
            "avg_processing_time": round(results["group_b"]["avg_processing_time"], 4),
        },
        "approval_rate_test": {
            "z_statistic": round(results["approval_rate_test"]["z_statistic"], 4),
            "p_value": round(results["approval_rate_test"]["p_value"], 6),
            "ci_lower": round(results["approval_rate_test"]["ci_lower"], 6),
            "ci_upper": round(results["approval_rate_test"]["ci_upper"], 6),
            "difference": round(results["approval_rate_test"]["difference"], 6),
            "power": round(results["approval_power"], 4),
            "mde": round(results["approval_mde"], 4),
            "significant": bool(results["approval_rate_test"]["p_value"] < results["alpha"]),
        },
        "default_rate_test": {
            "z_statistic": round(results["default_rate_test"]["z_statistic"], 4),
            "p_value": round(results["default_rate_test"]["p_value"], 6),
            "ci_lower": round(results["default_rate_test"]["ci_lower"], 6),
            "ci_upper": round(results["default_rate_test"]["ci_upper"], 6),
            "difference": round(results["default_rate_test"]["difference"], 6),
            "power": round(results["default_power"], 4),
            "mde": round(results["default_mde"], 4),
            "significant": bool(results["default_rate_test"]["p_value"] < results["alpha"]),
        },
        "alpha": results["alpha"],
        "interpretations": interpret_results(results),
    }

    # Save JSON output
    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    print("\n" + "=" * 70)
    print("JSON SUMMARY")
    print("=" * 70)
    print(json.dumps(summary, indent=2))

    return summary


if __name__ == "__main__":
    main()