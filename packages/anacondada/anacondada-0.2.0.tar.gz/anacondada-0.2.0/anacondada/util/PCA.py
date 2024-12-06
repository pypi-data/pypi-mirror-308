import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load the data
columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
path = "iris\\iris.data"
data = pd.read_csv(path, names=columns)

# Define features and target
features = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
target = data['class']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Perform PCA
pca = PCA(n_components=2)  # You can adjust the number of components (e.g., 2)
X_pca = pca.fit_transform(X_scaled)

# Train Logistic Regression on original data
model_original = LogisticRegression(max_iter=200)
model_original.fit(X_train, y_train)
y_pred_original = model_original.predict(X_test)
accuracy_original = accuracy_score(y_test, y_pred_original)

# Train Logistic Regression on PCA-transformed data
# Use the same split for PCA as original
model_pca = LogisticRegression(max_iter=200)
model_pca.fit(X_pca, y_train)  # Train on the PCA-transformed data
y_pred_pca = model_pca.predict(pca.transform(scaler.transform(X_test)))  # Apply PCA transform to X_test
accuracy_pca = accuracy_score(y_test, y_pred_pca)

# Print the results
print(f'Accuracy without PCA: {accuracy_original}')
print(f'Accuracy with PCA: {accuracy_pca}')

# Plot the comparison
plt.figure(figsize=(8,6))
plt.bar(['Original', 'PCA'], [accuracy_original, accuracy_pca], color=['blue', 'green'])
plt.ylim([0.8, 1])
plt.ylabel('Accuracy')
plt.title('Comparison of Logistic Regression Accuracy (Original vs PCA)')
plt.show()