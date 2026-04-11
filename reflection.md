# Reflection Notes

## Profile-to-Profile Comparisons

### High-Energy Pop vs Chill Study Lofi

These two profiles produced almost opposite outputs. The pop profile prioritized high valence, danceability, and upbeat tags like `bright`, `dance`, and `party`, so pop and EDM songs dominated. The lofi profile wanted low energy, calmer tempo, higher acousticness, and study-style tags, so the recommendations shifted toward `Focus Flow`, `Library Rain`, and `Sunday Sketchbook`.

### Chill Study Lofi vs Festival EDM

The lofi profile rewarded closeness to slow tempo and soft energy, while the EDM profile rewarded the fastest and most intense tracks. That is why songs like `Bassline Sprint` and `City Pulse Nova` climbed to the top for EDM, but almost disappeared for the study profile. This difference makes sense because the target “vibe” is fundamentally different.

### Festival EDM vs Acoustic Wind-Down

The EDM profile looked for festival, workout, and euphoric energy. The acoustic profile wanted relaxed mood, low energy, acousticness, and cozy tags. As a result, `Campfire Letters` became the clear winner for the acoustic listener, while it would never be a top match for the festival listener.

### High-Energy Pop vs Acoustic Wind-Down

High-Energy Pop and Acoustic Wind-Down profiles can like positive songs, but they disagree on intensity. The pop profile wants songs that feel active and danceable, while the acoustic profile wants songs that feel calm and intimate. That is why `Paper Planes Parade` ranks very high for pop, but `Campfire Letters` wins for the wind-down profile.

## Biggest Learning Moment

My biggest learning moment was seeing how strongly the output depends on the scoring recipe. A recommender can look smart, but a lot of its behavior comes from small human choices like “How much should genre matter?” or “Should popularity get any bonus at all?”

## How AI Tools Helped

AI tools are useful for brainstorming structure, generating extra dataset rows, and checking whether the code is readable. But the weights and explanations still needed to be verified manually. It would have been easy to accept a scoring rule that sounded reasonable but did not actually reflect the intended vibe.

## What Surprised Me

I was interesting that a simple weighted system can already produce recommendations that feel believable. It made the project feel more realistic, but it also showed how easy it is to accidentally build bias into a recommender when the dataset is small or uneven.

## What I Would Try Next

I would try a hybrid version next: keep the explainable content-based score, but also add lightweight feedback like likes, skips, and repeat plays. That would move the project closer to how real streaming systems personalize recommendations.
