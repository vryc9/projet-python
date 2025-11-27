# core/model.py
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
import os
import pandas as pd
from core.config import MODELS_DIR, RANDOM_SEED, N_CLUSTERS

def train_clustering(X, df):
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=RANDOM_SEED, n_init=10)
    kmeans.fit(X)
    
    labels = kmeans.labels_
    df['cluster'] = labels
    
    try:
        score = silhouette_score(X, labels)
    except:
        score = 0 
        
    with open(os.path.join(MODELS_DIR, "model.pkl"), "wb") as f:
        pickle.dump(kmeans, f)
        
    return df, score, kmeans