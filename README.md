# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (treatment group B) outperforms their current model (control group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans originated)
- **Default Rate**: Lower is better (lower risk)

The new model is expected to improve both metrics simultaneously — more approvals with fewer defaults. However, the improvement must be statistically significant before deploying to production.

## Methodology

1. **Synthetic Data Generation**: Simulate 5,000 loan applications split evenly between control (A) and treatment (B)
2. **Two-Proportion Z-Test**: Test whether the observed difference in approval_rate and default_rate between groups is statistically significant
3. **Confidence Intervals**: Report 95% CI for the true difference in proportions
4. **Effect Size**: Report minimum detectable effect at 80% power

## Key Assumptions

| Parameter | Control (A) | Treatment (B) |
|-----------|-------------|---------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |
| Sample Size | 2,500 | 2,500 |
| Significance Level (α) | 0.05 | 0.05 |

## Files

- `src/data_generator.py` — Generate synthetic loan data
- `src/statistical.py` — Two-proportion z-test, CIs, power analysis
- `src/simulate.py` — Run experiment simulation
- `src/report.py` — Human-readable summary
- `run_pipeline.py` — Execute full pipeline

## Interpretation Guide

- **p < 0.05**: Statistically significant difference — reject null hypothesis
- **p ≥ 0.05**: Not statistically significant — cannot conclude improvement
- **CI excludes 0**: Consistent with statistically significant result