# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (treatment group B) outperforms their current model (control group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans approved
- **Default Rate**: Lower is better — fewer defaults
- **Average Loan Size**: Informational metric
- **Processing Time**: Informational metric

## Methodology

1. **Data Generation**: Simulate 5,000 loan applicants per group with realistic noise:
   - Group A (Control): approval_rate ≈ 0.62, default_rate ≈ 0.11
   - Group B (Treatment): approval_rate ≈ 0.71, default_rate ≈ 0.09

2. **Statistical Testing**: Two-proportion z-test for approval_rate and default_rate
   - Null hypothesis: No difference between groups
   - Report: z-statistic, p-value, 95% CI for difference, significance at α=0.05

3. **Power Analysis**: Calculate statistical power and minimum detectable effect (MDE)

## Files

- `src/data_generator.py` — Generate synthetic loan data
- `src/statistical.py` — Z-test, confidence intervals, power analysis
- `src/simulate.py` — Run experiment simulation
- `src/report.py` — Generate summary report
- `run_pipeline.py` — Execute full pipeline

## Interpretation

| Metric | Significance | Implication |
|--------|-------------|-------------|
| p < 0.05 | Statistically significant | Reject null; new model is different |
| p ≥ 0.05 | Not significant | Insufficient evidence to reject null |

For approval_rate: significant positive difference → new model approves more
For default_rate: significant negative difference → new model defaults less
