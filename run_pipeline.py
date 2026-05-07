"""
Executes the full A/B testing pipeline end-to-end.
"""

import json
import sys
from src.simulate import run_simulation
from src.report import generate_report, results_to_dict


def main():
    print("Starting A/B Testing Pipeline...\n")

    results = run_simulation(seed=42)
    report = generate_report(results)
    print(report)

    # Save JSON output
    output_dict = results_to_dict(results)
    json_path = '/home/workspace/Projects/ab-testing-eligibility/results.json'
    with open(json_path, 'w') as f:
        json.dump(output_dict, f, indent=2)

    print(f"\n[OUTPUT] Results saved to results.json")

    # Build a compact summary for Telegram
    approval = results['tests']['approval_rate']
    default = results['tests']['default_rate']
    approval_sig = "✓ SIGNIFICANT" if approval['significant'] else "✗ not significant"
    default_sig = "✓ SIGNIFICANT" if default['significant'] else "✗ not significant"

    summary = (
        f"Approval Rate: Group A={results['stats']['A']['approval_rate']:.4f}  "
        f"Group B={results['stats']['B']['approval_rate']:.4f}  "
        f"z={approval['z_statistic']:.3f}  p={approval['p_value']:.4f}  "
        f"95% CI=[{approval['ci_95'][0]:+.4f}, {approval['ci_95'][1]:+.4f}]  "
        f"{approval_sig}\n"
        f"Default Rate: Group A={results['stats']['A']['default_rate']:.4f}  "
        f"Group B={results['stats']['B']['default_rate']:.4f}  "
        f"z={default['z_statistic']:.3f}  p={default['p_value']:.4f}  "
        f"95% CI=[{default['ci_95'][0]:+.4f}, {default['ci_95'][1]:+.4f}]  "
        f"{default_sig}"
    )

    print(f"\n[SUMMARY FOR COMMIT]\n{summary}")

    return output_dict


if __name__ == '__main__':
    main()