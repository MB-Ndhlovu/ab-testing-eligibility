"""Run the A/B experiment simulation and compute treatment effects."""
import json
from pathlib import Path

from .data_generator import generate_data
from .statistical import two_proportion_ztest, power_min_detectable_effect


def run_simulation(seed=42):
    """Generate data and run statistical tests for all metrics.

    Returns
    -------
    dict with metrics, group summaries, and test results
    """
    df = generate_data()

    # Group summaries
    def grp_summary(g):
        gdf = df[df['group'] == g]
        n = len(gdf)
        approved = int(gdf['approved'].sum())
        defaulted = int(gdf['defaulted'].sum())
        defaulted = min(defaulted, approved)  # can't default more than approved
        avg_loan = float(gdf['loan_size'].mean())
        avg_proc = float(gdf['processing_time_hours'].mean())
        return {
            'n': n,
            'approval_rate': round(approved / n, 6),
            'default_rate': round(defaulted / approved, 6) if approved > 0 else 0.0,
            'avg_loan_size': round(avg_loan, 2),
            'avg_processing_time': round(avg_proc, 4),
            'approved': approved,
            'defaulted': defaulted,
        }

    summary_A = grp_summary('A')
    summary_B = grp_summary('B')

    # Two-proportion z-tests
    approval_test = two_proportion_ztest(
        summary_A['n'], summary_A['approved'],
        summary_B['n'], summary_B['approved'],
    )
    default_test = two_proportion_ztest(
        summary_A['n'], summary_A['defaulted'],
        summary_B['n'], summary_B['defaulted'],
    )

    mde = power_min_detectable_effect(summary_A['n'], summary_B['n'])

    return {
        'group_A': summary_A,
        'group_B': summary_B,
        'approval_rate_test': approval_test,
        'default_rate_test': default_test,
        'mde_at_80_power': mde,
    }


def save_results(results, path='results.json'):
    with open(path, 'w') as f:
        json.dump(results, f, indent=2, default=str)