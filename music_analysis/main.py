import logging
from core import config, fetcher, cleaner, analyzer, features, model, viz
import pandas as pd
import numpy as np


def main():
    logging.info("Starting Music Analysis Pipeline...")
    
    # 1. Data Collection
    spotify = fetcher.SpotifyFetcher()
    
    # Check if we have keys, otherwise use mock data
    if spotify.sp:
        # Fetch data for a few countries to get a mix
        countries = ['US', 'FR', 'BR', 'DE', 'JP', 'IT', 'ES', 'CA', 'AU', 'MX']
        all_tracks = []
        for country in countries:
            tracks = spotify.get_top_tracks_by_country(country_code=country)
            all_tracks.extend(tracks)
            
        # Get artist info (for genres)
        artist_ids = list(set([t['artists'][0]['id'] for t in all_tracks if t['artists']]))
        artists_info = spotify.get_artists(artist_ids)
        
        # Create a map of artist_id -> genres
        artist_genres = {a['id']: a['genres'] for a in artists_info if a}
        
        # Combine data
        data = []
        for track in all_tracks:
            artist_id = track['artists'][0]['id']
            genres = artist_genres.get(artist_id, [])
            genre_str = ", ".join(genres) if genres else "unknown"
            
            track_data = {
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'id': track['id'],
                'popularity': track['popularity'],
                'genres': genre_str
            }
            data.append(track_data)
        
        df = pd.DataFrame(data)
        logging.info(f"Collected {len(df)} tracks.")
        
        if df.empty:
            logging.warning("Data collection returned empty DataFrame. Falling back to mock data.")
            # Mock Data
            data = {
                'name': [f'Track {i}' for i in range(50)],
                'artist': [f'Artist {i%5}' for i in range(50)],
                'popularity': np.random.randint(0, 100, 50),
                'genres': np.random.choice(['pop', 'rock', 'hip hop', 'jazz', 'classical'], 50),
                'country': np.random.choice(['US', 'FR', 'BR'], 50)
            }
            df = pd.DataFrame(data)
        
    else:
        logging.warning("No Spotify keys found. Using mock data.")
        # Mock Data
        data = {
            'name': [f'Track {i}' for i in range(50)],
            'artist': [f'Artist {i%5}' for i in range(50)],
            'popularity': np.random.randint(0, 100, 50),
            'genres': np.random.choice(['pop', 'rock', 'hip hop', 'jazz', 'classical'], 50),
            'country': np.random.choice(['US', 'FR', 'BR'], 50)
        }
        df = pd.DataFrame(data)

    # 2. Cleaning & Analysis
    # Mock text for wordcloud since we don't have lyrics
    text_data = " ".join(df['name'] + " " + df['artist'])
    cleaned_text = cleaner.clean_text(text_data)
    
    kpis = analyzer.compute_kpis(df)
    logging.info(f"KPIs: {kpis}")

    # 3. ML
    # 3. ML
    # Clustering on Genres (Text Features)
    if 'genres' in df.columns:
        # Use TF-IDF on genres
        X, vectorizer = features.extract_tfidf(df['genres'])
        # Convert sparse matrix to dense for KMeans if needed, or keep sparse
        # KMeans handles sparse input
        kmeans, labels = model.train_clustering(X)
        score = model.evaluate_clustering(X, labels)
        logging.info(f"Clustering Score: {score}")
        df['cluster'] = labels
    else:
        score = 0
        logging.warning("Not enough features for clustering.")

    # 4. Visualization
    viz.plot_wordcloud(cleaned_text)
    viz.plot_wordcloud(cleaned_text)
    # viz.plot_bpm_stats(df) # Removed as we don't have audio features
    viz.plot_styles_by_country(df)
    # Mock latencies for technical plot
    viz.plot_technical_stats([0.1, 0.2, 0.15, 0.3, 0.12]) 
    
    viz.generate_dashboard(kpis, score)
    logging.info("Dashboard generated.")
    
    logging.info("Pipeline completed.")

if __name__ == "__main__":
    main()
