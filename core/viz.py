import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from core.config import FIGS_DIR, REPORTS_DIR

def generate_plots(df, stats, raw_data_list):
    """
    Génère et sauvegarde les figures (PNG) pour le rapport.
    
    Args:
        df (pd.DataFrame): DataFrame des données traitées.
        stats (dict): Statistiques globales.
        raw_data_list (list): Données brutes pour extraire les latences.
    """
    # Configuration du style
    plt.style.use('ggplot')
    
    # 1. Volume par source
    plt.figure(figsize=(8, 5))
    sns.countplot(x='source', data=df, hue='source', legend=False)
    plt.title("Volume de données par API")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "sources_bar.png"))
    plt.close()

    # 2. Top Mots-clés
    if stats.get('top_keywords'):
        words, counts = zip(*stats['top_keywords'])
        plt.figure(figsize=(10, 6))
        plt.barh(words, counts, color='skyblue')
        plt.title("Top 10 Mots-clés")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(FIGS_DIR, "top_keywords.png"))
        plt.close()

    # 3. Latence des APIs
    # Extraction des latences depuis raw_data_list
    latencies = [{'source': d.get('source'), 'latency': d.get('latency', 0)} for d in raw_data_list]
    df_lat = pd.DataFrame(latencies)
    
    if not df_lat.empty:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='source', y='latency', data=df_lat, palette="Set3", hue='source', legend=False)
        plt.ylabel("Secondes")
        plt.title("Distribution des Latences par API")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGS_DIR, "latency_box.png"))
        plt.close()

    # 4. Codes Statut HTTP
    statuses = [str(d.get('status', 0)) for d in raw_data_list]
    plt.figure(figsize=(6, 6))
    sns.countplot(x=statuses, hue=statuses, legend=False, palette="pastel")
    plt.title("Répartition des Codes Statut HTTP")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "status_codes.png"))
    plt.close()

    # 5. Chronologie (Simulée car pas de timestamp dans les données API temps réel, on utilise l'index ou une fausse date)
    # Pour l'exercice, on va simuler une activité temporelle ou utiliser l'index comme "temps"
    plt.figure(figsize=(10, 5))
    # On crée une série temporelle fictive ou basée sur l'ordre d'arrivée
    plt.plot(df.index, df.index, label='Volume cumulé (simulé)') 
    plt.title("Chronologie de l'activité (Volume/Temps)")
    plt.xlabel("Temps (Index)")
    plt.ylabel("Volume")
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "timeline_activity.png"))
    plt.close()

    # 6. Clustering (ML Viz)
    if 'cluster' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(x='cluster', data=df, hue='cluster', palette='viridis', legend=False)
        plt.title("Segmentation des Artistes (Clustering)")
        plt.tight_layout()
        plt.savefig(os.path.join(FIGS_DIR, "ml_clusters.png"))
        plt.close()

def generate_pdf_report(stats, ml_score):
    """
    Génère le rapport PDF final agrégeant les figures et les stats.
    
    Args:
        stats (dict): Statistiques globales.
        ml_score (float): Score de performance du modèle ML.
    """
    pdf_path = os.path.join(REPORTS_DIR, "dashboard.pdf")
    pp = PdfPages(pdf_path)
    
    # Page de garde
    plt.figure(figsize=(11, 8.5))
    plt.text(0.5, 0.8, "Rapport Marketing Data & IA", ha='center', fontsize=24, weight='bold')
    plt.text(0.5, 0.6, f"Documents analysés : {stats.get('total_docs', 0)}", ha='center', fontsize=18)
    plt.text(0.5, 0.5, f"Score Silhouette ML : {ml_score:.3f}", ha='center', fontsize=18)
    plt.axis('off')
    pp.savefig()
    plt.close()
    
    # Figures
    imgs = [
        "sources_bar.png", 
        "top_keywords.png", 
        "latency_box.png", 
        "status_codes.png", 
        "timeline_activity.png", 
        "ml_clusters.png"
    ]
    
    for img_name in imgs:
        img_path = os.path.join(FIGS_DIR, img_name)
        if os.path.exists(img_path):
            try:
                img = plt.imread(img_path)
                plt.figure(figsize=(10, 8))
                plt.imshow(img)
                plt.axis('off')
                plt.title(img_name, fontsize=14)
                pp.savefig()
                plt.close()
            except Exception as e:
                print(f"Erreur lors de l'ajout de l'image {img_name}: {e}")
            
    pp.close()