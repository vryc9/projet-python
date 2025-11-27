import os

# --- Clés API ---
# Idéalement, ces clés devraient être dans des variables d'environnement
LASTFM_API_KEY = "af8093c6179fe70451d808ddde036d3f"
SPOTIFY_CLIENT_ID = "db0463739a2c4feab2aca38c83a7952f"
SPOTIFY_CLIENT_SECRET = "b94f15f6154e48ad903ff1d3e1988200"

# --- URLs API ---
URL_DEEZER_CHART = "https://api.deezer.com/chart/0/artists"
URL_LASTFM_API = "http://ws.audioscrobbler.com/2.0/"
URL_SPOTIFY_TOKEN = "https://accounts.spotify.com/api/token"
URL_SPOTIFY_SEARCH = "https://api.spotify.com/v1/search"

# --- Chemins de fichiers ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "data", "models")
FIGS_DIR = os.path.join(BASE_DIR, "figs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# --- Paramètres ML ---
RANDOM_SEED = 42
N_CLUSTERS = 3
TOP_K_KEYWORDS = 10
TEST_SIZE = 0.2  # Pour la classification si utilisée

# --- Stopwords (FR/EN) ---
STOPWORDS = {
    # English
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "it", "that", "for", "on", "with", "as", "by", "at", 
    "this", "be", "are", "from", "not", "but", "what", "all", "were", "we", "when", "your", "can", "said", "there",
    "use", "an", "each", "which", "she", "do", "how", "their", "if", "will", "up", "other", "about", "out", "many",
    "then", "them", "these", "so", "some", "her", "would", "make", "like", "him", "into", "time", "has", "look",
    "two", "more", "write", "go", "see", "number", "no", "way", "could", "people", "my", "than", "first", "water",
    "been", "call", "who", "oil", "its", "now", "find",
    # French
    "le", "la", "les", "de", "des", "du", "et", "ou", "est", "sont", "en", "dans", "par", "pour", "sur", "avec",
    "un", "une", "ce", "ces", "cette", "qui", "que", "quoi", "dont", "où", "mais", "donc", "or", "ni", "car",
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "mon", "ton", "son", "notre", "votre", "leur",
    "mes", "tes", "ses", "nos", "vos", "leurs", "aux", "au", "à", "se", "sa", "ça", "ne", "pas", "plus", "moins",
    "être", "avoir", "faire", "tout", "tous", "toute", "toutes", "autre", "autres", "comme", "si"
}