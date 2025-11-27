# core/config.py
import os

# --- API CREDENTIALS ---
LASTFM_API_KEY = "af8093c6179fe70451d808ddde036d3f"
SPOTIFY_CLIENT_ID = "db0463739a2c4feab2aca38c83a7952f"
SPOTIFY_CLIENT_SECRET = "b94f15f6154e48ad903ff1d3e1988200" 

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "data", "models")
FIGS_DIR = os.path.join(BASE_DIR, "figs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# --- ML PARAMS ---
RANDOM_SEED = 42
N_CLUSTERS = 3  # Pour le clustering (ex: Pop, Rock, Indie)
TOP_K_KEYWORDS = 10