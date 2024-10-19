# Importing libraries 
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Step 1: Read Data
data = pd.read_excel("C:\\Users\\Ahmed\\Desktop\\Clean.xlsx")

# Step 2: Data Cleaning
data['Order Date'] = pd.to_datetime(data['Order Date'])

# Step 3: Aggregate Sales by Segment
data['Month'] = data['Order Date'].dt.to_period('M')
monthly_sales = data.groupby(['Month', 'Segment'])['Sales'].sum().reset_index()

# Step 4: Prepare Data for Prophet
monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()  # Convert to datetime for Prophet
prophet_data = monthly_sales.rename(columns={'Month': 'ds', 'Sales': 'y'})  # Rename columns for Prophet

# Step 5: Fit the Prophet Model for Each Segment
forecasts = {}

for segment in prophet_data['Segment'].unique():
    segment_data = prophet_data[prophet_data['Segment'] == segment]
    
    # Fit the model
    model = Prophet()
    model.fit(segment_data)

    # Make future predictions
    future = model.make_future_dataframe(periods=12, freq='M')  # Predicting for 12 months ahead
    forecast = model.predict(future)
    
    # Store the forecasted sales in the dictionary
    forecasts[segment] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Step 6: Plot the forecasts for each segment and evaluate predictions
evaluation_summary = {}

for segment, forecast in forecasts.items():
    plt.figure(figsize=(10, 5))
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicted Sales')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
    
    # Historical data for the segment
    historical_data = prophet_data[prophet_data['Segment'] == segment]
    plt.plot(historical_data['ds'], historical_data['y'], label='Historical Sales', marker='o', color='orange')
    
    plt.title(f'Sales Forecast for {segment} Segment')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
    
    # Evaluate Predictions
    # Merge historical and forecast data to compare actual and predicted sales
    merged = historical_data.merge(forecast, on='ds', how='left')
    
    # Calculate MAE
    mae = mean_absolute_error(merged['y'], merged['yhat'].fillna(0))  # Fill NaN with 0 for missing predictions
    
    # Calculate RMSE
    rmse = mean_squared_error(merged['y'], merged['yhat'].fillna(0), squared=False)  # Fill NaN with 0 for missing predictions
    
    evaluation_summary[segment] = {'MAE': mae, 'RMSE': rmse}

# Step 7: Print the Summary of MAE and RMSE
evaluation_summary_df = pd.DataFrame(evaluation_summary).T  # Transpose for better readability
print(evaluation_summary_df)

# Step 8: Summarize the forecasted sales for the last year only
last_year_summary = {}
for segment, forecast in forecasts.items():
    # Filter the forecast data to include only the last 12 months
    last_year_forecast = forecast[forecast['ds'] >= forecast['ds'].max() - pd.DateOffset(months=12)]
    last_year_summary[segment] = last_year_forecast['yhat'].sum()  # Sum only the last year's predicted sales

last_year_summary_df = pd.DataFrame(list(last_year_summary.items()), columns=['Segment', 'Total Predicted Sales Last Year'])

# Print the summary of predicted sales contributions for the last year
print(last_year_summary_df)
