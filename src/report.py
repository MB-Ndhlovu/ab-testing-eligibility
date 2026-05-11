"""Generate human-readable summary report."""

import json
from typing import Dict


def format_result(result: Dict, metric_label: str) -> str:
    """Format a single test result nicely."""
    sig = "✓ SIGNIFICANT" if result['significant'] else "✗ NOT SIGNIFICANT"
    return f"""
  {metric_label}
  ─────────────────────────────────────────
  Group A (Control):     {result['group_a_value']:.4f}
  Group B (Treatment):   {result['group_b_value']:.4f}
  Treatment Effect:      {result['treatment_effect']:+.4f}
  z-statistic:           {result['z_statistic']:.4f}
  p-value:              {result['p_value']:.6f}
  95% Confidence Interval: [{result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f}]
  Statistical Decision (α=0.05): {sig}
"""


def generate_report(results: Dict) -> str:
    """Build full report from experiment results."""

    ma = results['metrics_a']
    mb = results['metrics_b']
    ap = results['approval_rate_test']
    dr = results['default_rate_test']

    report = """
╔══════════════════════════════════════════════════════════════╗
║        A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY              ║
║                        FINAL REPORT                           ║
╚══════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│  SAMPLE SIZES                                                │
│  Control (Group A): 2,500 applicants                         │
│  Treatment (Group B): 2,500 applicants                      │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  DESCRIPTIVE METRICS                                         │
│                                                              │
│  Metric                 Group A      Group B      Effect     │
│  ─────────────────────────────────────────────────────────  │"""

    for key in ['approval_rate', 'default_rate', 'avg_loan_size', 'avg_processing_time']:
        v1 = ma[key]
        v2 = mb[key]
        eff = v2 - v1
        report += f"\n│  {key:<20} {v1:>9.4f}   {v2:>9.4f}   {eff:>+8.4f}   │"

    report += f"""
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  APPROVAL RATE TEST                                          │
│  H₀: No difference in approval rates between groups          │"""

    report += format_result(ap, "")
    report += f"""
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  DEFAULT RATE TEST                                           │
│  H₀: No difference in default rates between groups          │"""
    report += format_result(dr, "")
    report += """
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SUMMARY & RECOMMENDATION                                    │
│                                                              │"""

    both_sig = ap['significant'] and dr['significant']
    if both_sig:
        recommendation = (
            "  The new credit eligibility model (B) is recommended.\n"
            "  It shows a statistically significant increase in approval rate\n"
            "  and a statistically significant decrease in default rate.\n"
            "  Both primary metrics moved in the favorable direction."
        )
    elif ap['significant'] and not dr['significant']:
        recommendation = (
            "  Mixed results: approval rate improved significantly but\n"
            "  default rate change is not statistically significant.\n"
            "  Further analysis recommended before full deployment."
        )
    elif not ap['significant'] and dr['significant']:
        recommendation = (
            "  Mixed results: default rate improved significantly but\n"
            "  approval rate change is not statistically significant.\n"
            "  Further analysis recommended before full deployment."
        )
    else:
        recommendation = (
            "  Neither metric showed a statistically significant difference\n"
            "  at α=0.05. The new model does not demonstrate sufficient\n"
            "  improvement over the current model to justify adoption."
        )

    report += recommendation
    report += """
└──────────────────────────────────────────────────────────────┘
"""

    return report


def save_results_json(results: Dict, filepath: str = 'results.json'):
    """Save results dict to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[OUTPUT] Results saved to {filepath}")


if __name__ == '__main__':
    from src.simulate import run_experiment
    results = run_experiment()
    report = generate_report(results)
    print(report)