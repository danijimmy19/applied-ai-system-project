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


def render_profile(name: str, prefs: dict, songs: list[dict]) -> None:
    """Print one recommendation table for one profile."""
    recommendations = recommend_songs(prefs, songs, k=5)
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append(
            [
                rank,
                song["title"],
                song["artist"],
                song["genre"],
                f"{score:.2f}",
                explanation,
            ]
        )

    print(f"\n{'=' * 100}")
    print(f"PROFILE: {name} | mode={prefs['ranking_mode']}")
    print(f"{'=' * 100}")
    print(
        tabulate(
            rows,
            headers=["#", "Title", "Artist", "Genre", "Score", "Why it ranked"],
            tablefmt="grid",
            maxcolwidths=[None, 18, 16, 12, None, 56],
        )
    )


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # recommendations = recommend_songs(user_prefs, songs, k=5)

    # print("\nTop recommendations:\n")
    # for rec in recommendations:
    #     # You decide the structure of each returned item.
    #     # A common pattern is: (song, score, explanation)
    #     song, score, explanation = rec
    #     print(f"{song['title']} - Score: {score:.2f}")
    #     print(f"Because: {explanation}")
    #     print()

    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(str(csv_path))

    print(f"Loaded songs: {len(songs)}")
    print("Ranking modes available: balanced, genre_first, energy_similarity")
    print("Diversity reranking is enabled to avoid too many repeats from one artist or genre.")

    for name, prefs in PROFILES.items():
        render_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
