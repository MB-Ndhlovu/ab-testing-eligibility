"""Execute the full A/B testing pipeline."""

import json
from src.simulate import run_experiment
from src.report import generate_report, results_to_json

def main():
    print("Running A/B Testing Pipeline...")
    print("-" * 40)

    # Run experiment
    results = run_experiment(n=5000, seed=42)

    # Generate and print report
    report = generate_report(results)
    print(report)

    # Save JSON results
    output = results_to_json(results)
    with open('results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\n[OUTPUT]")
    print("  Results saved to: results.json")
    print("-" * 40)

    return results

if __name__ == '__main__':
    results = main()
