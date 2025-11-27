import re
import pandas as pd
from core.config import STOPWORDS

def clean_text(text):
    """
    Nettoie le texte : minuscule, suppression balises HTML/ponctuation, stopwords.
    
    Args:
        text (str): Le texte brut à nettoyer.
        
    Returns:
        str: Le texte nettoyé.
    """
    if not isinstance(text, str):
        return ""
    
    # Minuscule
    text = text.lower()
    
    # Suppression balises HTML
    text = re.sub(r'<[^>]+>', '', text)
    
    # Suppression ponctuation et caractères spéciaux
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenization et suppression stopwords
    tokens = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    
    return " ".join(tokens)

def process_data(raw_data):
    """
    Transforme les données brutes (liste de dicts) en DataFrame pandas unifié.
    
    Args:
        raw_data (list): Liste des résultats de collecte.
        
    Returns:
        pd.DataFrame: DataFrame contenant les données nettoyées.
    """
    processed_list = []
    
    for entry in raw_data:
        source = entry.get('source', 'unknown')
        items = entry.get('data', [])
        
        for item in items:
            name = item.get('name', 'Unknown')
            content = name 
            
            # Enrichissement du contenu selon la source pour avoir plus de texte à analyser
            if source == 'lastfm':
                listeners = item.get('listeners', '0')
                playcount = item.get('playcount', '0')
                content += f" music artist popular with {listeners} listeners and {playcount} playcount"
            elif source == 'spotify':
                genres = " ".join(item.get('genres', []))
                popularity = item.get('popularity', 0)
                content += f" {genres} popularity {popularity}"
            elif source == 'deezer':
                position = item.get('position', 0)
                content += f" music artist deezer chart position {position}"

            processed_list.append({
                "source": source,
                "name": name,
                "raw_text": content,
                "clean_text": clean_text(content)
            })
            
    df = pd.DataFrame(processed_list)
    
    # Suppression des doublons basés sur le nom de l'artiste
    if not df.empty:
        df = df.drop_duplicates(subset=['name'])
        
    return df