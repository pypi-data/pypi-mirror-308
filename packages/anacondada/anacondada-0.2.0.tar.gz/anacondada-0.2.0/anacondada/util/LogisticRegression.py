import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, hinge_loss
from sklearn.preprocessing import StandardScaler

# Load the dataset
url = "adult\\adult.data"
columns = [
    'age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status',
    'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss',
    'hours_per_week', 'native_country', 'income'
]
df = pd.read_csv(url, names=columns)

categorical_cols = ['workclass', 'education', 'marital_status', 'occupation', 
                    'relationship', 'race', 'native_country']
binary_cols = ['sex']
ordinal_numerical_cols = ['age', 'education_num', 'capital_gain', 'capital_loss', 'hours_per_week', 'fnlwgt']
target_col = 'income'

categorical_imputer = SimpleImputer(strategy='most_frequent')
df[categorical_cols] = categorical_imputer.fit_transform(df[categorical_cols])

binary_numerical_imputer = SimpleImputer(strategy='most_frequent')
df[binary_cols + ordinal_numerical_cols] = binary_numerical_imputer.fit_transform(df[binary_cols + ordinal_numerical_cols])

label_encoder = LabelEncoder()
for col in binary_cols:
    df[col] = label_encoder.fit_transform(df[col])

# Encode the target column ('income')
df[target_col] = label_encoder.fit_transform(df[target_col])

# Step 4: One-hot encode categorical features
df_encoded = pd.get_dummies(df, columns=categorical_cols + ordinal_numerical_cols, drop_first=True)

# Step 5: Define features (X) and target variable (y)
X = df_encoded.drop(target_col, axis=1)  # Drop the target column
y = df_encoded[target_col]  # Target column

# Step 6: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 7: Scale the features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 8: Train the Logistic Regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Step 9: Make predictions on the test set
y_pred = model.predict(X_test_scaled)

# Step 10: Print the classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Step 12: Print Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# from sklearn.metrics import confusion_matrix
# import seaborn as sns
# import matplotlib.pyplot as plt

# Confusion Matrix
# cm = confusion_matrix(y_test, y_pred)
# plt.figure(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['<=50K', '>50K'], yticklabels=['<=50K', '>50K'])
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Confusion Matrix')
# plt.show()

# fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test_scaled)[:, 1])
# plt.figure()
# plt.plot(fpr, tpr, label=f'ROC curve (area = {roc_auc:.2f})')
# plt.plot([0, 1], [0, 1], 'k--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC Curve')
# plt.legend(loc='lower right')
# plt.show()