from prophet import Prophet

# Prepare dataframe: ds = date, y = search interest
prophet_df = df[['Cartier_TW']].reset_index().rename(columns={'date':'ds', 'Cartier_TW':'y'})

model = Prophet(weekly_seasonality=True)
model.fit(prophet_df)

future = model.make_future_dataframe(periods=8, freq='W')  # next 8 weeks
forecast = model.predict(future)

# forecast[['ds','yhat','yhat_lower','yhat_upper']] contains predictions
