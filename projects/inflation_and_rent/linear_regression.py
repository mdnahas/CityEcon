#! /usr/bin/env python3

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the data from the two CSV files
# Data is actually PRICE LEVELS (basket prices) not inflation rates
data1 = pd.read_csv('City_CPIs_Monthly.csv')
data2 = pd.read_csv('City_CPI_rent_Monthly.csv')




data1['sum'] = data1.loc[:, data1.columns != 'DATE'].sum(axis=1)

# Merge the two datasets on the date column
data = pd.merge(data1, data2, on='DATE', suffixes=("_CPI","_rent"))

# Ignore data prior to 1935-07-01, when data started to
# be gathered quarterly.

# Create lagged variables for the independent variable
data['lag_0'] = data['independent_variable']
data['lag_3'] = data['independent_variable'].shift(3)
data['lag_6'] = data['independent_variable'].shift(6)
data['lag_12'] = data['independent_variable'].shift(12)

# Drop any rows with missing values
data.dropna(inplace=True)

# Split the data into training and test sets
train_data = data[data['date'] < '2022-01-01']
test_data = data[data['date'] >= '2022-01-01']

# Fit the linear regression model on the training data
model = LinearRegression()
X_train = train_data[['lag_0', 'lag_3', 'lag_6', 'lag_12']]
y_train = train_data['dependent_variable']
model.fit(X_train, y_train)

# Make predictions on the test data
X_test = test_data[['lag_0', 'lag_3', 'lag_6', 'lag_12']]
y_test = test_data['dependent_variable']
predictions = model.predict(X_test)

# Print the coefficient estimates
print('Intercept:', model.intercept_)
print('Lag 0 Coefficient:', model.coef_[0])
print('Lag 3 Coefficient:', model.coef_[1])
print('Lag 6 Coefficient:', model.coef_[2])
print('Lag 12 Coefficient:', model.coef_[3])

# Print the R-squared value
print('R-squared:', model.score(X_test, y_test))
