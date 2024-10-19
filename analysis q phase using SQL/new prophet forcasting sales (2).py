import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# read data 
data = pd.read_excel("C:\\Users\\Ahmed\\Desktop\\Clean.xlsx")

# Convert 'Order Date' to datetime
data['Order Date'] = pd.to_datetime(data['Order Date']) 

# Step 2: Aggregate sales by month, ensuring only 'Sales' column is summed
monthly_sales = data.resample('MS', on='Order Date').agg({'Sales': 'sum'}).reset_index()

# Step 3: Rename columns for compatibility with Prophet
monthly_sales.rename(columns={'Order Date': 'ds', 'Sales': 'y'}, inplace=True)

# Step 4: Train the Prophet model
model = Prophet()
model.fit(monthly_sales)

# Step 5: Make predictions for the next 12 months
future = model.make_future_dataframe(periods=12, freq='MS')
forecast = model.predict(future)

# Step 6: Plot the results
fig = model.plot(forecast)
plt.title('Actual vs Predicted Sales')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.show()

# Step 7: Calculate Total Forecasted Sales for the next 12 months
# Extract future sales forecast only for the next 12 months
future_sales = forecast[forecast['ds'] > monthly_sales['ds'].max()].head(12)
total_forecasted_sales = future_sales['yhat'].sum()
print(f"Total Forecasted Sales for the Next 12 Months: {total_forecasted_sales}")

# model evaluation 
actual = monthly_sales['y']
predicted = forecast.loc[forecast['ds'].isin(monthly_sales['ds']), 'yhat']

# Calculate MAE , RMSE
mae = mean_absolute_error(actual, predicted)
rmse = np.sqrt(mean_squared_error(actual, predicted))

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
