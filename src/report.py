def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("    A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 60)
    lines.append("")

    lines.append("[ SAMPLE METRICS ]")
    lines.append(f"  Group A (Control):   n={results['group_a']['n']}, "
                f"approval={results['group_a']['approval_rate']:.4f}, "
                f"default={results['group_a']['default_rate']:.4f}")
    lines.append(f"  Group B (Treatment):  n={results['group_b']['n']}, "
                f"approval={results['group_b']['approval_rate']:.4f}, "
                f"default={results['group_b']['default_rate']:.4f}")
    lines.append("")

    lines.append("[ APPROVAL RATE TEST ]")
    lines.append(f"  Treatment Effect:    {results['approval_rate']['treatment_effect']:+.4f}")
    lines.append(f"  Z-Statistic:         {results['approval_rate']['z_statistic']:.4f}")
    lines.append(f"  P-Value:              {results['approval_rate']['p_value']:.6f}")
    lines.append(f"  95% CI:               [{results['approval_rate']['ci_lower']:.4f}, "
                f"{results['approval_rate']['ci_upper']:.4f}]")
    lines.append(f"  Statistical Power:    {results['approval_rate']['power']:.4f}")
    lines.append(f"  Min Detectable Eff:  {results['approval_rate']['mde']:.4f}")
    sig_ar = "YES" if results['approval_rate']['significant'] else "NO"
    lines.append(f"  Significant (α=0.05): {sig_ar}")
    lines.append("")

    lines.append("[ DEFAULT RATE TEST ]")
    lines.append(f"  Treatment Effect:    {results['default_rate']['treatment_effect']:+.4f}")
    lines.append(f"  Z-Statistic:         {results['default_rate']['z_statistic']:.4f}")
    lines.append(f"  P-Value:              {results['default_rate']['p_value']:.6f}")
    lines.append(f"  95% CI:               [{results['default_rate']['ci_lower']:.4f}, "
                f"{results['default_rate']['ci_upper']:.4f}]")
    lines.append(f"  Statistical Power:    {results['default_rate']['power']:.4f}")
    lines.append(f"  Min Detectable Eff:  {results['default_rate']['mde']:.4f}")
    sig_dr = "YES" if results['default_rate']['significant'] else "NO"
    lines.append(f"  Significant (α=0.05): {sig_dr}")
    lines.append("")

    lines.append("[ CONCLUSION ]")
    ar_sig = results['approval_rate']['significant']
    dr_sig = results['default_rate']['significant']

    if ar_sig and dr_sig:
        lines.append("  Both metrics show statistically significant improvement.")
        lines.append("  RECOMMENDATION: Deploy the new model (Group B).")
    elif ar_sig:
        lines.append("  Approval rate improved significantly; default rate not significant.")
        lines.append("  RECOMMENDATION: Further analysis needed on default rate impact.")
    elif dr_sig:
        lines.append("  Default rate improved significantly; approval rate not significant.")
        lines.append("  RECOMMENDATION: Investigate approval rate dynamics.")
    else:
        lines.append("  Neither metric showed statistically significant improvement.")
        lines.append("  RECOMMENDATION: Retain current model or gather more data.")
        lines.append("  NOTE: Results may be underpowered due to small effect size.")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


if __name__ == "__main__":
    from src.simulate import run_simulation
    results = run_simulation()
    print(generate_report(results))