# core/features.py
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from core.config import MODELS_DIR

def extract_features(df):
    # TF-IDF : ngrams 1 à 2 pour capter "pop rock" etc.
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['clean_text'])
    
    # Sauvegarde vectorizer
    with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
        
    return X, vectorizer