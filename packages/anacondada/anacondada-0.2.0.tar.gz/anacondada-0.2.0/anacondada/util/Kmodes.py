import pandas as pd
from kmodes.kmodes import KModes
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

data = {
    'Person': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8'],
    'Hair_Color': ['blonde', 'brunette', 'red', 'black', 'brunette', 'black', 'red', 'black'],
    'Eye_Color': ['amber', 'gray', 'green', 'hazel', 'amber', 'gray', 'green', 'hazel'],
    'Skin_Color': ['fair', 'brown', 'brown', 'brown', 'fair', 'brown', 'fair', 'fair']
}

df = pd.DataFrame(data)
print("=== Original Dataset ===")
print(df)

le_hair = LabelEncoder()
le_eye = LabelEncoder()
le_skin = LabelEncoder()

df['Hair_Color_Encoded'] = le_hair.fit_transform(df['Hair_Color'])
df['Eye_Color_Encoded'] = le_eye.fit_transform(df['Eye_Color'])
df['Skin_Color_Encoded'] = le_skin.fit_transform(df['Skin_Color'])

features = ['Hair_Color', 'Eye_Color', 'Skin_Color']
X = df[features].values

K = range(1, 6)
cost = []

for k in K:
    km = KModes(n_clusters=k, init='Huang', n_init=5, verbose=0, random_state=42)
    km.fit_predict(X)
    cost.append(km.cost_)

plt.figure(figsize=(8, 5))
plt.plot(K, cost, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Cost (Number of Mismatches)')
plt.xticks(K)
plt.grid(True)
plt.show()

optimal_k = 3
print(f"\nOptimal number of clusters selected: {optimal_k}")

km = KModes(n_clusters=optimal_k, init='Huang', n_init=5, verbose=1, random_state=42)

clusters = km.fit_predict(X)
df['Cluster'] = clusters

print("\n=== Cluster Assignments ===")
print(df[['Person', 'Hair_Color', 'Eye_Color', 'Skin_Color', 'Cluster']])

encoded_features = ['Hair_Color_Encoded', 'Eye_Color_Encoded', 'Skin_Color_Encoded']
X_encoded = df[encoded_features].values

pca = PCA(n_components=2, random_state=42)
principal_components = pca.fit_transform(X_encoded)

pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
pca_df = pd.concat([pca_df, df['Cluster']], axis=1)

print("\n=== PCA DataFrame ===")
print(pca_df)

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x='PC1',
    y='PC2',
    hue='Cluster',
    palette='viridis',
    data=pca_df,
    s=100,
    edgecolor='k'
)

centroids = km.cluster_centroids_
centroids_encoded = []
for mode in centroids:
    hair_enc = le_hair.transform([mode[0]])[0]
    eye_enc = le_eye.transform([mode[1]])[0]
    skin_enc = le_skin.transform([mode[2]])[0]
    centroids_encoded.append([hair_enc, eye_enc, skin_enc])

centroids_pca = pca.transform(centroids_encoded)

plt.scatter(
    centroids_pca[:, 0],
    centroids_pca[:, 1],
    s=300,
    c='red',
    label='Centroids',
    marker='X'
)

plt.title('K-Modes Clustering Visualization with PCA')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.show()

km_verbose = KModes(n_clusters=optimal_k, init='Huang', n_init=5, verbose=1, max_iter=10, random_state=42)

clusters_verbose = km_verbose.fit_predict(X)

epochs = km_verbose.n_iter_
print(f"\nConverged in {epochs} epoch(s).")