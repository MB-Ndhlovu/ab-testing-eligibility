"""
End-to-end A/B test pipeline for credit eligibility.
"""

import os
from src.simulate import run_experiment
from src.report import generate_report, results_to_json

def main():
    print("Running A/B test pipeline for credit eligibility...\n")

    results = run_experiment(n=5000, alpha=0.05, seed=42)
    report = generate_report(results)
    print(report)

    # Save JSON
    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, "results.json")
    results_to_json(results, json_path)
    print(f"\n[Results saved to results.json]\n")

if __name__ == "__main__":
    main()