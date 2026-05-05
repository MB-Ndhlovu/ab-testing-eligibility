import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src.simulate import run_experiment
from src.report import generate_report, save_results_json


def main():
    print("Running A/B Test Pipeline...\n")

    results = run_experiment(n_applicants=5000)

    report = generate_report(results)
    print(report)

    output_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(output_dir, "ab_test_results.json")
    save_results_json(results, json_path)
    print(f"\nResults saved to: {json_path}")

    return results


if __name__ == "__main__":
    main()