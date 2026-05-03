import json

def generate_report(results):
    n = results["n_per_group"]
    alpha = results["alpha"]

    lines = []
    lines.append("=" * 60)
    lines.append("   A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY SUMMARY")
    lines.append("=" * 60)
    lines.append(f"  Sample size per group : {n}")
    lines.append(f"  Significance level    : α = {alpha}")
    lines.append("-" * 60)

    for metric in ["approval_rate", "default_rate"]:
        m = results[metric]
        label = "Approval Rate" if metric == "approval_rate" else "Default Rate"
        lines.append(f"\n  [{label}]")
        lines.append(f"    Group A (control)  : {m['group_A']:.4f}")
        lines.append(f"    Group B (treatment): {m['group_B']:.4f}")
        lines.append(f"    Treatment effect    : {m['effect']:+.4f}")
        lines.append(f"    Z-statistic         : {m['z_statistic']:.4f}")
        lines.append(f"    P-value             : {m['p_value']:.6f}")
        lines.append(f"    95% CI              : [{m['ci_95'][0]:+.4f}, {m['ci_95'][1]:+.4f}]")
        lines.append(f"    Statistical power   : {m['power']:.4f}")
        lines.append(f"    Min. detectable eff.: {m['mde']:.4f}")
        sig = "SIGNIFICANT" if m["significant"] else "NOT SIGNIFICANT"
        lines.append(f"    Conclusion          : {sig} at α={alpha}")

    lines.append("\n" + "=" * 60)
    lines.append("  OVERALL RECOMMENDATION")
    lines.append("=" * 60)

    ar_sig = results["approval_rate"]["significant"]
    dr_sig = results["default_rate"]["significant"]

    if ar_sig and dr_sig:
        lines.append("  Deploy the new model — better approval rate with lower default risk.")
    elif ar_sig:
        lines.append("  Deploy cautiously — higher approval rate but no default improvement.")
    elif dr_sig:
        lines.append("  Deploy cautiously — lower default rate but no approval improvement.")
    else:
        lines.append("  Do not deploy — insufficient evidence of improvement.")

    report = "\n".join(lines)
    print(report)
    return report