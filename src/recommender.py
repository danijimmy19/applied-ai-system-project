from typing import List, Dict, Tuple, Optional, Iterable
from dataclasses import dataclass
import csv
from pathlib import Path

NUMERIC_FLOAT_FIELDS = {
    "energy",
    "tempo_bpm",
    "valence",
    "danceability",
    "acousticness",
    "instrumentalness",
    "liveness",
}
NUMERIC_INT_FIELDS = {"id", "popularity", "release_decade"}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2020
    instrumentalness: float = 0.0
    liveness: float = 0.1
    mood_tags: str = ""

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo: float = 110.0
    target_valence: float = 0.65
    target_danceability: float = 0.65
    preferred_decade: Optional[int] = None
    desired_tags: Optional[List[str]] = None
    ranking_mode: str = "balanced"

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        user_prefs = user_profile_to_dict(user)
        ranked = recommend_songs(user_prefs, [song_to_dict(song) for song in self.songs], k=k)
        top_ids = [item[0]["id"] for item in ranked]
        songs_by_id = {song.id: song for song in self.songs}
        return [songs_by_id[song_id] for song_id in top_ids]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        _, reasons = score_song(user_profile_to_dict(user), song_to_dict(song), mode=user.ranking_mode)
        return "; ".join(reasons)

def resolve_path(csv_path: str) -> Path:
    """Resolve a CSV path from either the repo root or an absolute path."""
    path = Path(csv_path)
    if path.is_absolute() and path.exists():
        return path
    project_root = Path(__file__).resolve().parents[1]
    candidate = project_root / csv_path
    if candidate.exists():
        return candidate
    if path.exists():
        return path.resolve()
    raise FileNotFoundError(f"Could not find CSV file: {csv_path}")


def normalize_song_row(row: Dict[str, str]) -> Dict:
    """Convert CSV strings into a typed song dictionary."""
    song: Dict[str, object] = {}
    for key, value in row.items():
        if key in NUMERIC_INT_FIELDS:
            song[key] = int(float(value))
        elif key in NUMERIC_FLOAT_FIELDS:
            song[key] = float(value)
        else:
            song[key] = value.strip()
    return song


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    resolved = resolve_path(csv_path)
    songs: List[Dict] = []
    with resolved.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            songs.append(normalize_song_row(row))
    return songs

def song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass into a dictionary."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
        "popularity": song.popularity,
        "release_decade": song.release_decade,
        "instrumentalness": song.instrumentalness,
        "liveness": song.liveness,
        "mood_tags": song.mood_tags,
    }


