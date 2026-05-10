"""
Execute the full A/B testing pipeline.
Generates data, runs statistical tests, prints report, saves JSON.
"""

import json
import sys
from pathlib import Path

from src.simulate import run_experiment
from src.report import generate_report


def main():
    project_root = Path(__file__).parent
    output_path = project_root / "results.json"

    print("Running A/B experiment simulation...\n")

    results = run_experiment(n=5000)
    report = generate_report(results)

    print(report)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    results = main()