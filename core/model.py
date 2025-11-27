from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
import os
from core.config import MODELS_DIR, RANDOM_SEED, N_CLUSTERS

def train_clustering(X, df):
    """
    Entraîne un modèle de clustering K-Means sur les features.
    
    Args:
        X (sparse matrix): Matrice de features TF-IDF.
        df (pd.DataFrame): DataFrame original pour ajouter les labels.
        
    Returns:
        tuple: (DataFrame enrichi, Score Silhouette, Modèle entraîné)
    """
    # Configuration du modèle
    kmeans = KMeans(
        n_clusters=N_CLUSTERS, 
        random_state=RANDOM_SEED, 
        n_init=10
    )
    
    # Entraînement
    kmeans.fit(X)
    
    # Attribution des clusters
    labels = kmeans.labels_
    df['cluster'] = labels
    
    # Évaluation
    try:
        # Le score de silhouette nécessite au moins 2 clusters et > 1 échantillon
        if X.shape[0] > N_CLUSTERS:
            score = silhouette_score(X, labels)
        else:
            score = 0
    except Exception:
        score = 0 
        
    # Sauvegarde du modèle
    model_path = os.path.join(MODELS_DIR, "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(kmeans, f)
        
    return df, score, kmeans