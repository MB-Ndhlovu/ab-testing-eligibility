# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a new credit eligibility model (Group B / treatment) against their current model (Group A / control). The goal is to determine whether the new model improves approval rates and reduces default rates without introducing statistical false positives.

## Methodology

- **Population**: 5,000 synthetic credit applications, split 50/50 into control (A) and treatment (B)
- **Control Group (A)**: Current eligibility model
  - Approval rate: ~62%
  - Default rate: ~11%
- **Treatment Group (B)**: New eligibility model
  - Approval rate: ~71% (improved)
  - Default rate: ~9% (improved)
- **Metrics tested**: Approval rate, Default rate
- **Statistical test**: Two-proportion z-test (α = 0.05)
- **Output**: z-statistic, p-value, 95% CI for difference, statistical conclusion

## Files

| File | Purpose |
|------|---------|
| `src/data_generator.py` | Generate synthetic credit application data |
| `src/statistical.py` | Two-proportion z-test, CI, power, MDE |
| `src/simulate.py` | Run experiment simulation |
| `src/report.py` | Generate readable summary report |
| `run_pipeline.py` | Execute full pipeline and save JSON results |

## Getting Started

```bash
pip install -r requirements.txt
python run_pipeline.py
```