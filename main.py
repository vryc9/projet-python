import logging
import sys
import os
import json
import pandas as pd

# Création des répertoires si nécessaire (devrait être fait avant imports si imports dépendent de paths, 
# mais ici config définit les paths, donc on peut créer après ou avant)
from core.config import (
    DATA_RAW, DATA_PROCESSED, MODELS_DIR, REPORTS_DIR, FIGS_DIR, LOG_DIR
)

for d in [DATA_RAW, DATA_PROCESSED, MODELS_DIR, REPORTS_DIR, FIGS_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

from core.fetcher import Fetcher
from core.cleaner import process_data
from core.analyzer import analyze_dataset
from core.features import extract_features
from core.model import train_clustering
from core.viz import generate_plots, generate_pdf_report

# Configuration du logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'marketing.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
# Ajout d'un handler pour la console
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger("marketing_ai")

def main():
    """
    Fonction principale d'orchestration du pipeline.
    1. Collecte (Fetcher)
    2. Nettoyage (Cleaner)
    3. Analyse (Analyzer)
    4. Features (Features)
    5. Modélisation (Model)
    6. Visualisation (Viz)
    """
    logger.info("=== DÉMARRAGE DU PIPELINE ===")

    # 1. Collecte
    logger.info("Étape 1 : Collecte des données...")
    fetcher = Fetcher()
    raw_data_list = fetcher.run()
    
    if not raw_data_list:
        logger.error("Aucune donnée récupérée. Arrêt du pipeline.")
        return

    # 2. Nettoyage
    logger.info("Étape 2 : Nettoyage des données...")
    df = process_data(raw_data_list)
    logger.info(f"Données propres : {len(df)} entrées")
    
    # Sauvegarde clean_data.json
    clean_data_path = os.path.join(DATA_PROCESSED, "clean_data.json")
    df.to_json(clean_data_path, orient="records", indent=4)

    # 3. Analyse
    logger.info("Étape 3 : Analyse des KPIs...")
    stats = analyze_dataset(df)
    
    # Sauvegarde summary.json
    with open(os.path.join(REPORTS_DIR, "summary.json"), "w") as f:
        json.dump(stats, f, indent=4)
        
    # Sauvegarde keywords.csv
    if stats.get('top_keywords'):
        keywords_df = pd.DataFrame(stats['top_keywords'], columns=['keyword', 'count'])
        keywords_df.to_csv(os.path.join(REPORTS_DIR, "keywords.csv"), index=False)

    # 4. Features & 5. ML
    logger.info("Étape 4 & 5 : Features et Machine Learning (Clustering)...")
    score = 0
    if len(df) > 5:
        # Extraction features
        X, vectorizer = extract_features(df)
        
        # Entraînement modèle
        df, score, model = train_clustering(X, df)
        logger.info(f"Clustering terminé. Silhouette Score: {score:.3f}")
    else:
        logger.warning("Pas assez de données pour le ML (min 5 documents).")

    # 6. Visualisation
    logger.info("Étape 6 : Génération des rapports et figures...")
    generate_plots(df, stats, raw_data_list)
    generate_pdf_report(stats, score)

    logger.info(f"Pipeline terminé avec succès. Rapport disponible : {os.path.join(REPORTS_DIR, 'dashboard.pdf')}")

if __name__ == "__main__":
    main()