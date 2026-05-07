"""Generate readable summary report from experiment results."""
import json
import numpy as np


def format_result(label, result):
    verdict = "✅ SIGNIFICANT" if result["significant"] else "⚠️ NOT SIGNIFICANT"
    return (
        f"  {label}\n"
        f"    z-statistic : {result['z_statistic']}\n"
        f"    p-value     : {result['p_value']}\n"
        f"    95% CI      : [{result['ci_95_lower']}, {result['ci_95_upper']}]\n"
        f"    Conclusion  : {verdict} (α=0.05)\n"
    )


def generate_report(results):
    a = results["group_a"]
    b = results["group_b"]

    lines = [
        "=" * 60,
        "  A/B TESTING REPORT — Credit Eligibility Model",
        "=" * 60,
        "",
        "SAMPLE SIZES",
        f"  Group A (Control)  : n = {a['n']}",
        f"  Group B (Treatment): n = {b['n']}",
        "",
        "DESCRIPTIVE STATISTICS",
        f"  Group A — Approval Rate: {a['approval_rate']:.4f}  |  Default Rate: {a['default_rate']:.4f}",
        f"  Group B — Approval Rate: {b['approval_rate']:.4f}  |  Default Rate: {b['default_rate']:.4f}",
        f"  Group A — Avg Loan Size (ZAR): {a['avg_loan_size']:,.2f}",
        f"  Group B — Avg Loan Size (ZAR): {b['avg_loan_size']:,.2f}",
        f"  Group A — Avg Processing Time: {a['avg_processing_time']:.2f} hrs",
        f"  Group B — Avg Processing Time: {b['avg_processing_time']:.2f} hrs",
        "",
        "STATISTICAL TESTS (Two-Proportion Z-Test, α=0.05)",
        format_result("Approval Rate", results["approval_rate_test"]),
        format_result("Default Rate",  results["default_rate_test"]),
        "",
        "POWER ANALYSIS",
        f"  Statistical Power (Approval Rate): {results['power_approval']}",
        f"  Min Detectable Effect (Approval) : {results['mde_approval']}",
        "",
        "OVERALL RECOMMENDATION",
    ]

    ar = results["approval_rate_test"]
    dr = results["default_rate_test"]

    if ar["significant"] and dr["significant"]:
        lines.append("  ✅ Deploy Group B model — better approvals AND lower defaults.")
    elif ar["significant"]:
        lines.append("  ⚠️  Approvals improved but default rate change is not significant.")
    elif dr["significant"]:
        lines.append("  ⚠️  Default rate improved but approval rate change is not significant.")
    else:
        lines.append("  ❌ No statistically significant difference detected.")

    lines.append("=" * 60)
    return "\n".join(lines)


def make_serializable(obj):
    """Recursively convert numpy types to native Python for JSON serialization."""
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, "item"):  # numpy scalar
        return obj.item()
    else:
        return obj


def save_json_report(results, path="ab_test_results.json"):
    serializable = make_serializable(results)
    with open(path, "w") as f:
        json.dump(serializable, f, indent=2)
