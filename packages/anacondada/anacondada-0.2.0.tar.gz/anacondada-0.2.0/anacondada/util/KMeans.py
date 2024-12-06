import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# Load the dataset
url = "sales+transactions+dataset+weekly\\Sales_Transactions_Dataset_Weekly.csv"
df = pd.read_csv(url)

# Display first 5 rows and dataset information
print("First 5 rows of the dataset:")
print(df.head())

print("\nDataset Information:")
print(df.info())

# Step 1: Preprocess the data (e.g., handling missing values, scaling features)
# Handling missing values: Fill with median or mode as appropriate
df.fillna(df.mode().iloc[0], inplace=True)

# Step 2: Extract relevant numerical columns (remove non-numeric columns if any)
# Assume 'Invoice' and 'Customer' are non-numeric, so drop them
df_numerical = df.select_dtypes(include=[np.number])

# Step 3: Scale the features using StandardScaler
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_numerical)

# Step 4: Apply Elbow Method to determine optimal K
wcss = []  # Within-cluster sum of squares (inertia)

# Test for a range of K values (e.g., 1 to 10)
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)

# Plot the Elbow Graph
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of clusters (K)')
plt.ylabel('WCSS (Within-cluster sum of squares)')
plt.show()

# From the plot, identify the "elbow" point to choose the optimal K.

# Step 5: Calculate Silhouette Score for different K values to validate the best K
silhouette_scores = []

for k in range(2, 11):  # Silhouette score is only defined for K >= 2
    kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(df_scaled)
    score = silhouette_score(df_scaled, kmeans.labels_)
    silhouette_scores.append(score)

# Plot the Silhouette Scores for each K value
plt.figure(figsize=(8, 6))
plt.plot(range(2, 11), silhouette_scores)
plt.title('Silhouette Score for Different K values')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Silhouette Score')
plt.show()

optimal_k = 4 
kmeans_optimal = KMeans(n_clusters=optimal_k, init='k-means++', max_iter=300, n_init=10, random_state=42)
y_kmeans = kmeans_optimal.fit_predict(df_scaled)

pca = PCA(n_components=2)
df_pca = pca.fit_transform(df_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(df_pca[y_kmeans == 0, 0], df_pca[y_kmeans == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(df_pca[y_kmeans == 1, 0], df_pca[y_kmeans == 1, 1], s=100, c='blue', label='Cluster 2')
plt.scatter(df_pca[y_kmeans == 2, 0], df_pca[y_kmeans == 2, 1], s=100, c='green', label='Cluster 3')
plt.scatter(df_pca[y_kmeans == 3, 0], df_pca[y_kmeans == 3, 1], s=100, c='purple', label='Cluster 4')

plt.scatter(kmeans_optimal.cluster_centers_[:, 0], kmeans_optimal.cluster_centers_[:, 1], s=200, c='yellow', label='Centroids')
plt.title('Clusters Visualization with PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.show()