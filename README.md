# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a new credit eligibility model (Group B - treatment) against their current model (Group A - control). The goal is to determine whether the new model improves approval rates and reduces default rates without adverse side effects.

## Key Metrics

- **Approval Rate**: Percentage of loan applications approved
- **Default Rate**: Percentage of approved loans that go into default
- **Average Loan Size**: Average dollar amount of approved loans
- **Processing Time**: Average time to process applications

## Methodology

### Data Generation

- 5,000 synthetic loan applications split evenly between Group A (control) and Group B (treatment)
- Group A simulates current eligibility rules: ~62% approval rate, ~11% default rate
- Group B simulates new eligibility rules: ~71% approval rate, ~9% default rate
- Realistic noise added to prevent perfectly clean results

### Statistical Analysis

Two-proportion z-test for each binary metric (approval_rate, default_rate):

```
H₀: p_B - p_A = 0 (no difference between models)
H₁: p_B - p_A ≠ 0 (significant difference exists)

z = (p̂_B - p̂_A) / √(p̄(1-p̄)(1/n_A + 1/n_B))

where p̄ = (x_A + x_B) / (n_A + n_B)
```

### Decision Criteria

- Significance level: α = 0.05
- 95% Confidence Intervals
- Statistical power considerations

## Expected Outcomes

- New model (B) should show higher approval rate
- New model (B) should show lower or similar default rate
- If results are statistically significant, recommend adopting new model