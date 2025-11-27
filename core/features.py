import json
import pickle
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .config import DATA_CLEAN, VECT_PATH

logger = logging.getLogger(__name__)

def extract_features():
    logger.info("Extraction des features (TF-IDF)...")
    
    with open(DATA_CLEAN, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    corpus = [d['cleaned_text'] for d in data]
    
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
    X = vectorizer.fit_transform(corpus)
    
    with open(VECT_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    logger.info(f"Vectorisation terminée. Shape: {X.shape}")
    return X, vectorizer, data