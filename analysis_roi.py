import pandas as pd

def estimate_roi(base_engagement, peak_increase_pct, revenue_per_point=1000):
    # Step 1: Adjust engagement by % increase
    expected_engagement = base_engagement * (1 + peak_increase_pct / 100)
    # Step 2: Translate that into a revenue estimate
    revenue_estimate = expected_engagement * revenue_per_point
    return expected_engagement, revenue_estimate

# Example using your cleaned data
df = pd.read_csv('richemont_trends_clean.csv')

base_cartier = df['Cartier_TW'].mean()
peak_increase_pct = ((df['Cartier_TW'].max() - base_cartier) / base_cartier) * 100

expected, revenue = estimate_roi(base_cartier, peak_increase_pct)
print(f"Expected engagement after peak: {expected:.0f}")
print(f"Estimated revenue proxy: ${revenue:,.0f}")
