"""
Roblox discovery project - data pull
Pulls the experiences Roblox shows on its Charts/Explore page, then enriches
each one with live stats (players, visits, genre, dates) and like/dislike votes.

Run it 3+ times at different times of day (e.g. Fri night, Sat afternoon,
Sun morning). Each run saves a timestamped CSV in data/raw/.

NOTE: the explore-api endpoints are undocumented and can change. If a call
fails, print the response and adjust the field names - that debugging is
normal and worth a line in your project log.
"""
import os
import time
import uuid
from datetime import datetime, timezone

import pandas as pd
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (student data project)"}
SESSION_ID = str(uuid.uuid4())
OUT_DIR = "data/raw"
os.makedirs(OUT_DIR, exist_ok=True)


def get(url, params=None):
    """GET with a polite pause and a simple retry on rate limits."""
    for attempt in range(4):
        r = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if r.status_code == 429:  # rate limited
            time.sleep(5 * (attempt + 1))
            continue
        r.raise_for_status()
        time.sleep(0.5)
        return r.json()
    raise RuntimeError(f"Gave up on {url}")


# ---- Step 1: which sorts (rows) does the Charts page show? ----
def get_sorts():
    data = get(
        "https://apis.roblox.com/explore-api/v1/get-sorts",
        params={"sessionId": SESSION_ID, "device": "computer", "country": "all"},
    )
    sorts = data.get("sorts", [])
    for s in sorts:
        print(s.get("sortId"), "|", s.get("sortDisplayName"))
    return sorts


# ---- Step 2: the experiences inside each sort ----
def get_sort_content(sort_id):
    data = get(
        "https://apis.roblox.com/explore-api/v1/get-sort-content",
        params={"sessionId": SESSION_ID, "sortId": sort_id,
                "device": "computer", "country": "all"},
    )
    return data.get("games", [])


# ---- Step 3: enrich with details + votes (100 ids per call) ----
def chunks(lst, n=100):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_details(universe_ids):
    rows = []
    for batch in chunks(universe_ids):
        ids = ",".join(map(str, batch))
        rows += get("https://games.roblox.com/v1/games",
                    params={"universeIds": ids}).get("data", [])
    return pd.DataFrame(rows)


def get_votes(universe_ids):
    rows = []
    for batch in chunks(universe_ids):
        ids = ",".join(map(str, batch))
        rows += get("https://games.roblox.com/v1/games/votes",
                    params={"universeIds": ids}).get("data", [])
    return pd.DataFrame(rows)


def main():
    pulled_at = datetime.now(timezone.utc)
    sorts = get_sorts()

    # Keep track of WHICH row each game appeared in and at what position.
    # This is your discovery data: where Roblox chooses to put games.
    placements = []
    for s in sorts:
        sort_id = s.get("sortId")
        if not sort_id:
            continue
        try:
            games = get_sort_content(sort_id)
        except Exception as e:
            print("skip", sort_id, e)
            continue
        for pos, g in enumerate(games, start=1):
            placements.append({
                "universe_id": g.get("universeId"),
                "sort_id": sort_id,
                "sort_name": s.get("sortDisplayName"),
                "position": pos,
            })

    placements = pd.DataFrame(placements).dropna(subset=["universe_id"])
    placements["universe_id"] = placements["universe_id"].astype(int)
    ids = placements["universe_id"].unique().tolist()
    print(f"{len(ids)} unique experiences across {placements.sort_id.nunique()} sorts")

    details = get_details(ids)
    votes = get_votes(ids)

    keep = ["id", "rootPlaceId", "name", "genre", "playing", "visits",
            "favoritedCount", "maxPlayers", "created", "updated"]
    details = details[[c for c in keep if c in details.columns]]
    details = details.rename(columns={"id": "universe_id"})
    votes = votes.rename(columns={"id": "universe_id"})

    games = details.merge(votes, on="universe_id", how="left")
    games["pulled_at_utc"] = pulled_at.isoformat()

    stamp = pulled_at.strftime("%Y%m%d_%H%M")
    games.to_csv(f"{OUT_DIR}/games_{stamp}.csv", index=False)
    placements.to_csv(f"{OUT_DIR}/placements_{stamp}.csv", index=False)
    print("saved", stamp)


if __name__ == "__main__":
    main()
