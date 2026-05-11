# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a **new credit eligibility model (Group B)** against their **current model (Group A)**. The goal is to determine whether the new model improves approval rates without increasing default rates — or ideally, improving both.

## Metrics Under Test

| Metric | Group A (Control) | Group B (Treatment) | Target Direction |
|---|---|---|---|
| Approval Rate | ~62% | ~71% | ↑ Higher is better |
| Default Rate | ~11% | ~9% | ↓ Lower is better |
| Avg Loan Size | Simulated | Simulated | Neutral |
| Processing Time | Simulated | Simulated | Neutral |

## Methodology

1. **Synthetic Data Generation**: 5,000 loan applications are simulated — 2,500 per group. Realistic noise is added to all metrics so results are not artificially clean.

2. **Statistical Testing**: A **two-proportion z-test** is run for approval_rate and default_rate. This tests whether the observed difference between groups is statistically significant.

3. **Reporting**: For each metric, we compute:
   - Z-statistic
   - P-value (two-tailed)
   - 95% confidence interval for the difference
   - Statistical conclusion at α = 0.05

## Files

- `src/data_generator.py` — Synthetic data generation
- `src/statistical.py` — Two-proportion z-test, CIs, power, MDE
- `src/simulate.py` — Experiment runner
- `src/report.py` — Human-readable output
- `run_pipeline.py` — Orchestrates the full pipeline