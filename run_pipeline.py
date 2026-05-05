import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.simulate import run_simulation
from src.report import generate_report, save_results_json

def main():
    print("Running A/B Test Simulation...")
    print("")
    
    results, df, summary = run_simulation(seed=42)
    
    report = generate_report(results)
    print(report)
    
    os.makedirs('output', exist_ok=True)
    save_results_json(results, 'output/ab_test_results.json')
    df.to_csv('output/credit_data.csv', index=False)
    summary.to_csv('output/group_summary.csv', index=False)
    
    print(f"Results saved to output/ab_test_results.json")
    print(f"Data saved to output/credit_data.csv")
    print(f"Summary saved to output/group_summary.csv")
    
    return results

if __name__ == "__main__":
    results = main()