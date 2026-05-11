"""Generate a readable summary report."""
import json

def format_result(name, result, is_ztest=True):
    lines = [f"\n{'='*60}"]
    lines.append(f"  {name}")
    lines.append('='*60)

    if is_ztest:
        sig = "✅ SIGNIFICANT" if result["significant"] else "❌ NOT SIGNIFICANT"
        lines.append(f"  Group A (Control):   {result['p1']:.4f} ({result['p1']*100:.2f}%)")
        lines.append(f"  Group B (Treatment): {result['p2']:.4f} ({result['p2']*100:.2f}%)")
        lines.append(f"  Difference (A - B):  {result['difference']:+.4f}")
        lines.append(f"  95% CI:              [{result['ci_95'][0]:+.4f}, {result['ci_95'][1]:+.4f}]")
        lines.append(f"  Z-statistic:         {result['z_stat']:.4f}")
        lines.append(f"  P-value:             {result['p_value']:.6f}")
        lines.append(f"  Conclusion (α=0.05):  {sig}")
    else:
        lines.append(f"  T-statistic: {result.get('t_stat')}")
        lines.append(f"  P-value:     {result.get('p_value'):.6f}")
        sig = "✅ SIGNIFICANT" if result.get("p_value", 1) < 0.05 else "❌ NOT SIGNIFICANT"
        lines.append(f"  Conclusion:  {sig}")

    return "\n".join(lines)

def generate_report(exp_results):
    lines = [
        "\n" + "="*60,
        "       A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY",
        "="*60,
        f"\n  Sample Sizes — Group A: {exp_results['n_a']}  |  Group B: {exp_results['n_b']}",
    ]

    lines.append(format_result("APPROVAL RATE", exp_results["approval_rate"]))
    lines.append(format_result("DEFAULT RATE", exp_results["default_rate"]))
    lines.append(format_result("AVG LOAN SIZE", exp_results["avg_loan_size"], is_ztest=False))
    lines.append(format_result("PROCESSING TIME", exp_results["processing_time"], is_ztest=False))

    # Summary verdict
    # difference = p1 - p2  (positive = A higher, negative = B higher)
    ar_diff = exp_results["approval_rate"]["difference"]
    dr_diff = exp_results["default_rate"]["difference"]
    ar_sig  = exp_results["approval_rate"]["significant"]
    dr_sig  = exp_results["default_rate"]["significant"]

    lines.append("\n" + "="*60)
    lines.append("  SUMMARY VERDICT")
    lines.append("="*60)

    if ar_sig and ar_diff < 0:
        lines.append("  ✅ Approval rate is SIGNIFICANTLY HIGHER with the new model.")
    elif ar_sig and ar_diff > 0:
        lines.append("  ⚠️  Approval rate is SIGNIFICANTLY LOWER with the new model.")
    else:
        lines.append("  ⚠️  No significant difference in approval rate.")

    if dr_sig and dr_diff < 0:
        lines.append("  ❌ Default rate is SIGNIFICANTLY HIGHER with the new model — WARNING.")
    elif dr_sig and dr_diff > 0:
        lines.append("  ✅ Default rate is SIGNIFICANTLY LOWER with the new model.")
    else:
        lines.append("  ⚠️  No significant difference in default rate.")

    report_text = "\n".join(lines) + "\n"

    output = {
        "approval_rate": {
            "group_a": float(exp_results["approval_rate"]["p1"]),
            "group_b": float(exp_results["approval_rate"]["p2"]),
            "difference": float(exp_results["approval_rate"]["difference"]),
            "ci_95": [float(x) for x in exp_results["approval_rate"]["ci_95"]],
            "z_stat": float(exp_results["approval_rate"]["z_stat"]),
            "p_value": float(exp_results["approval_rate"]["p_value"]),
            "significant": bool(exp_results["approval_rate"]["significant"]),
        },
        "default_rate": {
            "group_a": float(exp_results["default_rate"]["p1"]),
            "group_b": float(exp_results["default_rate"]["p2"]),
            "difference": float(exp_results["default_rate"]["difference"]),
            "ci_95": [float(x) for x in exp_results["default_rate"]["ci_95"]],
            "z_stat": float(exp_results["default_rate"]["z_stat"]),
            "p_value": float(exp_results["default_rate"]["p_value"]),
            "significant": bool(exp_results["default_rate"]["significant"]),
        },
        "avg_loan_size": {
            "t_stat": float(exp_results["avg_loan_size"]["t_stat"]),
            "p_value": float(exp_results["avg_loan_size"]["p_value"]),
        },
        "processing_time": {
            "t_stat": float(exp_results["processing_time"]["t_stat"]),
            "p_value": float(exp_results["processing_time"]["p_value"]),
        },
        "n_a": int(exp_results["n_a"]),
        "n_b": int(exp_results["n_b"]),
    }

    return report_text, output