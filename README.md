# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (treatment group B) performs better than the current model (control group A). Better performance means:
- **Higher approval rate** — more loans approved without increasing risk
- **Lower default rate** — fewer loans that go into default

The framework simulates a credit decisioning experiment, generates synthetic data, and applies statistical inference to determine whether the difference between groups is statistically significant.

---

## Methodology

### Data Generation
- **Sample size**: 5,000 applicants per group (A and B)
- **Group A (Control)**: Current eligibility model
  - Approval rate: ~62%
  - Default rate: ~11% (conditional on approval)
  - Avg loan size: R50,000 ± R20,000
  - Processing time: 4.2s ± 1.5s
- **Group B (Treatment)**: New eligibility model
  - Approval rate: ~71% (+9pp lift)
  - Default rate: ~9% (−2pp improvement)
  - Avg loan size: R52,000 ± R22,000
  - Processing time: 3.8s ± 1.2s

Realistic noise is added so results are not perfectly clean.

### Statistical Analysis
For each metric, a **two-proportion z-test** is performed:
- Null hypothesis H₀: p_B − p_A = 0
- Alternative H₁: p_B ≠ p_A (two-sided)
- Significance level: α = 0.05

**Metrics tested:**
1. **Approval rate** — proportion of applicants approved
2. **Default rate** — proportion of approved loans that default

**Outputs:**
- Z-statistic and p-value
- 95% confidence interval for the difference
- Statistical conclusion (significant / not significant)

---

## Project Structure

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── run_pipeline.py
└── src/
    ├── __init__.py
    ├── data_generator.py   # Generate 5000-row synthetic dataset
    ├── statistical.py      # Two-proportion z-test, CIs, power
    ├── simulate.py          # Run experiment + compute effects
    └── report.py            # Human-readable summary report
```

---

## Key Statistical Concepts

### Two-Proportion Z-Test
Used to compare proportions from two independent groups:

```
z = (p̂_B - p̂_A) / √(p̂_pool * (1 - p̂_pool) * (1/n_A + 1/n_B))
```

Where `p̂_pool` is the pooled proportion under H₀.

### Confidence Interval
95% CI for the difference:

```
(p̂_B - p̂_A) ± 1.96 * SE
SE = √(p̂_A(1-p̂_A)/n_A + p̂_B(1-p̂_B)/n_B)
```

### Minimum Detectable Effect (MDE)
The smallest effect size the test can detect given:
- Sample size n per group
- Significance level α = 0.05 (power = 0.80)