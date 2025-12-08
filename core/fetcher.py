import requests
import time
import json
import logging
import xml.etree.ElementTree as ET
from .config import URLS, DATA_RAW

logger = logging.getLogger(__name__)

def fetch_data():
    """
    Collecte des données sur toutes les API configurées et sauvegarde le brut en JSON.
    """
    raw_data = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    logger.info("Début de la collecte")

    for source, url in URLS.items():
        start = time.time()
        content_extracted = []
        status = 0
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            status = resp.status_code
            
            if status == 200:
                if source == 'reddit':
                    data = resp.json()
                    content_extracted = data['data']['children']
                
                elif source == 'arxiv':
                    root = ET.fromstring(resp.content)
                    ns = {'atom': 'http://www.w3.org/2005/Atom'}
                    for entry in root.findall('atom:entry', ns):
                        title = entry.find('atom:title', ns).text
                        summary = entry.find('atom:summary', ns).text
                        content_extracted.append({'title': title, 'summary': summary})
                
                elif source == 'wikipedia':
                    data = resp.json()
                    content_extracted = data['query']['search']

                elif source == 'hackernews':
                    ids = resp.json()[:15]
                    for i in ids:
                        s_url = f"https://hacker-news.firebaseio.com/v0/item/{i}.json"
                        story = requests.get(s_url).json()
                        if story: content_extracted.append(story)
                
                else:
                    content_extracted = resp.json()

            latency = round(time.time() - start, 3)
            
            raw_data.append({
                "source": source,
                "status": status,
                "latency": latency,
                "raw_content": content_extracted,
                "timestamp": time.time()
            })
            logger.info(f"[{source}] Latency: {latency}s | Items: {len(content_extracted)}")

        except Exception as e:
            logger.error(f"Erreur {source}: {e}")
            raw_data.append({"source": source, "status": 500, "latency": 0, "error": str(e)})

    with open(DATA_RAW, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, indent=4)
    
    return raw_data
