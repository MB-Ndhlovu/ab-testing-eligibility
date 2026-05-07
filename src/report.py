"""Generate a human-readable summary report."""
from .simulate import run_simulation


ALPHA = 0.05


def format_result(name, result):
    """Build a readable text block for a single z-test result."""
    significant = result['p_value'] < ALPHA
    verdict = 'SIGNIFICANT' if significant else 'NOT SIGNIFICANT'
    symbol = '✓' if significant else '✗'

    return f"""
--- {name} ---
  Group A rate : {result['p_A']:.4f}
  Group B rate : {result['p_B']:.4f}
  Difference (B−A): {result['diff']:+.4f}
  Z-statistic   : {result['z_statistic']}
  P-value       : {result['p_value']:.6f}
  95% CI        : [{result['ci_lower']:.4f}, {result['ci_upper']:.4f}]
  Conclusion     : {verdict} at α={ALPHA} {symbol}
"""


def generate_report():
    """Return a formatted multi-line string report."""
    r = run_simulation()

    lines = [
        '=' * 60,
        '  A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY',
        '  Pipeline Report',
        '=' * 60,
        '',
        'GROUP SUMMARY',
        f"  Group A (control)  n={r['group_A']['n']}",
        f"    Approval rate   : {r['group_A']['approval_rate']:.4f}",
        f"    Default rate    : {r['group_A']['default_rate']:.4f}",
        f"    Avg loan size   : R{r['group_A']['avg_loan_size']:,.2f}",
        f"    Avg proc. time  : {r['group_A']['avg_processing_time']:.2f} hrs",
        '',
        f"  Group B (treatment) n={r['group_B']['n']}",
        f"    Approval rate   : {r['group_B']['approval_rate']:.4f}",
        f"    Default rate    : {r['group_B']['default_rate']:.4f}",
        f"    Avg loan size   : R{r['group_B']['avg_loan_size']:,.2f}",
        f"    Avg proc. time  : {r['group_B']['avg_processing_time']:.2f} hrs",
        '',
        '=' * 60,
        'STATISTICAL TESTS (Two-proportion Z-test, α=0.05)',
        format_result('Approval Rate', r['approval_rate_test']),
        format_result('Default Rate', r['default_rate_test']),
        f"  Minimum detectable effect @ 80% power: {r['mde_at_80_power']:.4f}",
        '',
        '=' * 60,
    ]
    return '\n'.join(lines)