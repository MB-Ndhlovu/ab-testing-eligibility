"""Generate readable summary reports for A/B test results."""

import json
from datetime import datetime


def generate_report(results, format='text'):
    """
    Generate a formatted report from experiment results.

    Args:
        results: dict from run_experiment()
        format: 'text' or 'markdown'

    Returns:
        Formatted report string
    """
    if format == 'markdown':
        return generate_markdown_report(results)
    else:
        return generate_text_report(results)


def generate_markdown_report(results):
    """Generate markdown-formatted report."""
    a = results['metrics']['A']
    b = results['metrics']['B']
    ap = results['stats']['approval']
    dp = results['stats']['default']
    te = results['treatment_effect']

    report = f"""# A/B Test Results: Credit Eligibility Model

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

| Metric | Group A (Control) | Group B (Treatment) | Difference | P-value | Significant? |
|--------|-------------------|---------------------|------------|---------|--------------|
| Approval Rate | {a['approval_rate']:.4f} | {b['approval_rate']:.4f} | {ap['diff']:+.4f} | {ap['p_value']:.6f} | {'✅ YES' if ap['significant'] else '❌ NO'} |
| Default Rate | {a['default_rate']:.4f} | {b['default_rate']:.4f} | {dp['diff']:+.4f} | {dp['p_value']:.6f} | {'✅ YES' if dp['significant'] else '❌ NO'} |

## Sample Information

- **Total Sample Size:** {results['n']}
- **Control Group (A):** {a['n']} applicants
- **Treatment Group (B):** {b['n']} applicants
- **Significance Level (α):** {results['alpha']}

## Approval Rate Analysis

| Statistic | Value |
|-----------|-------|
| Control Rate | {ap['control_rate']:.4f} ({a['approved_count']}/{a['n']}) |
| Treatment Rate | {ap['treatment_rate']:.4f} ({b['approved_count']}/{b['n']}) |
| Difference | {ap['diff']:+.4f} ({ap['diff']*100:+.2f}%) |
| 95% Confidence Interval | [{ap['ci_lower']:.4f}, {ap['ci_upper']:.4f}] |
| Z-statistic | {ap['z_statistic']:.4f} |
| P-value | {ap['p_value']:.6f} |
| Statistical Power | {ap['power']:.4f} |
| Minimum Detectable Effect | {ap['mde']:.4f} |

**Conclusion:** {'The difference in approval rates is statistically significant.' if ap['significant'] else 'The difference in approval rates is NOT statistically significant.'}

## Default Rate Analysis

| Statistic | Value |
|-----------|-------|
| Control Rate | {dp['control_rate']:.4f} ({a['default_count']}/{a['approved_count']} of approved) |
| Treatment Rate | {dp['treatment_rate']:.4f} ({b['default_count']}/{b['approved_count']} of approved) |
| Difference | {dp['diff']:+.4f} ({dp['diff']*100:+.2f}%) |
| 95% Confidence Interval | [{dp['ci_lower']:.4f}, {dp['ci_upper']:.4f}] |
| Z-statistic | {dp['z_statistic']:.4f} |
| P-value | {dp['p_value']:.6f} |

**Conclusion:** {'The difference in default rates is statistically significant.' if dp['significant'] else 'The difference in default rates is NOT statistically significant.'}

## Additional Metrics

| Metric | Group A | Group B |
|--------|---------|---------|
| Avg Loan Size ($k) | {a['avg_loan_size']:.2f} | {b['avg_loan_size']:.2f} |
| Avg Processing Time (min) | {a['avg_processing_time']:.2f} | {b['avg_processing_time']:.2f} |

## Interpretation

- **Approval Rate Lift:** {te['approval_rate_lift']*100:+.2f}%
- **Default Rate Lift:** {te['default_rate_lift']*100:+.2f}%

"""

    if ap['significant'] and dp['significant']:
        report += """## Final Recommendation

**DEPLOY THE NEW MODEL (Group B)**

The new credit eligibility model significantly outperforms the current model on both key metrics:
1. Higher approval rate (more loans originated)
2. Lower default rate (better credit quality)

"""
    elif ap['significant'] or dp['significant']:
        report += """## Final Recommendation

**CONDITIONAL DEPLOYMENT**

The new model shows improvement on one metric but not both. Consider:
- If only approval rate improved: Review risk profile before full deployment
- If only default rate improved: May indicate stricter eligibility criteria

"""
    else:
        report += """## Final Recommendation

**GATHER MORE DATA**

No statistically significant difference detected. The experiment may be underpowered
or the true effect size is smaller than expected. Consider:
- Increasing sample size
- Running a longer experiment
- Accepting current model performance

"""

    return report


