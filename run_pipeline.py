#!/usr/bin/env python3
"""
Execute the full A/B test pipeline.

Usage:
    python run_pipeline.py
"""

import json
import os
from src.simulate import run_experiment
from src.report import generate_report, save_json_results


def main():
    print("Starting A/B Testing Pipeline...")
    print()

    # Run experiment
    print("Running experiment simulation...")
    results = run_experiment(n=5000, seed=42, alpha=0.05)

    # Generate report
    print("Generating report...")
    report = generate_report(results)
    print(report)

    # Save outputs
    output_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(output_dir, 'results.json')
    save_json_results(results, json_path)
    print(f"\nResults saved to: {json_path}")

    report_path = os.path.join(output_dir, 'report.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_path}")

    # Summary for Telegram
    approval_sig = results['tests']['approval_rate']['significant']
    default_sig = results['tests']['default_rate']['significant']
    approval_diff = results['tests']['approval_rate']['difference']
    default_diff = results['tests']['default_rate']['difference']

    print("\n" + "=" * 60)
    print("TELEGRAM SUMMARY:")
    print("=" * 60)
    print(f"Approval Rate: {'SIGNIFICANT' if approval_sig else 'NOT SIGNIFICANT'} (diff: {approval_diff:+.4f})")
    print(f"Default Rate:  {'SIGNIFICANT' if default_sig else 'NOT SIGNIFICANT'} (diff: {default_diff:+.4f})")

    if approval_sig and default_sig and approval_diff > 0 and default_diff < 0:
        print("Recommendation: ADOPT new model")
    elif approval_sig or default_sig:
        print("Recommendation: ADOPT with monitoring")
    else:
        print("Recommendation: No significant difference - more data needed")

    return results


if __name__ == '__main__':
    results = main()