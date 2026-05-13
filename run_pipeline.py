#!/usr/bin/env python3
"""Execute the full A/B test pipeline for credit eligibility."""

import json
import os
from src.simulate import run_simulation, print_simulation_results
from src.report import generate_report, save_json_results


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(project_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    print("\n🚀 Starting A/B Test Pipeline...")
    print("=" * 60)

    results = run_simulation(n_per_group=5000)

    print_simulation_results(results)

    report_path = os.path.join(results_dir, "ab_test_report.txt")
    report = generate_report(results, output_path=report_path)

    json_path = os.path.join(results_dir, "ab_test_results.json")
    save_json_results(results, json_path)

    print(f"\n✅ Pipeline complete!")
    print(f"   Report saved to: {report_path}")
    print(f"   JSON saved to:   {json_path}")

    return results


if __name__ == "__main__":
    main()