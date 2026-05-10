# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) improves upon their current model (Group A). The key metrics of interest are:

- **Approval Rate** — percentage of loan applications approved
- **Default Rate** — percentage of approved loans that go into default

The goal is to determine if the new model approves more loans without significantly increasing default risk, or ideally, improves both metrics.

## Methodology

### Experimental Design

- **Control (Group A):** Current eligibility model
- **Treatment (Group B):** New eligibility model
- **Sample size:** 5,000 applicants per group (10,000 total)
- **Assignment:** Simple random assignment, 50/50 split

### Target Parameters

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-------------------|---------------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

### Statistical Approach

We apply a **two-proportion z-test** to each metric independently. For each test:

1. **Null hypothesis (H₀):** No difference between group proportions
2. **Alternative (H₁):** Significant difference exists
3. **Significance level:** α = 0.05
4. **Test statistic:** Two-proportion z-test

We compute:
- **z-statistic** — standard normal test statistic
- **p-value** — two-tailed probability under H₀
- **95% confidence interval** — for the difference in proportions
- **Statistical power** — probability of detecting a true effect
- **Minimum detectable effect (MDE)** — smallest effect the study can detect

## Output

The pipeline produces:
- `results.json` — full statistical results for each metric
- Console summary — human-readable findings

## Files

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── run_pipeline.py
└── src/
    ├── __init__.py
    ├── data_generator.py
    ├── statistical.py
    ├── simulate.py
    └── report.py
```