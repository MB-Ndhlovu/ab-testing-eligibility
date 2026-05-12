def generate_report(results):
    """Generate a human-readable summary report."""
    lines = []
    lines.append("=" * 60)
    lines.append("       A/B TEST RESULTS: CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 60)
    lines.append("")

    # Sample sizes
    lines.append(f"Sample Size: Group A (n={results['n_A']}), Group B (n={results['n_B']})")
    lines.append("")

    # Approval Rate
    lines.append("-" * 60)
    lines.append("METRIC: APPROVAL RATE (higher is better)")
    lines.append("-" * 60)
    a = results['approval']
    lines.append(f"  Group A (Control): {a['rate_A']:.4f} ({a['rate_A']*100:.2f}%)")
    lines.append(f"  Group B (Treatment): {a['rate_B']:.4f} ({a['rate_B']*100:.2f}%)")
    lines.append(f"  Observed Effect: {a['effect']:+.4f} ({a['effect']*100:+.2f}pp)")
    lines.append(f"  Minimum Detectable Effect: {a['mde']:.4f} ({a['mde']*100:.2f}pp)")
    lines.append(f"  z-statistic: {a['z_statistic']:.4f}")
    lines.append(f"  p-value: {a['p_value']:.6f}")
    lines.append(f"  95% CI for difference: [{a['ci_95'][0]:+.4f}, {a['ci_95'][1]:+.4f}]")
    lines.append(f"  Conclusion: {'SIGNIFICANT' if a['significant'] else 'NOT SIGNIFICANT'} at α=0.05")
    lines.append("")

    # Default Rate
    lines.append("-" * 60)
    lines.append("METRIC: DEFAULT RATE (lower is better)")
    lines.append("-" * 60)
    d = results['default']
    lines.append(f"  Group A (Control): {d['rate_A']:.4f} ({d['rate_A']*100:.2f}%)")
    lines.append(f"  Group B (Treatment): {d['rate_B']:.4f} ({d['rate_B']*100:.2f}%)")
    lines.append(f"  Observed Effect: {d['effect']:+.4f} ({d['effect']*100:+.2f}pp)")
    lines.append(f"  Minimum Detectable Effect: {d['mde']:.4f} ({d['mde']*100:.2f}pp)")
    lines.append(f"  z-statistic: {d['z_statistic']:.4f}")
    lines.append(f"  p-value: {d['p_value']:.6f}")
    lines.append(f"  95% CI for difference: [{d['ci_95'][0]:+.4f}, {d['ci_95'][1]:+.4f}]")
    lines.append(f"  Conclusion: {'SIGNIFICANT' if d['significant'] else 'NOT SIGNIFICANT'} at α=0.05")
    lines.append("")

    # Secondary metrics
    lines.append("-" * 60)
    lines.append("SECONDARY METRICS (not statistically tested)")
    lines.append("-" * 60)
    lines.append(f"  Avg Loan Size - Group A: R{results['avg_loan_size']['A']:,.2f}")
    lines.append(f"  Avg Loan Size - Group B: R{results['avg_loan_size']['B']:,.2f}")
    lines.append(f"  Avg Processing Time - Group A: {results['avg_processing_time']['A']:.2f} hours")
    lines.append(f"  Avg Processing Time - Group B: {results['avg_processing_time']['B']:.2f} hours")
    lines.append("")

    # Overall recommendation
    lines.append("=" * 60)
    if a['significant'] and d['significant']:
        lines.append("RECOMMENDATION: DEPLOY NEW MODEL (Group B)")
        lines.append("  - Significantly higher approval rate")
        lines.append("  - Significantly lower default rate")
    elif a['significant']:
        lines.append("RECOMMENDATION: DEPLOY NEW MODEL (Group B)")
        lines.append("  - Significantly higher approval rate")
        lines.append("  - Default rate change not significant")
    elif d['significant']:
        lines.append("RECOMMENDATION: REVIEW CAREFULLY")
        lines.append("  - Default rate significantly improved")
        lines.append("  - Approval rate change not significant")
    else:
        lines.append("RECOMMENDATION: COLLECT MORE DATA")
        lines.append("  - No statistically significant differences detected")
    lines.append("=" * 60)

    return "\n".join(lines)

if __name__ == '__main__':
    from src.simulate import run_simulation
    results = run_simulation()
    print(generate_report(results))