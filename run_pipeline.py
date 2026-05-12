"""Execute the full A/B testing pipeline."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.simulate import run_experiment, summarize_results
from src.report import generate_report, save_json_results


def main():
    print("Running A/B Test Experiment...")
    print("-" * 40)

    experiment = run_experiment(seed=42, n_per_group=2500)

    summary = summarize_results(experiment)
    print(summary)

    report = generate_report(experiment)
    print("\n" + "=" * 60)
    print("MARKDOWN REPORT")
    print("=" * 60)
    print(report)

    save_json_results(experiment, "ab_test_results.json")
    print("\nPipeline complete.")


if __name__ == "__main__":
    main()