from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_content(query_vector, X, df, top_k=5):
    """
    Recommande des contenus similaires à une requête vectorisée.
    
    Args:
        query_vector (array-like): Vecteur TF-IDF de la requête.
        X (sparse matrix): Matrice de features de l'ensemble des documents.
        df (pd.DataFrame): DataFrame contenant les métadonnées.
        top_k (int): Nombre de recommandations à retourner.
        
    Returns:
        pd.DataFrame: Top-k documents les plus similaires.
    """
    # Calcul de la similarité cosinus
    similarities = cosine_similarity(query_vector, X).flatten()
    
    # Récupération des indices des top-k plus proches
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    # Retourne les résultats correspondants
    return df.iloc[top_indices]
