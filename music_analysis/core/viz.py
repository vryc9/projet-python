import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from fpdf import FPDF
import numpy as np
from . import config

# Set global theme
sns.set_theme(style="whitegrid")

def plot_wordcloud(text, title="Word Cloud"):
    if not text:
        return
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "wordcloud.png")
    plt.close()

def plot_bpm_stats(df):
    if 'tempo' not in df.columns:
        return
    plt.figure(figsize=(10, 6))
    sns.histplot(df['tempo'], kde=True, color='teal')
    plt.title("BPM Distribution")
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "bpm_dist.png")
    plt.close()

def plot_technical_stats(latencies):
    plt.figure(figsize=(8, 6))
    plt.boxplot(latencies)
    plt.title("API Latency Distribution")
    plt.ylabel("Seconds")
    plt.tight_layout()
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
    plt.figure(figsize=(10, 8))
    # Split genres if they are comma separated and count
    all_genres = df['genres'].str.split(', ').explode()
    top_genres = all_genres.value_counts().head(15)
    
    sns.barplot(x=top_genres.values, y=top_genres.index, palette='rocket')
    plt.title('Top 15 Genres Distribution')
    plt.xlabel('Count')
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
    if 'country' in df.columns and 'cluster' in df.columns:
        plt.figure(figsize=(12, 6))
        sns.countplot(data=df, x='country', hue='cluster', palette='Set2')
        plt.title("Top Styles (Clusters) by Country")
        plt.tight_layout()
        plt.savefig(config.FIGS_DIR / "styles_by_country.png")
        plt.close()

def plot_correlation_matrix(df):
    # Select numerical columns
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return
    
    plt.figure(figsize=(10, 8))
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "correlation_matrix.png")
    plt.close()

def plot_popularity_by_genre(df):
    # Explode genres to handle tracks with multiple genres
    df_exploded = df.assign(genre=df['genres'].str.split(', ')).explode('genre')
    
    # Get top 10 genres to keep the plot readable
    top_genres = df_exploded['genre'].value_counts().head(10).index
    df_filtered = df_exploded[df_exploded['genre'].isin(top_genres)]
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_filtered, x='genre', y='popularity', palette='Set3')
    plt.title("Popularity Distribution by Top Genres")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(config.FIGS_DIR / "popularity_by_genre.png")
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
        "correlation_matrix.png",
        "popularity_by_genre.png",
        "latency_box.png"
    ]
    
    y_pos = 60
    for i, img in enumerate(images):
        img_path = config.FIGS_DIR / img
        if img_path.exists():
            if y_pos > 250:
                pdf.add_page()
                y_pos = 20
            
            pdf.image(str(img_path), x=10, y=y_pos, w=180)
            y_pos += 110 # Approximate height + padding
            
    pdf.output(config.REPORTS_DIR / "dashboard.pdf")
