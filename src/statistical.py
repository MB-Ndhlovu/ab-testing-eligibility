"""Statistical tests and power analysis for two-proportion A/B tests."""

import numpy as np
from scipy import stats
from typing import NamedTuple


class ZTestResult(NamedTuple):
    """Result of a two-proportion z-test."""
    z_statistic: float
    p_value: float
    ci_lower: float
    ci_upper: float
    point_estimate: float
    significant: bool
    alpha: float

    def summary(self) -> str:
        verdict = "SIGNIFICANT" if self.significant else "not significant"
        return (
            f"  z-statistic  : {self.z_statistic:+.4f}\n"
            f"  p-value      : {self.p_value:.4f}\n"
            f"  95% CI       : [{self.ci_lower:+.4f}, {self.ci_upper:+.4f}]\n"
            f"  Point est.    : {self.point_estimate:+.4f}\n"
            f"  Conclusion    : {verdict} at α={self.alpha}"
        )


def two_proportion_ztest(
    n_treatment: int,
    n_control: int,
    conversions_treatment: int,
    conversions_control: int,
    alpha: float = 0.05,
    alternative: str = "two-sided",
) -> ZTestResult:
    """
    Two-proportion z-test comparing treatment vs. control conversion rates.

    Parameters
    ----------
    n_treatment : total sample size in treatment group
    n_control : total sample size in control group
    conversions_treatment : number of successes in treatment
    conversions_control : number of successes in control
    alpha : significance level (default 0.05)
    alternative : 'two-sided' (default), 'larger', or 'smaller'

    Returns
    -------
    ZTestResult with z-statistic, p-value, 95% CI, and significance flag.
    """
    p1 = conversions_treatment / n_treatment  # treatment rate
    p2 = conversions_control / n_control       # control rate
    point_est = p1 - p2                         # observed difference

    # Pooled proportion under null hypothesis
    p_pool = (conversions_treatment + conversions_control) / (n_treatment + n_control)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_treatment + 1 / n_control))

    if se == 0:
        raise ValueError("Standard error is zero — check sample sizes and conversions.")

    z_stat = (p1 - p2) / se

    if alternative == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    elif alternative == "larger":
        p_value = 1 - stats.norm.cdf(z_stat)
    else:  # smaller
        p_value = stats.norm.cdf(z_stat)

    # WALD 95% confidence interval for the difference
    se_diff = np.sqrt(p1 * (1 - p1) / n_treatment + p2 * (1 - p2) / n_control)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = point_est - z_crit * se_diff
    ci_upper = point_est + z_crit * se_diff

    significant = p_value < alpha

    return ZTestResult(
        z_statistic=round(z_stat, 4),
        p_value=round(p_value, 6),
        ci_lower=round(ci_lower, 4),
        ci_upper=round(ci_upper, 4),
        point_estimate=round(point_est, 4),
        significant=significant,
        alpha=alpha,
    )


def compute_power(
    n_total: int,
    p_control: float,
    mde: float,
    alpha: float = 0.05,
) -> float:
    """
    Compute statistical power for a two-proportion test.

    Assumes equal allocation between treatment and control.

    Parameters
    ----------
    n_total : total sample size across both groups
    p_control : baseline conversion rate in control group
    mde : minimum detectable effect (absolute difference)
    alpha : significance level

    Returns
    -------
    Power (probability of detecting a true effect of size mde).
    """
    n = n_total // 2
    p1 = p_control + mde

    se_null = np.sqrt(2 * p_control * (1 - p_control) / n)
    se_alt  = np.sqrt(p1 * (1 - p1) / n + p_control * (1 - p_control) / n)

    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = (mde - z_crit * se_null) / se_alt

    power = stats.norm.cdf(z_power)
    return round(power, 4)


def minimum_detectable_effect(
    n_total: int,
    p_control: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> float:
    """
    Compute the minimum detectable effect (MDE) at given power.

    Parameters
    ----------
    n_total : total sample size across both groups
    p_control : baseline conversion rate in control group
    alpha : significance level
    power : desired statistical power (default 0.80)

    Returns
    -------
    Minimum absolute difference in proportions that can be detected.
    """
    n = n_total // 2
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta  = stats.norm.ppf(power)

    se_null = np.sqrt(2 * p_control * (1 - p_control) / n)

    mde = (z_alpha + z_beta) * se_null
    return round(mde, 4)


def required_sample_size(
    p_control: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> int:
    """
    Required total sample size (both groups) for a two-proportion test.

    Returns
    -------
    Total n needed per group.
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta  = stats.norm.ppf(power)

    p1 = p_control + mde
    se_sq = 2 * p_control * (1 - p_control) + 2 * p1 * (1 - p1)
    n = int(np.ceil(((z_alpha + z_beta) ** 2 * se_sq) / (mde ** 2)))
    return n


if __name__ == "__main__":
    # Smoke test
    result = two_proportion_ztest(2500, 2500, 1775, 1550)
    print(result.summary())

    print(f"\nPower for MDE=0.05, n=5000, p=0.62: {compute_power(5000, 0.62, 0.05):.2%}")
    print(f"MDE with 5000 samples, p=0.62, power=0.80: {minimum_detectable_effect(5000, 0.62):.4f}")
    print(f"Required n per group: {required_sample_size(0.62, 0.05)}")