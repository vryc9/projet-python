from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import pandas as pd

def extract_tfidf(texts, max_features=1000):
    vectorizer = TfidfVectorizer(max_features=max_features, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix, vectorizer

def scale_features(df, columns):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[columns])
    return scaled_data, scaler
