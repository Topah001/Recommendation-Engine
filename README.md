# Recommendation Engine

A local, explainable recommendation demo using explicit 1?5 ratings and item-based cosine similarity. It considers co-ratings by other users, excludes items the target user has already rated, and displays the weighted predicted rating plus the source items and similarity weights. No network calls or external dependencies.

## Run

```powershell
python recommend.py
python -m unittest -v
```

Edit `catalog.json` and `ratings.json` for the sample data. Import `recommend(user, ratings, catalog, limit=5)` for your own in-memory data. Items with no positive co-rating evidence are omitted. Similarity is uncentered cosine over explicit co-ratings, so this compact educational baseline can favor popular items and is not a production personalization system.
