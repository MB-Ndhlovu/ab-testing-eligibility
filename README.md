# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a **new credit eligibility model (Group B)** performs better than the **current model (Group A)**. The new model is expected to:
- Increase approval rates (more good borrowers approved)
- Decrease default rates (fewer bad borrowers approved)

The experiment is run as an A/B test on 5,000 synthetic loan applications — 2,500 per group.

## Metrics

| Metric | Group A (Control) | Group B (Treatment) | Direction |
|---|---|---|---|
| Approval Rate | ~62% | ~71% | Higher is better |
| Default Rate | ~11% | ~9% | Lower is better |
| Avg Loan Size | Simulated | Simulated | Context |
| Processing Time | Simulated | Simulated | Context |

## Methodology

1. **Data Generation**: Synthetic loan applications are generated with realistic distributions for both groups.
2. **Statistical Testing**: A two-proportion z-test is applied to approval and default rates.
3. **Confidence Intervals**: 95% CI for the difference between groups.
4. **Decision**: Significant at α = 0.05 if p-value < 0.05.

## Output

- Console summary report
- `results.json` with full statistical output