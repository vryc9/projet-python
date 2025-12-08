import json
import re
import logging
from .config import DATA_RAW, DATA_CLEAN

logger = logging.getLogger(__name__)

STOPWORDS = set(["the", "a", "an", "of", "to", "in", "for", "on", "and", "is", "with",
                 "le", "la", "les", "de", "et", "des", "du", "un", "une", "est", "sont"])

def clean_text(text):
    """
    Nettoie une chaîne : minuscules, suppression HTML, caractères spéciaux et stopwords.
    """
    if not text: return ""
    text = text.lower()
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return " ".join([w for w in text.split() if w not in STOPWORDS and len(w) > 2])

def run_cleaner():
    """
    Charge les données brutes, extrait les textes selon la source et génère un dataset nettoyé.
    """
    try:
        with open(DATA_RAW, 'r', encoding='utf-8') as f:
            raw_list = json.load(f)
    except FileNotFoundError:
        logger.error(f"Fichier {DATA_RAW} introuvable. Lancez le fetcher d'abord.")
        return []

    processed_docs = []

    for entry in raw_list:
        source = entry['source']
        contents = entry.get('raw_content', [])
        
        items = []

        if source == 'newsapi':
            if isinstance(contents, dict):
                items = contents.get('articles', [])
            else:
                items = []

        elif source == 'reddit':
            items = contents 

        else:
            items = contents if isinstance(contents, list) else []

        for item in items:
            text_raw = ""

            if source == 'reddit':
                data_obj = item.get('data', {})
                text_raw = (data_obj.get('title', '') or '') + " " + (data_obj.get('selftext', '') or '')
            
            elif source == 'wikipedia':
                text_raw = (item.get('title', '') or '') + " " + (item.get('snippet', '') or '')

            elif source == 'arxiv':
                text_raw = (item.get('title', '') or '') + " " + (item.get('summary', '') or '')
            
            else:
                text_raw = (item.get('title', '') or '') + " " + (item.get('description', '') or '')

            text_clean = clean_text(text_raw)
            
            if text_clean:
                processed_docs.append({
                    "source": source,
                    "original": text_raw[:100] + "...",
                    "cleaned_text": text_clean
                })

    with open(DATA_CLEAN, 'w', encoding='utf-8') as f:
        json.dump(processed_docs, f, indent=4)
    
    logger.info(f"Nettoyage terminé. {len(processed_docs)} documents")
    return processed_docs
