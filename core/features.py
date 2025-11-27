from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from core.config import MODELS_DIR

def extract_features(df):
    vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['clean_text'])
    
    with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
        
    return X, vectorizer