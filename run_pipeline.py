"""Execute the full A/B testing pipeline."""

import subprocess
import sys
import json

def run_pipeline():
    print("Step 1: Generating synthetic data...")
    subprocess.run([sys.executable, "-c", "from src import data_generator; exec(open('src/data_generator.py').read())"], cwd="/home/workspace/Projects/ab-testing-eligibility")
    
    print("\nStep 2: Running experiment simulation...")
    from src.simulate import run_experiment
    results, _, _ = run_experiment()
    
    print("\nStep 3: Generating report...")
    from src.report import generate_report
    generate_report(results)
    
    print("\nPipeline complete. Results saved to results.json")
    return results

if __name__ == "__main__":
    results = run_pipeline()