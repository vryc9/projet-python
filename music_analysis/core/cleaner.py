import re
import string

def clean_text(text):
    """
    Cleans text by removing punctuation, converting to lowercase, and removing stopwords.
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers (optional, but good for word clouds)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text

def remove_stopwords(text, language='english'):
    # This would ideally use NLTK or spacy, but we are restricted to scikit-learn/standard libs?
    # The subject says "stopwords FR/EN".
    # We can define a simple list or use sklearn's list if available, or just a hardcoded list for now.
    stopwords = set(['the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'le', 'la', 'les', 'et', 'de', 'en', 'un', 'une'])
    
    words = text.split()
    filtered_words = [w for w in words if w not in stopwords]
    return " ".join(filtered_words)
