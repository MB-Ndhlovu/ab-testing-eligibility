# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (treatment group B) outperforms their current model (control group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans approved
- **Default Rate**: Lower is better — fewer bad loans

The goal is to determine if the new model produces a statistically significant improvement without harming the portfolio.

## Methodology

### Data Generation
- 5,000 synthetic loan applications
- Group A (control): current eligibility model
  - Target approval rate: ~62%
  - Target default rate: ~11%
- Group B (treatment): new eligibility model
  - Target approval rate: ~71%
  - Target default rate: ~9%
- Realistic noise added (binomial sampling) so results are not perfectly clean

### Statistical Testing
- **Two-proportion z-test** for each metric
- Null hypothesis: no difference between group proportions
- Alternative hypothesis: significant difference exists
- Significance level: α = 0.05

### Output Metrics
For each metric (approval_rate, default_rate):
- Z-statistic
- P-value (two-tailed)
- 95% Confidence Interval for the difference
- Statistical conclusion (significant / not significant)

## Files

| File | Purpose |
|------|---------|
| `src/data_generator.py` | Generate synthetic loan data for both groups |
| `src/statistical.py` | Two-proportion z-test, CIs, power analysis |
| `src/simulate.py` | Run experiment simulation and compute treatment effects |
| `src/report.py` | Generate human-readable summary report |
| `run_pipeline.py` | Orchestrate full pipeline, print results, save JSON |