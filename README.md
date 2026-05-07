# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) outperforms their current model (Group A). The goal is to make data-driven decisions about adopting the new model by rigorously testing the difference in key business metrics.

## Metrics Under Test

| Metric | Group A (Control) | Group B (Treatment) | Direction |
|--------|------------------|---------------------|-----------|
| Approval Rate | ~62% | ~71% | Higher is better |
| Default Rate | ~11% | ~9% | Lower is better |
| Avg Loan Size | Simulated | Simulated | Contextual |
| Processing Time | Simulated | Simulated | Lower is better |

## Methodology

### Statistical Approach
- **Test**: Two-Proportion Z-Test (for approval_rate and default_rate)
- **Significance Level**: α = 0.05
- **Confidence Intervals**: 95% CI for the difference between proportions

### Key Outputs
- Z-statistic and p-value for each metric
- 95% Confidence Interval for the treatment effect
- Statistical power and minimum detectable effect (MDE)
- Clear GO/NO-GO recommendation per metric

## Project Structure

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── run_pipeline.py
└── src/
    ├── __init__.py
    ├── data_generator.py   # Generate 5000 synthetic loan records
    ├── statistical.py     # Z-test, CI, power, MDE calculations
    ├── simulate.py        # Run experiment and compute effects
    └── report.py          # Human-readable summary
```