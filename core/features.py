from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import numpy as np
from core.config import MODELS_DIR

def extract_features(df):
    """
    Extrait les features TF-IDF du texte nettoyé.
    Sauvegarde le vectorizer et la matrice de features.
    
    Args:
        df (pd.DataFrame): DataFrame contenant la colonne 'clean_text'.
        
    Returns:
        tuple: (Matrice sparse TF-IDF, objet vectorizer)
    """
    # TF-IDF avec n-grams (1, 2)
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['clean_text'])
    
    # Sauvegarde du vectorizer
    vectorizer_path = os.path.join(MODELS_DIR, "vectorizer.pkl")
    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)
        
    # Sauvegarde des features (format numpy compressé ou brut si sparse)
    # Ici on sauvegarde en .npz pour respecter la consigne "features.npz"
    features_path = os.path.join(MODELS_DIR, "features.npz")
    # On convertit en dense pour simplifier la sauvegarde npz standard, 
    # ou on utilise scipy.sparse.save_npz si on voulait rester en sparse.
    # Pour l'exercice, on sauvegarde une version dense ou sparse selon besoin.
    # La consigne demande features.npz.
    try:
        from scipy import sparse
        sparse.save_npz(features_path, X)
    except ImportError:
        # Fallback si scipy pas dispo (mais il est dans requirements)
        np.savez(features_path, data=X.toarray())
        
    return X, vectorizer