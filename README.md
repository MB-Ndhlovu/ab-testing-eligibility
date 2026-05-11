# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Treatment B) improves outcomes compared to their current model (Control A). The key metrics are:

- **Approval Rate**: Higher is better — more loans approved means more business
- **Default Rate**: Lower is better — fewer defaults means less losses

The goal is to determine if the new model produces a statistically significant improvement.

## Methodology

### Data Generation
- 5,000 synthetic loan applicants split evenly: 2,500 in Group A (control), 2,500 in Group B (treatment)
- Group A targets: approval_rate ≈ 0.62, default_rate ≈ 0.11
- Group B targets: approval_rate ≈ 0.71, default_rate ≈ 0.09
- Realistic noise added so results aren't perfectly clean

### Statistical Testing
- **Two-Proportion Z-Test** for both approval_rate and default_rate
- **Null Hypothesis (H₀)**: No difference between groups
- **Alternative Hypothesis (H₁)**: There is a difference
- **Significance Level**: α = 0.05
- Reports: z-statistic, p-value, 95% confidence interval, statistical conclusion

### Metrics Computed Per Group
- `approval_rate`: proportion of applications approved
- `default_rate`: proportion of approved loans that defaulted
- `avg_loan_size`: average loan amount (in generated synthetic data)
- `processing_time`: average processing duration in hours

## Output
- JSON results saved to `results.json`
- Human-readable summary report printed to console