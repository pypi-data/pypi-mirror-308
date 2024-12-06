import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

path = "multivariate+gait+data\\gait.csv"
df = pd.read_csv(path)

# Generate lagged features for time-series prediction
df['angle_lag1'] = df['angle'].shift(1)
df['angle_lag2'] = df['angle'].shift(2)
df.dropna(inplace=True)  # Remove rows with NaN values due to lagging

# Define features and target for regression
X = df[['angle_lag1', 'angle_lag2']]
y = df['angle']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
print(y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error for Future Angle Prediction: {mse}")


# Print coefficients
print("Coefficients for Future Angle Prediction:", model.coef_)
print("Intercept for Future Angle Prediction:", model.intercept_)


np.random.seed(42)
df['gait_speed'] = np.random.uniform(0.5, 1.5, size=len(df))

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Define features and target
features = ['subject', 'condition', 'replication', 'leg', 'joint', 'time', 'angle']
X = df[features]
y = df['gait_speed']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize and train the regression model
gait_speed_model = LinearRegression()
gait_speed_model.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = gait_speed_model.predict(X_test)
mse_gait_speed = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error for Gait Speed Prediction: {mse_gait_speed}")

# Print the coefficients
print("Coefficients for Gait Speed Prediction:", gait_speed_model.coef_)
print("Intercept for Gait Speed Prediction:", gait_speed_model.intercept_)