def generate_text_report(results):
    """Generate plain text report."""
    a = results['metrics']['A']
    b = results['metrics']['B']
    ap = results['stats']['approval']
    dp = results['stats']['default']
    te = results['treatment_effect']

    lines = [
        "=" * 70,
        "A/B TESTING FRAMEWORK - CREDIT ELIGIBILITY",
        "=" * 70,
        "",
        f"Experiment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Sample Size: {results['n']}",
        f"Significance Level: α = {results['alpha']}",
        "",
        "-" * 70,
        "SAMPLE METRICS",
        "-" * 70,
        f"Group A (Control): {a['n']} applicants, {a['approved_count']} approved ({a['approval_rate']:.4f})",
        f"Group B (Treatment): {b['n']} applicants, {b['approved_count']} approved ({b['approval_rate']:.4f})",
        "",
        "-" * 70,
        "APPROVAL RATE TEST",
        "-" * 70,
        f"Control rate:     {ap['control_rate']:.4f}",
        f"Treatment rate:   {ap['treatment_rate']:.4f}",
        f"Difference:       {ap['diff']:+.4f} ({ap['diff']*100:+.2f}%)",
        f"95% CI:          [{ap['ci_lower']:.4f}, {ap['ci_upper']:.4f}]",
        f"Z-statistic:      {ap['z_statistic']:.4f}",
        f"P-value:          {ap['p_value']:.6f}",
        f"Power:            {ap['power']:.4f}",
        f"MDE:              {ap['mde']:.4f}",
        f"SIGNIFICANT:      {'YES' if ap['significant'] else 'NO'}",
        "",
        "-" * 70,
        "DEFAULT RATE TEST",
        "-" * 70,
        f"Control rate:     {dp['control_rate']:.4f}",
        f"Treatment rate:   {dp['treatment_rate']:.4f}",
        f"Difference:       {dp['diff']:+.4f} ({dp['diff']*100:+.2f}%)",
        f"95% CI:          [{dp['ci_lower']:.4f}, {dp['ci_upper']:.4f}]",
        f"Z-statistic:      {dp['z_statistic']:.4f}",
        f"P-value:          {dp['p_value']:.6f}",
        f"SIGNIFICANT:      {'YES' if dp['significant'] else 'NO'}",
        "",
        "-" * 70,
        "TREATMENT EFFECTS",
        "-" * 70,
        f"Approval Rate Lift:  {te['approval_rate_lift']:+.4f} ({te['approval_rate_lift']*100:+.2f}%)",
        f"Default Rate Lift:   {te['default_rate_lift']:+.4f} ({te['default_rate_lift']*100:+.2f}%)",
        "",
        "=" * 70,
        "CONCLUSION",
        "=" * 70,
    ]

    if ap['significant'] and dp['significant']:
        lines.extend([
            "✅ New model (B) significantly outperforms current model (A) on BOTH metrics.",
            "✅ RECOMMEND DEPLOYMENT.",
            ""
        ])
    elif ap['significant']:
        lines.extend([
            "⚠️  New model (B) shows higher approval rate.",
            "⚠️  Default rate difference is not significant.",
            ""
        ])
    elif dp['significant']:
        lines.extend([
            "⚠️  New model (B) shows lower default rate.",
            "⚠️  Approval rate difference is not significant.",
            ""
        ])
    else:
        lines.extend([
            "❌ No statistically significant difference detected.",
            "❌ More data may be needed.",
            ""
        ])

    return "\n".join(lines)


def save_report(results, filepath='experiment_report.md'):
    """Save report to file."""
    report = generate_report(results, format='markdown')

    with open(filepath, 'w') as f:
        f.write(report)

    print(f"Report saved to {filepath}")

    return report


if __name__ == '__main__':
    from src.simulate import run_experiment

    results = run_experiment()
    print(generate_text_report(results))