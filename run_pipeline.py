"""Execute full A/B test pipeline."""

import json
from src.simulate import run_experiment
from src.report import generate_report, save_results_json


def main():
    print("\nStarting A/B Testing Pipeline...\n")

    results = run_experiment()
    report = generate_report(results)
    print(report)

    save_results_json(results, 'results.json')

    output_summary = {
        'approval_rate': {
            'group_a': results['metrics_a']['approval_rate'],
            'group_b': results['metrics_b']['approval_rate'],
            'effect': results['approval_rate_test']['treatment_effect'],
            'p_value': results['approval_rate_test']['p_value'],
            'significant': results['approval_rate_test']['significant']
        },
        'default_rate': {
            'group_a': results['metrics_a']['default_rate'],
            'group_b': results['metrics_b']['default_rate'],
            'effect': results['default_rate_test']['treatment_effect'],
            'p_value': results['default_rate_test']['p_value'],
            'significant': results['default_rate_test']['significant']
        }
    }

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\nResults saved to results.json")
    print(f"\nApproval Rate: A={output_summary['approval_rate']['group_a']:.4f}, "
          f"B={output_summary['approval_rate']['group_b']:.4f}, "
          f"effect={output_summary['approval_rate']['effect']:+.4f}, "
          f"p={output_summary['approval_rate']['p_value']:.6f}, "
          f"sig={output_summary['approval_rate']['significant']}")
    print(f"Default Rate: A={output_summary['default_rate']['group_a']:.4f}, "
          f"B={output_summary['default_rate']['group_b']:.4f}, "
          f"effect={output_summary['default_rate']['effect']:+.4f}, "
          f"p={output_summary['default_rate']['p_value']:.6f}, "
          f"sig={output_summary['default_rate']['significant']}")

    return output_summary


if __name__ == '__main__':
    main()