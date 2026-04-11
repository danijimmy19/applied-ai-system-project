import mermaid from 'mermaid';

mermaid.initialize({ startOnLoad: true, securityLevel: 'loose' });

export const recommenderFlowchart = `
flowchart TD
    A[User Profile Input<br/>genre, mood, energy, tempo, era] --> B[Load songs.csv]
    B --> C[Loop through each song]
    C --> D[score_song(user_prefs, song, mode)]
    M[Ranking Mode<br/>balanced / genre_first / energy_focus] --> D

    D --> E{Compare features}
    E --> E1[Genre match]
    E --> E2[Mood match]
    E --> E3[Energy similarity]
    E --> E4[Tempo similarity]
    E --> E5[Extra attributes<br/>danceability, acousticness, popularity, decade, valence]

    E1 --> F[Build total score]
    E2 --> F
    E3 --> F
    E4 --> F
    E5 --> F

    F --> G[Generate human-readable reasons]
    G --> H[Store song + score + reasons]
    H --> I[Sort all songs by score]
    I --> J[Apply diversity penalty / rerank]
    J --> K[Select top K recommendations]
    K --> L[Display formatted CLI table]
    L --> N[User sees titles, scores, and reasons]
`;

export async function renderRecommenderFlowchart(elementId = 'recommender-flowchart') {
  const element = document.getElementById(elementId);
  if (!element) {
    throw new Error(`No element found with id "${elementId}"`);
  }

  const { svg, bindFunctions } = await mermaid.render(
    'recommender-flowchart-svg',
    recommenderFlowchart,
  );

  element.innerHTML = svg;
  if (bindFunctions) bindFunctions(element);
}

// Optional auto-render in a browser page that contains:
// <div id="recommender-flowchart"></div>
if (typeof document !== 'undefined') {
  const target = document.getElementById('recommender-flowchart');
  if (target) {
    renderRecommenderFlowchart().catch(console.error);
  }
}