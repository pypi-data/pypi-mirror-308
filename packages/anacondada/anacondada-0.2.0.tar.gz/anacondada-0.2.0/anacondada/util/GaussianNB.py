import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Load the dataset with specified column names
columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
path = "iris\\iris.data"
data = pd.read_csv(path, names=columns)

# Define features and target
features = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
target = data['class']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize the Gaussian Naive Bayes model
model = GaussianNB()

# Perform cross-validation to check for overfitting
cross_val_scores = cross_val_score(model, features, target, cv=5)
print("Cross-Validation Scores:", cross_val_scores)
print("Mean Cross-Validation Score:", cross_val_scores.mean())

# Train on the split dataset and evaluate
model.fit(X_train, y_train)
predictions = model.predict(X_test)
score = accuracy_score(y_test, predictions)
print("Accuracy on Test Set:", score)