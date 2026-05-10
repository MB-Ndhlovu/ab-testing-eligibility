"""Generate readable summary report from A/B test results."""

import json


def generate_report(results):
    """Print a human-readable summary report."""
    print("=" * 60)
    print("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    print("=" * 60)

    print("\n[SAMPLE SIZES]")
    print(f"  Group A (Control):  {results['sample_sizes']['group_A']}")
    print(f"  Group B (Treatment): {results['sample_sizes']['group_B']}")

    print("\n[GROUP SUMMARY STATISTICS]")
    print("\n  Group A (Control):")
    print(f"    Approval Rate:        {results['group_A_summary']['approval_rate']:.2%}")
    print(f"    Default Rate:         {results['group_A_summary']['default_rate']:.2%}")
    print(f"    Avg Loan Size:        R{results['group_A_summary']['avg_loan_size']:.2f}k")
    print(f"    Avg Processing Time:  {results['group_A_summary']['avg_processing_time']:.2f} hrs")

    print("\n  Group B (Treatment):")
    print(f"    Approval Rate:        {results['group_B_summary']['approval_rate']:.2%}")
    print(f"    Default Rate:         {results['group_B_summary']['default_rate']:.2%}")
    print(f"    Avg Loan Size:        R{results['group_B_summary']['avg_loan_size']:.2f}k")
    print(f"    Avg Processing Time:  {results['group_B_summary']['avg_processing_time']:.2f} hrs")

    print("\n" + "=" * 60)
    print("STATISTICAL TEST RESULTS — Two-Proportion Z-Test (α = 0.05)")
    print("=" * 60)

    ar = results["approval_rate_analysis"]
    print("\n[APPROVAL RATE]")
    print(f"  Group A Rate:          {ar['group_A_rate']:.4f}")
    print(f"  Group B Rate:          {ar['group_B_rate']:.4f}")
    print(f"  Treatment Effect:      {ar['treatment_effect']:+.4f}")
    print(f"  Z-Statistic:           {ar['z_statistic']:.4f}")
    print(f"  P-Value:               {ar['p_value']:.6f}")
    print(f"  95% CI:                [{ar['ci_95'][0]:.4f}, {ar['ci_95'][1]:.4f}]")
    sig_word = "SIGNIFICANT" if ar["significant"] else "NOT SIGNIFICANT"
    print(f"  Conclusion:           {sig_word}")

    dr = results["default_rate_analysis"]
    print("\n[DEFAULT RATE]")
    print(f"  Group A Rate:          {dr['group_A_rate']:.4f}")
    print(f"  Group B Rate:          {dr['group_B_rate']:.4f}")
    print(f"  Treatment Effect:      {dr['treatment_effect']:+.4f}")
    print(f"  Z-Statistic:           {dr['z_statistic']:.4f}")
    print(f"  P-Value:               {dr['p_value']:.6f}")
    print(f"  95% CI:                [{dr['ci_95'][0]:.4f}, {dr['ci_95'][1]:.4f}]")
    sig_word = "SIGNIFICANT" if dr["significant"] else "NOT SIGNIFICANT"
    print(f"  Conclusion:           {sig_word}")

    print("\n" + "=" * 60)
    print("OVERALL RECOMMENDATION")
    print("=" * 60)
    if ar["significant"] and dr["significant"]:
        print("  ✓ Adopt the new model — higher approvals, lower defaults")
    elif ar["significant"]:
        print("  ✓ Adopt the new model — significantly higher approvals")
    elif dr["significant"]:
        print("  ⚠ Caution — default rate increased significantly")
    else:
        print("  ✗ Insufficient evidence to change models")
    print("=" * 60 + "\n")

    return results


def save_json(results, path="ab_test_results.json"):
    """Save results as JSON."""
    # Convert numpy types to native Python types for JSON serialization
    def to_native(obj):
        if isinstance(obj, dict):
            return {k: to_native(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [to_native(i) for i in obj]
        elif hasattr(obj, "item"):  # numpy types
            return obj.item()
        return obj

    with open(path, "w") as f:
        json.dump(to_native(results), f, indent=2)
    print(f"Results saved to {path}")