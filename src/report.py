from typing import Dict, Any


def format_pct(value: float) -> str:
    """Format a proportion as a percentage string."""
    return f"{value * 100:.2f}%"


def generate_report(results: Dict[str, Any]) -> str:
    """
    Generate a human-readable summary report from experiment results.

    Args:
        results: Dictionary returned by run_experiment()

    Returns:
        Formatted report as a multi-line string
    """
    meta = results['metadata']
    approval = results['approval_rate']
    default = results['default_rate']
    group_stats = results['group_stats']

    verdict_approval = "SIGNIFICANT" if approval['significant'] else "NOT SIGNIFICANT"
    verdict_default = "SIGNIFICANT" if default['significant'] else "NOT SIGNIFICANT"

    lines = [
        "=" * 60,
        "A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY",
        "=" * 60,
        "",
        "EXPERIMENT SUMMARY",
        "-" * 40,
        f"Sample Size:    {meta['n_total']} total ({meta['n_control']} control / {meta['n_treatment']} treatment)",
        f"Random Seed:     {meta['seed']}",
        "",
        "GROUP-LEVEL METRICS",
        "-" * 40,
        f"{'':20} {'Group A (Control)':>20} {'Group B (Treatment)':>20}",
        f"{'Approval Rate':20} {format_pct(group_stats['A']['approval_rate']):>20} {format_pct(group_stats['B']['approval_rate']):>20}",
        f"{'Default Rate':20} {format_pct(group_stats['A']['default_rate']):>20} {format_pct(group_stats['B']['default_rate']):>20}",
        f"{'Avg Loan Size':20} {'R${:,.0f}'.format(group_stats['A']['avg_loan_size']):>20} {'R${:,.0f}'.format(group_stats['B']['avg_loan_size']):>20}",
        f"{'Processing Time':20} {group_stats['A']['processing_time_mean']:.1f} min{'':10} {group_stats['B']['processing_time_mean']:.1f} min{'':10}",
        "",
        "STATISTICAL RESULTS",
        "-" * 40,
        "",
        "1. APPROVAL RATE",
        f"   Observed difference:  {approval['treatment_effect']:+.4f} ({format_pct(approval['treatment_effect'])})",
        f"   z-statistic:         {approval['z_statistic']:.4f}",
        f"   p-value:             {approval['p_value']:.4f}",
        f"   95% CI:              [{approval['ci_95'][0]:.4f}, {approval['ci_95'][1]:.4f}]",
        f"   Statistical power:   {approval['power']:.4f}",
        f"   Min detectable eff:  {approval['mde']:.4f}",
        f"   Result (alpha=0.05): {verdict_approval}",
        "",
        "2. DEFAULT RATE",
        f"   Observed difference:  {default['treatment_effect']:+.4f} ({format_pct(default['treatment_effect'])})",
        f"   z-statistic:         {default['z_statistic']:.4f}",
        f"   p-value:             {default['p_value']:.4f}",
        f"   95% CI:              [{default['ci_95'][0]:.4f}, {default['ci_95'][1]:.4f}]",
        f"   Statistical power:   {default['power']:.4f}",
        f"   Min detectable eff:  {default['mde']:.4f}",
        f"   Result (alpha=0.05): {verdict_default}",
        "",
        "=" * 60,
        "CONCLUSION",
        "-" * 40,
    ]

    if approval['significant'] and default['significant']:
        if (approval['treatment_effect'] > 0 and default['treatment_effect'] < 0):
            lines.append("The new model (Group B) SIGNIFICANTLY outperforms the current model")
            lines.append("on BOTH metrics — higher approval rate AND lower default rate.")
            lines.append("Recommendation: DEPLOY the new model.")
        else:
            lines.append("Mixed results — see individual metric conclusions above.")
    elif approval['significant']:
        lines.append("Approval rate improved significantly. Default rate not significant.")
        lines.append("Recommendation: Review default rate impact before deploying.")
    elif default['significant']:
        lines.append("Default rate improved significantly. Approval rate not significant.")
        lines.append("Recommendation: Review approval rate impact before deploying.")
    else:
        lines.append("Neither metric showed a statistically significant improvement.")
        lines.append("Recommendation: Do NOT deploy the new model at this time.")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def print_report(results: Dict[str, Any]) -> None:
    """Print the report to stdout."""
    print(generate_report(results))


if __name__ == '__main__':
    from src.simulate import run_experiment
    results = run_experiment()
    print_report(results)