#!/usr/bin/env python3
"""Execute the full A/B test pipeline end-to-end."""

import json
import sys
from pathlib import Path

from src.simulate import run_experiment
from src.report import generate_report


def main():
    project_root = Path(__file__).parent
    output_json  = project_root / "results.json"
    output_txt  = project_root / "report.txt"

    print("Running A/B experiment simulation...\n")

    # Run experiment
    results = run_experiment(n=5000, seed=42)

    # Save JSON
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)

    # Generate and print human-readable report
    report = generate_report(results)
    print(report)

    # Save report
    with open(output_txt, "w") as f:
        f.write(report)

    print(f"\nResults saved to {output_json}")
    print(f"Report saved to {output_txt}")

    # Exit with non-zero if any key metric is not significant
    appr_sig = results["approval_rate"]["significant"]
    defr_sig = results["default_rate"]["significant"]

    if not (appr_sig or defr_sig):
        print("\n⚠ Neither metric showed significance — consider a larger sample.")
        sys.exit(1)
    else:
        print("\n✓ Experiment completed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()