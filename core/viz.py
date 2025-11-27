import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pandas as pd
import os
from .config import FIGS_DIR, REPORTS_DIR

def generate_dashboard(df, model, vectorizer, raw_data_info):
    if not os.path.exists(FIGS_DIR): os.makedirs(FIGS_DIR)
    
    lat_df = pd.DataFrame([{'source': d['source'], 'latency': d.get('latency', 0), 'status': d.get('status', 0)} for d in raw_data_info])

    figs = [] 

    f1 = plt.figure(figsize=(10, 6))
    sns.countplot(y='source', data=df, palette='magma')
    plt.title("Volume de documents par Source")
    plt.tight_layout()
    f1.savefig(os.path.join(FIGS_DIR, "sources_bar.png"))
    figs.append(f1)

    f2 = plt.figure(figsize=(10, 6))
    sns.barplot(x='source', y='latency', data=lat_df, palette='coolwarm')
    plt.title("Latence API (secondes)")
    plt.tight_layout()
    f2.savefig(os.path.join(FIGS_DIR, "latency_box.png"))
    figs.append(f2)

    f3 = plt.figure(figsize=(6, 6))
    status_counts = lat_df['status'].value_counts()
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#66b3ff','#ff9999'])
    plt.title("Répartition des Statuts HTTP")
    f3.savefig(os.path.join(FIGS_DIR, "status_codes.png"))
    figs.append(f3)

    f4 = plt.figure(figsize=(10, 5))
    df['dummy_time'] = range(len(df))
    sns.histplot(data=df, x='dummy_time', hue='source', element="step", bins=20)
    plt.title("Flux d'activité (Distribution séquentielle)")
    f4.savefig(os.path.join(FIGS_DIR, "timeline_activity.png"))
    figs.append(f4)

    f5 = plt.figure(figsize=(10, 6))
    from collections import Counter
    all_words = " ".join(df['cleaned_text']).split()
    common = Counter(all_words).most_common(15)
    sns.barplot(x=[x[1] for x in common], y=[x[0] for x in common], palette='viridis')
    plt.title("Top 15 Mots-clés globaux")
    plt.tight_layout()
    f5.savefig(os.path.join(FIGS_DIR, "top_keywords.png"))
    figs.append(f5)

    f6 = plt.figure(figsize=(10, 4))
    plt.axis('off')
    terms = vectorizer.get_feature_names_out()
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    text_str = "INTERPRÉTATION DES CLUSTERS (K-MEANS):\n\n"
    for i in range(model.n_clusters):
        top_w = [terms[ind] for ind in order_centroids[i, :6]]
        text_str += f"Cluster {i}: {', '.join(top_w)}\n"
    plt.text(0.05, 0.2, text_str, fontsize=11, family='monospace')
    plt.title("Extraction des thèmes par Cluster")
    f6.savefig(os.path.join(FIGS_DIR, "ml_clusters.png"))
    figs.append(f6)

    pdf_path = os.path.join(REPORTS_DIR, "dashboard.pdf")
    with PdfPages(pdf_path) as pdf:
        for fig in figs:
            pdf.savefig(fig)
            plt.close(fig) 
    
    print(f"Dashboard PDF généré : {pdf_path}")