# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender currently uses a credit eligibility model (Group A - control). They have developed a new model (Group B - treatment) and want to determine if it improves outcomes before rolling out broadly.

**Key Metrics:**
- **Approval Rate**: Higher is better — more loans approved
- **Default Rate**: Lower is better — fewer defaults

**Decision**: If Group B shows statistically significant improvement, the lender will adopt the new model.

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control and treatment groups
2. **Two-Proportion Z-Test**: Test whether the observed differences are statistically significant
3. **Confidence Intervals**: Report 95% CI for the difference between groups
4. **Statistical Power**: Calculate minimum detectable effect given the sample size

## Expected Results

- Group A (control): approval_rate ≈ 62%, default_rate ≈ 11%
- Group B (treatment): approval_rate ≈ 71%, default_rate ≈ 9%
- The new model should show slight improvements on both metrics