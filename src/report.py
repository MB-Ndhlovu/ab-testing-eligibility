"""
Generate a human-readable summary report from the experiment results.
"""

from src.simulate import run_experiment


def generate_report(results: dict) -> str:
    """Build a formatted text report."""
    lines = []
    sep = "=" * 60
    thin = "-" * 60

    lines.append(sep)
    lines.append("  A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("  Experiment Summary Report")
    lines.append(sep)
    lines.append("")

    # Sample info
    lines.append(f"  Sample size per group : {results['n_per_group']:,}")
    lines.append("")

    # --- Group metrics ---
    lines.append("GROUP METRICS")
    lines.append(thin)
    ma = results["metrics_A"]
    mb = results["metrics_B"]

    lines.append(f"                    Group A (Control)   Group B (Treatment)")
    lines.append(f"  Approval rate      {ma['approval_rate']:>17.2%}   {mb['approval_rate']:>17.2%}")
    lines.append(f"  Default rate       {ma['default_rate']:>17.2%}   {mb['default_rate']:>17.2%}")
    lines.append(f"  Avg loan size      R{ma['avg_loan_size']:>14,.0f}   R{mb['avg_loan_size']:>14,.0f}")
    lines.append(f"  Avg proc. time     {ma['avg_processing_time']:>16.1f}s   {mb['avg_processing_time']:>16.1f}s")
    lines.append("")

    # --- Statistical test for approval rate ---
    lines.append("STATISTICAL TEST: APPROVAL RATE")
    lines.append(thin)
    ar = results["approval_rate_test"]
    sig = "SIGNIFICANT" if ar["significant"] else "NOT SIGNIFICANT"
    lines.append(f"  Z-statistic        : {ar['z_stat']:.4f}")
    lines.append(f"  P-value            : {ar['p_value']:.6f}  (α = 0.05)")
    lines.append(f"  95% CI             : [{ar['ci_lower']:+.4f}, {ar['ci_upper']:+.4f}]")
    lines.append(f"  MDE (80% power)    : {ar['mde']:.4f}")
    lines.append(f"  Power at obs. MDE  : {ar['power_at_obs_mde']:.4f}")
    lines.append(f"  Conclusion         : {sig}")
    lines.append("")

    # --- Statistical test for default rate ---
    lines.append("STATISTICAL TEST: DEFAULT RATE")
    lines.append(thin)
    dr = results["default_rate_test"]
    sig_dr = "SIGNIFICANT" if dr["significant"] else "NOT SIGNIFICANT"
    lines.append(f"  Z-statistic        : {dr['z_stat']:.4f}")
    lines.append(f"  P-value            : {dr['p_value']:.6f}  (α = 0.05)")
    lines.append(f"  95% CI             : [{dr['ci_lower']:+.4f}, {dr['ci_upper']:+.4f}]")
    lines.append(f"  MDE (80% power)    : {dr['mde']:.4f}")
    lines.append(f"  Power at obs. MDE  : {dr['power_at_obs_mde']:.4f}")
    lines.append(f"  Conclusion         : {sig_dr}")
    lines.append("")
    lines.append(sep)

    return "\n".join(lines)


if __name__ == "__main__":
    results = run_experiment()
    print(generate_report(results))