"""Generate a human-readable summary report."""

import json


def format_rate(val):
    return f"{val:.4f}"


def format_pct(val):
    return f"{val * 100:.2f}%"


def generate_report(run_results):
    lines = []
    lines.append("=" * 65)
    lines.append("     A/B TEST RESULTS — CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 65)
    lines.append("")

    a = run_results["data"]["group_a"]
    b = run_results["data"]["group_b"]

    lines.append("DESCRIPTIVE STATISTICS")
    lines.append("-" * 40)
    lines.append(f"  Sample size  — Control: {a['n']:,}  Treatment: {b['n']:,}")
    lines.append("")

    for metric, label in [
        ("approval_rate", "Approval Rate"),
        ("default_rate", "Default Rate"),
    ]:
        s = run_results["stats"][metric]
        ctrl = s["control_rate"]
        treat = s["treatment_rate"]
        diff_pct = (treat - ctrl) / ctrl * 100
        direction = "▲" if diff_pct > 0 else "▼"
        sig = "SIGNIFICANT" if s["significant"] else "NOT SIGNIFICANT"

        lines.append(f"  {label}")
        lines.append(f"    Control:     {format_rate(ctrl)} ({format_pct(ctrl)})")
        lines.append(f"    Treatment:   {format_rate(treat)} ({format_pct(treat)})")
        lines.append(f"    Difference:  {s['diff']:+.4f} ({direction} {abs(diff_pct):.2f}%)")
        lines.append(f"    95% CI:      [{s['ci_95'][0]:+.4f}, {s['ci_95'][1]:+.4f}]")
        lines.append(f"    z-statistic: {s['z']:.4f}")
        lines.append(f"    p-value:     {s['p_value']:.6f}")
        lines.append(f"    MDE (80%):   {s['mde']:.4f}")
        lines.append(f"    Result:      {sig} at α=0.05")
        lines.append("")

    lines.append("SUMMARY")
    lines.append("-" * 40)
    ar_sig = run_results["stats"]["approval_rate"]["significant"]
    dr_sig = run_results["stats"]["default_rate"]["significant"]
    ar_better = run_results["stats"]["approval_rate"]["diff"] > 0
    dr_better = run_results["stats"]["default_rate"]["diff"] < 0

    if ar_sig and ar_better:
        lines.append("  ✓ Treatment approval rate is significantly HIGHER")
    if dr_sig and dr_better:
        lines.append("  ✓ Treatment default rate is significantly LOWER")

    if ar_sig and not ar_better:
        lines.append("  ✗ Treatment approval rate is significantly LOWER (unexpected)")

    if not ar_sig:
        lines.append("  — Approval rate difference not statistically significant")

    if not dr_sig:
        lines.append("  — Default rate difference not statistically significant")

    lines.append("")
    lines.append("=" * 65)

    return "\n".join(lines)


def save_report(run_results, path="report.json"):
    with open(path, "w") as f:
        json.dump(run_results, f, indent=2, default=float)


def print_and_save(run_results, json_path="results.json"):
    report = generate_report(run_results)
    print(report)
    save_report(run_results, json_path)
    print(f"\nResults saved to: {json_path}")
    return report