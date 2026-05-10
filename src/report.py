"""Generate readable summary reports for A/B test results."""
import json
import numpy as np
from src.simulate import run_experiment, summarize_results


def generate_report(results, output_path='results.json'):
    """Generate and save experiment report.

    Args:
        results: Experiment results dictionary
        output_path: Path to save JSON results

    Returns:
        Human-readable report string
    """
    # Save JSON results
    serializable_results = {
        'sample_size': results['sample_size'],
        'alpha': results['alpha'],
        'power': results['power'],
        'mde': results['mde'],
        'group_a': {k: float(v) if isinstance(v, (int, float)) else v
                    for k, v in results['group_a'].items()},
        'group_b': {k: float(v) if isinstance(v, (int, float)) else v
                    for k, v in results['group_b'].items()},
        'approval_rate_test': {k: float(v) if isinstance(v, (int, float, np.floating)) else bool(v) if isinstance(v, (bool, np.bool_)) else v
                               for k, v in results['approval_rate_test'].items()},
        'default_rate_test': {k: float(v) if isinstance(v, (int, float, np.floating)) else bool(v) if isinstance(v, (bool, np.bool_)) else v
                              for k, v in results['default_rate_test'].items()},
        'treatment_effect': results['treatment_effect']
    }

    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2)

    # Generate human-readable summary
    summary = summarize_results(results)
    summary += f"\nResults saved to: {output_path}\n"
    summary += "=" * 60

    return summary


if __name__ == '__main__':
    results = run_experiment()
    report = generate_report(results)
    print(report)