"""Explainable item-based recommendations from explicit ratings."""
import json
import math
from pathlib import Path

def load_catalog(path=None):
    path = Path(path) if path else Path(__file__).with_name("catalog.json")
    return json.loads(path.read_text(encoding="utf-8"))

def recommend(user, ratings, catalog, limit=5):
    """Score unseen items via cosine similarity to items rated by user.

    Similarity is cosine over users who explicitly rated both items. Candidate
    score is the similarity-weighted average of this user's source ratings.
    Return entries include the normalized score and contributing similarities.
    """
    if user not in ratings:
        raise ValueError(f"unknown user: {user}")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError("limit must be a non-negative integer")
    items = {row["id"]: row for row in catalog}
    if len(items) != len(catalog):
        raise ValueError("catalog item IDs must be unique")
    for person, values in ratings.items():
        for item, value in values.items():
            if item not in items: raise ValueError(f"unknown item: {item}")
            if isinstance(value, bool) or not isinstance(value, (int,float)) or not 1 <= value <= 5:
                raise ValueError("ratings must be numbers from 1 to 5")
    own = ratings[user]
    scored = []
    for candidate in items.keys() - own.keys():
        numerator = denominator = 0.0
        evidence = []
        for source, rating in own.items():
            common = [(other[source], other[candidate]) for other_user, other in ratings.items() if other_user != user and source in other and candidate in other]
            dot = sum(a*b for a,b in common)
            norm_a = math.sqrt(sum(a*a for a,_ in common))
            norm_b = math.sqrt(sum(b*b for _,b in common))
            similarity = dot/(norm_a*norm_b) if norm_a and norm_b else 0.0
            if similarity > 0:
                numerator += similarity*rating; denominator += similarity
                evidence.append({"source_item": source, "similarity": similarity})
        if denominator:
            scored.append({"item": items[candidate], "score": numerator/denominator, "evidence": sorted(evidence,key=lambda x:x["source_item"])})
    return sorted(scored,key=lambda row:(-row["score"],row["item"]["id"]))[:limit]

def demo():
    catalog=load_catalog(); ratings=json.loads(Path(__file__).with_name("ratings.json").read_text(encoding="utf-8"))
    for row in recommend("ava", ratings, catalog):
        why=", ".join(f"{x['source_item']} similarity {x['similarity']:.2f}" for x in row["evidence"])
        print(f"{row['item']['title']} ? predicted rating {row['score']:.2f}; based on {why}")

if __name__ == "__main__": demo()
