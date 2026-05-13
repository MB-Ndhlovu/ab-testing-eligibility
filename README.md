# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender currently uses an eligibility model (Group A - Control) that approves approximately 62% of applicants with a default rate of 11%. A new credit eligibility model (Group B - Treatment) is proposed with a target improvement: higher approval rate (~71%) and lower default rate (~9%).

We need to rigorously test whether the new model actually delivers these improvements before deploying it to production.

## Methodology

### Data Generation
- 5,000 synthetic loan applications generated per group
- Group A (Control): Current eligibility model
- Group B (Treatment): New eligibility model
- Realistic noise added to simulate real-world variance

### Statistical Approach
- **Two-Proportion Z-Test**: Compare approval and default rates between groups
- **Confidence Intervals**: 95% CI for the difference in proportions
- **Null Hypothesis (H₀)**: No difference in rates between groups
- **Alternative Hypothesis (H₁)**: There is a difference in rates
- **Significance Level (α)**: 0.05

### Key Metrics
| Metric | Group A (Control) | Group B (Treatment) | Desired Direction |
|--------|-------------------|---------------------|-------------------|
| Approval Rate | ~0.62 | ~0.71 | ↑ |
| Default Rate | ~0.11 | ~0.09 | ↓ |
| Avg Loan Size | Simulated | Simulated | Contextual |
| Processing Time | Simulated | Simulated | Contextual |

## Output
- Full statistical report with z-statistics, p-values, and confidence intervals
- JSON results file for programmatic consumption
- Pass/fail conclusion for each metric at α=0.05