from pytrends.request import TrendReq
import pandas as pd
import datetime
import time

def refresh_trends():
    pytrends = TrendReq(hl='en-US', tz=480)
    brands = ["Cartier", "Van Cleef & Arpels"]
    timeframe = '2024-10-01 ' + datetime.date.today().strftime('%Y-%m-%d')

    def fetch(geo):
        pytrends.build_payload(brands, timeframe=timeframe, geo=geo)
        df = pytrends.interest_over_time().drop(columns=['isPartial'], errors='ignore')
        suffix = '_TW' if geo == 'TW' else '_Global'
        return df.add_suffix(suffix)

    df_global = fetch('')
    time.sleep(2)
    df_tw = fetch('TW')
    df = pd.concat([df_global, df_tw], axis=1)

    df['Cartier_TW/Global_pct'] = df['Cartier_TW'] / df['Cartier_Global'] * 100
    df['VCA_TW/Global_pct'] = df['Van Cleef & Arpels_TW'] / df['Van Cleef & Arpels_Global'] * 100

    df.to_csv('richemont_trends_clean.csv')
    print("✅ Updated CSV saved!")

# Run manually now, or schedule weekly with Google Cloud Scheduler
refresh_trends()