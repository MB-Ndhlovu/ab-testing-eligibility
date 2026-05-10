# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) improves on their current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans approved)
- **Default Rate**: Lower is better (fewer defaults)
- **Avg Loan Size**: Context metric
- **Processing Time**: Operational efficiency

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control (A) and treatment (B)
2. **Statistical Testing**: Two-proportion z-test for approval and default rates
3. **Confidence Intervals**: 95% CI for the difference in proportions
4. **Power Analysis**: Compute statistical power and minimum detectable effect
5. **Reporting**: Clear summary of findings with actionable conclusions

## Hypotheses

- **Approval Rate**: H0: p_B ≤ p_A vs H1: p_B > p_A (one-sided, treatment should improve approvals)
- **Default Rate**: H0: p_B ≥ p_A vs H1: p_B < p_A (one-sided, treatment should reduce defaults)

## Success Criteria

- p-value < 0.05 for both metrics indicates the new model is statistically significantly better
- Practical significance: treatment effect size matters (not just statistical significance)