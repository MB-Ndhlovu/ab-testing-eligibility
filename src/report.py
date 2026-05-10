"""Generate readable summary report for A/B test results."""

import json
from src.simulate import run_experiment


def generate_report(results, output_path="results.json"):
    """Generate and print summary report."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print("=" * 70)
    print("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    print("=" * 70)
    print()
    
    for metric, r in results.items():
        print(f"[{metric.upper()}]")
        print(f"  Group A rate : {r['rate_a']:.4f}")
        print(f"  Group B rate : {r['rate_b']:.4f}")
        print(f"  Effect (B-A) : {r['treatment_effect']:+.4f}")
        print(f"  z-statistic  : {r['z_statistic']:.4f}")
        print(f"  p-value      : {r['p_value']:.6f}")
        print(f"  95% CI       : [{r['ci_95'][0]:+.4f}, {r['ci_95'][1]:+.4f}]")
        print(f"  Significant  : {'YES' if r['significant'] else 'NO'} (α=0.05)")
        print(f"  Beneficial   : {'YES' if r['beneficial'] else 'NO'}")
        print()
    
    approval_sig = results["approval_rate"]["significant"]
    default_sig = results["default_rate"]["significant"]
    
    approval_effect = results["approval_rate"]["treatment_effect"]
    default_effect = results["default_rate"]["treatment_effect"]
    
    print("-" * 70)
    print("CONCLUSION")
    print("-" * 70)
    
    if approval_effect > 0 and not default_sig:
        rec = "APPROVE — Higher approvals with no significant increase in defaults."
    elif approval_effect > 0 and default_effect > 0 and not approval_sig:
        rec = "REJECT — Default rate increased significantly."
    elif approval_sig and default_sig and approval_effect > 0 and default_effect < 0:
        rec = "APPROVE — Strong improvement on both metrics."
    else:
        rec = "REVIEW NEEDED — Results inconclusive, manual review recommended."
    
    print(f"  Recommendation: {rec}")
    print("=" * 70)
    
    return results