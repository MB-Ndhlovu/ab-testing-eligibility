"""Execute the full A/B test pipeline."""

import json
import os
from src.simulate import run_simulation
from src.report import generate_report, save_json


def main():
    print("Running A/B test pipeline...\n")
    results = run_simulation()

    report = generate_report(results)
    print(report)
    print()

    out_path = os.path.join(os.path.dirname(__file__), "results.json")
    save_json(results, out_path)
    print(f"Results saved to {out_path}")

    return results


if __name__ == "__main__":
    main()