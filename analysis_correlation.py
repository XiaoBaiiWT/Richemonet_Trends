from scipy.stats import pearsonr
import statsmodels.api as sm

import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm

# Step 1: Load cleaned dataset
df = pd.read_csv('richemont_trends_clean.csv', parse_dates=['date'])

# Step 2: Compute Pearson correlation
corr_cartier, _ = pearsonr(df['Cartier_Global'], df['Cartier_TW'])
corr_vca, _ = pearsonr(df['Van Cleef & Arpels_Global'], df['Van Cleef & Arpels_TW'])
print(f"Cartier correlation = {corr_cartier:.2f}")
print(f"VCA correlation = {corr_vca:.2f}")

# Step 3: Run simple linear regression
X = sm.add_constant(df['Cartier_Global'])   # independent variable (Global)
y = df['Cartier_TW']                        # dependent variable (Taiwan)
model = sm.OLS(y, X).fit()
print(model.summary())
