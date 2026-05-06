# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) outperforms their current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans approved
- **Default Rate**: Lower is better — fewer defaults

## Methodology

1. **Data Generation**: Simulate 5,000 loan applicants, randomly assigned to control (A) or treatment (B)
2. **Statistical Testing**: Two-proportion z-test for each metric at α = 0.05
3. **Reporting**: Confidence intervals, p-values, and statistical conclusions

## Results Interpretation

- If p-value < 0.05: Statistically significant difference detected
- 95% CI for difference must not include zero for significance
- Both metrics must show improvement for the new model to be recommended