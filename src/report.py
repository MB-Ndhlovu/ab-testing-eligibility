"""
Generate readable summary report from A/B test results.
"""

from typing import Dict


def generate_report(results: Dict) -> str:
    """
    Build a human-readable report from the experiment results dict.

    Args:
        results: Dictionary returned by run_experiment()

    Returns:
        Multi-line string report
    """
    n = results["sample_size_per_group"]
    ga = results["group_A"]
    gb = results["group_B"]
    app = results["approval_rate_test"]
    default = results["default_rate_test"]

    lines = [
        "=" * 60,
        "A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY",
        "=" * 60,
        "",
        "SAMPLE SIZE",
        f"  Applicants per group: {n:,}",
        "",
        "-" * 60,
        "GROUP STATISTICS",
        "-" * 60,
        f"{'':20} {'Group A (Control)':>20} {'Group B (Treatment)':>20}",
        f"{'Approval Rate':20} {ga['approval_rate']*100:>19.2f}% {gb['approval_rate']*100:>19.2f}%",
        f"{'Default Rate':20} {ga['default_rate']*100:>19.2f}% {gb['default_rate']*100:>19.2f}%",
        f"{'Avg Loan Size':20} {'R'+str(f'{ga['avg_loan_size']:,.0f}'):>19} {'R'+str(f'{gb['avg_loan_size']:,.0f}'):>19}",
        f"{'Avg Processing Time':20} {ga['avg_processing_time_hrs']:>18.1f}h {gb['avg_processing_time_hrs']:>19.1f}h",
        "",
        "-" * 60,
        "APPROVAL RATE — TWO-PROPORTION Z-TEST",
        "-" * 60,
        f"  Difference (B - A):       {app['diff']:+.4f} ({app['diff']*100:+.2f}%)",
        f"  95% CI for difference:    [{app['ci_95_lower']:.4f}, {app['ci_95_upper']:.4f}]",
        f"  z-statistic:              {app['z_statistic']:.4f}",
        f"  p-value:                  {app['p_value']:.6f}",
        f"  Statistical power:        {app['power']:.4f}",
        f"  Min detectable effect:   {app['mde']:.4f} ({app['mde']*100:.2f}%)",
        f"  Significant (α=0.05)?    {'YES' if app['significant'] else 'NO'}",
        "",
        "-" * 60,
        "DEFAULT RATE — TWO-PROPORTION Z-TEST",
        "-" * 60,
        f"  Difference (B - A):       {default['diff']:+.4f} ({default['diff']*100:+.2f}%)",
        f"  95% CI for difference:    [{default['ci_95_lower']:.4f}, {default['ci_95_upper']:.4f}]",
        f"  z-statistic:              {default['z_statistic']:.4f}",
        f"  p-value:                  {default['p_value']:.6f}",
        f"  Statistical power:        {default['power']:.4f}",
        f"  Min detectable effect:   {default['mde']:.4f} ({default['mde']*100:.2f}%)",
        f"  Significant (α=0.05)?    {'YES' if default['significant'] else 'NO'}",
        "",
        "=" * 60,
        "CONCLUSION",
        "=" * 60,
    ]

    if app["significant"] and default["significant"]:
        conclusion = (
            "The new eligibility model (Group B) significantly outperforms the current "
            "model (Group A) on BOTH metrics — higher approval rate AND lower default rate. "
            "Recommendation: APPROVE deployment of the new model."
        )
    elif app["significant"] and not default["significant"]:
        conclusion = (
            "Group B shows a significantly higher approval rate, but the default rate "
            "difference is not statistically significant. Deploy with caution — monitor "
            "default rate closely post-launch."
        )
    elif not app["significant"] and default["significant"]:
        conclusion = (
            "Group B shows a significantly lower default rate, but the approval rate "
            "difference is not significant. The new model may be more conservative. "
            "Consider relaxing eligibility thresholds."
        )
    else:
        conclusion = (
            "No statistically significant differences detected between groups. "
            "The sample may lack power to detect meaningful effects. "
            "Recommendation: GATHER more data before making a decision."
        )

    lines.extend([
        f"  {conclusion}",
        "=" * 60,
    ])

    return "\n".join(lines)