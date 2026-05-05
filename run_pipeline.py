"""Execute the full A/B testing pipeline."""

import json
from pathlib import Path

from src.simulate import run_simulation
from src.report import generate_report, results_to_json


def main():
    print("Running A/B Test Pipeline...\n")
    results = run_simulation(n_total=5000, seed=42)

    report = generate_report(results)
    print(report)

    output_path = Path("/home/workspace/Projects/ab-testing-eligibility/results.json")
    output_path.write_text(results_to_json(results))
    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    main()