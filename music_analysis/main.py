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
        
        # Initialize other fetchers
        genius = fetcher.GeniusFetcher()
        mb = fetcher.MusicBrainzFetcher()
        
        # Cache for MusicBrainz to avoid redundant calls
        mb_cache = {}

        # Combine data
        data = []
        for i, track in enumerate(all_tracks):
            # Limit API calls to first 20 tracks to save time/quota during dev, or fetch all if needed
            # For this demo, we'll fetch for a subset to be fast
            
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            artist_id = track['artists'][0]['id']
            genres = artist_genres.get(artist_id, [])
            genre_str = ", ".join(genres) if genres else "unknown"
            
            # Genius Data
            genius_data = genius.search_song(track_name, artist_name) if i < 20 else None
            genius_url = genius_data.get('genius_url', '') if genius_data else ''
            
            # MusicBrainz Data
            if artist_name not in mb_cache:
                if i < 20: # Limit MB calls too
                    mb_cache[artist_name] = mb.get_artist_info(artist_name)
                else:
                    mb_cache[artist_name] = None
            
            mb_info = mb_cache.get(artist_name)
            mb_country = mb_info.get('mb_country', 'Unknown') if mb_info else 'Unknown'
            mb_tags = ", ".join(mb_info.get('mb_tags', [])) if mb_info else ''

            track_data = {
                'name': track_name,
                'artist': artist_name,
                'id': track['id'],
                'popularity': track['popularity'],
                'genres': genre_str,
                'genius_url': genius_url,
                'mb_country': mb_country,
                'mb_tags': mb_tags
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
    # Use collected text data (names, artists, genres, tags)
    text_parts = df['name'] + " " + df['artist'] + " " + df['genres']
    if 'mb_tags' in df.columns:
        text_parts = text_parts + " " + df['mb_tags']
        
    text_data = " ".join(text_parts.fillna(''))
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
    viz.plot_top_artists(df)
    viz.plot_genre_dist(df)
    viz.plot_popularity_dist(df)
    # Mock latencies for technical plot
    viz.plot_technical_stats([0.1, 0.2, 0.15, 0.3, 0.12]) 
    
    viz.generate_dashboard(kpis, score)
    logging.info("Dashboard generated.")
    
    logging.info("Pipeline completed.")

if __name__ == "__main__":
    main()
