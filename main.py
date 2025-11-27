import logging
import sys
import pandas as pd
from core import fetcher, cleaner, features, model, viz, analyzer
from core.config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MAIN")

def main():
    logger.info("=== DÉMARRAGE DU PIPELINE MARKETING AI ===")

    raw_data_info = fetcher.fetch_data()
    
    clean_data_list = cleaner.run_cleaner()
    
    df_clean = pd.DataFrame(clean_data_list)

    if df_clean.empty:
        logger.error("Aucune donnée nettoyée disponible. Arrêt du pipeline.")
        return

    summary = analyzer.analyze_and_report(df_clean)
    logger.info(f"Rapport généré. Stats globales : {summary}")

    X, vectorizer, _ = features.extract_features()

    kmeans_model, score = model.train_model(X)
    
    df_clean['cluster'] = kmeans_model.labels_

    viz.generate_dashboard(df_clean, kmeans_model, vectorizer, raw_data_info)
    
    logger.info("=== PIPELINE TERMINÉ AVEC SUCCÈS ===")
    logger.info("Ouvrez le dossier /reports pour voir dashboard.pdf et le dossier /figs pour les images.")

if __name__ == "__main__":
    main()