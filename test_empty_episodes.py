"""
Debug script to find episodes with empty titles/subtitles
"""

import sys
import os
from unittest.mock import MagicMock

# Mock Kodi modules before importing
sys.modules["xbmc"] = MagicMock()
sys.modules["xbmcgui"] = MagicMock()
sys.modules["xbmcaddon"] = MagicMock()
sys.modules["xbmcplugin"] = MagicMock()
sys.modules["xbmcvfs"] = MagicMock()
sys.modules["routing"] = MagicMock()

# Add parent directory to path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "plugin.video.nhkworldtv")
)

from lib import url, nhk_api  # noqa: E402

print("=" * 80)
print("Analyzing Episodes with Empty Titles/Subtitles")
print("=" * 80)

# Test a specific program that might have empty episodes
# Let's check "DEEPER LOOK" which had issues
program_id = "deeperlook"
api_url = nhk_api.rest_url["get_programs_episode_list"].format(program_id)

print(f"\nFetching episodes for program: {program_id}")
print(f"API URL: {api_url}\n")

api_result = url.get_json(api_url)

if api_result and "items" in api_result:
    episodes = api_result["items"]
    print(f"Total episodes returned: {len(episodes)}\n")

    empty_count = 0
    valid_count = 0

    for i, episode in enumerate(episodes, 1):
        title = episode.get("title") or ""
        subtitle = episode.get("subtitle") or ""
        episode_id = episode.get("id", "unknown")

        # Check if both are empty
        if not title and not subtitle:
            empty_count += 1
            print(f"\n⚠️ EMPTY EPISODE #{i} (id: {episode_id})")
            print("=" * 60)
            print("Full episode data:")
            import json

            print(json.dumps(episode, indent=2))
            print("=" * 60)
        else:
            valid_count += 1
            if i <= 3:  # Show first 3 valid episodes
                print(
                    f"✓ Episode #{i}: title='{title[:50]}', subtitle='{subtitle[:50]}'"
                )

    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total episodes: {len(episodes)}")
    print(f"Valid episodes (with title or subtitle): {valid_count}")
    print(f"Empty episodes (no title and no subtitle): {empty_count}")

    if empty_count == 0:
        print(
            "\nNo empty episodes found! The API is returning valid data."
        )
        print("Empty list items might be caused by different issue.")
else:
    print("Failed to fetch episode data or no items in response")
