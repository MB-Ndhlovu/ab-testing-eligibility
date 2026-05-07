"""Execute the full A/B testing pipeline."""
import json
from src.simulate import run_experiment
from src.report import generate_report, save_json_report


def main():
    print("Running A/B experiment simulation...\n")
    results = run_experiment(n=5000)

    # Save JSON
    save_json_report(results, "ab_test_results.json")
    print("Results saved to ab_test_results.json\n")

    # Print readable report
    report = generate_report(results)
    print(report)

    return results


if __name__ == "__main__":
    main()
