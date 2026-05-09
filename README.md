# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) improves key lending metrics compared to their current model (Group A). The experiment runs on synthetic applicant data and measures:

- **Approval Rate** — higher is better (more loans originated)
- **Default Rate** — lower is better (less credit risk)
- **Average Loan Size** — secondary metric
- **Processing Time** — secondary metric (operational efficiency)

## Methodology

1. **Generate synthetic data**: 5,000 simulated credit applicants split 50/50 into control (A) and treatment (B) groups
2. **Apply eligibility rules**: Group A uses current (tighter) rules; Group B uses new (looser) rules with slight noise for realism
3. **Simulate outcomes**: Each applicant who is approved may default; loan size and processing time vary by credit tier
4. **Statistical testing**: Two-proportion z-test for approval_rate and default_rate; report z-statistic, p-value, 95% CI, and significance at α=0.05
5. **Decision**: Launch recommendation based on statistical and business significance

## Key Results (Interpretation)

| Metric | Group A | Group B | Δ | z | p-value | Significant? |
|--------|---------|---------|---|----|--------|-------------|
| Approval Rate | ~62% | ~71% | +9pp | ... | <0.05 | Yes → B better |
| Default Rate | ~11% | ~9% | −2pp | ... | <0.05 | Yes → B better |

**Recommendation**: Adopt Group B model if results are significant — it approves more applicants with a lower default rate, a rare win-win scenario.

## Files

- `src/data_generator.py` — Synthetic data generation
- `src/statistical.py` — Two-proportion z-test, CI, power, MDE
- `src/simulate.py` — Experiment runner
- `src/report.py` — Human-readable summary
- `run_pipeline.py` — End-to-end execution