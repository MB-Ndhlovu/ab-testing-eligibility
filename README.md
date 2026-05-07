# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) outperforms their current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans originated)
- **Default Rate**: Lower is better (less credit risk)

The challenge is distinguishing genuine improvement from random noise in a controlled experiment.

## Methodology

### Experimental Design

- **Control Group (A)**: Current eligibility model
- **Treatment Group (B)**: New eligibility model
- **Sample Size**: 5,000 applicants per group (10,000 total)
- **Allocation**: 50/50 random split

### Target Metrics

| Metric | Group A (Control) | Group B (Treatment) | Direction |
|--------|-------------------|---------------------|-----------|
| Approval Rate | ~62% | ~71% | ↑ better |
| Default Rate | ~11% | ~9% | ↓ better |

### Statistical Approach

We use a **two-proportion z-test** for each metric to determine if the difference between groups is statistically significant at α = 0.05.

For each metric:
1. Compute observed proportions for each group
2. Calculate the pooled proportion under null hypothesis
3. Compute z-statistic: `z = (p_B - p_A) / sqrt(p_pool * (1 - p_pool) * (1/n_A + 1/n_B))`
4. Calculate p-value from standard normal distribution
5. Construct 95% confidence interval for the true difference

### Key Thresholds

- **α (significance level)**: 0.05
- **Power**: 80% minimum
- **Minimum Detectable Effect**: Calculated for each metric

## Output

The pipeline produces:
- JSON results file: `results.json`
- Console summary report
- Statistical conclusions per metric

## Files

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── run_pipeline.py
└── src/
    ├── __init__.py
    ├── data_generator.py   # Synthetic data generation
    ├── statistical.py      # Two-proportion z-test implementation
    ├── simulate.py          # Experiment simulation
    └── report.py            # Report generation
```