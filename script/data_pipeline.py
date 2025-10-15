from pytrends.request import TrendReq
import pandas as pd
import time
import random

print('Start')
pytrends = TrendReq(hl='en-US', tz=480, timeout=(10,25),retries=2,backoff_factor=0.4)  # tz 480 = UTC+8 (Taiwan) — set to local timezone if desired
brands = ["Cartier", "Van Cleef & Arpels"]
timeframe = '2024-10-01 2025-10-12'

def fetch_trends(geo_code, max_retries=5):
    """Fetch Google Trends data safely with retry logic."""
    for attempt in range(max_retries):
        try:
            pytrends.build_payload(brands, timeframe=timeframe, geo=geo_code)
            df = pytrends.interest_over_time()
            if df is None or df.empty:
                raise ValueError(f"No data returned for geo: {geo_code}")
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])
            suffix = '_TW' if geo_code == 'TW' else '_Global'
            df = df.add_suffix(suffix)
            return df
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {geo_code}: {e}")
            time.sleep(5 + random.uniform(0, 5))  # wait 5–10 seconds before retry
    raise RuntimeError(f"Failed to fetch trends for {geo_code} after {max_retries} retries.")

# Fetch global and Taiwan datasets
global_df = fetch_trends(geo_code='')
time.sleep(10)
tw_df = fetch_trends(geo_code='TW')
print('Stop')
# Merge (align on date index)
df = pd.concat([global_df, tw_df], axis=1)

# Save raw
df.to_csv("richemont_trends_raw.csv", index=True)

# Compute localization metrics
df['Cartier_TW/Global_pct'] = df['Cartier_TW'] / df['Cartier_Global'] * 100
df['VCA_TW/Global_pct'] = df['Van Cleef & Arpels_TW'] / df['Van Cleef & Arpels_Global'] * 100

# Smooth trends (4-week moving average)
df['Cartier_MA4'] = df['Cartier_TW'].rolling(window=4, min_periods=1).mean()
df['VCA_MA4'] = df['Van Cleef & Arpels_TW'].rolling(window=4, min_periods=1).mean()

# Week-over-week percent change
df['Cartier_WoW_pct'] = df['Cartier_TW'].pct_change() * 100
df['VCA_WoW_pct'] = df['Van Cleef & Arpels_TW'].pct_change() * 100

# Rolling volatility (4-week rolling std)
df['Cartier_roll_std4'] = df['Cartier_TW'].rolling(window=4, min_periods=1).std()
df['VCA_roll_std4'] = df['Van Cleef & Arpels_TW'].rolling(window=4, min_periods=1).std()

# Save cleaned output
df.to_csv("richemont_trends_clean.csv", index=True)




# Google Trends API (Cartier & VCA)
#          │
#          ▼
# Fetch Taiwan & Global Data (pytrends)
#          │
#          ▼
# Label Columns (_TW / _Global)
#          │
#          ▼
# Merge by Date → Aligned Dataset
#          │
#          ▼
# Clean Data (drop isPartial, handle missing)
#          │
#          ▼
# Compute Metrics (TW/Global ratio, MA, WoW%, volatility)
#          │
#          ▼
# Export Clean CSV → Input for Dashboard / Analysis