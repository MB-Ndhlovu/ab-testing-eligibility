"""Generate readable summary reports for A/B test results."""

from typing import Dict, Any
from src.simulate import interpret_results


def generate_report(results: Dict[str, Any]) -> str:
    """
    Generate a formatted text report of A/B test results.

    Args:
        results: Dictionary from run_experiment()

    Returns:
        Formatted report string
    """
    interpretations = interpret_results(results)

    lines = [
        "=" * 70,
        "A/B TESTING FRAMEWORK FOR CREDIT ELIGIBILITY",
        "=" * 70,
        "",
        "EXECUTIVE SUMMARY",
        "-" * 40,
        f"Group A (Control): {results['group_a']['n']} samples",
        f"  Approval Rate:  {results['group_a']['approval_rate']:.4f}",
        f"  Default Rate:  {results['group_a']['default_rate']:.4f}",
        f"  Avg Loan Size: ${results['group_a']['avg_loan_size']:.2f}",
        f"  Avg Processing Time: {results['group_a']['avg_processing_time']:.2f} hours",
        "",
        f"Group B (Treatment): {results['group_b']['n']} samples",
        f"  Approval Rate:  {results['group_b']['approval_rate']:.4f}",
        f"  Default Rate:  {results['group_b']['default_rate']:.4f}",
        f"  Avg Loan Size: ${results['group_b']['avg_loan_size']:.2f}",
        f"  Avg Processing Time: {results['group_b']['avg_processing_time']:.2f} hours",
        "",
        "=" * 70,
        "STATISTICAL TESTS (Two-Proportion Z-Test, α=0.05)",
        "=" * 70,
        "",
        "[1] APPROVAL RATE",
        "-" * 40,
        f"  Observed Difference:   {results['approval_rate_test']['difference']:+.4f}",
        f"  95% CI for Difference: [{results['approval_rate_test']['ci_lower']:.4f}, {results['approval_rate_test']['ci_upper']:.4f}]",
        f"  Z-Statistic:           {results['approval_rate_test']['z_statistic']:.4f}",
        f"  P-Value:               {results['approval_rate_test']['p_value']:.6f}",
        f"  Statistical Power:      {results['approval_power']:.4f}",
        f"  Min Detectable Effect: {results['approval_mde']:.4f}",
        "",
        f"  Conclusion: {interpretations['approval']}",
        "",
        "[2] DEFAULT RATE",
        "-" * 40,
        f"  Observed Difference:   {results['default_rate_test']['difference']:+.4f}",
        f"  95% CI for Difference: [{results['default_rate_test']['ci_lower']:.4f}, {results['default_rate_test']['ci_upper']:.4f}]",
        f"  Z-Statistic:           {results['default_rate_test']['z_statistic']:.4f}",
        f"  P-Value:               {results['default_rate_test']['p_value']:.6f}",
        f"  Statistical Power:      {results['default_power']:.4f}",
        f"  Min Detectable Effect: {results['default_mde']:.4f}",
        "",
        f"  Conclusion: {interpretations['default']}",
        "",
        "=" * 70,
        "RECOMMENDATION",
        "-" * 40,
    ]

    # Determine overall recommendation
    ar_sig = results["approval_rate_test"]["p_value"] < results["alpha"]
    dr_sig = results["default_rate_test"]["p_value"] < results["alpha"]

    if ar_sig and dr_sig:
        ar_better = results["approval_rate_test"]["difference"] > 0
        dr_better = results["default_rate_test"]["difference"] < 0  # lower is better

        if ar_better and dr_better:
            lines.append("ADOPT the new credit eligibility model (Group B).")
            lines.append("  - Significantly higher approval rate")
            lines.append("  - Significantly lower default rate")
        elif ar_better and not dr_better:
            lines.append("CAUTION: Higher approval rate but worse default rate.")
            lines.append("  Further analysis required on risk-adjusted returns.")
        elif not ar_better and dr_better:
            lines.append("CAUTION: Lower default rate but lower approval rate.")
            lines.append("  Trade-off may favor one metric depending on business priorities.")
        else:
            lines.append("REJECT the new model — both metrics moved in undesirable direction.")
    elif ar_sig or dr_sig:
        lines.append("PARTIAL SUPPORT for the new model.")
        if ar_sig:
            lines.append(f"  - Approval rate {'improved' if results['approval_rate_test']['difference'] > 0 else 'worsened'} significantly")
        if dr_sig:
            lines.append(f"  - Default rate {'improved' if results['default_rate_test']['difference'] < 0 else 'worsened'} significantly")
        lines.append("  Consider a longer test or larger sample for the non-significant metric.")
    else:
        lines.append("INSUFFICIENT EVIDENCE to change the current model.")
        lines.append("  Neither metric showed a statistically significant difference.")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


if __name__ == "__main__":
    from src.simulate import run_experiment

    results = run_experiment()
    print(generate_report(results))