"""
Execute the full A/B testing pipeline.
"""
import json
from src.report import generate_report
from src.simulate import run_simulation
from src.data_generator import summary_a, summary_b

OUTPUT_JSON = "ab_test_results.json"


def main():
    print("Running A/B test pipeline...\n")
    report = generate_report()
    print(report)

    # Save results as JSON
    sim = run_simulation()
    output = {
        "summary_a": summary_a,
        "summary_b": summary_b,
        "tests": sim,
    }
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2, default=float)

    print(f"\n[Pipeline complete] Results saved to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()