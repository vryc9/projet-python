import os

NEWS_API_KEY = "V3cada7b20d3849c3a2497fd0cc3caaf3" 

URLS = {
    "newsapi": f"https://newsapi.org/v2/everything?q=artificial+intelligence&language=en&pageSize=20&apiKey={NEWS_API_KEY}",
    "devto": "https://dev.to/api/articles?tag=ai&top=20",
    "hackernews": "https://hacker-news.firebaseio.com/v0/topstories.json", 
    "reddit": "https://www.reddit.com/r/MachineLearning/top.json?limit=20&t=week",
    "arxiv": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=20",
    "wikipedia": "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Machine%20Learning&format=json"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGS_DIR = os.path.join(BASE_DIR, "figs")

DATA_RAW = os.path.join(BASE_DIR, "data", "raw", "data.json")
DATA_CLEAN = os.path.join(BASE_DIR, "data", "processed", "clean_data.json")

MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "model.pkl")
VECT_PATH = os.path.join(BASE_DIR, "data", "models", "vectorizer.pkl")

LOG_FILE = os.path.join(BASE_DIR, "logs", "marketing.log")

SEED = 42
N_CLUSTERS = 4