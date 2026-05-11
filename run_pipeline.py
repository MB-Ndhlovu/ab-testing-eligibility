"""
Orchestrates the full A/B test pipeline:
  1. Generate / load synthetic data
  2. Run experiment simulation
  3. Print human-readable report
  4. Save results as JSON
"""

import json
import sys
import pandas as pd
from src.data_generator import get_summary_stats
from src.simulate import run_experiment
from src.report import generate_report

def main():
    print("Generating synthetic data...")
    from src import data_generator
    df = pd.DataFrame({
        "group": data_generator.group,
        "approved": data_generator.approved,
        "defaulted": data_generator.defaulted,
        "loan_size": data_generator.loan_size,
        "processing_time": data_generator.processing_time,
    })

    print("Running experiment simulation...")
    results = run_experiment(df)

    print("\n" + generate_report(results))

    out_path = "ab_test_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=lambda x: float(x) if isinstance(x, (float,)) else int(x))
    print(f"\nResults saved to {out_path}")

    # Exit with non-zero if any key test was not significant
    approval_sig = results["approval_rate"]["significant"]
    default_sig  = results["default_rate"]["significant"]
    print(f"\nApproval Rate significant: {approval_sig}")
    print(f"Default Rate significant: {default_sig}")

    return 0

if __name__ == "__main__":
    sys.exit(main())