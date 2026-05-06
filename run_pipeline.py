import json
import sys
from src.data_generator import generate_credit_data
from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Generating credit eligibility data...")
    df = generate_credit_data(n=5000, seed=42)
    df.to_csv('/home/workspace/Projects/ab-testing-eligibility/credit_data.csv', index=False)
    print(f"  Generated {len(df)} rows -> credit_data.csv")
    
    print("\nRunning A/B test simulation...")
    results = run_simulation(df)
    
    output_path = '/home/workspace/Projects/ab-testing-eligibility/results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved -> results.json")
    
    print("\n" + generate_report(results))
    
    return results

if __name__ == '__main__':
    results = main()