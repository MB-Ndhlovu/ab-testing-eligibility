# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model improves key lending metrics compared to the current model. The experiment assigns loan applicants into two groups:

- **Group A (Control)**: Current eligibility model
- **Group B (Treatment)**: New eligibility model

The goal is to determine if Group B outperforms Group A on approval rate and default rate.

## Key Metrics

| Metric | Group A (Control) | Group B (Treatment) | Desired Direction |
|---|---|---|---|
| Approval Rate | ~62% | ~71% | Higher is better |
| Default Rate | ~11% | ~9% | Lower is better |
| Avg Loan Size | Simulated | Simulated | — |
| Processing Time | Simulated | Simulated | — |

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications per group with realistic noise
2. **Statistical Testing**: Two-proportion z-test for each binary metric (approval, default)
3. **Confidence Intervals**: 95% CI for the difference between proportions
4. **Decision Rule**: Reject null hypothesis if p-value < 0.05

## Files

- `src/data_generator.py` — Synthetic data generation
- `src/statistical.py` — Two-proportion z-test, CI, power analysis
- `src/simulate.py` — Experiment runner
- `src/report.py` — Formatted output
- `run_pipeline.py` — End-to-end execution