"""
Generate a human-readable summary report from the simulation results.
"""

from src.simulate import run_simulation
from src.data_generator import summary_a, summary_b

ALPHA = 0.05


def fmt_rate(val):
    return f"{val * 100:.2f}%"


def fmt_zar(val):
    return f"R{val:,.0f}"


def fmt_hours(val):
    return f"{val:.2f} hrs"


def fmt_pct(val):
    return f"{val * 100:.2f}%"


def generate_report():
    sim = run_simulation()

    lines = []
    divider = "=" * 60

    lines.append(divider)
    lines.append("       A/B TEST RESULTS — CREDIT ELIGIBILITY MODEL")
    lines.append(divider)

    # ── Data Summary ──────────────────────────────────────────
    lines.append("\n📊 DATA SUMMARY")
    lines.append(f"  {'Metric':<22} {'Group A (Control)':>20} {'Group B (Treatment)':>20}")
    lines.append(f"  {'n':<22} {summary_a['n']:>20} {summary_b['n']:>20}")
    lines.append(f"  {'Approved':<22} {summary_a['n_approved']:>20} {summary_b['n_approved']:>20}")
    lines.append(f"  {'Approval Rate':<22} {fmt_rate(summary_a['approval_rate']):>20} {fmt_rate(summary_b['approval_rate']):>20}")
    lines.append(f"  {'Default Rate':<22} {fmt_rate(summary_a['default_rate']):>20} {fmt_rate(summary_b['default_rate']):>20}")
    lines.append(f"  {'Avg Loan Size':<22} {fmt_zar(summary_a['avg_loan_size']):>20} {fmt_zar(summary_b['avg_loan_size']):>20}")
    lines.append(f"  {'Avg Processing Time':<22} {fmt_hours(summary_a['avg_processing_time']):>20} {fmt_hours(summary_b['avg_processing_time']):>20}")

    # ── Approval Rate Test ─────────────────────────────────────
    ar = sim["approval_rate"]
    verdict = "✅ SIGNIFICANT" if ar["significant"] else "⚪ NOT SIGNIFICANT"
    lines.append(f"\n📈 APPROVAL RATE TEST (α = {ALPHA})")
    lines.append(f"  Group A rate : {fmt_rate(ar['group_a_rate'])}")
    lines.append(f"  Group B rate : {fmt_rate(ar['group_b_rate'])}")
    lines.append(f"  Difference   : {ar['diff']:+.4f} ({fmt_rate(ar['diff'])})")
    lines.append(f"  Z-statistic  : {ar['z_stat']:.4f}")
    lines.append(f"  P-value      : {ar['p_value']:.6f}")
    lines.append(f"  95% CI       : [{ar['ci_95'][0]:+.4f}, {ar['ci_95'][1]:+.4f}]")
    lines.append(f"  Power        : {fmt_pct(ar['power'])}")
    lines.append(f"  MDE (80%)    : {fmt_rate(ar['mde'])}")
    lines.append(f"  Conclusion   : {verdict}")

    # ── Default Rate Test ───────────────────────────────────────
    dr = sim["default_rate"]
    verdict_dr = "✅ SIGNIFICANT" if dr["significant"] else "⚪ NOT SIGNIFICANT"
    lines.append(f"\n📉 DEFAULT RATE TEST (α = {ALPHA})")
    lines.append(f"  Group A rate : {fmt_rate(dr['group_a_rate'])}")
    lines.append(f"  Group B rate : {fmt_rate(dr['group_b_rate'])}")
    lines.append(f"  Difference   : {dr['diff']:+.4f} ({fmt_rate(dr['diff'])})")
    lines.append(f"  Z-statistic  : {dr['z_stat']:.4f}")
    lines.append(f"  P-value      : {dr['p_value']:.6f}")
    lines.append(f"  95% CI       : [{dr['ci_95'][0]:+.4f}, {dr['ci_95'][1]:+.4f}]")
    lines.append(f"  Power        : {fmt_pct(dr['power'])}")
    lines.append(f"  MDE (80%)    : {fmt_rate(dr['mde'])}")
    lines.append(f"  Conclusion   : {verdict_dr}")

    # ── Avg Loan Size ───────────────────────────────────────────
    als = sim["avg_loan_size"]
    lines.append(f"\n💰 AVG LOAN SIZE (t-test)")
    lines.append(f"  Group A mean : {fmt_zar(als['group_a_mean'])}")
    lines.append(f"  Group B mean : {fmt_zar(als['group_b_mean'])}")
    lines.append(f"  Difference   : {als['diff']:+.0f} ZAR")
    lines.append(f"  t-statistic  : {als['t_stat']:.4f}")
    lines.append(f"  P-value      : {als['p_value']:.6f}")

    # ── Avg Processing Time ─────────────────────────────────────
    apt = sim["avg_processing_time"]
    lines.append(f"\n⏱️  AVG PROCESSING TIME (t-test)")
    lines.append(f"  Group A mean : {fmt_hours(apt['group_a_mean'])}")
    lines.append(f"  Group B mean : {fmt_hours(apt['group_b_mean'])}")
    lines.append(f"  Difference   : {apt['diff']:+.2f} hrs")
    lines.append(f"  t-statistic  : {apt['t_stat']:.4f}")
    lines.append(f"  P-value      : {apt['p_value']:.6f}")

    # ── Final Verdict ───────────────────────────────────────────
    both_sig = ar["significant"] and dr["significant"]
    lines.append(f"\n{'=' * 60}")
    if both_sig:
        lines.append("🎯 RECOMMENDATION: Adopt the new model — statistically")
        lines.append("   significant improvement on BOTH approval rate AND default rate.")
    elif ar["significant"]:
        lines.append("⚠️  PARTIAL: New model improves approval rate significantly,")
        lines.append("   but default rate improvement is NOT statistically significant.")
    elif dr["significant"]:
        lines.append("⚠️  PARTIAL: New model lowers default rate significantly,")
        lines.append("   but approval rate improvement is NOT statistically significant.")
    else:
        lines.append("❌ NO SIGNIFICANT DIFFERENCE detected between models.")
    lines.append(f"{'=' * 60}")

    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_report())