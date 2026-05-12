import json
from src.simulate import simulate_experiment, format_results
from src.report import generate_report, save_json_report

def main():
    print("Running A/B Testing Pipeline...")
    print()
    
    # Run experiment simulation
    results = simulate_experiment(seed=42)
    
    # Print console output
    console_output = format_results(results)
    print(console_output)
    
    # Generate and print full report
    report = generate_report(results)
    print("\n")
    print(report)
    
    # Save JSON results
    save_json_report(results, 'results.json')
    print("\nResults saved to results.json")
    
    # Return summary for Telegram
    approval_sig = results['approval_analysis']['significant']
    default_sig = results['default_analysis']['significant']
    approval_te = results['treatment_effect_approval']
    default_te = results['treatment_effect_default']
    
    summary = (
        f"Approval rate effect: {approval_te*100:+.2f}% "
        f"({'significant' if approval_sig else 'not significant'})\n"
        f"Default rate effect: {default_te*100:+.2f}% "
        f"({'significant' if default_sig else 'not significant'})\n"
        f"Recommendation: {'Adopt new model' if (approval_sig and default_sig) else 'Further analysis needed'}"
    )
    
    return results, summary

if __name__ == '__main__':
    results, summary = main()