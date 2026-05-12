import numpy as np
import pandas as pd

np.random.seed(42)

N = 2500  # per group

def generate_data():
    # Group A (control): approval ~0.62, default ~0.11
    group_a_approved = np.random.rand(N) < 0.62
    group_a_defaulted = np.zeros(N, dtype=bool)
    group_a_defaulted[group_a_approved] = np.random.rand(group_a_approved.sum()) < 0.11

    # Group B (treatment): approval ~0.71, default ~0.09
    group_b_approved = np.random.rand(N) < 0.71
    group_b_defaulted = np.zeros(N, dtype=bool)
    group_b_defaulted[group_b_approved] = np.random.rand(group_b_approved.sum()) < 0.09

    # Processing time (seconds) - skewed distribution
    group_a_time = np.random.lognormal(mean=4.0, sigma=0.5, size=N)
    group_b_time = np.random.lognormal(mean=3.8, sigma=0.5, size=N)

    # Loan amounts (in ZAR) - skewed distribution
    group_a_amounts = np.random.lognormal(mean=10.5, sigma=0.9, size=N) * 1000
    group_b_amounts = np.random.lognormal(mean=10.5, sigma=0.9, size=N) * 1000

    # Build DataFrame
    df_a = pd.DataFrame({
        'group': 'A',
        'approved': group_a_approved,
        'defaulted': group_a_defaulted,
        'processing_time': group_a_time,
        'loan_amount': group_a_amounts,
    })

    df_b = pd.DataFrame({
        'group': 'B',
        'approved': group_b_approved,
        'defaulted': group_b_defaulted,
        'processing_time': group_b_time,
        'loan_amount': group_b_amounts,
    })

    df = pd.concat([df_a, df_b], ignore_index=True)

    return df

if __name__ == "__main__":
    df = generate_data()
    print(df.head(10))
    print(f"\nGroup A: {len(df[df.group=='A'])} rows")
    print(f"Group B: {len(df[df.group=='B'])} rows")