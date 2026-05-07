# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) outperforms the current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans originated
- **Default Rate**: Lower is better — less credit risk

The experiment simulates a randomised controlled trial where each loan applicant is assigned to either the control (current model) or treatment (new model) group.

## Methodology

1. **Data Generation**: Synthetic dataset of 5,000 loan applications (2,500 per group) with realistic feature distributions
2. **Simulation**: Outcome variables are drawn from binomial distributions parameterised by true underlying rates with Poisson noise on counts
3. **Statistical Testing**: Two-proportion z-test for each metric, comparing Group A vs Group B
4. **Reporting**: Summary report with z-statistic, p-value, 95% CI, and statistical conclusion at α = 0.05

## Files

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data_generator.py   # Generate synthetic loan data
│   ├── statistical.py       # Z-test, CIs, power calculations
│   ├── simulate.py          # Run experiment + compute effects
│   └── report.py            # Human-readable summary
└── run_pipeline.py          # Orchestrate full workflow
```

## Key Results Interpretation

- **p < 0.05**: Reject H₀ → the difference is statistically significant
- **95% CI does not include 0**: Confirms significance via区间 estimation
- **Treatment effect**: Difference (B − A) with confidence interval

## Tech Stack

- Python 3.12
- numpy, scipy, matplotlib