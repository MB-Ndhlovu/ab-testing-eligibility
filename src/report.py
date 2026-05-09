"""Generate a readable summary report from simulation results."""
import json
import numpy as np

def format_results(results):
    lines = []
    lines.append("=" * 60)
    lines.append("        A/B TEST RESULTS — CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 60)

    for metric, data in results.items():
        lines.append(f"\n{'─' * 60}")
        lines.append(f"  METRIC: {metric.upper()}")
        lines.append(f"{'─' * 60}")

        if metric in ("approval_rate", "default_rate"):
            lines.append(f"  Group A (Control):  {data['group_a']:.4f}")
            lines.append(f"  Group B (Treatment): {data['group_b']:.4f}")
            lines.append(f"  Treatment Effect:   {data['treatment_effect']:+.4f}")
            lines.append(f"  z-statistic:        {data['z_statistic']:.4f}")
            lines.append(f"  p-value:            {data['p_value']:.4f}")
            lines.append(f"  95% CI:             [{data['ci_lower']:+.4f}, {data['ci_upper']:+.4f}]")
            lines.append(f"  Power:              {data['power']:.4f}")
            sig = "SIGNIFICANT" if data["significant"] else "NOT significant"
            lines.append(f"  Conclusion (α=0.05): {sig}")
        else:
            lines.append(f"  Group A (Control):  {data['group_a']:.4f}")
            lines.append(f"  Group B (Treatment): {data['group_b']:.4f}")
            lines.append(f"  Treatment Effect:   {data['treatment_effect']:+.4f}")

    lines.append("\n" + "=" * 60)
    lines.append("  SUMMARY")
    lines.append("=" * 60)
    ar_sig = "✓ YES" if results["approval_rate"]["significant"] else "✗ NO"
    dr_sig = "✓ YES" if results["default_rate"]["significant"] else "✗ NO"
    lines.append(f"  Approval rate lift significant? {ar_sig}")
    lines.append(f"  Default rate reduction significant? {dr_sig}")
    lines.append("=" * 60)

    return "\n".join(lines)

def save_json(results, path):
    def convert(obj):
        if isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        return obj
    serializable = {k: {mk: convert(v) for mk, v in m.items()} for k, m in results.items()}
    with open(path, "w") as f:
        json.dump(serializable, f, indent=2)