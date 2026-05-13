"""Execute the full A/B testing pipeline and save results."""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simulate import run_simulation, print_results
from src.report import generate_report, save_json_results


def main():
    print("Starting A/B Testing Pipeline...")
    print()

    results = run_simulation()

    print_results(results)

    output_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(output_dir, 'results.json')
    save_json_results(results, json_path)
    print(f"\n[Saved] JSON results: {json_path}")

    report_path = os.path.join(output_dir, 'report.txt')
    report = generate_report(results, filepath=report_path)
    print(f"[Saved] Text report: {report_path}")

    summary = {
        'approval_rate': {
            'control': f"{results['metrics']['approval_rate']['group_a_rate']*100:.2f}%",
            'treatment': f"{results['metrics']['approval_rate']['group_b_rate']*100:.2f}%",
            'diff': f"{results['metrics']['approval_rate']['absolute_diff']*100:+.2f}%",
            'p_value': f"{results['metrics']['approval_rate']['p_value']:.6f}",
            'significant': results['metrics']['approval_rate']['significant']
        },
        'default_rate': {
            'control': f"{results['metrics']['default_rate']['group_a_rate']*100:.2f}%",
            'treatment': f"{results['metrics']['default_rate']['group_b_rate']*100:.2f}%",
            'diff': f"{results['metrics']['default_rate']['absolute_diff']*100:+.2f}%",
            'p_value': f"{results['metrics']['default_rate']['p_value']:.6f}",
            'significant': results['metrics']['default_rate']['significant']
        }
    }

    print("\n[Pipeline Complete]")
    return summary


if __name__ == '__main__':
    summary = main()