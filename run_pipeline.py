"""
Execute full A/B test pipeline.
"""
import json
from src.simulate import run_simulation
from src.report import generate_report, save_results_json


def main():
    print("Running A/B test simulation...\n")
    results = run_simulation(seed=42)

    report = generate_report(results)
    print(report)

    save_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    save_results_json(results, save_path)
    print(f"\nResults saved to: {save_path}")

    return results


if __name__ == "__main__":
    main()