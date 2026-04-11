from src.recommender import Song, UserProfile, Recommender

import pytest

from src.recommender import normalize_song_row, similarity_score, score_song
from src.recommender import recommend_songs, apply_diversity_rerank, song_to_dict, user_profile_to_dict

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


@pytest.fixture
def sample_user():
    return {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "likes_acoustic": False,
        "tempo_bpm": 120.0,
        "valence": 0.75,
        "danceability": 0.80,
        "preferred_decade": 2020,
        "desired_tags": ["uplifting", "party"],
        "ranking_mode": "balanced",
    }


@pytest.fixture
def sample_songs():
    return [
        {
            "id": 1,
            "title": "Neon Summer",
            "artist": "Starline",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.82,
            "tempo_bpm": 122.0,
            "valence": 0.78,
            "danceability": 0.84,
            "acousticness": 0.12,
            "popularity": 90,
            "release_decade": 2020,
            "instrumentalness": 0.0,
            "liveness": 0.15,
            "mood_tags": "uplifting;party",
        },
        {
            "id": 2,
            "title": "Midnight Echo",
            "artist": "Starline",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.79,
            "tempo_bpm": 118.0,
            "valence": 0.74,
            "danceability": 0.81,
            "acousticness": 0.10,
            "popularity": 88,
            "release_decade": 2020,
            "instrumentalness": 0.0,
            "liveness": 0.12,
            "mood_tags": "party",
        },
        {
            "id": 3,
            "title": "Forest Letters",
            "artist": "Pine House",
            "genre": "acoustic",
            "mood": "calm",
            "energy": 0.30,
            "tempo_bpm": 85.0,
            "valence": 0.45,
            "danceability": 0.35,
            "acousticness": 0.92,
            "popularity": 55,
            "release_decade": 2010,
            "instrumentalness": 0.10,
            "liveness": 0.08,
            "mood_tags": "soft;reflective",
        },
        {
            "id": 4,
            "title": "Voltage Rush",
            "artist": "Pulse FX",
            "genre": "edm",
            "mood": "energetic",
            "energy": 0.95,
            "tempo_bpm": 128.0,
            "valence": 0.70,
            "danceability": 0.90,
            "acousticness": 0.03,
            "popularity": 80,
            "release_decade": 2020,
            "instrumentalness": 0.0,
            "liveness": 0.20,
            "mood_tags": "party;euphoric",
        },
    ]


def test_normalize_song_row_converts_numeric_fields():
    row = {
        "id": "1",
        "title": "Test Song",
        "artist": "Tester",
        "genre": "pop",
        "mood": "happy",
        "energy": "0.8",
        "tempo_bpm": "120",
        "valence": "0.7",
        "danceability": "0.9",
        "acousticness": "0.1",
        "popularity": "85",
        "release_decade": "2020",
        "instrumentalness": "0.0",
        "liveness": "0.2",
        "mood_tags": "uplifting;party",
    }

    song = normalize_song_row(row)

    assert isinstance(song["id"], int)
    assert isinstance(song["energy"], float)
    assert isinstance(song["tempo_bpm"], float)
    assert isinstance(song["popularity"], int)
    assert song["title"] == "Test Song"


def test_similarity_score_exact_match_returns_full_weight():
    assert similarity_score(0.8, 0.8, max_gap=1.0, weight=2.0) == 2.0


def test_similarity_score_large_gap_returns_zero():
    assert similarity_score(0.0, 2.0, max_gap=1.0, weight=2.0) == 0.0


def test_score_song_returns_numeric_score_and_reasons(sample_user, sample_songs):
    score, reasons = score_song(sample_user, sample_songs[0])

    assert isinstance(score, float)
    assert score > 0
    assert isinstance(reasons, list)
    assert any("genre match" in r for r in reasons)
    assert any("mood match" in r for r in reasons)
    assert any("energy close" in r for r in reasons)


def test_score_song_better_match_scores_higher(sample_user, sample_songs):
    strong_match_score, _ = score_song(sample_user, sample_songs[0])
    weak_match_score, _ = score_song(sample_user, sample_songs[2])

    assert strong_match_score > weak_match_score


def test_ranking_mode_changes_score(sample_user, sample_songs):
    user_balanced = dict(sample_user)
    user_energy = dict(sample_user)
    user_energy["ranking_mode"] = "energy_similarity"

    balanced_score, _ = score_song(user_balanced, sample_songs[3])
    energy_score, _ = score_song(user_energy, sample_songs[3])

    assert balanced_score != energy_score


def test_recommend_songs_returns_k_results(sample_user, sample_songs):
    results = recommend_songs(sample_user, sample_songs, k=3)

    assert len(results) == 3
    assert all(len(item) == 3 for item in results)


def test_recommend_songs_returns_explanation_string(sample_user, sample_songs):
    results = recommend_songs(sample_user, sample_songs, k=2)

    song, score, explanation = results[0]
    assert isinstance(song, dict)
    assert isinstance(score, float)
    assert isinstance(explanation, str)
    assert len(explanation) > 0


def test_apply_diversity_rerank_penalizes_repeat_artist():
    scored = [
        ({"id": 1, "title": "A", "artist": "Same", "genre": "pop"}, 10.0, ["base"]),
        ({"id": 2, "title": "B", "artist": "Same", "genre": "pop"}, 9.8, ["base"]),
        ({"id": 3, "title": "C", "artist": "Other", "genre": "rock"}, 9.7, ["base"]),
    ]

    reranked = apply_diversity_rerank(scored, k=3)

    assert reranked[0][0]["id"] == 1
    assert reranked[1][0]["id"] == 3
    assert any("diversity penalty" in reason or "variety penalty" in reason for reason in reranked[2][2])


def test_song_and_userprofile_conversion_helpers():
    song = Song(
        id=1,
        title="Glow",
        artist="Nova",
        genre="pop",
        mood="happy",
        energy=0.8,
        tempo_bpm=120.0,
        valence=0.7,
        danceability=0.9,
        acousticness=0.1,
        popularity=80,
        release_decade=2020,
        instrumentalness=0.0,
        liveness=0.2,
        mood_tags="uplifting;party",
    )

    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_tempo=120.0,
        target_valence=0.7,
        target_danceability=0.9,
        preferred_decade=2020,
        desired_tags=["uplifting"],
        ranking_mode="balanced",
    )

    song_dict = song_to_dict(song)
    user_dict = user_profile_to_dict(user)

    assert song_dict["title"] == "Glow"
    assert user_dict["genre"] == "pop"
    assert user_dict["desired_tags"] == ["uplifting"]


def test_recommender_returns_song_objects(sample_songs):
    songs = [Song(**song) for song in sample_songs]
    recommender = Recommender(songs)
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_tempo=120.0,
        target_valence=0.75,
        target_danceability=0.8,
        preferred_decade=2020,
        desired_tags=["uplifting", "party"],
        ranking_mode="balanced",
    )

    recommendations = recommender.recommend(user, k=2)

    assert len(recommendations) == 2
    assert all(isinstance(song, Song) for song in recommendations)


def test_explain_recommendation_returns_readable_text(sample_songs):
    songs = [Song(**song) for song in sample_songs]
    recommender = Recommender(songs)
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
        target_tempo=120.0,
        target_valence=0.75,
        target_danceability=0.8,
        preferred_decade=2020,
        desired_tags=["uplifting", "party"],
        ranking_mode="balanced",
    )

    explanation = recommender.explain_recommendation(user, songs[0])

    assert isinstance(explanation, str)
    assert "genre match" in explanation or "mood match" in explanation