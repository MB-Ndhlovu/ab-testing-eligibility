from src.simulate import run_simulation


def generate_report(results):
    stats = results["group_stats"]
    alpha = 0.05

    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)

    lines.append("\n[ SAMPLE OVERVIEW ]")
    lines.append(f"  Total applicants: {results['sample_size']}")
    for group in ["A", "B"]:
        g = stats[group]
        lines.append(f"  Group {group}: n={g['n']}, approval={g['approval_rate']:.4f}, "
                     f"default={g['default_rate']:.4f}, avg_loan=R{g['avg_loan_size']:,.0f}, "
                     f"proc_time={g['processing_time_mean']:.1f}s")

    for test_key in ["approval_rate_test", "default_rate_test"]:
        test = results[test_key]
        metric = test["metric"]
        lines.append(f"\n[ {metric.upper()} TEST ]")
        lines.append(f"  Group A rate:      {test['group_a_rate']:.4f}")
        lines.append(f"  Group B rate:      {test['group_b_rate']:.4f}")
        lines.append(f"  Treatment effect:  {test['treatment_effect']:+.4f}")
        lines.append(f"  Z-statistic:       {test['z_statistic']:.4f}")
        lines.append(f"  P-value:           {test['p_value']:.6f}")
        lines.append(f"  95% CI:            [{test['ci_lower']:.4f}, {test['ci_upper']:.4f}]")
        lines.append(f"  Significant (α=0.05): {'YES' if test['significant'] else 'NO'}")
        lines.append(f"  Power:             {test['power']:.4f}")
        lines.append(f"  Min. det. effect:  {test['mde']:.4f}")

    lines.append("\n" + "=" * 60)
    lines.append("CONCLUSION")
    lines.append("=" * 60)
    ar = results["approval_rate_test"]
    dr = results["default_rate_test"]
    if ar["significant"] and dr["significant"]:
        lines.append("  Both metrics show statistical significance.")
        lines.append("  Group B (new model) approves more loans AND defaults less.")
        lines.append("  RECOMMENDATION: Deploy new credit eligibility model.")
    elif ar["significant"] and not dr["significant"]:
        lines.append("  Approval rate is significantly better in Group B.")
        lines.append("  Default rate difference is not significant.")
        lines.append("  RECOMMENDATION: Consider with caution; monitor defaults.")
    elif dr["significant"] and not ar["significant"]:
        lines.append("  Default rate is significantly lower in Group B.")
        lines.append("  Approval rate difference is not significant.")
        lines.append("  RECOMMENDATION: Evaluate if higher approval is needed.")
    else:
        lines.append("  Neither metric shows statistical significance.")
        lines.append("  Insufficient evidence to change models.")
        lines.append("  RECOMMENDATION: Collect more data or revisit effect size.")

    return "\n".join(lines)