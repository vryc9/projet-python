# Projet Marketing Data & IA

Ce projet implémente un pipeline complet de collecte, nettoyage, analyse et modélisation de données textuelles issues de divers API.

## Structure du Projet

```
/marketing_ai/
├─ main.py              # Orchestration du pipeline
├─ core/
│ ├─ config.py          # Configuration (URLs, clés, paramètres)
│ ├─ fetcher.py         # Collecte des données (APIs)
│ ├─ cleaner.py         # Nettoyage et normalisation du texte
│ ├─ analyzer.py        # Calcul des KPIs descriptifs
│ ├─ features.py        # Extraction de features (TF-IDF)
│ ├─ model.py           # Clustering K-Means
│ ├─ recommender.py     # Système de recommandation (contenu)
│ └─ viz.py             # Génération des figures et du rapport PDF
├─ data/                # Données brutes, traitées et modèles
├─ reports/             # Rapports générés (JSON, CSV, PDF)
├─ figs/                # Figures générées (PNG)
└─ logs/                # Fichiers de log
```

## Installation

1.  Cloner le dépôt.
2.  Créer un environnement virtuel :
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Exécution

Lancer le script principal :

```bash
python main.py
```

Le pipeline s'exécute automatiquement sans interaction.

## Choix Techniques & ML

- **APIs** : newsapi, devto, hackernews, reddit, arxiv, wikipedia
- **Nettoyage** : Minuscule, suppression ponctuation/HTML, stopwords (FR/EN).
- **Features** : TF-IDF (n-grams 1-2, max 100 features).
- **Machine Learning** : Clustering K-Means (k=3) pour segmenter les artistes.
- **Métriques** : Silhouette Score pour évaluer la qualité du clustering.

## Résultats

Les résultats sont disponibles dans le dossier `reports/` :

- `dashboard.pdf` : Rapport complet avec visualisations.
- `summary.json` : Statistiques globales.
- `keywords.csv` : Top mots-clés.&