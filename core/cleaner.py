import re
import pandas as pd

STOPWORDS = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "le", "la", "les", "de", "et"}

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return " ".join(tokens)

def process_data(raw_data):
    """Transforme les dumps JSON hétérogènes en un DataFrame unifié."""
    processed_list = []
    
    for entry in raw_data:
        source = entry['source']
        items = entry['data']
        
        for item in items:
            name = item.get('name', 'Unknown')
            content = name 
            
            if source == 'lastfm':
                listeners = item.get('listeners', '0')
                content += f" music artist popular with {listeners} listeners"
            elif source == 'spotify':
                genres = " ".join(item.get('genres', []))
                content += f" {genres}"
            elif source == 'deezer':
                content += " music artist deezer chart"

            processed_list.append({
                "source": source,
                "name": name,
                "raw_text": content,
                "clean_text": clean_text(content)
            })
            
    df = pd.DataFrame(processed_list)
    # Supprimer doublons
    df = df.drop_duplicates(subset=['name'])
    return df