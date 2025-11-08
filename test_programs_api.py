#!/usr/bin/env python3
"""
Quick test to check NHK Programs API response for empty titles
"""

import sys

sys.path.insert(0, "plugin.video.nhkworldtv/lib")

from lib import nhk_api, url

# Fetch the programs API
api_result = url.get_json(nhk_api.rest_url["get_programs"])

if api_result and "items" in api_result:
    programs = api_result["items"]
    print(f"\n=== Total programs: {len(programs)} ===\n")

    empty_title_count = 0
    zero_episodes_count = 0
    valid_count = 0

    for idx, prog in enumerate(programs):
        prog_id = prog.get("id", "NO_ID")
        title = prog.get("title", "")
        total_episodes = prog.get("video_episodes", {}).get("total", 0)

        # Check for issues
        has_issue = False
        issues = []

        if not title or not title.strip():
            empty_title_count += 1
            issues.append("EMPTY_TITLE")
            has_issue = True

        if total_episodes == 0:
            zero_episodes_count += 1
            issues.append("ZERO_EPISODES")
            has_issue = True

        if has_issue:
            print(f"[{idx + 1}] ID: {prog_id}")
            print(f"    Title: '{title}'")
            print(f"    Episodes: {total_episodes}")
            print(f"    Issues: {', '.join(issues)}")
            print()
        else:
            valid_count += 1

    print("\n=== Summary ===")
    print(f"Valid programs: {valid_count}")
    print(f"Empty titles: {empty_title_count}")
    print(f"Zero episodes: {zero_episodes_count}")
    print(f"Would show in list: {valid_count}")

else:
    print("Failed to fetch API data")
    print("Failed to fetch API data")
