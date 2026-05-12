#!/usr/bin/env python3
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Running A/B Test Pipeline...")
    print("")

    # Run simulation
    results = run_simulation(n=5000, seed=42)

    # Generate and print report
    report = generate_report(results)
    print(report)

    # Save JSON results
    output_path = os.path.join(os.path.dirname(__file__), 'results.json')

    # Convert tuples to lists for JSON serialization
    results_json = {
        'n_A': results['n_A'],
        'n_B': results['n_B'],
        'approval': {
            'rate_A': float(results['approval']['rate_A']),
            'rate_B': float(results['approval']['rate_B']),
            'effect': float(results['approval']['effect']),
            'mde': float(results['approval']['mde']),
            'z_statistic': float(results['approval']['z_statistic']),
            'p_value': float(results['approval']['p_value']),
            'ci_95': [float(x) for x in results['approval']['ci_95']],
            'significant': bool(results['approval']['significant'])
        },
        'default': {
            'rate_A': float(results['default']['rate_A']),
            'rate_B': float(results['default']['rate_B']),
            'effect': float(results['default']['effect']),
            'mde': float(results['default']['mde']),
            'z_statistic': float(results['default']['z_statistic']),
            'p_value': float(results['default']['p_value']),
            'ci_95': [float(x) for x in results['default']['ci_95']],
            'significant': bool(results['default']['significant'])
        },
        'avg_loan_size': {
            'A': float(results['avg_loan_size']['A']),
            'B': float(results['avg_loan_size']['B'])
        },
        'avg_processing_time': {
            'A': float(results['avg_processing_time']['A']),
            'B': float(results['avg_processing_time']['B'])
        }
    }

    with open(output_path, 'w') as f:
        json.dump(results_json, f, indent=2)

    print("")
    print(f"Results saved to: {output_path}")

    return results

if __name__ == '__main__':
    main()