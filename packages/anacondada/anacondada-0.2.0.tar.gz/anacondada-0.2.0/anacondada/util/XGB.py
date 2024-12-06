import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, hinge_loss
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from xgboost import XGBClassifier

# Load the dataset
url = "breast+cancer\\breast-cancer.data"
column_names = ['Class', 'age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 
                'breast', 'breast-quad', 'irradiat']
data = pd.read_csv(url, names=column_names)

# Step 1: Preprocess the Data

# Handle missing values for categorical columns
categorical_cols = ['menopause', 'tumor-size', 'inv-nodes', 'breast-quad', 'breast']
categorical_imputer = SimpleImputer(strategy='most_frequent')
data[categorical_cols] = categorical_imputer.fit_transform(data[categorical_cols])

# Handle missing values for binary and ordinal numerical columns
binary_cols = ['node-caps', 'irradiat']
ordinal_numerical_cols = ['age', 'deg-malig']
binary_numerical_imputer = SimpleImputer(strategy='most_frequent')
data[binary_cols + ordinal_numerical_cols] = binary_numerical_imputer.fit_transform(data[binary_cols + ordinal_numerical_cols])

# Encode binary columns
label_encoder = LabelEncoder()
for col in binary_cols:
    data[col] = label_encoder.fit_transform(data[col])

# Label encode the target variable (Class)
data['Class'] = label_encoder.fit_transform(data['Class'])

# One-Hot Encode categorical variables
data = pd.get_dummies(data, columns=categorical_cols + ordinal_numerical_cols, drop_first=True)

# Step 2: Prepare features and target
y = data['Class']
X = data.drop(columns=['Class'])

# Step 3: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 4: Initialize models

# AdaBoost Classifier with DecisionTree as base estimator
base_model = DecisionTreeClassifier(max_depth=1)
adaboost = AdaBoostClassifier(estimator=base_model, n_estimators=50, learning_rate=1, random_state=42)

# Random Forest Classifier
random_forest = RandomForestClassifier(n_estimators=100, random_state=42)

# XGBoost Classifier
xgboost = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)

# Support Vector Classifier
svc = SVC(kernel='linear', random_state=42, probability=True)

# Step 5: Train and Evaluate Models

# AdaBoost
adaboost.fit(X_train, y_train)
y_pred_adaboost = adaboost.predict(X_test)
accuracy_adaboost = accuracy_score(y_test, y_pred_adaboost)
print(f"AdaBoost Accuracy: {accuracy_adaboost:.4f}")
print("AdaBoost Classification Report:")
print(classification_report(y_test, y_pred_adaboost))

# Random Forest
random_forest.fit(X_train, y_train)
y_pred_random_forest = random_forest.predict(X_test)
accuracy_random_forest = accuracy_score(y_test, y_pred_random_forest)
print(f"Random Forest Accuracy: {accuracy_random_forest:.4f}")
print("Random Forest Classification Report:")
print(classification_report(y_test, y_pred_random_forest))

# XGBoost
xgboost.fit(X_train, y_train)
y_pred_xgboost = xgboost.predict(X_test)
accuracy_xgboost = accuracy_score(y_test, y_pred_xgboost)
print(f"XGBoost Accuracy: {accuracy_xgboost:.4f}")
print("XGBoost Classification Report:")
print(classification_report(y_test, y_pred_xgboost))

# Support Vector Classifier
svc.fit(X_train, y_train)
y_pred_svc = svc.predict(X_test)
accuracy_svc = accuracy_score(y_test, y_pred_svc)
print(f"SVC Accuracy: {accuracy_svc:.4f}")
print("SVC Classification Report:")
print(classification_report(y_test, y_pred_svc))

# Step 6: Calculate Hinge Loss (for SVC)
hinge_loss_svc = hinge_loss(y_test, svc.decision_function(X_test))
print(f"SVC Hinge Loss: {hinge_loss_svc:.4f}")