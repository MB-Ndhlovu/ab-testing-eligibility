"""
Generates a human-readable summary report from the experiment results dict.
"""

def format_rate(r: float) -> str:
    return f"{r * 100:.2f}%"

def generate_report(results: dict) -> str:
    ga = results["group_a"]
    gb = results["group_b"]

    lines = [
        "=" * 60,
        "     A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY SUMMARY",
        "=" * 60,
        "",
        "SAMPLE SIZES",
        f"  Group A (Control)  : n = {ga['n']:,}",
        f"  Group B (Treatment): n = {gb['n']:,}",
        "",
        "DESCRIPTIVE STATISTICS",
        f"  {'Metric':<22} {'Group A':>12} {'Group B':>12} {'Diff':>10}",
        f"  {'-'*22} {'-'*12} {'-'*12} {'-'*10}",
        f"  {'Approval Rate':<22} {format_rate(ga['approval_rate']):>12} {format_rate(gb['approval_rate']):>12} {format_rate(gb['approval_rate'] - ga['approval_rate']):>10}",
        f"  {'Default Rate':<22} {format_rate(ga['default_rate']):>12} {format_rate(gb['default_rate']):>12} {format_rate(gb['default_rate'] - ga['default_rate']):>10}",
        f"  {'Avg Loan Size (ZAR)':<22} {ga['avg_loan_size']:>12,.2f} {gb['avg_loan_size']:>12,.2f} {gb['avg_loan_size'] - ga['avg_loan_size']:>10,.2f}",
        f"  {'Avg Processing Time (h)':<22} {ga['avg_processing_time']:>12.2f} {gb['avg_processing_time']:>12.2f} {gb['avg_processing_time'] - ga['avg_processing_time']:>10.2f}",
        "",
        "STATISTICAL TESTS  (α = 0.05, two-proportion z-test)",
        "",
        "─── Approval Rate ───",
        _fmt_test(results["approval_rate"]),
        "",
        "─── Default Rate ───",
        _fmt_test(results["default_rate"]),
        "",
        "POWER ANALYSIS",
        f"  Power (Approval Rate test): {results['power_approval']:.4f}",
        f"  Power (Default Rate test) : {results['power_default']:.4f}",
        f"  Min Detectable Effect (MDE): {results['mde']:.5f}",
        "",
        "=" * 60,
    ]
    return "\n".join(lines)

def _fmt_test(t: dict) -> str:
    sig = "SIGNIFICANT" if t["significant"] else "NOT SIGNIFICANT"
    return (
        f"  Observed rate A  : {t['rate_a']:.4f}  ({t['x_a']:,} / {t['x_a']//(t['rate_a'] if t['rate_a'] else 1):,})\n"
        f"  Observed rate B  : {t['rate_b']:.4f}  ({t['x_b']:,} / {t['x_b']//(t['rate_b'] if t['rate_b'] else 1):,})\n"
        f"  Difference (B-A) : {t['diff']:+.5f}\n"
        f"  95% CI for diff : [{t['ci_95'][0]:+.5f}, {t['ci_95'][1]:+.5f}]\n"
        f"  z-statistic      : {t['z_statistic']:.4f}\n"
        f"  p-value          : {t['p_value']:.6f}\n"
        f"  Verdict          : {sig}"
    )