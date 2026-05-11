"""
Generates 5 000 synthetic loan applications split into control (A) and treatment (B).
Each row represents one loan application with:
  - group: 'A' or 'B'
  - approved: 0/1
  - defaulted: 0/1
  - loan_size: float (ZAR)
  - processing_time: float (hours)
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000
HALF = N // 2

# ── Group assignment ───────────────────────────────────────────────────────────
group = np.array(["A"] * HALF + ["B"] * HALF)

# ── Approval outcomes ──────────────────────────────────────────────────────────
# Group A: ~62 %  |  Group B: ~71 %
approved = np.where(
    group == "A",
    np.random.binomial(1, 0.62, N),
    np.random.binomial(1, 0.71, N),
)

# ── Default outcomes (only possible for approved loans) ───────────────────────
defaulted = np.where(
    approved == 1,
    np.where(
        group == "A",
        np.random.binomial(1, 0.11, N),
        np.random.binomial(1, 0.09, N),
    ),
    0,
)

# ── Loan size (ZAR) ───────────────────────────────────────────────────────────
base_size = np.random.uniform(10_000, 500_000, N)
loan_size = np.round(base_size * (1 + np.random.uniform(-0.05, 0.05, N)), 2)

# ── Processing time (hours) ───────────────────────────────────────────────────
base_time = np.random.uniform(0.5, 8.0, N)
processing_time = np.round(base_time * (1 + np.random.uniform(-0.1, 0.1, N)), 2)

# ── Assemble DataFrame ─────────────────────────────────────────────────────────
df = pd.DataFrame(
    {"group": group, "approved": approved, "defaulted": defaulted,
     "loan_size": loan_size, "processing_time": processing_time}
)

def get_summary_stats(df: pd.DataFrame) -> dict:
    out = {}
    for g in ("A", "B"):
        sub = df[df["group"] == g]
        n = len(sub)
        out[g] = {
            "n": n,
            "approval_rate": sub["approved"].mean(),
            "default_rate": sub["defaulted"].mean(),
            "avg_loan_size": sub["loan_size"].mean(),
            "avg_processing_time": sub["processing_time"].mean(),
        }
    return out

if __name__ == "__main__":
    df.to_csv("synthetic_data.csv", index=False)
    stats = get_summary_stats(df)
    print("=== Synthetic Data Summary ===")
    for g, s in stats.items():
        print(f"\nGroup {g} (n={s['n']}):")
        print(f"  Approval rate    : {s['approval_rate']:.4f}")
        print(f"  Default rate     : {s['default_rate']:.4f}")
        print(f"  Avg loan size    : ZAR {s['avg_loan_size']:,.2f}")
        print(f"  Avg process time  : {s['avg_processing_time']:.2f} hrs")