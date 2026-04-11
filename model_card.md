# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Response: This model suggests 5 songs from a small classroom catalog based on a listener's stated preferences. It is designed for learning how recommender systems map user preferences to item features.

This is intended for classroom use only. It does not have enough data, enough users, or enough nuance to model real musical taste.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Response: The recommender compares one user profile to one song at a time.

It rewards:

- exact matches on **genre** and **mood**
- close matches on **energy**, **tempo**, **valence**, **danceability**, and **acousticness**
- matching **mood tags** like `study`, `festival`, or `cozy`
- a close **release decade**
- a small **popularity** bonus

After scoring every song, the model sorts the catalog from highest score to lowest score. Then it applies a small diversity penalty if an artist or genre is already present in the top results.

The project also includes three ranking modes:

- `balanced`
- `genre_first`
- `energy_similarity`

These modes use the same structure but different weights.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset

Response: The dataset contains **20 songs** in `data/songs.csv`.

The original starter catalog had 10 songs. I expanded it with 10 more songs and added extra features so the recommender had more signal to work with.

Song attributes used:

- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness
- popularity
- release_decade
- instrumentalness
- liveness
- mood_tags

Genres in the catalog include pop, indie pop, lofi, rock, jazz, ambient, acoustic, synthwave, and edm. Even with that range, the catalog is still small and does not represent the full space of musical taste.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

Response: This system works best when the user profile is clear and the dataset already contains songs that fit that vibe.

Examples:

- The **Chill Study Lofi** profile strongly preferred `Focus Flow`, `Library Rain`, and `Sunday Sketchbook`, which matched my intuition.
- The **Festival EDM** profile correctly raised `Bassline Sprint` and `City Pulse Nova` because they matched energy, tempo, danceability, and tags.
- The explanation strings make the model easy to inspect. I can see *why* a song ranked high instead of just seeing a black-box result.

Another strength is transparency. Because the model is rule-based, it is easy to debug and easy to explain to a non-programmer.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Resonse: The model has several limitations.

First, the dataset is very small. If a user wants music outside the catalog, the system can only recommend the “closest wrong answer.”

Second, the labels are subjective. A song's mood or genre may be debatable, and those labels heavily influence the score.

Third, the popularity bonus introduces a mild popularity bias. Songs that are already marked as more popular get an extra edge.

Fourth, the hand-tuned weights reflect my judgment. If I overvalue genre, the system may ignore songs that match the mood and energy but sit in a different genre.

Fifth, the diversity penalty helps reduce repetition, but it is a shallow fairness tool. It does not solve deeper representation problems in the dataset.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Response: I evaluated the system by running it on four distinct profiles:

- High-Energy Pop
- Chill Study Lofi
- Festival EDM
- Acoustic Wind-Down

I looked at whether the top 5 results matched the intended vibe and whether the written reasons matched the score logic.

I also compared different ranking modes. For the Festival EDM profile, `energy_similarity` mode allowed very energetic non-EDM songs like **Gym Hero** and **Storm Runner** to move closer to the top. That showed the scoring strategy changes the personality of the recommender.

I also inspected the diversity behavior. In the Chill Study Lofi case, the penalty reduced repetition from the same artist and made the final list a bit broader.

The starter unit tests pass, and the CLI output remained stable after the dataset and logic changes.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Response: I would improve the system in the following ways:

1. Learn the weights from user feedback instead of hand-tuning them.
2. Add more songs and much richer features, especially lyric themes, vocals, and multilingual labels.
3. Track user history so the recommender can blend content-based filtering with collaborative filtering.
4. Improve diversity with a stronger reranking method instead of a fixed penalty.
5. Add a feedback loop where users can like, skip, or save recommendations.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Response: The most important learning moment was realizing that scoring and ranking are different jobs. The score explains one song at a time, but the ranking step decides what the user actually sees. That is where design choices like diversity penalties matter.

It is interesting to me that without training any ML model, weighted feature matching already produced recommendations that felt plausible. 

I think I would trust real-world systems less bilndly. Even small change in weights changes what looks relevant, which means human judgement still matters a lot in how these systems are built.