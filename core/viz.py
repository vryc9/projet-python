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
    """
    Trace les top mots-clés par cluster sous forme de barres (Exigence Sujet).
    """
    terms = vectorizer.get_feature_names_out()
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    n_clusters = model.n_clusters
    
    rows = (n_clusters + 1) // 2
    fig, axes = plt.subplots(rows, 2, figsize=(12, 4 * rows))
    axes = axes.flatten()
    
    for i in range(n_clusters):
        top_indices = order_centroids[i, :10]
        top_terms = [terms[ind] for ind in top_indices]
        top_weights = [model.cluster_centers_[i, ind] for ind in top_indices]
        
        sns.barplot(x=top_weights, y=top_terms, ax=axes[i], palette='viridis', orient='h')
        axes[i].set_title(f"Cluster {i}", fontsize=12, fontweight='bold')
        axes[i].set_xlabel("Poids TF-IDF")
    
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.suptitle(f"Top Mots-clés par Cluster (K-Means k={n_clusters})", fontsize=14)
    plt.tight_layout()
    
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