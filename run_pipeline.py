"""Execute the full A/B testing pipeline end-to-end."""
import json
import sys
from pathlib import Path

# Add project root to path so src/ is importable
sys.path.insert(0, str(Path(__file__).parent))

from src.report import generate_report
from src.simulate import run_simulation, save_results


def main():
    project_root = Path(__file__).parent
    output_json = project_root / 'results.json'

    print("Running A/B test pipeline ...")
    results = run_simulation()
    save_results(results, output_json)
    print(f"JSON results saved → {output_json}")

    report = generate_report()
    print(report)

    # Print machine-readable summary for Telegram
    ar = results['approval_rate_test']
    dr = results['default_rate_test']

    ar_sig = '✓ SIGNIFICANT' if ar['p_value'] < 0.05 else '✗ not significant'
    dr_sig = '✓ SIGNIFICANT' if dr['p_value'] < 0.05 else '✗ not significant'

    print("\n=== MACHINE SUMMARY ===")
    print(f"Approval Rate : A={ar['p_A']:.4f} B={ar['p_B']:.4f} diff={ar['diff']:+.4f} "
          f"p={ar['p_value']:.6f} [{ar['ci_lower']:.4f}, {ar['ci_upper']:.4f}] {ar_sig}")
    print(f"Default Rate   : A={dr['p_A']:.4f} B={dr['p_B']:.4f} diff={dr['diff']:+.4f} "
          f"p={dr['p_value']:.6f} [{dr['ci_lower']:.4f}, {dr['ci_upper']:.4f}] {dr_sig}")


if __name__ == '__main__':
    main()