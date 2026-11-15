# 🔍 TheStatsWay - Ligas in Portugal Manager 🔍
 <br>
Ligas in Portugal Manager is a Football-Manager-style simulation game built with Streamlit. It covers one 2026/27 season of the Portuguese football pyramid (Liga Portugal, Liga 2 and Liga 3), with tactical depth, match preparation and in-game management.  
 <br>
 <br>
 
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://thestatsway-football-game-simulator-app.streamlit.app/)

 <br>
 
## 📋 Key Features & Description

# 1. Career Setup & Squad Management (Squad & Tactics)

 • Pick your division, then your club: start in any of the three divisions (Liga Portugal with 18 clubs, Liga 2 with 18, Liga 3 with 20) and manage any club in it.
  <br>
 • No transfers: you work exclusively with the roster your chosen club already has.
  <br>
 • Detailed player attributes: filter, search and analyse players by division, club, position and attributes (Goal-Scoring, Assist-Creation, Attack, Dribbling, Possession, Defense, Physical, Goalkeeping), with letter grades from S to F.
  <br>
 • Radar comparisons: compare two players side by side on an interactive radar chart.
  <br>
 • Interactive pitch and lineup: choose players for preset formations (4-3-3, 4-4-2, 4-2-3-1, 5-3-2 and more) or build your own shape, and assign individual roles (Attack, Balanced, Defensive).

# 2. Deep Tactical Engine (Tactics & Playing Philosophies)

 • Playing Philosophies: Choose a foundational Type of Play such as Gegenpress, Tiki-taka, Catenaccio, Counter-attack, or Balanced, each impacting team fatigue, card risks, and xG generation.
  <br>
 • Tactical Customization: Fine-tune mentalities, tempos, defensive lines, pressing intensity, passing styles (Short, Balanced, Direct), defensive stances, and attacking preferences (wing play vs. middle play).
  <br>
 • Squad Fit Calculator: The app dynamically calculates how well your squad's attributes match your selected tactical setup.   

# 3. Match Simulation & Scouting (Play Matchday)

 • Match engine: matches use an expected-goals (xG) model that takes into account player ratings, tactical matchups, home advantage, red cards and suspensions, substitutions and late-game fatigue.
  <br>
 • Realistic substitutions: at most 3 substitution moments per team. A centre-back is only replaced by a centre-back and never more than one leaves, and at most one substitute plays out of position.   
  <br>
 • Assistant manager: replaces suspended players and keeps your lineup valid while you simulate several matchdays. 
  <br>
 • Flexible simulation: play one matchday at a time, simulate to mid-season (to the end of the regular phase in Liga 3), or simulate the rest of the season.
  <br>
 • Pre-match scouting reports: before every fixture you get the opponent’s expected set-up, league position, form and earlier meetings.
  <br>
 • Match reports and commentary: text commentary, a timeline of goals, cards and substitutions, box-score stats and visual match reports.
  <br>

# 4. League Progress & Statistics (Table & Fixtures)

 • All three divisions run at the same time: each has its own live table, with colour-coded zones. 
  <br>
 • Liga 3 is played in two phases:  
 
####   The 1st phase has two series of 10 clubs, with 18 rounds.
####   In the 2nd phase the top 4 of each series play the Championship round (8 clubs, starting from 0 points).
####   The others play the Maintenance round (two groups of 6, with bonus points for their 1st-phase position).
####   The bottom 2 of each Maintenance group would go down to the Campeonato de Portugal, which is not in the game, so they stay in Liga 3.
 <br>
 • Promotion and relegation: 
 
####   The top 2 of Liga 2 and of the Liga 3 Championship round are promoted.
####   The bottom 2 of Liga Portugal and of Liga 2 are relegated.
####   The 3rd of Liga 2 plays the 16th of Liga Portugal, and the 3rd of the Liga 3 Championship round plays the 16th of Liga 2, in a two-legged play-off.
 <br>
 • B-team rule: B teams (Benfica B, Porto B, Sporting CP B, Vitória SC B) cannot be promoted to the division of their main club. The next club takes the place; with Benfica B champion of Liga 2, the 2nd and 3rd are promoted and the 4th plays the play-off.
  <br>
 • Player statistics and fixtures: top scorers, top assisters and average match ratings (filterable by division), plus a results matrix for each division.

# 5. Season Awards & Report Card (Season Awards)

 • Season-end summary: your finish, the champions, who was promoted and relegated, and the play-off results.
  <br>
 • Team of the Season: the best-performing XI of any division, based on ratings and appearances.
  <br>
 • Player accolades: Player of the Season, Top Scorer and Top Assister, per division.
  <br>
 • Shareable report card: one image with your final table (for Liga 3, your own Championship or Maintenance group), promotion or relegation badge, Team of the Season and your club’s starting XI, with built-in export and share options.
  <br>
 • Results log: each finished season is saved to a results database, including your club, position, tactics, matches and scorers.
