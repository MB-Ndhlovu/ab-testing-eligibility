"""Generate readable summary report from simulation results."""

import json


def generate_report(results: dict) -> str:
    """Build a human-readable string report."""
    stats = results["stats"]
    ap = results["approval_test"]
    dr = results["default_test"]
    n = results["n_per_group"]
    mde_app = results["approval_mde"]
    mde_def = results["default_mde"]

    lines = [
        "=" * 60,
        "  A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY",
        "  Summary Report",
        "=" * 60,
        "",
        f"Sample size per group: {n:,}",
        f"Alpha (significance level): 0.05",
        "",
        "--- Observed Group Metrics ---",
        f"  Group A (Control):",
        f"    Approval Rate : {stats['A']['approval_rate']:.4f}  ({int(stats['A']['approval_rate']*n):,} / {n:,})",
        f"    Default Rate  : {stats['A']['default_rate']:.4f}",
        f"    Avg Loan Size : R{stats['A']['avg_loan_size']:,.2f}",
        f"    Avg Proc Time : {stats['A']['avg_processing_time']:.2f}h",
        "",
        f"  Group B (Treatment):",
        f"    Approval Rate : {stats['B']['approval_rate']:.4f}  ({int(stats['B']['approval_rate']*n):,} / {n:,})",
        f"    Default Rate  : {stats['B']['default_rate']:.4f}",
        f"    Avg Loan Size : R{stats['B']['avg_loan_size']:,.2f}",
        f"    Avg Proc Time : {stats['B']['avg_processing_time']:.2f}h",
        "",
        "--- Approval Rate (Two-Proportion Z-Test) ---",
        f"  z-statistic : {ap['z_stat']:.4f}",
        f"  p-value     : {ap['p_value']:.6f}",
        f"  95% CI diff : [{ap['ci'][0]:+.4f}, {ap['ci'][1]:+.4f}]",
        f"  Significant : {'YES' if ap['significant'] else 'NO'}  (α=0.05)",
        "",
        "--- Default Rate (Two-Proportion Z-Test) ---",
        f"  z-statistic : {dr['z_stat']:.4f}",
        f"  p-value     : {dr['p_value']:.6f}",
        f"  95% CI diff : [{dr['ci'][0]:+.4f}, {dr['ci'][1]:+.4f}]",
        f"  Significant : {'YES' if dr['significant'] else 'NO'}  (α=0.05)",
        "",
        "--- Power Analysis ---",
        f"  Approval Rate MDE (80% power): {mde_app['mde']:.4f} ({mde_app['mde']*100:.2f}pp)",
        f"  Default Rate  MDE (80% power): {mde_def['mde']:.4f} ({mde_def['mde']*100:.2f}pp)",
        "",
        "--- Conclusion ---",
    ]

    if ap["significant"] and dr["significant"]:
        lines += [
            "  The new eligibility model (Group B) is significantly better.",
            "  -> Higher approval rate AND lower default rate detected.",
            "  Recommendation: ADOPT the new model.",
        ]
    elif ap["significant"]:
        lines += [
            "  Group B shows a significantly higher approval rate.",
            "  Default rate difference is not statistically significant.",
            "  Recommendation: REVIEW default rate impact before adopting.",
        ]
    elif dr["significant"]:
        lines += [
            "  Group B shows a significantly lower default rate.",
            "  Approval rate difference is not statistically significant.",
            "  Recommendation: REVIEW approval rate impact before adopting.",
        ]
    else:
        lines += [
            "  No statistically significant difference detected between groups.",
            "  Recommendation: CONTINUE monitoring; insufficient evidence to adopt.",
        ]

    lines += ["", "=" * 60]
    return "\n".join(lines)


def results_to_json(results: dict) -> str:
    """Serialize key results to JSON string."""
    def _serialize(obj):
        if hasattr(obj, "tolist"):
            return obj.tolist()
        if isinstance(obj, (float, int)):
            return float(obj)
        return obj

    output = {
        "n_per_group": results["n_per_group"],
        "stats_A": {k: _serialize(v) for k, v in results["stats"]["A"].items()},
        "stats_B": {k: _serialize(v) for k, v in results["stats"]["B"].items()},
        "approval_test": {k: _serialize(v) if k != "ci" else list(v)
                          for k, v in results["approval_test"].items()},
        "default_test": {k: _serialize(v) if k != "ci" else list(v)
                         for k, v in results["default_test"].items()},
        "approval_mde": {k: _serialize(v) for k, v in results["approval_mde"].items()},
        "default_mde": {k: _serialize(v) for k, v in results["default_mde"].items()},
    }
    return json.dumps(output, indent=2)