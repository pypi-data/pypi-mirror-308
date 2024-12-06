import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import hinge_loss

url = "breast+cancer\\breast-cancer.data"
column_names = ['Class', 'age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 
                'breast', 'breast-quad', 'irradiat']
data = pd.read_csv(url, names=column_names)

categorical_cols = ['menopause', 'tumor-size', 'inv-nodes', 'breast-quad', 'breast']
binary_cols = ['node-caps', 'irradiat']
ordinal_numerical_cols = ['age', 'deg-malig']

categorical_imputer = SimpleImputer(strategy='most_frequent')
data[categorical_cols] = categorical_imputer.fit_transform(data[categorical_cols])

binary_numerical_imputer = SimpleImputer(strategy='most_frequent')
data[binary_cols + ordinal_numerical_cols] = binary_numerical_imputer.fit_transform(data[binary_cols + ordinal_numerical_cols])

label_encoder = LabelEncoder()
for col in binary_cols:
    data[col] = label_encoder.fit_transform(data[col])

data['Class'] = label_encoder.fit_transform(data['Class'])
data = pd.get_dummies(data, columns=categorical_cols + ordinal_numerical_cols, drop_first=True)

# print("Processed Data (first 5 rows):")
# print(data.head())

y = data['Class'] 
X = data.drop(columns=['Class'])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train and evaluate SVM models
svm_linear = SVC(kernel='linear')
svm_linear.fit(X_train, y_train)
y_pred_linear = svm_linear.predict(X_test)

# Model performance for linear kernel
accuracy = accuracy_score(y_test, y_pred_linear)
conf_matrix = confusion_matrix(y_test, y_pred_linear)
class_report = classification_report(y_test, y_pred_linear)
print(f"Accuracy of the SVM model with linear kernel: {accuracy * 100:.2f}%")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(class_report)


decision_values = svm_linear.decision_function(X_test)
hinge_loss_value = hinge_loss(y_test, decision_values)
print(f"Hinge Loss: {hinge_loss_value:.4f}")

# Train and evaluate SVM model with RBF kernel
svm_rbf = SVC(kernel='rbf')
svm_rbf.fit(X_train, y_train)
y_pred_rbf = svm_rbf.predict(X_test)

# Model performance for RBF kernel
accuracy_rbf = accuracy_score(y_test, y_pred_rbf)
conf_matrix_rbf = confusion_matrix(y_test, y_pred_rbf)
class_report_rbf = classification_report(y_test, y_pred_rbf)
print(f"Accuracy of the SVM model with RBF kernel: {accuracy_rbf * 100:.2f}%")
print("\nConfusion Matrix (RBF):")
print(conf_matrix_rbf)
print("\nClassification Report (RBF):")
print(class_report_rbf)

decision_values = svm_rbf.decision_function(X_test)
hinge_loss_value = hinge_loss(y_test, decision_values)
print(f"Hinge Loss: {hinge_loss_value:.4f}")