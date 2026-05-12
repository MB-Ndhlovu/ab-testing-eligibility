def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)

    gs = results["group_stats"]
    lines.append(f"\nSample size: {results['n']} (seed={results['seed']})")
    lines.append(f"\nControl Group (A) — {gs['A']['n']} applicants")
    lines.append(f"  Approval rate:    {gs['A']['approval_rate']:.4f}")
    lines.append(f"  Default rate:     {gs['A']['default_rate']:.4f}")
    lines.append(f"  Avg loan size:    R{gs['A']['avg_loan_size']:.2f}")
    lines.append(f"  Avg proc. time:   {gs['A']['avg_processing_time']:.2f} hrs")

    lines.append(f"\nTreatment Group (B) — {gs['B']['n']} applicants")
    lines.append(f"  Approval rate:    {gs['B']['approval_rate']:.4f}")
    lines.append(f"  Default rate:     {gs['B']['default_rate']:.4f}")
    lines.append(f"  Avg loan size:    R{gs['B']['avg_loan_size']:.2f}")
    lines.append(f"  Avg proc. time:   {gs['B']['avg_processing_time']:.2f} hrs")

    for test_result in [results["approval_rate_test"], results["default_rate_test"]]:
        label = test_result["metric"]
        lines.append(f"\n{'-' * 60}")
        lines.append(f"TEST: {label.upper()}")
        lines.append(f"{'-' * 60}")
        lines.append(f"  Control rate:    {test_result['control_rate']:.4f}")
        lines.append(f"  Treatment rate:  {test_result['treatment_rate']:.4f}")
        lines.append(f"  Difference:     {test_result['treatment_rate'] - test_result['control_rate']:.4f}")
        lines.append(f"  z-statistic:     {test_result['z_statistic']}")
        lines.append(f"  p-value:        {test_result['p_value']}")
        lines.append(f"  95% CI:         [{test_result['ci_95_low']:.4f}, {test_result['ci_95_high']:.4f}]")
        lines.append(f"  Statistical power: {test_result['power']:.4f}")
        lines.append(f"  Min. detectable effect: {test_result['mde']:.4f}")
        conclusion = "SIGNIFICANT" if test_result["significant"] else "NOT SIGNIFICANT"
        lines.append(f"  Conclusion (α=0.05): {conclusion}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

if __name__ == "__main__":
    from src.simulate import run_simulation
    results = run_simulation()
    print(generate_report(results))