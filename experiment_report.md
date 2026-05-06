# A/B Test Results: Credit Eligibility Model

**Generated:** 2026-05-06 02:15:01

## Executive Summary

| Metric | Group A (Control) | Group B (Treatment) | Difference | P-value | Significant? |
|--------|-------------------|---------------------|------------|---------|--------------|
| Approval Rate | 0.6188 | 0.7228 | +0.1040 | 0.000000 | ✅ YES |
| Default Rate | 0.1125 | 0.0891 | -0.0234 | 0.024392 | ✅ YES |

## Sample Information

- **Total Sample Size:** 5000
- **Control Group (A):** 2500 applicants
- **Treatment Group (B):** 2500 applicants
- **Significance Level (α):** 0.05

## Approval Rate Analysis

| Statistic | Value |
|-----------|-------|
| Control Rate | 0.6188 (1547/2500) |
| Treatment Rate | 0.7228 (1807/2500) |
| Difference | +0.1040 (+10.40%) |
| 95% Confidence Interval | [0.0781, 0.1299] |
| Z-statistic | 7.8246 |
| P-value | 0.000000 |
| Statistical Power | 1.0000 |
| Minimum Detectable Effect | 0.0385 |

**Conclusion:** The difference in approval rates is statistically significant.

## Default Rate Analysis

| Statistic | Value |
|-----------|-------|
| Control Rate | 0.1125 (174/1547 of approved) |
| Treatment Rate | 0.0891 (161/1807 of approved) |
| Difference | -0.0234 (-2.34%) |
| 95% Confidence Interval | [-0.0439, -0.0029] |
| Z-statistic | -2.2509 |
| P-value | 0.024392 |

**Conclusion:** The difference in default rates is statistically significant.

## Additional Metrics

| Metric | Group A | Group B |
|--------|---------|---------|
| Avg Loan Size ($k) | 81.79 | 87.93 |
| Avg Processing Time (min) | 19.19 | 13.92 |

## Interpretation

- **Approval Rate Lift:** +10.40%
- **Default Rate Lift:** -2.34%

## Final Recommendation

**DEPLOY THE NEW MODEL (Group B)**

The new credit eligibility model significantly outperforms the current model on both key metrics:
1. Higher approval rate (more loans originated)
2. Lower default rate (better credit quality)

