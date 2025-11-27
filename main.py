import logging
import sys
import os
import json
for d in ["data/raw", "data/processed", "data/models", "reports", "figs", "logs", "core"]:
    os.makedirs(d, exist_ok=True)

from core.fetcher import Fetcher
from core.cleaner import process_data
from core.analyzer import analyze_dataset
from core.features import extract_features
from core.model import train_clustering
from core.viz import generate_plots, generate_pdf_report
from core.config import DATA_PROCESSED, REPORTS_DIR, LOG_DIR

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'marketing.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler(sys.stdout)
logging.getLogger('').addHandler(console)
logger = logging.getLogger("marketing_ai")

def main():
    logger.info("=== DÉMARRAGE DU PIPELINE ===")

    fetcher = Fetcher()
    raw_data_list = fetcher.run()
    if not raw_data_list:
        logger.error("Aucune donnée récupérée.")
        return

    logger.info("Nettoyage des données...")
    df = process_data(raw_data_list)
    logger.info(f"Données propres : {len(df)} entrées")
    
    df.to_json(os.path.join(DATA_PROCESSED, "clean_data.json"), orient="records")

    logger.info("Analyse des KPIs...")
    stats = analyze_dataset(df)
    with open(os.path.join(REPORTS_DIR, "summary.json"), "w") as f:
        json.dump(stats, f, indent=4)

    logger.info("Entraînement du modèle ML (K-Means)...")
    if len(df) > 5:
        X, vectorizer = extract_features(df)
        df, score, model = train_clustering(X, df)
        logger.info(f"Clustering terminé. Silhouette Score: {score:.3f}")
    else:
        logger.warning("Pas assez de données pour le ML.")
        score = 0

    logger.info("Génération des figures et du rapport...")
    generate_plots(df, stats, raw_data_list)
    generate_pdf_report(stats, score)

    logger.info(f"Pipeline terminé avec succès. Rapport : {os.path.join(REPORTS_DIR, 'dashboard.pdf')}")

if __name__ == "__main__":
    main()