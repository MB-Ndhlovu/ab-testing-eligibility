import json
import sys
from src.simulate import run_simulation
from src.report import generate_report

ALPHA = 0.05
OUTPUT_JSON = "ab_test_results.json"


def main():
    print("Running A/B Test Simulation...\n")
    results = run_simulation(alpha=ALPHA)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(results, f, indent=2, default=float)

    report = generate_report(results)
    print(report)
    print(f"\nResults saved to: {OUTPUT_JSON}")

    return results


if __name__ == "__main__":
    results = main()
    sys.exit(0)