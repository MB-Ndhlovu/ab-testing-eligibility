"""Execute the full A/B test pipeline and save results."""

import json
import os
import numpy as np

def make_serializable(obj):
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    return obj

from src.simulate import run_simulation
from src.report import generate_report

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    print("Running A/B test pipeline...\n")
    results = run_simulation()
    results = make_serializable(results)

    # Save JSON
    json_path = os.path.join(OUTPUT_DIR, "results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved results to {json_path}")

    # Print report
    report = generate_report(results)
    print(report)

    return results


if __name__ == "__main__":
    main()