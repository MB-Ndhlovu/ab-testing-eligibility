import numpy as np
from scipy import stats
from typing import Tuple, Dict


def two_proportion_z_test(n1: int, x1: int, n2: int, x2: int) -> Dict:
    """
    Two-proportion z-test for comparing two proportions.

    Args:
        n1: Number of trials in group 1
        x1: Number of successes in group 1
        n2: Number of trials in group 2
        x2: Number of successes in group 2

    Returns:
        Dict with z_statistic, p_value (two-tailed), and confidence_interval
    """
    p1 = x1 / n1 if n1 > 0 else 0
    p2 = x2 / n2 if n2 > 0 else 0
    p_diff = p2 - p1

    # Pooled proportion
    p_pooled = (x1 + x2) / (n1 + n2) if (n1 + n2) > 0 else 0

    # Standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2)) if (n1 > 0 and n2 > 0) else 1

    # Z-statistic
    z_stat = (p_diff / se) if se > 0 else 0

    # P-value (two-tailed)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% CI for the difference (using unpooled SE)
    se_diff = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2) if (n1 > 0 and n2 > 0) else 1
    ci_lower = p_diff - 1.96 * se_diff
    ci_upper = p_diff + 1.96 * se_diff

    return {
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p1": p1,
        "p2": p2,
        "p_diff": p_diff,
        "significant": p_value < 0.05
    }


def calculate_statistical_power(n1: int, n2: int, effect_size: float,
                                 alpha: float = 0.05) -> float:
    """
    Calculate statistical power for a two-proportion z-test.

    Args:
        n1: Sample size group 1
        n2: Sample size group 2
        effect_size: Minimum detectable effect (difference in proportions)
        alpha: Significance level

    Returns:
        Statistical power (probability of detecting a true effect)
    """
    se = np.sqrt(1/n1 + 1/n2)
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_effect = effect_size / se
    power = stats.norm.cdf(z_effect - z_alpha) + stats.norm.cdf(-z_effect - z_alpha)
    return power


def minimum_detectable_effect(n1: int, n2: int, alpha: float = 0.05,
                               power: float = 0.80) -> float:
    """
    Calculate minimum detectable effect (MDE) for a two-proportion z-test.

    Args:
        n1: Sample size group 1
        n2: Sample size group 2
        alpha: Significance level
        power: Desired statistical power

    Returns:
        Minimum detectable effect (difference in proportions)
    """
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    se = np.sqrt(1/n1 + 1/n2)
    mde = (z_alpha + z_beta) * se
    return mde


def interpret_results(result: Dict, metric_name: str, alpha: float = 0.05) -> str:
    """Generate a human-readable interpretation of test results."""
    sig = result["significant"]
    z = result["z_statistic"]
    p = result["p_value"]
    diff = result["p_diff"]
    ci_l = result["ci_lower"]
    ci_u = result["ci_upper"]

    if sig:
        direction = "higher" if diff > 0 else "lower"
        return (f"{metric_name}: SIGNIFICANT — Group B has a {direction} rate "
                f"(diff={diff:.4f}, 95% CI [{ci_l:.4f}, {ci_u:.4f}]). "
                f"z={z:.3f}, p={p:.4f}")
    else:
        return (f"{metric_name}: NOT SIGNIFICANT — No evidence of difference "
                f"(diff={diff:.4f}, 95% CI [{ci_l:.4f}, {ci_u:.4f}]). "
                f"z={z:.3f}, p={p:.4f}")