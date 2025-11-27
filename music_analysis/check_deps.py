import sys
import importlib

packages = [
    'requests',
    'spotipy',
    'dotenv', # python-dotenv
    'pandas',
    'numpy',
    'sklearn',
    'matplotlib',
    'seaborn',
    'wordcloud',
    'fpdf'
]

missing = []
for pkg in packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    print(f"Missing packages: {', '.join(missing)}")
    sys.exit(1)
else:
    print("All packages installed.")
    sys.exit(0)
