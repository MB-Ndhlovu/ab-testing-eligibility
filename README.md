# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) outperforms the current model (Group A). The goal is to make data-driven decisions about adopting the new model by running a proper statistical experiment.

**Key Questions:**
- Does the new model increase approval rates without significantly increasing default rates?
- Is the improvement statistically significant, or just noise?

## Methodology

### Experiment Design

- **Population:** Simulated loan applicants
- **Control Group (A):** Current eligibility model
- **Treatment Group (B):** New eligibility model
- **Sample Size:** 5,000 applicants split evenly (2,500 per group)

### Target Metrics

| Metric | Group A (Control) | Group B (Treatment) | Direction |
|--------|-------------------|---------------------|-----------|
| Approval Rate | ~62% | ~71% | Higher is better |
| Default Rate | ~11% | ~9% | Lower is better |
| Avg Loan Size | Varies | Varies | Contextual |
| Processing Time | Varies | Varies | Lower is better |

### Statistical Test

**Two-Proportion Z-Test** — Used to compare approval rates and default rates between groups.

For each metric:
1. Compute observed proportions in each group
2. Calculate pooled proportion under null hypothesis
3. Compute z-statistic: $z = \frac{p_B - p_A}{\sqrt{p(1-p)(1/n_A + 1/n_B)}}$
4. Calculate p-value from standard normal distribution
5. Construct 95% confidence interval for the difference
6. Conclude significance at α = 0.05

### Decision Rules

- **p-value < 0.05:** Reject null hypothesis → Statistically significant difference
- **p-value ≥ 0.05:** Fail to reject null hypothesis → No significant difference

## Files

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── statistical.py
│   ├── simulate.py
│   └── report.py
└── run_pipeline.py
```

## Getting Started

```bash
pip install -r requirements.txt
python run_pipeline.py
```