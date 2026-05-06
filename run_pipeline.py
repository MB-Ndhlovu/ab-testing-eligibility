#!/usr/bin/env python3
"""
A/B Testing Pipeline for Credit Eligibility Model Evaluation.

Run this script to execute the full experiment pipeline:
1. Generate synthetic loan data
2. Compute group metrics
3. Run statistical analysis
4. Print results and save reports
"""

import os
import sys
import json
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_generator import generate_loan_data, compute_group_metrics
from src.statistical import run_statistical_analysis
from src.report import generate_text_report, generate_markdown_report, save_report


def run_pipeline(n=5000, seed=42, alpha=0.05, output_dir=None):
    """
    Run the complete A/B testing pipeline.

    Args:
        n: Total sample size
        seed: Random seed for reproducibility
        alpha: Significance level
        output_dir: Directory to save outputs (default: script directory)

    Returns:
        dict with all experiment results
    """
    print("\n" + "=" * 70)
    print("A/B TESTING FRAMEWORK FOR CREDIT ELIGIBILITY")
    print("=" * 70)
    print(f"\nRunning pipeline with n={n}, seed={seed}, alpha={alpha}")

    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Generate data
    print("\n[1/5] Generating synthetic loan application data...")
    df = generate_loan_data(n=n, seed=seed)
    print(f"      Generated {len(df)} records")

    # Step 2: Compute metrics
    print("\n[2/5] Computing group metrics...")
    metrics = compute_group_metrics(df)

    for group in ['A', 'B']:
        m = metrics[group]
        print(f"      Group {group}: {m['approved_count']}/{m['n']} approved "
              f"(rate={m['approval_rate']:.4f}), "
              f"default rate={m['default_rate']:.4f}")

    # Step 3: Statistical analysis
    print("\n[3/5] Running statistical analysis (two-proportion z-test)...")
    stats_results = run_statistical_analysis(
        metrics['A'], metrics['B'], alpha=alpha
    )
    print("      Statistical tests complete")

    # Step 4: Compute treatment effects
    print("\n[4/5] Computing treatment effects...")
    treatment_effect = {
        'approval_rate_lift': metrics['B']['approval_rate'] - metrics['A']['approval_rate'],
        'default_rate_lift': metrics['B']['default_rate'] - metrics['A']['default_rate'],
        'avg_loan_size_A': float(metrics['A']['avg_loan_size']),
        'avg_loan_size_B': float(metrics['B']['avg_loan_size']),
        'avg_processing_time_A': float(metrics['A']['avg_processing_time']),
        'avg_processing_time_B': float(metrics['B']['avg_processing_time'])
    }

    # Compile results
    results = {
        'n': n,
        'seed': seed,
        'alpha': alpha,
        'metrics': metrics,
        'stats': stats_results,
        'treatment_effect': treatment_effect
    }

    # Step 5: Output results
    print("\n[5/5] Generating reports...")
    print("\n" + generate_text_report(results))

    # Save JSON results
    json_path = os.path.join(output_dir, 'experiment_results.json')
    serializable_results = {
        'n': n,
        'seed': seed,
        'alpha': alpha,
        'metrics': {
            group: {
                key: float(val) if isinstance(val, (np.floating, float)) else val
                for key, val in m.items()
            }
            for group, m in metrics.items()
        },
        'stats': stats_results,
        'treatment_effect': treatment_effect
    }

    with open(json_path, 'w') as f:
        json.dump(serializable_results, f, indent=2, default=str)
    print(f"\nJSON results saved to: {json_path}")

    # Save markdown report
    report_path = os.path.join(output_dir, 'experiment_report.md')
    report = generate_markdown_report(results)
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"Markdown report saved to: {report_path}")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)

    return results


def get_summary_for_telegram(results):
    """Extract key metrics for Telegram message."""
    ap = results['stats']['approval']
    dp = results['stats']['default']
    te = results['treatment_effect']

    summary = []
    summary.append(f"Approval Rate: A={results['metrics']['A']['approval_rate']:.4f}, B={results['metrics']['B']['approval_rate']:.4f}")
    summary.append(f"Default Rate: A={results['metrics']['A']['default_rate']:.4f}, B={results['metrics']['B']['default_rate']:.4f}")
    summary.append(f"Approval lift: {te['approval_rate_lift']*100:+.2f}%")
    summary.append(f"Default lift: {te['default_rate_lift']*100:+.2f}%")
    summary.append(f"Approval p-value: {ap['p_value']:.6f} {'(SIG)' if ap['significant'] else '(not sig)'}")
    summary.append(f"Default p-value: {dp['p_value']:.6f} {'(SIG)' if dp['significant'] else '(not sig)'}")

    return "\n".join(summary)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='A/B Testing Pipeline for Credit Eligibility')
    parser.add_argument('--n', type=int, default=5000, help='Total sample size')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--alpha', type=float, default=0.05, help='Significance level')
    parser.add_argument('--output-dir', type=str, default=None, help='Output directory')

    args = parser.parse_args()

    results = run_pipeline(n=args.n, seed=args.seed, alpha=args.alpha, output_dir=args.output_dir)

    # Print Telegram summary for copy
    print("\n--- TELEGRAM MESSAGE PREVIEW ---")
    print(get_summary_for_telegram(results))