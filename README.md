# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) improves upon their current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans originated
- **Default Rate**: Lower is better — fewer losses from bad loans

The challenge: distinguish genuine improvement from random noise.

## Methodology

### Data Generation

Synthetic loan applicant data is generated for 5,000 applicants:

- **Group A (Control)**: Current eligibility model
  - Approval rate: ~62%
  - Default rate: ~11%
  - Avg loan size: ~$18,500
  - Processing time: ~4.2 days

- **Group B (Treatment)**: New eligibility model
  - Approval rate: ~71%
  - Default rate: ~9%
  - Avg loan size: ~$19,200
  - Processing time: ~3.8 days

Realistic noise (binomial sampling variation) is introduced so results aren't perfectly clean.

### Statistical Testing

A **two-proportion z-test** is used to compare each metric between groups:

$$z = \frac{\hat{p}_B - \hat{p}_A}{\sqrt{p(1-p)(\frac{1}{n_A} + \frac{1}{n_B})}}$$

Where $p$ is the pooled proportion.

Outputs per metric:
- z-statistic
- p-value (two-tailed)
- 95% confidence interval for the difference
- Statistical conclusion at α = 0.05

### Power Analysis

Minimum detectable effect (MDE) is computed at 80% power, α = 0.05, to determine the smallest effect size the experiment could detect given the sample size.

## Files

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── run_pipeline.py
└── src/
    ├── __init__.py
    ├── data_generator.py   # Generate synthetic loan data
    ├── statistical.py      # Two-proportion z-test, CI, power
    ├── simulate.py          # Run experiment, compute effects
    └── report.py            # Human-readable summary output
```