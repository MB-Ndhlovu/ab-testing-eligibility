# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) outperforms the current model (Group A). The goal is to determine if the new model:

1. Increases **approval rate** (good for business — more loans approved)
2. Lowers **default rate** (good for risk management — fewer defaults)

If the new model is statistically significantly better on both metrics, the lender will adopt it.

---

## Methodology

### Experiment Design

- **Population**: 5,000 loan applicants, randomly split 50/50 into two groups
- **Group A (Control)**: Current eligibility model
- **Group B (Treatment)**: New eligibility model
- **Metrics**:
  - `approval_rate` — proportion of applicants approved
  - `default_rate` — proportion of approved loans that default
  - `avg_loan_size` — average approved loan amount
  - `avg_processing_time` — average processing time in hours

### Target Outcomes

| Metric | Group A (Control) | Group B (Treatment) |
|---|---|---|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

### Statistical Test

For each of `approval_rate` and `default_rate`, we run a **two-proportion z-test**:

- **Null hypothesis (H₀)**: p_B - p_A = 0 (no difference)
- **Alternative hypothesis (H₁)**: p_B - p_A ≠ 0 (two-sided)
- **Significance level**: α = 0.05

**Test statistics:**
- Pooled proportion: p̂_pooled = (x_A + x_B) / (n_A + n_B)
- Standard error: SE = √(p̂_pooled × (1 - p̂_pooled) × (1/n_A + 1/n_B))
- Z-statistic: Z = (p̂_B - p̂_A) / SE

**Reported:**
- Z-statistic
- P-value (two-tailed)
- 95% confidence interval for the difference (p_B - p_A)
- Decision: Reject or fail to reject H₀ at α = 0.05

### Additional Outputs

- Statistical power (1 - β) at α = 0.05
- Minimum detectable effect (MDE) at 80% power