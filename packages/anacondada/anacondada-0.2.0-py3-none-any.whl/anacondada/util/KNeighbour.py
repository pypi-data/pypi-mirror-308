import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

path = "DryBeanDataset\\Dry_Bean_Dataset.xlsx"
df = pd.read_excel(path)

X = df.drop(columns=['Class'])
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scalers = {
    'MinMaxScaler': MinMaxScaler(),
    'StandardScaler': StandardScaler(),
    'RobustScaler': RobustScaler()
}

results = {}
for scaler_name, scaler in scalers.items():
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train_scaled, y_train)
    y_pred = knn.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    results[scaler_name] = accuracy

# plt.bar(results.keys(), results.values())
# plt.xlabel('Scaling Technique')
# plt.ylabel('Accuracy')
# plt.title('Comparison of Scaling Techniques on k-NN Classifier')
# plt.show()

best_scaler = max(results, key=results.get)
print(f"The best scaling technique is {best_scaler} with an accuracy of {results[best_scaler]:.4f}")

new_instance = pd.DataFrame({
    'Area': [42020],
    'Perimeter': [674.16],
    'MajorAxisLength': [208.81],
    'MinorAxisLength': [162.14],
    'AspectRation': [1.29],
    'Eccentricity': [0.5174],
    'ConvexArea': [42530],
    'EquivDiameter': [231.01],
    'Extent': [0.7213],
    'Solidity': [0.9880],
    'ShapeFactor1': [0.4949],
    'ShapeFactor2': [0.9637],
    'ShapeFactor3': [0.9975],
    'ShapeFactor4': [0.9128],
    'roundness': [0.0],
    'Compactness': [0.0]
})

print("Feature names during fitting:")
print(X_train.columns)

print("Feature names of new instance:")
print(new_instance.columns)

new_instance = new_instance[X_train.columns]
new_instance_scaled = scaler.transform(new_instance)
prediction = knn.predict(new_instance_scaled)
print(f"The predicted target class is: {prediction[0]}")

from sklearn.model_selection import cross_val_score
import numpy as np

k_values = list(range(1, 21))
cv_scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train_scaled, y_train, cv=10, scoring='accuracy')
    cv_scores.append(scores.mean())

# Plotting k values against accuracy scores
# plt.plot(k_values, cv_scores, marker='o')
# plt.xlabel('Number of Neighbors (k)')
# plt.ylabel('Cross-Validated Accuracy')
# plt.title('k-NN Accuracy for Different Values of k')
# plt.show()

from sklearn.metrics import classification_report, roc_curve, auc, roc_auc_score
best_k = k_values[np.argmax(cv_scores)]
knn = KNeighborsClassifier(n_neighbors=best_k)
knn.fit(X_train_scaled, y_train)
y_pred = knn.predict(X_test_scaled)

print("Classification Report:")
print(classification_report(y_test, y_pred))

accuracy = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(pd.get_dummies(y_test), pd.get_dummies(y_pred), multi_class='ovr')
print(f"Accuracy: {accuracy:.4f}")
print(f"ROC AUC Score: {roc_auc:.4f}")

# y_test_bin = pd.get_dummies(y_test).values
# y_pred_bin = pd.get_dummies(y_pred).values

# fpr = {}
# tpr = {}
# roc_auc = {}

# for i, class_name in enumerate(pd.get_dummies(y_test).columns):
#     fpr[class_name], tpr[class_name], _ = roc_curve(y_test_bin[:, i], y_pred_bin[:, i])
#     roc_auc[class_name] = auc(fpr[class_name], tpr[class_name])

# plt.figure()
# for i, class_name in enumerate(pd.get_dummies(y_test).columns):
#     plt.plot(fpr[class_name], tpr[class_name], label=f'{class_name} (AUC = {roc_auc[class_name]:.2f})')

# plt.plot([0, 1], [0, 1], 'k--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC Curve for each class')
# plt.legend(loc='lower right')
# plt.show()

# from sklearn.metrics import confusion_matrix
# import seaborn as sns

# cm = confusion_matrix(y_test, y_pred)
# plt.figure(figsize=(10, 7))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=knn.classes_, yticklabels=knn.classes_)
# plt.xlabel('Predicted')
# plt.ylabel('Actual')
# plt.title('Confusion Matrix')
# plt.show()