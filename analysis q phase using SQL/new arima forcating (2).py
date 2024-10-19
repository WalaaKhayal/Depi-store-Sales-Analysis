import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import register_matplotlib_converters
from sklearn.model_selection import train_test_split
register_matplotlib_converters()
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Loading data
df = pd.read_excel("C:\\Users\\Ahmed\\Desktop\\Clean.xlsx")

# Convert Order Date to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])  

# Aggregate sales by month
df_monthly_sales = df.resample('M', on='Order Date')['Sales'].sum()

#  Split the data into training and testing sets (80% train, 20% test)
train_size = int(len(df_monthly_sales) * 0.8)
train, test = df_monthly_sales[:train_size], df_monthly_sales[train_size:]

# Fit ARIMA model on the training set
model = ARIMA(train, order=(5, 1, 2))  # Order can be tuned
model_fit = model.fit()

#  Make predictions on the test set
predictions = model_fit.predict(start=test.index[0], end=test.index[-1], dynamic=False)

#  Generate future dates for the forecast (starting from the end of the test set)
future_dates = pd.date_range(start=test.index[-1], periods=13, freq='M')[1:]  

# Forecast for the next year (12 months)
forecast = model_fit.forecast(steps=12)

#  Calculate total predicted sales for the next year
total_predicted_sales = forecast.sum()
print(f"Total Predicted Sales for the Next Year: {total_predicted_sales}")

# Visualization

# Plot actual sales (Historical + Test)
plt.figure(figsize=(10, 6))
plt.plot(df_monthly_sales.index, df_monthly_sales.values, label='Actual Sales', color='blue')

# Plot test sales
plt.plot(test.index, test.values, label='Test Sales', color='green')

# Plot forecasted sales for the next year
plt.plot(future_dates, forecast, label='Forecasted Sales (Next Year)', color='red', linestyle='--')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Actual vs Test Sales vs Predicted and Forecasted Sales (ARIMA)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()

# Evaluation model 

#  Calculate MAE (Mean Absolute Error)
mae = mean_absolute_error(test, predictions)
print(f"Mean Absolute Error (MAE): {mae}")

# Calculate MSE (Mean Squared Error)
mse = mean_squared_error(test, predictions)
print(f"Mean Squared Error (MSE): {mse}")

# Calculate RMSE (Root Mean Squared Error)
rmse = np.sqrt(mse)
print(f"Root Mean Squared Error (RMSE): {rmse}")

#Calculate MAPE (Mean Absolute Percentage Error)
mape = np.mean(np.abs((test - predictions) / test)) * 100
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
