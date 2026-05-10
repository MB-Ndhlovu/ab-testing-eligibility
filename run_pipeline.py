"""Execute the full A/B testing pipeline."""

import os
from src.simulate import run_experiment
from src.report import generate_report, save_json


def main():
    print("Running A/B Test Pipeline...\n")
    results = run_experiment()
    generate_report(results)
    save_json(results, "ab_test_results.json")
    return results


if __name__ == "__main__":
    main()