import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pandas as pd
import os
from collections import Counter
from .config import FIGS_DIR, REPORTS_DIR


def save_and_store(fig, name, figs_list):
    """Enregistre une figure sur le disque et l'ajoute à la liste pour le PDF."""
    path = os.path.join(FIGS_DIR, name)
    fig.savefig(path)
    figs_list.append(fig)


def plot_source_distribution(df, figs):
    """Trace la distribution des sources de documents."""
    fig = plt.figure(figsize=(10, 6))
    sns.countplot(y='source', data=df, hue='source', palette='magma', legend=False)
    plt.title("Volume de documents par Source")
    plt.tight_layout()
    save_and_store(fig, "sources_bar.png", figs)

def plot_api_latency(lat_df, figs):
    """Trace la latence des appels API par source."""
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x='source', y='latency', data=lat_df, hue='source', palette='coolwarm', legend=False)
    plt.title("Latence API (secondes)")
    plt.tight_layout()
    save_and_store(fig, "latency_box.png", figs)

def plot_http_status(lat_df, figs):
    """Trace la répartition des codes de statut HTTP."""
    fig = plt.figure(figsize=(6, 6))
    status_counts = lat_df['status'].value_counts()
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#66b3ff','#ff9999'])
    plt.title("Répartition des Statuts HTTP")
    save_and_store(fig, "status_codes.png", figs)

def plot_activity_timeline(df, figs):
    """Trace le flux d'activité au fil du temps."""
    fig = plt.figure(figsize=(10, 5))
    df['dummy_time'] = range(len(df))
    sns.histplot(data=df, x='dummy_time', hue='source', element="step", bins=20)
    plt.title("Flux d'activité (Distribution séquentielle)")
    save_and_store(fig, "timeline_activity.png", figs)

def plot_top_keywords(df, figs):
    """Trace les 15 mots-clés les plus fréquents."""
    fig = plt.figure(figsize=(10, 6))
    all_words = " ".join(df['cleaned_text']).split()
    common = Counter(all_words).most_common(15)
    words, counts = zip(*common)
    sns.barplot(x=list(counts), y=list(words), hue=list(words), palette='viridis', legend=False)
    plt.title("Top 15 Mots-clés globaux")
    plt.tight_layout()
    save_and_store(fig, "top_keywords.png", figs)

def plot_cluster_interpretation(model, vectorizer, figs):
    """Trace l'interprétation des clusters KMeans."""
    fig = plt.figure(figsize=(10, 4))
    plt.axis('off')
    terms = vectorizer.get_feature_names_out()
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    
    text_str = "INTERPRÉTATION DES CLUSTERS (K-MEANS):\n\n"
    for i in range(model.n_clusters):
        top_w = [terms[ind] for ind in order_centroids[i, :6]]
        text_str += f"Cluster {i}: {', '.join(top_w)}\n"
        
    plt.text(0.05, 0.2, text_str, fontsize=11, family='monospace')
    plt.title("Extraction des thèmes par Cluster")
    save_and_store(fig, "ml_clusters.png", figs)


def generate_dashboard(df, model, vectorizer, raw_data_info):
    """
    Orchestre la génération du dashboard.
    """
    if not os.path.exists(FIGS_DIR): 
        os.makedirs(FIGS_DIR)
    
    figs = []
    lat_df = pd.DataFrame([{
        'source': d['source'], 
        'latency': d.get('latency', 0), 
        'status': d.get('status', 0)
    } for d in raw_data_info])

    plot_source_distribution(df, figs)
    plot_api_latency(lat_df, figs)
    plot_http_status(lat_df, figs)
    plot_activity_timeline(df, figs)
    plot_top_keywords(df, figs)
    plot_cluster_interpretation(model, vectorizer, figs)

    pdf_path = os.path.join(REPORTS_DIR, "dashboard.pdf")
    with PdfPages(pdf_path) as pdf:
        for fig in figs:
            pdf.savefig(fig)
            plt.close(fig) 
    
    print(f"Dashboard PDF généré : {pdf_path}")