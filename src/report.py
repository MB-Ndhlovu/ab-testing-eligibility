def fmt_pct(v):
    return f"{v*100:.2f}%"


def fmt_currency(v):
    return f"${v:,.0f}"


def generate_report(results: dict) -> str:
    """Generate a human-readable summary report."""
    alpha = results["alpha"]
    ga = results["group_a"]
    gb = results["group_b"]

    approval_sig = "YES — Significant" if results["approval_test"]["significant"] else "NO — Not Significant"
    default_sig = "YES — Significant" if results["default_test"]["significant"] else "NO — Not Significant"

    lines = [
        "=" * 60,
        "      A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY",
        "=" * 60,
        "",
        "EXPERIMENT SETUP",
        f"  Sample size:        {ga['n']} per group ({ga['n'] * 2} total)",
        f"  Alpha (significance level): {alpha}",
        "",
        "-" * 60,
        "GROUP SUMMARY",
        "-" * 60,
        f"{'':10} {'Group A (Control)':>20} {'Group B (Treatment)':>20}",
        f"{'N':10} {ga['n']:>20} {gb['n']:>20}",
        f"{'Approval %':10} {fmt_pct(ga['approval_rate']):>20} {fmt_pct(gb['approval_rate']):>20}",
        f"{'Default %':10} {fmt_pct(ga['default_rate']):>20} {fmt_pct(gb['default_rate']):>20}",
        f"{'Avg Loan $':10} {fmt_currency(ga['avg_loan_size']):>20} {fmt_currency(gb['avg_loan_size']):>20}",
        f"{'Avg Process (s)':10} {ga['avg_processing_time']:>20.2f} {gb['avg_processing_time']:>20.2f}",
        "",
        "-" * 60,
        "STATISTICAL TEST RESULTS",
        "-" * 60,
        "",
        "METRIC: Approval Rate",
        f"  Difference (B-A):   {results['approval_test']['difference']*100:+.2f} percentage points",
        f"  Z-statistic:         {results['approval_test']['z_statistic']:.4f}",
        f"  P-value:            {results['approval_test']['p_value']:.6f}",
        f"  95% CI:             [{results['approval_test']['ci_lower']*100:+.2f}pp, "
        f"{results['approval_test']['ci_upper']*100:+.2f}pp]",
        f"  Result:             {approval_sig} at alpha={alpha}",
        f"  Statistical Power:  {results['power_approval']:.4f}",
        f"  Min Detectable Eff:  {results['mde_approval']*100:.2f}pp",
        "",
        "METRIC: Default Rate",
        f"  Difference (B-A):   {results['default_test']['difference']*100:+.2f} percentage points",
        f"  Z-statistic:         {results['default_test']['z_statistic']:.4f}",
        f"  P-value:            {results['default_test']['p_value']:.6f}",
        f"  95% CI:             [{results['default_test']['ci_lower']*100:+.2f}pp, "
        f"{results['default_test']['ci_upper']*100:+.2f}pp]",
        f"  Result:             {default_sig} at alpha={alpha}",
        f"  Statistical Power:  {results['power_default']:.4f}",
        f"  Min Detectable Eff:  {results['mde_default']*100:.2f}pp",
        "",
        "-" * 60,
        "CONCLUSION",
        "-" * 60,
    ]

    if results["approval_test"]["significant"] and results["default_test"]["significant"]:
        conclusion = (
            "BOTH metrics show statistically significant improvement in Group B.\n"
            "  -> The new model (Group B) approves more applicants AND defaults less.\n"
            "  -> RECOMMENDATION: Deploy the new model."
        )
    elif results["approval_test"]["significant"]:
        conclusion = (
            "ONLY approval rate shows significant improvement in Group B.\n"
            "  -> Default rate difference is not statistically significant.\n"
            "  -> RECOMMENDATION: Proceed with caution."
        )
    elif results["default_test"]["significant"]:
        conclusion = (
            "ONLY default rate shows significant improvement in Group B.\n"
            "  -> Approval rate difference is not statistically significant.\n"
            "  -> RECOMMENDATION: Investigate why approval lift is not significant."
        )
    else:
        conclusion = (
            "NEITHER metric shows statistically significant improvement in Group B.\n"
            "  -> Observed differences may be due to random noise.\n"
            "  -> RECOMMENDATION: Do not deploy."
        )

    lines.extend([conclusion, "", "=" * 60])
    return "\n".join(lines)


if __name__ == "__main__":
    from src.data_generator import generate_credit_data
    from src.simulate import run_experiment

    df = generate_credit_data()
    results = run_experiment(df)
    print(generate_report(results))