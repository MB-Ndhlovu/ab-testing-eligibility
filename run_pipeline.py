"""Execute the full A/B testing pipeline."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.report import generate_report

def main():
    print("Running A/B Testing Pipeline...")
    print()

    from src.simulate import run_experiment

    results = run_experiment(n=5000, alpha=0.05)
    report = generate_report(results, output_path='results.json')

    print(report)
    print("\nPipeline completed successfully.")

if __name__ == '__main__':
    main()