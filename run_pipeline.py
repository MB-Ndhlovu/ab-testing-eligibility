"""
Execute the full A/B testing pipeline:
generate data → run statistical tests → print report → save JSON.
"""

import json
from src.simulate import run_experiment
from src.report import generate_report


def main():
    results = run_experiment()

    report = generate_report(results)
    print(report)

    # Save JSON results
    out_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=float)

    print(f"\n  Results saved to: {out_path}")


if __name__ == "__main__":
    main()