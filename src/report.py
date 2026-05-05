from src.simulate import run_experiment
from src.statistical import interpret_results
import json


def generate_report(results: dict) -> str:
    """Generate a readable summary report from experiment results."""
    metrics_a = results["metrics"]["group_a"]
    metrics_b = results["metrics"]["group_b"]
    approval_test = results["approval_rate_test"]
    default_test = results["default_rate_test"]
    power = results["power_analysis"]
    samples = results["sample_sizes"]

    lines = []
    lines.append("=" * 70)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY REPORT")
    lines.append("=" * 70)
    lines.append("")

    lines.append("EXPERIMENT SETUP")
    lines.append("-" * 40)
    lines.append(f"Group A (Control): Current eligibility model")
    lines.append(f"Group B (Treatment): New eligibility model")
    lines.append(f"Total Applicants: {samples['group_a'] + samples['group_b']}")
    lines.append(f"Significance Level (α): 0.05")
    lines.append("")

    lines.append("SAMPLE METRICS")
    lines.append("-" * 40)
    lines.append(f"{'Metric':<25} {'Group A':>15} {'Group B':>15}")
    lines.append("-" * 55)
    lines.append(f"{'Approval Rate':<25} {metrics_a['approval_rate']:>14.2%} {metrics_b['approval_rate']:>14.2%}")
    lines.append(f"{'Approval Count':<25} {metrics_a['approval_count']:>15} {metrics_b['approval_count']:>15}")
    lines.append(f"{'Default Rate':<25} {metrics_a['default_rate']:>14.2%} {metrics_b['default_rate']:>14.2%}")
    lines.append(f"{'Default Count':<25} {metrics_a['default_count']:>15} {metrics_b['default_count']:>15}")
    lines.append(f"{'Avg Loan Size ($)':<25} {metrics_a['avg_loan_size']:>15,.2f} {metrics_b['avg_loan_size']:>15,.2f}")
    lines.append(f"{'Avg Processing (hrs)':<25} {metrics_a['avg_processing_time']:>15.2f} {metrics_b['avg_processing_time']:>15.2f}")
    lines.append("")

    lines.append("APPROVAL RATE ANALYSIS")
    lines.append("-" * 40)
    lines.append(interpret_results(approval_test, "Approval Rate"))
    lines.append(f"  Treatment Effect: {approval_test['p_diff']:+.2%}")
    lines.append(f"  95% CI: [{approval_test['ci_lower']:.4f}, {approval_test['ci_upper']:.4f}]")
    lines.append(f"  Statistical Power: {power['approval_rate']['power']:.2%}")
    lines.append(f"  Min Detectable Effect: {power['approval_rate']['mde']:.4f}")
    lines.append("")

    lines.append("DEFAULT RATE ANALYSIS")
    lines.append("-" * 40)
    lines.append(interpret_results(default_test, "Default Rate"))
    lines.append(f"  Treatment Effect: {default_test['p_diff']:+.2%}")
    lines.append(f"  95% CI: [{default_test['ci_lower']:.4f}, {default_test['ci_upper']:.4f}]")
    lines.append(f"  Statistical Power: {power['default_rate']['power']:.2%}")
    lines.append(f"  Min Detectable Effect: {power['default_rate']['mde']:.4f}")
    lines.append("")

    lines.append("CONCLUSION")
    lines.append("-" * 40)
    approval_sig = approval_test["significant"]
    default_sig = default_test["significant"]

    if approval_sig and default_sig:
        lines.append("Group B shows SIGNIFICANT improvement in BOTH metrics:")
        lines.append(f"  - Approval rate is {'higher' if approval_test['p_diff'] > 0 else 'lower'} by {abs(approval_test['p_diff']):.2%}")
        lines.append(f"  - Default rate is {'lower' if default_test['p_diff'] < 0 else 'higher'} by {abs(default_test['p_diff']):.2%}")
        lines.append("RECOMMENDATION: Deploy the new credit eligibility model.")
    elif approval_sig:
        lines.append("Group B shows significant improvement in APPROVAL RATE only.")
        lines.append("RECOMMENDATION: Consider deployment with further monitoring of default rates.")
    elif default_sig:
        lines.append("Group B shows significant improvement in DEFAULT RATE only.")
        lines.append("RECOMMENDATION: Investigate why approval rate did not improve.")
    else:
        lines.append("No statistically significant difference detected between groups.")
        lines.append("RECOMMENDATION: Collect more data or adjust experiment parameters.")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def save_results_json(results: dict, filepath: str):
    """Save results summary to JSON file."""
    # Remove non-serializable data
    summary = {
        "metrics": results["metrics"],
        "approval_rate_test": {k: v for k, v in results["approval_rate_test"].items() if k != "significant" or isinstance(v, bool)},
        "default_rate_test": {k: v for k, v in results["default_rate_test"].items() if k != "significant" or isinstance(v, bool)},
        "power_analysis": results["power_analysis"],
        "sample_sizes": results["sample_sizes"]
    }

    # Convert numpy types to Python types for JSON serialization
    def convert_to_native(obj):
        if hasattr(obj, 'item'):
            return obj.item()
        if isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert_to_native(i) for i in obj]
        return obj

    summary = convert_to_native(summary)

    with open(filepath, "w") as f:
        json.dump(summary, f, indent=2)