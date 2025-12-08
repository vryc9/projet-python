import json
import pandas as pd
import os
import csv
from collections import Counter
from .config import DATA_CLEAN, REPORTS_DIR


def analyze_and_report(df_clean):
    """
        Génère des statistiques sur les textes nettoyés et crée des rapports CSV et JSON.
    """    
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    all_words = " ".join(df_clean['cleaned_text']).split()
    common_words = Counter(all_words).most_common(50)
    
    csv_path = os.path.join(REPORTS_DIR, "keywords.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "frequency"])
        writer.writerows(common_words)

    summary = {
        "total_documents": len(df_clean),
        "sources_count": df_clean['source'].value_counts().to_dict(),
        "avg_length": round(df_clean['cleaned_text'].apply(len).mean(), 2),
        "top_5_keywords": [w[0] for w in common_words[:5]]
    }

    json_path = os.path.join(REPORTS_DIR, "summary.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4)

    return summary