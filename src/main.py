"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from pathlib import Path
from tabulate import tabulate
from src.recommender import load_songs, recommend_songs

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "tempo_bpm": 126,
        "valence": 0.82,
        "danceability": 0.84,
        "likes_acoustic": False,
        "preferred_decade": 2020,
        "desired_tags": ["dance", "bright", "party"],
        "ranking_mode": "balanced",
    },
    "Chill Study Lofi": {
        "genre": "lofi",
        "mood": "focused",
        "energy": 0.35,
        "tempo_bpm": 78,
        "valence": 0.58,
        "danceability": 0.55,
        "likes_acoustic": True,
        "preferred_decade": 2020,
        "desired_tags": ["study", "coding", "calm"],
        "ranking_mode": "genre_first",
    },
    "Festival EDM": {
        "genre": "edm",
        "mood": "intense",
        "energy": 0.95,
        "tempo_bpm": 138,
        "valence": 0.76,
        "danceability": 0.90,
        "likes_acoustic": False,
        "preferred_decade": 2020,
        "desired_tags": ["festival", "workout", "euphoric"],
        "ranking_mode": "energy_similarity",
    },
    "Acoustic Wind-Down": {
        "genre": "acoustic",
        "mood": "relaxed",
        "energy": 0.28,
        "tempo_bpm": 86,
        "valence": 0.70,
        "danceability": 0.40,
        "likes_acoustic": True,
        "preferred_decade": 2000,
        "desired_tags": ["cozy", "acoustic", "storytelling"],
        "ranking_mode": "balanced",
    },
}

def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
