# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) improves outcomes compared to the current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans approved)
- **Default Rate**: Lower is better (fewer defaults)

The goal is to determine if the new model produces statistically significant improvements before deploying it to production.

## Methodology

### Experiment Design
- **Control Group (A)**: Current eligibility model
- **Treatment Group (B)**: New eligibility model
- **Sample Size**: 5,000 applicants split evenly (2,500 per group)
- **Assignment**: Random assignment to ensure statistical validity

### Statistical Approach
We use a **two-proportion z-test** to compare each metric between groups:

```
H₀: p_A = p_B (no difference)
H₁: p_A ≠ p_B (significant difference)
```

Significance level: α = 0.05

### Metrics Collected
| Metric | Description | Direction |
|--------|-------------|-----------|
| Approval Rate | Proportion of applications approved | Higher is better |
| Default Rate | Proportion of approved loans that default | Lower is better |
| Avg Loan Size | Average loan amount | Monitor for risk |
| Processing Time | Average time to process application | Lower is better |

### Synthetic Data Generation
- **Group A**: approval_rate ~0.62, default_rate ~0.11
- **Group B**: approval_rate ~0.71, default_rate ~0.09
- Realistic noise added via binomial sampling

## Output

The pipeline produces:
1. Console summary report with z-statistics, p-values, and 95% CIs
2. JSON results file for programmatic consumption