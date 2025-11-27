# core/viz.py
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.backends.backend_pdf import PdfPages
from core.config import FIGS_DIR, REPORTS_DIR

def generate_plots(df, stats, latency_data):
    # Style
    plt.style.use('ggplot')
    
    # 1. Volume par Source (Bar)
    plt.figure(figsize=(6, 4))
    sns.countplot(x='source', data=df)
    plt.title("Volume de données par API")
    plt.savefig(os.path.join(FIGS_DIR, "sources_bar.png"))
    plt.close()

    # 2. Top Keywords (Barh)
    words, counts = zip(*stats['top_keywords'])
    plt.figure(figsize=(8, 5))
    plt.barh(words, counts, color='skyblue')
    plt.title("Top 10 Mots-clés")
    plt.gca().invert_yaxis()
    plt.savefig(os.path.join(FIGS_DIR, "top_keywords.png"))
    plt.close()

    # 3. Latences (Boxplot)
    # Reconstruction simple des latences pour l'exemple
    lats = [d['latency'] for d in latency_data]
    srcs = [d['source'] for d in latency_data]
    plt.figure(figsize=(6, 4))
    plt.bar(srcs, lats, color='salmon')
    plt.ylabel("Secondes")
    plt.title("Latence des APIs")
    plt.savefig(os.path.join(FIGS_DIR, "latency_box.png"))
    plt.close()

    # 4. Répartition Statuts HTTP
    statuses = [str(d['status']) for d in latency_data]
    plt.figure(figsize=(5, 5))
    plt.hist(statuses)
    plt.title("Codes Statut HTTP")
    plt.savefig(os.path.join(FIGS_DIR, "status_codes.png"))
    plt.close()

    # 5. ML : Distribution des Clusters
    plt.figure(figsize=(6, 4))
    sns.countplot(x='cluster', data=df, palette='viridis')
    plt.title("Segmentation des Artistes (Clustering)")
    plt.savefig(os.path.join(FIGS_DIR, "ml_clusters.png"))
    plt.close()

def generate_pdf_report(stats, ml_score):
    pdf_path = os.path.join(REPORTS_DIR, "dashboard.pdf")
    pp = PdfPages(pdf_path)
    
    # Page titre
    plt.figure(figsize=(8, 6))
    plt.text(0.5, 0.8, "Rapport Marketing Data & IA", ha='center', fontsize=24)
    plt.text(0.5, 0.6, f"Documents analysés : {stats['total_docs']}", ha='center', fontsize=16)
    plt.text(0.5, 0.5, f"Score Silhouette ML : {ml_score:.3f}", ha='center', fontsize=16)
    plt.axis('off')
    pp.savefig()
    plt.close()
    
    # Ajout des images générées
    imgs = ["sources_bar.png", "top_keywords.png", "latency_box.png", "ml_clusters.png"]
    for img_name in imgs:
        img_path = os.path.join(FIGS_DIR, img_name)
        if os.path.exists(img_path):
            plt.figure(figsize=(10, 8))
            img = plt.imread(img_path)
            plt.imshow(img)
            plt.axis('off')
            plt.title(img_name)
            pp.savefig()
            plt.close()
            
    pp.close()