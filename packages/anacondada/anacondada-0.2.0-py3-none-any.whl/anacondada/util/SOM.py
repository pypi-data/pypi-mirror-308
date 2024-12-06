import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from minisom import MiniSom
import matplotlib.pyplot as plt

# Load the data
column_names = ['variance', 'skewness', 'curtosis', 'entropy', 'class']

path = "banknote+authentication\\data_banknote_authentication.txt"
df = pd.read_csv(path, names=column_names)

# Prepare the data
X = df.drop('class', axis=1).values
y = df['class'].values

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize the SOM
som = MiniSom(x=9, y=9, input_len=X_scaled.shape[1], learning_rate=0.5, topology='rectangular')

# Initialize weights and train the SOM
som.random_weights_init(X_scaled)
som.train_random(X_scaled, 500)

# Plot the SOM clustering
plt.figure(figsize=(7, 7))
markers = ['o', 's']
colors = ['r', 'g']
for i, x in enumerate(X_scaled):
    w = som.winner(x)  # Get the winning node for the current input
    plt.plot(w[0] + 0.5, w[1] + 0.5, markers[y[i]], markerfacecolor='None',
             markeredgecolor=colors[y[i]], markersize=10, markeredgewidth=2)

plt.title('SOM Clustering')
plt.grid()
plt.show()