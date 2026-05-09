# A/B Testing Framework for Credit Eligibility

## Business Problem

A consumer lender wants to evaluate whether a new credit eligibility model ("Model B") performs better than the current production model ("Model A"). The primary concern is twofold: **approval rate** (do we approve more deserving applicants?) and **default rate** (do we avoid bad loans?).

The new model is expected to:
- Increase approval rates (more good applicants pass through)
- Decrease default rates (better risk scoring)

We need statistical evidence before deploying to production.

## Methodology

1. **Experiment Design**: 5,000 synthetic loan applications are simulated — 2,500 assigned to Group A (control) and 2,500 to Group B (treatment). Each group gets eligibility decisions and outcomes from their respective models.

2. **Synthetic Data Generation**:
   - Group A (control): approval_rate ~62%, default_rate ~11%
   - Group B (treatment): approval_rate ~71%, default_rate ~9%
   - Realistic noise added (binomial sampling, covariate variation) so results aren't perfectly clean

3. **Statistical Testing**: Two-proportion z-test for each metric.
   - H₀: p_B - p_A = 0 (no difference)
   - H₁: p_B ≠ p_A (two-tailed)
   - Significance level: α = 0.05

4. **Metrics Reported**:
   - Z-statistic
   - P-value
   - 95% confidence interval for the difference
   - Statistical conclusion (significant / not significant)

## Files

| File | Purpose |
|------|---------|
| `src/data_generator.py` | Generate 5,000 synthetic loan records with group labels and outcomes |
| `src/statistical.py` | Two-proportion z-test, confidence intervals, power, MDE |
| `src/simulate.py` | Run the experiment and compute treatment effects |
| `src/report.py` | Human-readable summary of results |
| `run_pipeline.py` | Execute full pipeline, print results, save JSON |