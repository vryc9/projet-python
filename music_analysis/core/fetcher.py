import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import logging
import time
from . import config

# Setup logging
logging.basicConfig(filename=config.LOGS_DIR / "marketing.log", level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SpotifyFetcher:
    def __init__(self):
        try:
            # Try using User Authentication (Authorization Code Flow) to bypass potential restrictions
            # on Client Credentials flow for audio-features.
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=config.SPOTIPY_CLIENT_ID,
                client_secret=config.SPOTIPY_CLIENT_SECRET,
                redirect_uri=config.SPOTIPY_REDIRECT_URI,
                scope="user-read-private"
            ))
            logging.info("Spotify client initialized successfully (User Auth).")
        except Exception as e:
            logging.error(f"Failed to initialize Spotify client: {e}")
            self.sp = None

    def get_tracks(self, query, limit=50):
        if not self.sp:
            logging.warning("Spotify client not available.")
            return []
        
        try:
            results = self.sp.search(q=query, limit=limit, type='track')
            tracks = results['tracks']['items']
            logging.info(f"Fetched {len(tracks)} tracks for query '{query}'.")
            return tracks
        except Exception as e:
            logging.error(f"Error fetching tracks: {e}")
            return []

    def get_artists(self, artist_ids):
        if not self.sp:
            return []
        try:
            artists = []
            for i in range(0, len(artist_ids), 50):
                batch = artist_ids[i:i+50]
                batch_artists = self.sp.artists(batch)
                if batch_artists and 'artists' in batch_artists:
                    artists.extend(batch_artists['artists'])
            logging.info(f"Fetched info for {len(artists)} artists.")
            return artists
        except Exception as e:
            logging.error(f"Error fetching artists: {e}")
            return []

    def get_top_tracks_by_country(self, country_code='US', limit=50):
        if not self.sp:
            return []
        try:
            # Search for top tracks in a specific market
            # Note: "year:2024" or similar could be added to query
            query = f"year:2024" 
            results = self.sp.search(q=query, limit=limit, type='track', market=country_code)
            tracks = results['tracks']['items']
            logging.info(f"Fetched {len(tracks)} top tracks for country {country_code}.")
            return tracks
        except Exception as e:
            logging.error(f"Error fetching top tracks for {country_code}: {e}")
            return []

class GeniusFetcher:
    def __init__(self):
        self.base_url = "https://api.genius.com"
        self.headers = {'Authorization': f'Bearer {config.GENIUS_ACCESS_TOKEN}'}

    def search_song(self, title, artist):
        if not config.GENIUS_ACCESS_TOKEN:
            logging.warning("Genius token not provided.")
            return None
        
        search_url = f"{self.base_url}/search"
        params = {'q': f"{title} {artist}"}
        try:
            response = requests.get(search_url, params=params, headers=self.headers)
            if response.status_code == 200:
                hits = response.json()['response']['hits']
                if hits:
                    return hits[0]['result'] # Return top hit
            return None
        except Exception as e:
            logging.error(f"Genius API error: {e}")
            return None

    # Note: Genius API returns a URL to the lyrics, not the lyrics themselves directly in the search.
    # We would need to scrape the page, but scraping might be out of scope or require BeautifulSoup.
    # For this project, we might just use the snippet or title/tags if lyrics are hard to get without scraping.
    # However, the subject mentions "Collecte des données via plusieurs APIs".
    # I will assume we can get some text data or use a library like `lyricsgenius` if allowed, but `requests` is specified.
    # I'll stick to requests and maybe just get metadata or try to find an API that gives lyrics.
    # Actually, the subject says "Nettoie/structure les contenus textuels".
    # I'll leave a placeholder for lyrics fetching.

class MusicBrainzFetcher:
    def __init__(self):
        self.base_url = "https://musicbrainz.org/ws/2"

    def get_artist_info(self, artist_name):
        url = f"{self.base_url}/artist"
        params = {'query': artist_name, 'fmt': 'json'}
        try:
            response = requests.get(url, params=params)
            time.sleep(1) # Rate limiting
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logging.error(f"MusicBrainz API error: {e}")
            return None
