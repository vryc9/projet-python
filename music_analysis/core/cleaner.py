import re
import string
import unicodedata

def clean_text(text):
    """
    Cleans text by removing punctuation, converting to lowercase, removing accents, and removing stopwords.
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove accents
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove numbers (optional, but good for word clouds)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove stopwords
    text = remove_stopwords(text)
    
    return text

def remove_stopwords(text):
    # Expanded stopword list (English + French)
    stopwords = set([
        # English
        'the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'its', 'our', 'their',
        'this', 'that', 'these', 'those',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'but', 'or', 'as', 'if', 'when', 'than', 'because', 'while', 'where',
        # French
        'le', 'la', 'les', 'l', 'un', 'une', 'des', 'du', 'de', 'd',
        'et', 'ou', 'a', 'au', 'aux', 'en', 'dans', 'par', 'pour', 'sur', 'avec', 'sans', 'sous',
        'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles', 'me', 'te', 'se', 'ce', 'ces', 'cette',
        'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes', 'ses', 'notre', 'votre', 'leur', 'nos', 'vos', 'leurs',
        'qui', 'que', 'quoi', 'dont', 'ou', 'qu',
        'est', 'sont', 'ete', 'avoir', 'etre', 'fait', 'faire'
    ])
    
    words = text.split()
    filtered_words = [w for w in words if w not in stopwords]
    return " ".join(filtered_words)
