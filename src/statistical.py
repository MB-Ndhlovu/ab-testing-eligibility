import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Tuple


@dataclass
class TwoProportionResult:
    """Results from a two-proportion z-test."""
    z_statistic: float
    p_value: float
    ci_lower: float
    ci_upper: float
    point_estimate: float
    control_rate: float
    treatment_rate: float
    significant: bool

    def summary(self) -> str:
        verdict = "SIGNIFICANT" if self.significant else "NOT SIGNIFICANT"
        return (
            f"z = {self.z_statistic:.4f}, p = {self.p_value:.4f}\n"
            f"95% CI: [{self.ci_lower:.4f}, {self.ci_upper:.4f}]\n"
            f"Point estimate: {self.point_estimate:.4f}\n"
            f"Conclusion (α=0.05): {verdict}"
        )


def two_proportion_z_test(
    control_successes: int,
    control_total: int,
    treatment_successes: int,
    treatment_total: int,
    alpha: float = 0.05,
    alternative: str = 'two-sided'
) -> TwoProportionResult:
    """
    Perform a two-proportion z-test comparing treatment vs control.

    Args:
        control_successes: Number of successes in control group
        control_total: Total size of control group
        treatment_successes: Number of successes in treatment group
        treatment_total: Total size of treatment group
        alpha: Significance level
        alternative: 'two-sided', 'greater', or 'less'

    Returns:
        TwoProportionResult with test statistics and confidence interval
    """
    p1 = control_successes / control_total
    p2 = treatment_successes / treatment_total

    # Pooled proportion under null hypothesis
    p_pooled = (control_successes + treatment_successes) / (control_total + treatment_total)

    # Standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/control_total + 1/treatment_total))

    # Z-statistic
    if se == 0:
        z_stat = 0.0
    else:
        z_stat = (p2 - p1) / se

    # P-value
    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    elif alternative == 'greater':
        p_value = 1 - stats.norm.cdf(z_stat)
    else:  # 'less'
        p_value = stats.norm.cdf(z_stat)

    # 95% Confidence Interval for the difference (unpooled)
    se_unpooled = np.sqrt(
        (p1 * (1 - p1) / control_total) + (p2 * (1 - p2) / treatment_total)
    )
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = (p2 - p1) - z_crit * se_unpooled
    ci_upper = (p2 - p1) + z_crit * se_unpooled

    return TwoProportionResult(
        z_statistic=z_stat,
        p_value=p_value,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        point_estimate=p2 - p1,
        control_rate=p1,
        treatment_rate=p2,
        significant=p_value < alpha
    )


def compute_power(
    p1: float,
    p2: float,
    n1: int,
    n2: int,
    alpha: float = 0.05
) -> float:
    """
    Compute statistical power for a two-proportion z-test.

    Args:
        p1: Control proportion
        p2: Treatment proportion
        n1: Control sample size
        n2: Treatment sample size
        alpha: Significance level

    Returns:
        Power (probability of detecting true difference)
    """
    se_null = np.sqrt(p1 * (1 - p1) * (1/n1 + 1/n2))
    if se_null == 0:
        return 0.0

    # Critical value on the null distribution
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Effect size
    delta = abs(p2 - p1)
    se_alternative = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se_alternative == 0:
        return 0.0

    # Power = P(reject null | true effect = delta)
    z_effect = delta / se_alternative
    power = 1 - stats.norm.cdf(z_crit * (se_null / se_alternative) - z_effect)

    return power


def minimum_detectable_effect(
    n1: int,
    n2: int,
    p1: float,
    alpha: float = 0.05,
    power: float = 0.80
) -> float:
    """
    Find minimum detectable effect (MDE) given sample sizes and power.

    Args:
        n1: Control sample size
        n2: Treatment sample size
        p1: Baseline proportion
        alpha: Significance level
        power: Desired power (default 0.80)

    Returns:
        Minimum detectable absolute difference in proportions
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    se_null = np.sqrt(2 * p1 * (1 - p1) / ((n1 + n2) / 2))

    # MDE formula for two independent proportions
    mde = (z_alpha + z_beta) * se_null

    return mde


if __name__ == '__main__':
    # Quick sanity check
    result = two_proportion_z_test(
        control_successes=1550,
        control_total=2500,
        treatment_successes=1775,
        treatment_total=2500
    )
    print("Test result:")
    print(result.summary())

    print(f"\nPower: {compute_power(0.62, 0.71, 2500, 2500):.4f}")
    print(f"MDE: {minimum_detectable_effect(2500, 2500, 0.62):.4f}")