import requests
import json
import time
import logging
import base64
import os
from core.config import (
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, LASTFM_API_KEY,
    URL_DEEZER_CHART, URL_LASTFM_API, URL_SPOTIFY_TOKEN, URL_SPOTIFY_SEARCH,
    DATA_RAW
)

logger = logging.getLogger("marketing_ai")

class Fetcher:
    """
    Classe responsable de la collecte de données depuis plusieurs APIs publiques.
    Gère l'authentification (Spotify) et la récupération des données brutes.
    """

    def __init__(self):
        """Initialise le fetcher et récupère le token Spotify."""
        self.spotify_token = self._get_spotify_token()

    def _get_spotify_token(self):
        """
        Authentification Client Credentials flow pour Spotify.
        Retourne le token d'accès ou None en cas d'erreur.
        """
        if not SPOTIFY_CLIENT_SECRET or not SPOTIFY_CLIENT_ID:
            logger.warning("Identifiants Spotify manquants. L'API Spotify sera ignorée.")
            return None
        
        auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        
        try:
            headers = {"Authorization": f"Basic {b64_auth}"}
            data = {"grant_type": "client_credentials"}
            response = requests.post(URL_SPOTIFY_TOKEN, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            return response.json().get("access_token")
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification Spotify: {e}")
            return None

    def fetch_deezer_artists(self):
        """
        Récupère le top artistes depuis l'API Deezer.
        Retourne un dictionnaire contenant la source, la latence, le statut et les données.
        """
        start = time.time()
        try:
            resp = requests.get(URL_DEEZER_CHART, timeout=10)
            latency = time.time() - start
            status = resp.status_code
            
            if status == 200:
                data = resp.json().get('data', [])
                return {"source": "deezer", "latency": latency, "status": status, "data": data}
            
            logger.warning(f"Deezer API a retourné le statut {status}")
            return {"source": "deezer", "latency": latency, "status": status, "data": []}
            
        except Exception as e:
            logger.error(f"Erreur Deezer: {e}")
            return {"source": "deezer", "latency": time.time() - start, "status": 0, "data": []}

    def fetch_lastfm_artists(self):
        """
        Récupère le top artistes depuis l'API LastFM.
        Retourne un dictionnaire standardisé.
        """
        params = {
            "method": "chart.gettopartists",
            "api_key": LASTFM_API_KEY,
            "format": "json",
            "limit": 50
        }
        start = time.time()
        try:
            resp = requests.get(URL_LASTFM_API, params=params, timeout=10)
            latency = time.time() - start
            status = resp.status_code
            
            if status == 200:
                artists = resp.json().get('artists', {}).get('artist', [])
                return {"source": "lastfm", "latency": latency, "status": status, "data": artists}
            
            logger.warning(f"LastFM API a retourné le statut {status}")
            return {"source": "lastfm", "latency": latency, "status": status, "data": []}
            
        except Exception as e:
            logger.error(f"Erreur LastFM: {e}")
            return {"source": "lastfm", "latency": time.time() - start, "status": 0, "data": []}

    def fetch_spotify_artists(self):
        """
        Récupère des artistes depuis l'API Spotify (recherche 'year:2024').
        Retourne un dictionnaire standardisé.
        """
        if not self.spotify_token:
            return None

        start = time.time()
        try:
            headers = {"Authorization": f"Bearer {self.spotify_token}"}
            params = {"q": "year:2024", "type": "artist", "limit": 20}
            resp = requests.get(URL_SPOTIFY_SEARCH, headers=headers, params=params, timeout=10)
            latency = time.time() - start
            status = resp.status_code
            
            if status == 200:
                data = resp.json().get('artists', {}).get('items', [])
                return {"source": "spotify", "latency": latency, "status": status, "data": data}
            
            logger.warning(f"Spotify API a retourné le statut {status}")
            return {"source": "spotify", "latency": latency, "status": status, "data": []}
            
        except Exception as e:
            logger.error(f"Erreur Spotify: {e}")
            return {"source": "spotify", "latency": time.time() - start, "status": 0, "data": []}

    def run(self):
        """
        Exécute la collecte sur toutes les sources configurées.
        Sauvegarde les données brutes dans un fichier JSON timestampé.
        """
        results = []
        logger.info("Début de la collecte des données...")
        
        # Collecte séquentielle
        sources = [
            self.fetch_deezer_artists,
            self.fetch_lastfm_artists,
            self.fetch_spotify_artists
        ]
        
        for fetch_func in sources:
            res = fetch_func()
            if res:
                results.append(res)
        
        # Sauvegarde des données brutes
        timestamp = int(time.time())
        dump_path = os.path.join(DATA_RAW, f"dump_{timestamp}.json")
        try:
            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            logger.info(f"Données brutes sauvegardées dans {dump_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des données brutes: {e}")
            
        return results