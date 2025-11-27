import pandas as pd
from collections import Counter

def analyze_dataset(df):
    """
    Calcule des indicateurs clés (KPIs) sur le dataset.
    
    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.
        
    Returns:
        dict: Dictionnaire contenant les statistiques.
    """
    stats = {}
    
    if df.empty:
        return {
            'total_docs': 0,
            'by_source': {},
            'top_keywords': [],
            'avg_length': 0
        }

    # Nombre total de documents
    stats['total_docs'] = len(df)
    
    # Répartition par source
    stats['by_source'] = df['source'].value_counts().to_dict()
    
    # Top mots-clés
    all_text = " ".join(df['clean_text'].astype(str))
    words = all_text.split()
    stats['top_keywords'] = Counter(words).most_common(10)
    
    # Longueur moyenne des textes (en nombre de mots)
    df['length'] = df['clean_text'].apply(lambda x: len(str(x).split()))
    stats['avg_length'] = df['length'].mean()
    
    return stats