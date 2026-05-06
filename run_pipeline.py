"""
A/B Testing Pipeline — Credit Eligibility
Executes the full experiment: generate data, run stats, print report, save JSON.
"""
import os
import json
import numpy as np

np.random.seed(None)  # use true randomness for the pipeline run

from src.simulate import run_experiment, save_results
from src.report import generate_report

def main():
    print("Generating synthetic data...")
    summary, analysis, df = run_experiment()

    print("\n" + generate_report(summary, analysis))

    # Save JSON
    output_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(output_dir, "results.json")
    save_results(summary, analysis, results_path)
    print(f"\nResults saved to: {results_path}")

    # Save the raw data
    data_path = os.path.join(output_dir, "experiment_data.csv")
    df.to_csv(data_path, index=False)
    print(f"Raw data saved to: {data_path}")

    # Print the JSON-friendly summary for Telegram
    output_summary = {
        "approval_rate": {
            "group_A": f"{analysis['approval_rate']['group_A']:.2%}",
            "group_B": f"{analysis['approval_rate']['group_B']:.2%}",
            "difference": f"{analysis['approval_rate']['difference']:+.2%}",
            "z_statistic": analysis['approval_rate']['z_statistic'],
            "p_value": analysis['approval_rate']['p_value'],
            "ci_95": f"[{analysis['approval_rate']['ci_lower']:.2%}, {analysis['approval_rate']['ci_upper']:.2%}]",
            "significant": bool(analysis['approval_rate']['significant']),
        },
        "default_rate": {
            "group_A": f"{analysis['default_rate']['group_A']:.2%}",
            "group_B": f"{analysis['default_rate']['group_B']:.2%}",
            "difference": f"{analysis['default_rate']['difference']:+.2%}",
            "z_statistic": analysis['default_rate']['z_statistic'],
            "p_value": analysis['default_rate']['p_value'],
            "ci_95": f"[{analysis['default_rate']['ci_lower']:.2%}, {analysis['default_rate']['ci_upper']:.2%}]",
            "significant": bool(analysis['default_rate']['significant']),
        },
    }
    print("\n--- JSON OUTPUT SUMMARY ---")
    print(json.dumps(output_summary, indent=2))

if __name__ == "__main__":
    main()