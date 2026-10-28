# Project log

## Oct 13
- Starting hypothesis: Players struggle to find new, high-quality experiences
  because discovery surfaces favor games that are already popular.
- Set up folder, Anaconda, GitHub Desktop.

## Oct 16 — New-user walkthrough
Fresh account, incognito Chrome, US, computer.

| Surface | What it shows | Example games (rating, active) | Anything new (<6 months)? |
|---|---|---|---|
| Home – Recommended For You | Algorithm picks; first games shown are mostly new, very popular games | Steal An Egg: 91%, 1.3M active; Huss Valley: 88%, 95K active | both games came out this year; both updated frequently |
| Home – Standout Games | Staff picks; much smaller player counts than Recommended | Superstar Baseball: 92%, 1,115 active; Rise of Nations: 87%, 2,204 active | both games came out in 2018 and 2025; both updated this month |
| Charts – Top Trending | Games popular right now | Welcome to Bloxburg: 25.7K active; Vanguards: 2nd Anniversary: 66.9K active; Ragdoll Engine: 13.3K active | 2 of 4 in the row are new; all updated frequently |
| Charts – Up-and-Coming | Rising games, many already with large player counts | Chop A Forest: 54.8K active; First Person Boxing: 2.4K active; Ragdoll Engine: 13.3K active | 2 of 4 in the row are new; all updated frequently |
| Charts – Top Revisited | Games players come back to often | Vanguards: 2nd Anniversary: 66.9K active; [PATH 2 & MOBILE] Dragon: 4.5K active; Azure Latch: 11.7K active | 2 of 4 new; all updated frequently |
| Charts – Top Rated | Very highly rated games, many with small player counts | Jule's RNG: 98%, 231 active; Container RNG: 98%, 430 active; Missiles vs Cities: 98%, 1.1K active; Anime Dice: 99%, 53K active |  Most of them came out between (2024-2026) |
| Search ("tycoon") | Results for a genre keyword; top result is sponsored | WORLD TYCOON (sponsored): 90 active; Super Hero Tycoon: 792 active; Trading Tycoon: 4.2K active; Mansion Tycoon: 4.2K active |  2 of 4 are new (came out in 2026); all updated frequently |
| Game page recommendations | "You might also like" on Welcome to Bloxburg | Royale High: 9.7K active; Makeup Mania!: 11K active; Adopt Me!: 361.1K active | 1 of 3 new; mostly big established names |
| Friends | 0 friends → empty page, no suggestions | n/a | n/a |

Charts row order: Top Trending, Up-and-Coming, Top Playing Now, Fun with Friends,
Top Revisited, Top Earning, Top Paid Access, Top Rated, Most Popular.

### Observations
- **Home favors new hits.** "Recommended For You" showed mostly new games (created Jul–Aug 2026), but they were already very popular. Other surfaces showed a mix of new and old games.
- **Paid placement exists.** Searching "tycoon," the first result was a sponsored game (WORLD TYCOON, 90 active players).
- **Top Rated is dominated by small games.** Many had 98–99% ratings with only hundreds of players. Their high scores may partly come from having few votes, since small samples swing to extremes more easily.
- **Rows repeat the same games.** Vanguards appeared in Top Trending, Top Revisited, and Top Earning.
- **No social discovery for new users.** With 0 friends, the Friends page is empty and gives no suggestions.
- **Home recommendations changed between visits.** Cause unknown.

The best-rated small games I saw, like Jule’s RNG (98%, 231 players), only appeared in the Top Rated row, deep on the Charts page, not on Home.

### Revised hypothesis
I originally thought players struggle to find new, high-quality experiences because discovery surfaces favor games that are already popular. After looking at several surfaces, popularity isn't the only factor: sponsorship and ratings also shape what gets seen. My new hypothesis is that players struggle to find new, high-quality games because discovery is driven by popularity, paid placement, and ratings that can be unreliable for small games.



