import pickle
import logging
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from .config import MODEL_PATH, N_CLUSTERS, SEED

logger = logging.getLogger(__name__)

def train_model(X):
    logger.info(f"Entraînement du modèle KMeans (k={N_CLUSTERS})...")
    
    model = KMeans(n_clusters=N_CLUSTERS, random_state=SEED, n_init=10)
    model.fit(X)
    
    try:
        score = silhouette_score(X, model.labels_)
        logger.info(f"Silhouette Score: {score:.4f}")
    except:
        score = 0
        logger.warning("Pas assez de données pour calculer le silhouette score.")

    # Sauvegarde
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
        
    return model, score