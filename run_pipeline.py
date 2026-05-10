"""Execute the full A/B test pipeline and save results."""

import json
import os
from src.report import generate_report
from src.simulate import run_simulation

OUTPUT_DIR = "/home/workspace/Projects/ab-testing-eligibility"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print("Running A/B Test Pipeline...\n")
    report = generate_report(seed=42)
    print(report)

    results = run_simulation(seed=42)

    json_path = os.path.join(OUTPUT_DIR, "results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {json_path}")


if __name__ == "__main__":
    main()