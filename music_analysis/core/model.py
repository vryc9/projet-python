from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
from . import config

def train_clustering(data, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=config.RANDOM_SEED)
    labels = kmeans.fit_predict(data)
    return kmeans, labels

def evaluate_clustering(data, labels):
    if len(set(labels)) > 1:
        score = silhouette_score(data, labels)
        return score
    return 0.0

def save_model(model, filename):
    path = config.MODELS_DIR / filename
    with open(path, 'wb') as f:
        pickle.dump(model, f)
