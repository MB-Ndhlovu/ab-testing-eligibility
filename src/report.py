"""Generate a readable summary report from A/B test results."""

import json
from typing import Any


def format_test_result(name: str, test: dict, power: float) -> str:
    sig = "SIGNIFICANT" if test["significant_at_0.05"] else "NOT SIGNIFICANT"
    direction = "higher" if test["difference"] > 0 else "lower"
    lines = [
        f"\n{'='*60}",
        f"  {name}",
        f"{'='*60}",
        f"  Group A rate : {test['group_a_rate']:.2%}",
        f"  Group B rate : {test['group_b_rate']:.2%}",
        f"  Difference   : {test['difference']:+.2%} ({direction})",
        f"",
        f"  z-statistic  : {test['z_statistic']:.4f}",
        f"  p-value      : {test['p_value']:.6f}",
        f"  95% CI       : [{test['ci_95_lower']:+.2%}, {test['ci_95_upper']:+.2%}]",
        f"  Power        : {power:.2%}",
        f"",
        f"  Conclusion   : {sig} at α = {test['alpha']}",
    ]
    return "\n".join(lines)


def generate_report(results: dict[str, Any]) -> str:
    summary = results["summary"]
    approval = results["approval_rate_test"]
    default = results["default_rate_test"]

    lines = [
        "\n" + "=" * 60,
        "  A/B TEST REPORT — Credit Eligibility Model",
        "=" * 60,
        "",
        "DATA SUMMARY",
        f"  Group A (Control)   : n={summary['A']['n_total']}, approved={summary['A']['n_approved']}, "
        f"approval_rate={summary['A']['approval_rate']:.2%}, default_rate={summary['A']['default_rate']:.2%}",
        f"  Group B (Treatment) : n={summary['B']['n_total']}, approved={summary['B']['n_approved']}, "
        f"approval_rate={summary['B']['approval_rate']:.2%}, default_rate={summary['B']['default_rate']:.2%}",
        f"  Avg Loan Size       : A=R{summary['A']['avg_loan_size']:,.2f}  |  B=R{summary['B']['avg_loan_size']:,.2f}",
        f"  Avg Processing Time : A={summary['A']['avg_processing_hours']:.1f}h  |  B={summary['B']['avg_processing_hours']:.1f}h",
        format_test_result("APPROVAL RATE", approval, results["approval_power"]),
        format_test_result("DEFAULT RATE (among approved)", default, results["default_power"]),
        "\n" + "=" * 60,
        "  OVERALL CONCLUSION",
        "=" * 60,
    ]

    # Approval rate conclusion
    if approval["significant_at_0.05"]:
        lines.append(f"  ✓ Approval rate is significantly {('higher' if approval['difference'] > 0 else 'lower')} in Group B.")
    else:
        lines.append(f"  ✗ No significant difference in approval rate between groups.")

    # Default rate conclusion
    if default["significant_at_0.05"]:
        lines.append(f"  ✓ Default rate is significantly {'lower' if default['difference'] < 0 else 'higher'} in Group B.")
    else:
        lines.append(f"  ✗ No significant difference in default rate between groups.")

    lines.append("\n  Recommendation: " + get_recommendation(approval, default))
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def get_recommendation(approval: dict, default: dict) -> str:
    """Generate a business recommendation based on test results."""
    approval_sig = approval["significant_at_0.05"]
    default_sig = default["significant_at_0.05"]
    approval_b_better = approval["difference"] > 0
    default_b_better = default["difference"] < 0

    if approval_sig and default_sig and approval_b_better and default_b_better:
        return "Deploy Group B — both approval rate increased and default rate decreased significantly."
    elif approval_sig and default_sig and not approval_b_better and not default_b_better:
        return "Keep Group A — Group B shows worse outcomes on both metrics."
    elif approval_sig and not default_sig:
        if approval_b_better:
            return "Consider deploying Group B — significantly higher approvals; monitor default rate."
        else:
            return "Keep Group A — significantly lower approvals with no default improvement."
    elif default_sig and not approval_sig:
        if default_b_better:
            return "Consider deploying Group B — significantly lower defaults; check approval impact."
        else:
            return "Keep Group A — significantly higher defaults with no approval benefit."
    else:
        return "Inconclusive — run a larger experiment for clearer signals."


if __name__ == "__main__":
    from src.simulate import run_simulation
    results = run_simulation()
    print(generate_report(results))