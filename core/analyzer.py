# core/analyzer.py
import pandas as pd
from collections import Counter

def analyze_dataset(df):
    stats = {}
    stats['total_docs'] = len(df)
    stats['by_source'] = df['source'].value_counts().to_dict()
    
    # Mots fréquents
    all_text = " ".join(df['clean_text'])
    words = all_text.split()
    stats['top_keywords'] = Counter(words).most_common(10)
    
    # Longueur moyenne
    df['length'] = df['clean_text'].apply(lambda x: len(x.split()))
    stats['avg_length'] = df['length'].mean()
    
    return stats