import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load the Data
data = pd.read_excel("C:\\Users\\Ahmed\\Desktop\\Clean.xlsx")


# Step 2: Data Cleaning
data['Order Date'] = pd.to_datetime(data['Order Date'])

# Step 3: Aggregate Order Count by Shipping Mode
data['Month'] = data['Order Date'].dt.to_period('M')
monthly_shipping_demand = data.groupby(['Month', 'Ship Mode'])['Order ID'].count().reset_index()  # Count orders

# Step 4: Prepare Data for Prophet
monthly_shipping_demand['Month'] = monthly_shipping_demand['Month'].dt.to_timestamp()  # Convert to datetime for Prophet
prophet_data = monthly_shipping_demand.rename(columns={'Month': 'ds', 'Order ID': 'y'})  # Rename columns for Prophet

# Step 5: Fit the Prophet Model for Each Shipping Mode and Store Forecasts
forecasts = {}
rmse_values = {}

for ship_mode in prophet_data['Ship Mode'].unique():
    mode_data = prophet_data[prophet_data['Ship Mode'] == ship_mode]
    
    # Fit the model
    model = Prophet()
    model.fit(mode_data)

    # Make future predictions
    future = model.make_future_dataframe(periods=12, freq='M')  # Predicting for 12 months ahead
    forecast = model.predict(future)
    
    # Store the forecasted shipping demand in the dictionary
    forecasts[ship_mode] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecasts[ship_mode]['Ship Mode'] = ship_mode  # Add shipping mode to forecast DataFrame

    # Calculate RMSE using historical data
    historical_orders = mode_data['y']
    predicted_orders = forecast['yhat'][:len(historical_orders)]
    
    # Calculate RMSE
    rmse = np.sqrt(np.mean((predicted_orders - historical_orders) ** 2))
    rmse_values[ship_mode] = rmse

# Step 6: Plot All Shipping Modes Together for Actual vs. Predicted
plt.figure(figsize=(12, 6))

for ship_mode, forecast in forecasts.items():
    # Historical data for the shipping mode
    historical_data = prophet_data[prophet_data['Ship Mode'] == ship_mode]
    
    # Plot historical shipping demand
    plt.plot(historical_data['ds'], historical_data['y'], label=f'Historical Orders - {ship_mode}', marker='o', linestyle='--')
    
    # Plot predicted shipping demand
    plt.plot(forecast['ds'], forecast['yhat'], label=f'Predicted Orders - {ship_mode}')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)  # Confidence interval

plt.title('Shipping Demand Forecast by Shipping Mode')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout for better fit
plt.show()

# Step 7: Summarize the forecasted shipping demand for each mode
summary = {ship_mode: forecast['yhat'].sum() for ship_mode, forecast in forecasts.items()}
summary_df = pd.DataFrame(list(summary.items()), columns=['Ship Mode', 'Total Predicted Orders'])

# Print the summary of predicted shipping demands
print(summary_df)

# Step 8: Print RMSE Values for Each Shipping Mode
rmse_df = pd.DataFrame(list(rmse_values.items()), columns=['Ship Mode', 'RMSE'])
print(rmse_df)
