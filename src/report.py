"""Generate human-readable A/B test summary reports."""

import json
from typing import Dict, Any


def generate_report(experiment_output: dict, output_path: str = None) -> str:
    """Generate a full report from experiment output.

    Args:
        experiment_output: Dict from run_experiment.
        output_path: Optional path to save JSON results.

    Returns:
        Markdown-formatted report string.
    """
    stats = experiment_output["group_stats"]
    results = experiment_output["test_results"]

    lines = []
    lines.append("# A/B Test Report: Credit Eligibility Model\n")

    lines.append("## Experiment Setup")
    lines.append("- **Control**: Current eligibility model (Group A)")
    lines.append("- **Treatment**: New eligibility model (Group B)")
    lines.append("- **Sample size per group**: 2,500 applicants")
    lines.append("- **Significance level**: α = 0.05\n")

    lines.append("## Group Summary Statistics\n")
    lines.append("| Metric | Group A (Control) | Group B (Treatment) |")
    lines.append("|--------|-------------------|---------------------|")
    for group in ["A", "B"]:
        s = stats[group]
        lines.append(f"| Approval Rate | {s['approval_rate']:.4f} | {stats['B']['approval_rate']:.4f} |")
        lines.append(f"| Default Rate | {s['default_rate']:.4f} | {stats['B']['default_rate']:.4f} |")
        break

    lines.append("\n### Detailed Metrics\n")
    for group in ["A", "B"]:
        s = stats[group]
        lines.append(f"**Group {group}**")
        lines.append(f"- n = {s['n']}")
        lines.append(f"- Approval Rate: {s['approval_rate']:.4f} ({int(s['approval_rate']*s['n'])} approved)")
        lines.append(f"- Default Rate: {s['default_rate']:.4f}")
        lines.append(f"- Avg Loan Size: R{s['avg_loan_size']:,.2f}")
        lines.append(f"- Avg Processing Time: {s['avg_processing_time']:.1f} min")
        lines.append("")

    lines.append("## Statistical Test Results\n")
    lines.append("### Two-Proportion Z-Test (α = 0.05)\n")

    for metric, res in results.items():
        label = metric.replace("_", " ").title()
        sig_symbol = "✅" if res["significant_at_0.05"] else "❌"

        lines.append(f"#### {label} {sig_symbol}\n")
        lines.append(f"- Group A rate: `{res['group_a_rate']:.4f}`")
        lines.append(f"- Group B rate: `{res['group_b_rate']:.4f}`")
        lines.append(f"- Treatment effect: `{res['treatment_effect']:+.4f}`")
        lines.append(f"- Z-statistic: `{res['z_statistic']:.4f}`")
        lines.append(f"- P-value: `{res['p_value']:.6f}`")
        lines.append(f"- 95% CI: `[{res['ci_95_lower']:.4f}, {res['ci_95_upper']:.4f}]`")
        lines.append(f"- Statistical power: `{res['statistical_power']:.4f}`")
        lines.append(f"- MDE: `{res['mde']:.4f}`")
        lines.append(f"- **Conclusion: {res['conclusion']}**\n")

    lines.append("## Interpretation\n")
    ar = results["approval_rate"]
    dr = results["default_rate"]

    if ar["significant_at_0.05"]:
        lines.append(f"- Approval rate **increased by {ar['treatment_effect']:.2%}** (p={ar['p_value']:.4f})")
    else:
        lines.append(f"- Approval rate change not statistically significant (p={ar['p_value']:.4f})")

    if dr["significant_at_0.05"]:
        lines.append(f"- Default rate **decreased by {abs(dr['treatment_effect']):.2%}** (p={dr['p_value']:.4f})")
    else:
        lines.append(f"- Default rate change not statistically significant (p={dr['p_value']:.4f})")

    report_text = "\n".join(lines)

    if output_path:
        with open(output_path, "w") as f:
            json.dump(
                {
                    "group_stats": stats,
                    "test_results": results,
                },
                f,
                indent=2,
            )

    return report_text


def save_json_results(experiment_output: dict, filepath: str):
    """Save structured results as JSON."""
    with open(filepath, "w") as f:
        json.dump(
            {
                "group_stats": experiment_output["group_stats"],
                "test_results": experiment_output["test_results"],
            },
            f,
            indent=2,
        )
    print(f"Results saved to {filepath}")