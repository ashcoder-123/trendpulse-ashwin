import requests
import time
import json
import os
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {
    "User-Agent": "TrendPulse/1.0"
}
# Fetch the top 500 trending story IDs from HackerNews
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    response.raise_for_status()

    story_ids = response.json()[:500]

    print(f"Fetched {len(story_ids)} story IDs.")

except requests.RequestException as e:
    print(f"Failed to fetch top stories: {e}")

# Keywords used to classify stories into the five categories
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Track how many stories have been collected for each category
category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

stories = []
# Store valid story details fetched from the API
fetched_stories = []

# Fetch the details of each story using its ID
for story_id in story_ids:
    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            headers=headers
        )
        response.raise_for_status()

        story = response.json()

        if not story or "title" not in story:
            continue

        fetched_stories.append(story)

    except requests.RequestException as e:
        print(f"Failed to fetch story {story_id}: {e}")
        continue

# Collect up to 25 stories for each category
for category, keywords in categories.items():
    for story in fetched_stories:
        if category_counts[category] >= 25:
            break

        title = story["title"].lower()

        # Check whether the story title contains any keyword for this category
        if not any(keyword.lower() in title for keyword in keywords):
            continue

        # Store only the fields required for the project
        collected_story = {
            "post_id": story["id"],
            "title": story["title"],
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "Unknown"),
            "collected_at": datetime.now().isoformat()
        }

        stories.append(collected_story)
        category_counts[category] += 1

    # Wait 2 seconds before processing the next category
    time.sleep(2)

print("\nCategory counts:")
for category, count in category_counts.items():
    print(f"{category}: {count}")

# Create the data folder and save the collected stories as JSON
os.makedirs("data", exist_ok=True)

filename = datetime.now().strftime("%Y%m%d")
output_file = f"data/trends_{filename}.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(stories, file, indent=4)

print(f"Collected {len(stories)} stories. Saved to {output_file}")