import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np


# Step 1: Load the Data
data = pd.read_excel("C:\\Users\\Ahmed\\Desktop\\Clean.xlsx")


# Step 2: Data Cleaning
data['Order Date'] = pd.to_datetime(data['Order Date'])

# Step 3: Aggregate Order Count by Segment
data['Month'] = data['Order Date'].dt.to_period('M')
monthly_order_count = data.groupby(['Month', 'Segment'])['Order ID'].count().reset_index()  # Count orders

# Step 4: Prepare Data for Prophet
monthly_order_count['Month'] = monthly_order_count['Month'].dt.to_timestamp()  # Convert to datetime for Prophet
prophet_data = monthly_order_count.rename(columns={'Month': 'ds', 'Order ID': 'y'})  # Rename columns for Prophet

# Step 5: Fit the Prophet Model for Each Segment and Store Forecasts
forecasts = {}
rmse_values = {}

for segment in prophet_data['Segment'].unique():
    segment_data = prophet_data[prophet_data['Segment'] == segment]
    
    # Fit the model
    model = Prophet()
    model.fit(segment_data)

    # Make future predictions
    future = model.make_future_dataframe(periods=12, freq='M')  # Predicting for 12 months ahead
    forecast = model.predict(future)
    
    # Store the forecasted order frequency in the dictionary
    forecasts[segment] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecasts[segment]['Segment'] = segment  # Add segment to forecast DataFrame

    # Calculate RMSE using historical data
    historical_orders = segment_data['y']
    predicted_orders = forecast['yhat'][:len(historical_orders)]
    
    # Calculate RMSE
    rmse = np.sqrt(np.mean((predicted_orders - historical_orders) ** 2))
    rmse_values[segment] = rmse

# Step 6: Plot All Segments Together for Actual vs. Predicted
plt.figure(figsize=(12, 6))

for segment, forecast in forecasts.items():
    # Historical data for the segment
    historical_data = prophet_data[prophet_data['Segment'] == segment]
    
    # Plot historical order frequency
    plt.plot(historical_data['ds'], historical_data['y'], label=f'Historical Orders - {segment}', marker='o', linestyle='--')
    
    # Plot predicted order frequency
    plt.plot(forecast['ds'], forecast['yhat'], label=f'Predicted Orders - {segment}')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)  # Confidence interval

plt.title('Order Frequency Forecast by Customer Segment')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout for better fit
plt.show()

# Step 7: Summarize the forecasted order frequency for each segment
summary = {segment: forecast['yhat'].sum() for segment, forecast in forecasts.items()}
summary_df = pd.DataFrame(list(summary.items()), columns=['Segment', 'Total Predicted Orders'])

# Print the summary of predicted order frequencies
print(summary_df)

# Step 8: Print RMSE Values for Each Segment
rmse_df = pd.DataFrame(list(rmse_values.items()), columns=['Segment', 'RMSE'])
print(rmse_df)