## Oct 18 — Data collection, pull 1
- First run failed: games details call returned 400 Bad Request when sending 100 IDs at once.
  Fixed by reducing batch size from 100 to 50.
- Second run succeeded but only got 5 of 9 main Charts rows (313 games).
  The Explore API returns rows in pages; added a page-token loop to get all of them.
- Moved the incomplete pull (20261018_2118) into data/raw/test/ so it isn't mixed into the analysis.
- Pull 1 complete (~5:19pm ET): 879 games across 26 rows.
- Found "Trending in ___" genre rows (RPG, Simulation, etc.), which can replace hand-tagging genres.
- Some rows aren't discovery rows (Music Top 100, Trending Music Experiences,
  More When You Subscribe, Learn & Explore).

## Oct 19 — Pulls 2 and 3
- Oct 19 10:44am — pull 2, 885 games, 26 sorts. Small change from pull 1 because rows refresh over time.
- Oct 19 10:15pm — pull 3, 886 games, 26 sorts.
- Data collection complete: 3 pulls at different times of day (Sun evening, Mon morning, Mon night).

## Oct 23 — Cleaning (Part 5)
- Combined 3 pulls: 2,650 rows → 942 unique games (some games appeared in only 1–2 pulls).
- Date parsing failed because Roblox timestamps mix formats (with and without milliseconds).
  Fixed with format="ISO8601".
- Roblox's genre field was "All" for 746 of 942 games (79%), so it can't be used.
- Labeled genres from the "Trending in ___" Charts rows instead. Games in more than one genre row
  got the one where they ranked highest. 497 games labeled, 445 unlabeled.
- Unlabeled games are much smaller (median ~342 players vs ~3,840 for labeled),
  so the genre analysis describes more popular games.

## Oct 25 — Analysis (Part 5) and hero chart (Part 6)
- Q1 Concentration: top 10 games hold 38% of players, top 100 hold 72%, Gini 0.81.
- Q2 Age: games under 6 months old hold 38.8% of players; 16 of the top 50 are new.
  This contradicts my starting hypothesis that discovery mainly favors old games.
- Q3 Genre: Simulation has the largest player share (30%). RPG has the highest median
  like ratio (0.944) but only 4.5% of players, a possible underserved genre.
- Q4 Hidden gems: 110 games have a top-25% like ratio but below-median players.
  Expected them to be mostly new; only 22% are. Most are good games that never grew.
- Q5 Placement: all 94 Up-and-Coming games are new, and 75 of 95 in Top Trending.
  New games sit lower within rows on average (41 vs ~35), but rows differ in length.
- Rating vs. players Spearman correlation = 0.16 (weak).
- Revised hypothesis: the gap isn't "new games are hidden," it's that quality doesn't
  reliably lead to players. Many highly rated games, new and old, stay small.
- Hero chart: "A game's rating barely predicts how many people play it."
  Zoomed x-axis to 0.60–1.00; 22 games rated below 0.60 not shown (noted in subtitle).

## Oct 26 — Problem definition (Part 7)
- Problem: players can't reliably find great games that haven't gone big. Discovery
  mostly follows popularity, so many of the highest-rated games stay small.
- Softened "games players would love most" to "highest-rated games," since ratings
  only reflect players who already found the game.
- Competitive scan: Steam, Fortnite, TikTok, YouTube.

## Oct 28 — Feature, experiment plan, proposal (Parts 7–9)
- Feature: personalized Discovery Queue on Home (inspired by Steam) with slots
  reserved for hidden gems; games that keep players move up ("test small, then scale").
- Experiment: randomized by user, 90/10 split, 2 weeks. Primary metric: % of users who
  play a new-to-them experience and return within 7 days.
- Sizing: 10% baseline, +1 pt minimum lift, α = 0.05, 80% power →
  ~8,200 treatment / ~73,700 control users. Guide's original "~15,000 per group"
  assumed a 50/50 split, which didn't match the 90/10 plan.
- Wrote one-page proposal and README.