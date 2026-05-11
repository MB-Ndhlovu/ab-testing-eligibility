"""Execute the full A/B testing pipeline."""
import json
import sys
sys.path.insert(0, "/home/workspace/Projects/ab-testing-eligibility")

from src.data_generator import group_a, group_b, summary_stats
from src.simulate import run_experiment
from src.report import generate_report

def main():
    print("Generating synthetic data...")
    from src import data_generator  # trigger side effects (seeded globals)

    print("Running experiment simulation...")
    results = run_experiment()

    print("Generating report...")
    report_text, output_json = generate_report(results)

    # Print human-readable report
    print(report_text)

    # Save JSON
    out_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(out_path, "w") as f:
        json.dump(output_json, f, indent=2, default=float)
    print(f"\n  Results saved to: {out_path}")

    return output_json

if __name__ == "__main__":
    main()