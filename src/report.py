import json

def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    
    g = results['group_stats']
    lines.append("\n[Group Statistics]")
    lines.append(f"  Group A (Control): n={g['A']['n']}, approval={g['A']['approval_rate']:.2%}, default={g['A']['default_rate']:.2%}")
    lines.append(f"  Group B (Treatment): n={g['B']['n']}, approval={g['B']['approval_rate']:.2%}, default={g['B']['default_rate']:.2%}")
    
    for metric, label in [('approval_rate', 'Approval Rate'), ('default_rate', 'Default Rate')]:
        r = results[metric]
        sig = "SIGNIFICANT" if r['significant_at_0.05'] else "NOT SIGNIFICANT"
        lines.append(f"\n[{label}]")
        lines.append(f"  Control:  {r['group_a']:.2%}")
        lines.append(f"  Treatment: {r['group_b']:.2%}")
        lines.append(f"  Effect:   {r['treatment_effect']:+.2%}")
        lines.append(f"  z-stat:   {r['z_statistic']}")
        lines.append(f"  p-value:  {r['p_value']}")
        lines.append(f"  95% CI:   [{r['ci_95_lower']:.2%}, {r['ci_95_upper']:.2%}]")
        lines.append(f"  Power:    {r['statistical_power']:.2%}")
        lines.append(f"  Result:   {sig} at α=0.05")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

def save_json(results, path):
    with open(path, 'w') as f:
        json.dump(results, f, indent=2)