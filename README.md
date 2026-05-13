# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) performs better than the current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans approved)
- **Default Rate**: Lower is better (fewer defaults)
- **Avg Loan Size**: Indicates loan magnitude
- **Processing Time**: Operational efficiency

## Methodology

1. **Generate synthetic data**: 5,000 applicants split evenly into control (A) and treatment (B)
2. **Run experiment simulation**: Apply realistic eligibility rules with noise
3. **Statistical testing**: Two-proportion z-test for approval_rate and default_rate
4. **Confidence intervals**: 95% CI for the difference between groups
5. **Power analysis**: Minimum detectable effect at 80% power

## Expected Outcomes

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-----------------|-------------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

The treatment effect is subtle — designed to test whether the framework can detect small but meaningful improvements in credit decisioning.