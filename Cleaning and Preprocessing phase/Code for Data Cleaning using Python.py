import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = r"C:\Users\Lenovo\Desktop\Depi Superstore Sales Analysis\Final Data Cleaning\Original Store Sales Dataset.xlsx"
data = pd.read_excel(file_path)

# Display the first few rows of the dataset
print(data.head())

# Check Data type 
print(data.dtypes)


# ******************************************************************************************************
#  first : check for missing values
# Step 1: Convert empty strings to NaN for the entire DataFrame
# data.replace('', np.nan, inplace=True)

# # Step 2: Check for missing values across all columns
# missing_values = data.isnull().sum()

# # Step 3: Display missing values for each column
# print("Missing Values:\n", missing_values)

# # step 4: Check rows where Postal Code is missing and identify the city
# missing_postal_code_rows = data[data['Postal Code'].isnull()]
# print(missing_postal_code_rows[['City', 'State']])

# # Convert 'Postal Code' column to string to preserve leading zeros
# data['Postal Code'] = data['Postal Code'].astype(str)

# # Step 2: Remove decimal points
# data['Postal Code'] = data['Postal Code'].str.replace('.0', '', regex=False)

# # Handle missing values by replacing 'nan' with None
# data['Postal Code'] = data['Postal Code'].replace('nan', None)

# State_name = 'Vermont'
# postal_code_for_State = '05407'

# # # Fill missing Postal Code for that State
# data.loc[(data['State'] == State_name) & (data['Postal Code'].isnull()), 'Postal Code'] = postal_code_for_State

# # # Verify that missing postal codes are filled
# print(data['Postal Code'].isnull().sum())

# *******************************************************************************
# Second :   
# Convert 'Order Date' and 'Ship Date' to datetime format
# data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
# data['Ship Date'] = pd.to_datetime(data['Ship Date'], errors='coerce')

# # Check for any issues after conversion
# print(data[['Order Date', 'Ship Date']].dtypes)

# ************************************************************************************

# Third:  Check for duplicates in the dataset

# duplicates = data.duplicated()
# # Remove duplicates if found
# data_cleaned = data.drop_duplicates()

# print(f"Number of duplicates removed: {sum(duplicates)}")

# **********************************************************************
# Convert categorical columns to category type
# categorical_columns = ['Ship Mode', 'Category', 'Sub-Category', 'Region']
# data[categorical_columns] = data[categorical_columns].astype('category')

# # Verify conversion
# print(data[categorical_columns].dtypes)
#  *******************************************************
#  Finally : Save the cleaned dataset to a new Excel file

cleaned_file_path = r"C:\Users\Lenovo\Desktop\Depi Superstore Sales Analysis\Final Data Cleaning\Clean Data.xlsx"
# data_cleaned.to_excel(cleaned_file_path, index=False)
print(f"Cleaned data saved to {cleaned_file_path}")
