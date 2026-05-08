"""Generate readable summary report."""

import json


def generate_report(results: dict) -> str:
    """Build a markdown summary report."""
    lines = [
        "# A/B Test Results: Credit Eligibility Model\n",
        "## Approval Rate",
        f"- Group A (Control): {results['approval_rate']['group_a']:.2%}",
        f"- Group B (Treatment): {results['approval_rate']['group_b']:.2%}",
        f"- Z-statistic: {results['approval_rate']['z_statistic']:.4f}",
        f"- P-value: {results['approval_rate']['p_value']:.6f}",
        f"- 95% CI: ({results['approval_rate']['ci_95_lower']:.4f}, {results['approval_rate']['ci_95_upper']:.4f})",
        f"- **Significant (α=0.05)**: {results['approval_rate']['significant']}",
        "\n## Default Rate",
        f"- Group A (Control): {results['default_rate']['group_a']:.2%}",
        f"- Group B (Treatment): {results['default_rate']['group_b']:.2%}",
        f"- Z-statistic: {results['default_rate']['z_statistic']:.4f}",
        f"- P-value: {results['default_rate']['p_value']:.6f}",
        f"- 95% CI: ({results['default_rate']['ci_95_lower']:.4f}, {results['default_rate']['ci_95_upper']:.4f})",
        f"- **Significant (α=0.05)**: {results['default_rate']['significant']}",
        "\n## Summary",
        "The new credit eligibility model (Group B) shows "
        + ("a statistically significant improvement" if results["approval_rate"]["significant"] else "no statistically significant improvement")
        + " in approval rate and "
        + ("a statistically significant reduction" if results["default_rate"]["significant"] else "no statistically significant reduction")
        + " in default rate vs. the control model.",
    ]
    return "\n".join(lines)


def save_json(results: dict, path: str = "results.json"):
    with open(path, "w") as f:
        json.dump(results, f, indent=2)