def user_profile_to_dict(user: UserProfile) -> Dict:
    """Convert a UserProfile dataclass into the functional preference format."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
        "tempo_bpm": user.target_tempo,
        "valence": user.target_valence,
        "danceability": user.target_danceability,
        "preferred_decade": user.preferred_decade,
        "desired_tags": user.desired_tags or [],
        "ranking_mode": user.ranking_mode,
    }

def similarity_score(target: Optional[float], value: Optional[float], max_gap: float, weight: float) -> float:
    """Reward closeness between a target value and a song value."""
    if target is None or value is None:
        return 0.0
    gap = abs(float(target) - float(value))
    closeness = max(0.0, 1 - (gap / max_gap))
    return round(closeness * weight, 4)


def get_mode_weights(mode: str) -> Dict[str, float]:
    """Return a weight dictionary for the selected ranking mode."""
    presets = {
        "balanced": {
            "genre": 2.5,
            "mood": 2.0,
            "energy": 2.0,
            "tempo": 1.2,
            "valence": 1.1,
            "danceability": 1.0,
            "acoustic": 0.9,
            "tags": 1.5,
            "decade": 0.8,
            "popularity": 0.5,
        },
        "genre_first": {
            "genre": 3.5,
            "mood": 1.6,
            "energy": 1.5,
            "tempo": 0.8,
            "valence": 0.8,
            "danceability": 0.8,
            "acoustic": 0.7,
            "tags": 1.2,
            "decade": 0.6,
            "popularity": 0.4,
        },
        "energy_similarity": {
            "genre": 1.6,
            "mood": 1.4,
            "energy": 3.0,
            "tempo": 1.7,
            "valence": 0.9,
            "danceability": 1.1,
            "acoustic": 0.7,
            "tags": 1.0,
            "decade": 0.5,
            "popularity": 0.4,
        },
    }
    return presets.get(mode, presets["balanced"])

def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score one song against one user profile and return reasons."""
    weights = get_mode_weights(user_prefs.get("ranking_mode", mode))
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("genre"):
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    if song.get("mood") == user_prefs.get("mood"):
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    energy_points = similarity_score(user_prefs.get("energy"), song.get("energy"), 1.0, weights["energy"])
    if energy_points:
        score += energy_points
        reasons.append(f"energy close (+{energy_points:.2f})")

    tempo_points = similarity_score(user_prefs.get("tempo_bpm"), song.get("tempo_bpm"), 100.0, weights["tempo"])
    if tempo_points:
        score += tempo_points
        reasons.append(f"tempo close (+{tempo_points:.2f})")

    valence_points = similarity_score(user_prefs.get("valence"), song.get("valence"), 1.0, weights["valence"])
    if valence_points:
        score += valence_points
        reasons.append(f"valence close (+{valence_points:.2f})")

    dance_points = similarity_score(user_prefs.get("danceability"), song.get("danceability"), 1.0, weights["danceability"])
    if dance_points:
        score += dance_points
        reasons.append(f"danceability close (+{dance_points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    acoustic_pref = 0.85 if likes_acoustic else 0.15
    acoustic_points = similarity_score(acoustic_pref, song.get("acousticness"), 1.0, weights["acoustic"])
    if acoustic_points:
        score += acoustic_points
        reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    desired_tags = {tag.lower() for tag in user_prefs.get("desired_tags", [])}
    song_tags = {tag.strip().lower() for tag in str(song.get("mood_tags", "")).split(";") if tag.strip()}
    overlap = desired_tags & song_tags
    if overlap:
        tag_points = min(weights["tags"], 0.75 * len(overlap))
        score += tag_points
        reasons.append(f"matching tags {', '.join(sorted(overlap))} (+{tag_points:.2f})")

    preferred_decade = user_prefs.get("preferred_decade")
    if preferred_decade is not None:
        decade_gap = abs(int(preferred_decade) - int(song.get("release_decade", preferred_decade)))
        decade_points = max(0.0, weights["decade"] - (decade_gap / 20.0) * weights["decade"])
        if decade_points:
            score += decade_points
            reasons.append(f"era close (+{decade_points:.2f})")

    popularity = float(song.get("popularity", 50)) / 100.0
    popularity_points = popularity * weights["popularity"]
    score += popularity_points
    reasons.append(f"catalog popularity (+{popularity_points:.2f})")

    return round(score, 4), reasons


def apply_diversity_rerank(scored_songs: Iterable[Tuple[Dict, float, List[str]]], k: int) -> List[Tuple[Dict, float, List[str]]]:
    """Greedily rerank songs to reduce repetition by artist and genre."""
    remaining = list(scored_songs)
    selected: List[Tuple[Dict, float, List[str]]] = []
    chosen_artists = set()
    chosen_genres = set()

    while remaining and len(selected) < k:
        best_index = 0
        best_adjusted = None
        best_penalties: List[str] = []

        for idx, (song, base_score, reasons) in enumerate(remaining):
            adjusted = base_score
            penalties: List[str] = []
            if song["artist"] in chosen_artists:
                adjusted -= 0.85
                penalties.append("artist diversity penalty (-0.85)")
            if song["genre"] in chosen_genres:
                adjusted -= 0.30
                penalties.append("genre variety penalty (-0.30)")
            if best_adjusted is None or adjusted > best_adjusted:
                best_adjusted = adjusted
                best_index = idx
                best_penalties = penalties

        song, base_score, reasons = remaining.pop(best_index)
        combined_reasons = reasons + best_penalties if best_penalties else reasons
        selected.append((song, round(best_adjusted or base_score, 4), combined_reasons))
        chosen_artists.add(song["artist"])
        chosen_genres.add(song["genre"])

    return selected


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort the catalog, and return the top-k songs with explanations."""
    scored: List[Tuple[Dict, float, List[str]]] = []
    mode = user_prefs.get("ranking_mode", "balanced")

    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        scored.append((song, score, reasons))

    scored.sort(key=lambda item: item[1], reverse=True)
    reranked = apply_diversity_rerank(scored, k=k)

    results: List[Tuple[Dict, float, str]] = []
    for song, score, reasons in reranked:
        explanation = "; ".join(reasons)
        results.append((song, score, explanation))
    return results
