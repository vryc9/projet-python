import requests
import json
import time
import logging
import base64
from core.config import *

logger = logging.getLogger("marketing_ai")

class Fetcher:
    def __init__(self):
        self.spotify_token = self._get_spotify_token()

    def _get_spotify_token(self):
        if not SPOTIFY_CLIENT_SECRET:
            logger.warning("Spotify Secret manquant. Spotify sera ignoré.")
            return None
        
        auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        
        try:
            url = "https://accounts.spotify.com/api/token"
            headers = {"Authorization": f"Basic {b64_auth}"}
            data = {"grant_type": "client_credentials"}
            response = requests.post(url, headers=headers, data=data)
            return response.json().get("access_token")
        except Exception as e:
            logger.error(f"Erreur Auth Spotify: {e}")
            return None

    def fetch_deezer_artists(self):
        """Récupère le top artistes Deezer"""
        url = "https://api.deezer.com/chart/0/artists"
        start = time.time()
        try:
            resp = requests.get(url)
            latency = time.time() - start
            if resp.status_code == 200:
                data = resp.json().get('data', [])
                return {"source": "deezer", "latency": latency, "status": 200, "data": data}
            return {"source": "deezer", "latency": latency, "status": resp.status_code, "data": []}
        except Exception as e:
            logger.error(f"Deezer Error: {e}")
            return None

    def fetch_lastfm_artists(self):
        """Récupère le top artistes LastFM + Bio simplifiée"""
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "chart.gettopartists",
            "api_key": LASTFM_API_KEY,
            "format": "json",
            "limit": 50
        }
        start = time.time()
        try:
            resp = requests.get(url, params=params)
            latency = time.time() - start
            if resp.status_code == 200:
                artists = resp.json().get('artists', {}).get('artist', [])
                # Pour chaque artiste, on essaie de choper plus de détails (simulé ici pour performance)
                return {"source": "lastfm", "latency": latency, "status": 200, "data": artists}
            return {"source": "lastfm", "latency": latency, "status": resp.status_code, "data": []}
        except Exception as e:
            logger.error(f"LastFM Error: {e}")
            return None

    def run(self):
        results = []
        logger.info("Début de la collecte...")
        
        # 1. Deezer
        dz = self.fetch_deezer_artists()
        if dz: results.append(dz)
        
        # 2. LastFM
        lfm = self.fetch_lastfm_artists()
        if lfm: results.append(lfm)

        # 3. Spotify (Si token dispo) - Recherche "Top Hits" pour avoir des artistes
        if self.spotify_token:
            start = time.time()
            url = "https://api.spotify.com/v1/search?q=year:2024&type=artist&limit=20"
            headers = {"Authorization": f"Bearer {self.spotify_token}"}
            resp = requests.get(url, headers=headers)
            latency = time.time() - start
            if resp.status_code == 200:
                data = resp.json().get('artists', {}).get('items', [])
                results.append({"source": "spotify", "latency": latency, "status": 200, "data": data})
            else:
                results.append({"source": "spotify", "latency": latency, "status": resp.status_code, "data": []})

        # Sauvegarde Raw
        timestamp = int(time.time())
        with open(os.path.join(DATA_RAW, f"dump_{timestamp}.json"), 'w') as f:
            json.dump(results, f, indent=4)
        
        return results