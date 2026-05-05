# A/B Testing Framework for Credit Eligibility

## Business Problem

A consumer lender wants to evaluate whether a new credit eligibility model (treatment) performs better than their current model (control). The key metrics are:
- **Approval Rate** — higher is better (more loans originated)
- **Default Rate** — lower is better (fewer losses)

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control (Group A) and treatment (Group B).
2. **Synthetic Outcomes**: Group A uses current eligibility rules; Group B uses the new model.
   - Group A: approval_rate ≈ 62%, default_rate ≈ 11%
   - Group B: approval_rate ≈ 71%, default_rate ≈ 9% (new model is marginally better)
   - Realistic noise added so results are not perfectly clean
3. **Statistical Testing**: Two-proportion z-test for each metric.
   - Test: H₀: p_B = p_A vs H₁: p_B ≠ p_A
   - Significance level: α = 0.05
4. **Output**: z-statistic, p-value, 95% confidence interval for the difference, and a clear statistical conclusion.

## File Structure

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data_generator.py   # generate synthetic loan data
│   ├── statistical.py      # two-proportion z-test, CI, power
│   ├── simulate.py         # run experiment and compute effects
│   └── report.py           # human-readable summary
└── run_pipeline.py        # end-to-end execution
```

## Key Metrics

| Metric         | Group A (Control) | Group B (Treatment) | Direction |
|----------------|-------------------|----------------------|-----------|
| Approval Rate  | ~62%              | ~71%                 | ↑ better  |
| Default Rate   | ~11%              | ~9%                  | ↓ better  |