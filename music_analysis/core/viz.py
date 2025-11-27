import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from . import config

def plot_wordcloud(text, title="Word Cloud"):
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.savefig(config.FIGS_DIR / "wordcloud.png")
    plt.close()

def plot_bpm_stats(df):
    if 'tempo' not in df.columns:
        return
    plt.figure(figsize=(10, 6))
    sns.histplot(df['tempo'], kde=True)
    plt.title("BPM Distribution")
    plt.savefig(config.FIGS_DIR / "bpm_dist.png")
    plt.close()

from fpdf import FPDF

def plot_technical_stats(latencies):
    plt.figure(figsize=(8, 6))
    plt.boxplot(latencies)
    plt.title("API Latency Distribution")
    plt.savefig(config.FIGS_DIR / "latency_box.png")
    plt.close()

def plot_top_artists(df):
    plt.figure(figsize=(10, 6))
    top_artists = df['artist'].value_counts().head(10)
    sns.barplot(x=top_artists.values, y=top_artists.index, palette='viridis')
    plt.title('Top 10 Artists in Dataset')
    plt.xlabel('Count')
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "top_artists.png")
    plt.close()

def plot_genre_dist(df):
    plt.figure(figsize=(8, 8))
    # Split genres if they are comma separated and count
    all_genres = df['genres'].str.split(', ').explode()
    top_genres = all_genres.value_counts().head(8)
    plt.pie(top_genres, labels=top_genres.index, autopct='%1.1f%%', startangle=140)
    plt.title('Top Genres Distribution')
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "genre_dist.png")
    plt.close()

def plot_popularity_dist(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['popularity'], bins=20, kde=True, color='skyblue')
    plt.title('Track Popularity Distribution')
    plt.xlabel('Popularity (0-100)')
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "popularity_dist.png")
    plt.close()

def plot_styles_by_country(df):
    # Mock implementation for now as we don't have 'country' column in mock data easily
    # But if we did:
    if 'country' in df.columns and 'cluster' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='country', hue='cluster')
        plt.title("Top Styles (Clusters) by Country")
        plt.savefig(config.FIGS_DIR / "styles_by_country.png")
        plt.close()

def generate_dashboard(kpis, ml_score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Music Analysis Dashboard", ln=1, align='C')
    
    # KPIs
    pdf.cell(200, 10, txt="Key Performance Indicators", ln=1, align='L')
    for key, value in kpis.items():
        pdf.cell(200, 10, txt=f"{key}: {value:.2f}", ln=1, align='L')
        
    # ML Score
    pdf.cell(200, 10, txt=f"Clustering Silhouette Score: {ml_score:.2f}", ln=1, align='L')
    
    # Images
    images = [
        "wordcloud.png", 
        "styles_by_country.png", 
        "top_artists.png", 
        "genre_dist.png", 
        "popularity_dist.png",
        "latency_box.png"
    ]
    for img in images:
        img_path = config.FIGS_DIR / img
        if img_path.exists():
            pdf.image(str(img_path), w=100)
            pdf.ln(10)
            
    pdf.output(config.REPORTS_DIR / "dashboard.pdf")
