def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("        A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append("")
    lines.append("EXPERIMENT SUMMARY")
    lines.append("-" * 40)
    lines.append(f"{'Metric':<25} {'Group A (Control)':<20} {'Group B (Treatment)':<20}")
    lines.append("-" * 40)
    lines.append(f"{'Sample size':.<25} {results['group_a']['n']:<20} {results['group_b']['n']:<20}")
    lines.append(f"{'Approval rate':.<25} {results['group_a']['approval_rate']:<20.4f} {results['group_b']['approval_rate']:<20.4f}")
    lines.append(f"{'Default rate':.<25} {results['group_a']['default_rate']:<20.4f} {results['group_b']['default_rate']:<20.4f}")
    lines.append(f"{'Avg loan size (Rth)':.<25} {results['group_a']['avg_loan_size']:<20.2f} {results['group_b']['avg_loan_size']:<20.2f}")
    lines.append(f"{'Avg processing time (min)':.<25} {results['group_a']['avg_processing_time']:<20.2f} {results['group_b']['avg_processing_time']:<20.2f}")
    lines.append("")
    lines.append("STATISTICAL TESTS (Two-Proportion Z-Test, α=0.05)")
    lines.append("-" * 60)

    # Approval rate test
    at = results["approval_rate_test"]
    lines.append("")
    lines.append("APPROVAL RATE:")
    lines.append(f"  Z-statistic : {at['z_statistic']}")
    lines.append(f"  P-value     : {at['p_value']}")
    lines.append(f"  95% CI      : [{at['ci_lower']}, {at['ci_upper']}]")
    sig_word = "SIGNIFICANT" if at["significant"] else "NOT SIGNIFICANT"
    lines.append(f"  Result      : {sig_word}")
    lines.append("")

    # Default rate test
    dt = results["default_rate_test"]
    lines.append("DEFAULT RATE:")
    lines.append(f"  Z-statistic : {dt['z_statistic']}")
    lines.append(f"  P-value     : {dt['p_value']}")
    lines.append(f"  95% CI      : [{dt['ci_lower']}, {dt['ci_upper']}]")
    sig_word = "SIGNIFICANT" if dt["significant"] else "NOT SIGNIFICANT"
    lines.append(f"  Result      : {sig_word}")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)

if __name__ == "__main__":
    from src.simulate import run_experiment
    results = run_experiment()
    print(generate_report(results))