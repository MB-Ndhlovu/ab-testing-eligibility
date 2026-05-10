"""Run A/B experiment simulation and compute treatment effects."""

import pandas as pd
import numpy as np
from src.statistical import two_proportion_ztest, confidence_interval

ALPHA = 0.05


def run_experiment(data_path="data.csv"):
    """Run the A/B experiment analysis."""
    df = pd.read_csv(data_path)
    
    df_a = df[df["group"] == "A"]
    df_b = df[df["group"] == "B"]
    
    n_a = len(df_a)
    n_b = len(df_b)
    
    approved_a = int(df_a["approved"].sum())
    approved_b = int(df_b["approved"].sum())
    defaulted_a = int(df_a["defaulted"].sum())
    defaulted_b = int(df_b["defaulted"].sum())
    
    metrics = {
        "approval_rate": {
            "n_success": [approved_a, approved_b],
            "n_total": [n_a, n_b],
            "rate_a": df_a["approved"].mean(),
            "rate_b": df_b["approved"].mean(),
            "direction": "higher is better",
        },
        "default_rate": {
            "n_success": [defaulted_a, defaulted_b],
            "n_total": [n_a, n_b],
            "rate_a": df_a["defaulted"].mean(),
            "rate_b": df_b["defaulted"].mean(),
            "direction": "lower is better",
        },
    }
    
    results = {}
    for metric, data in metrics.items():
        z, p = two_proportion_ztest(data["n_success"], data["n_total"])
        ci_low, ci_high = confidence_interval(data["n_success"], data["n_total"])
        diff = data["rate_b"] - data["rate_a"]
        significant = p < ALPHA
        
        if data["direction"] == "higher is better":
            beneficial = diff > 0 and significant
        else:
            beneficial = diff < 0 and significant
        
        results[metric] = {
            "z_statistic": round(z, 4),
            "p_value": round(p, 6),
            "ci_95": (round(ci_low, 6), round(ci_high, 6)),
            "treatment_effect": round(diff, 6),
            "significant": bool(significant),
            "beneficial": bool(beneficial),
            "rate_a": round(data["rate_a"], 6),
            "rate_b": round(data["rate_b"], 6),
        }
    
    return results, df_a, df_b