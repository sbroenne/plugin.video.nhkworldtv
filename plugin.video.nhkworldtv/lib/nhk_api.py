"""
NHK API URL Constants

All API endpoints are hardcoded here instead of being dynamically parsed.
This makes the codebase more maintainable and easier to update when NHK
changes their API.

Current API: api.nhkworld.jp/showsapi/v1/ (migrated October 28, 2025)
"""

# API Base URLs
NHK_API_BASE = "https://api.nhkworld.jp/showsapi/v1/"
NHK_BASE = "https://www3.nhk.or.jp"

# Language
LANG = "en"

# NHK World API endpoints
rest_url = {
    # VOD - On Demand endpoints (new showsapi v1)
    "homepage_ondemand": f"{NHK_API_BASE}{LANG}/video_episodes?limit=20",
    "get_programs": f"{NHK_API_BASE}{LANG}/video_programs",
    "get_programs_episode_list": f"{NHK_API_BASE}{LANG}/video_episodes",
    "get_categories": f"{NHK_API_BASE}{LANG}/categories",
    "get_categories_episode_list": f"{NHK_API_BASE}{LANG}/video_episodes",
    "get_latest_episodes": f"{NHK_API_BASE}{LANG}/video_episodes?limit=23",
    "get_most_watched_episodes": f"{NHK_API_BASE}{LANG}/video_episodes?limit=20",
    "get_all_episodes": f"{NHK_API_BASE}{LANG}/video_episodes",
    "get_episode_detail": f"{NHK_API_BASE}{LANG}/video_episodes/{{0}}",
    # TV - Live stream and EPG (HLS streaming)
    "get_livestream": f"{NHK_BASE}/nhkworld/en/live/",
    "live_stream_url": "https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8",
    # News endpoints
    "homepage_news": f"{NHK_BASE}/nhkworld/data/en/news/all.json",
    "news_detail": f"{NHK_BASE}/nhkworld/data/en/news/{{0}}.json",
    "get_news_ataglance": f"{NHK_BASE}/nhkworld/en/news/ataglance/index.json",
    "news_video_url": (
        "https://nhkworld-vh.akamaihd.net/i/nhkworld/upld/medias/en/news/"
        "{0},L,H,Q.mp4.csmil/master.m3u8?set-akamai-hls-revision=5"
    ),
    "ataglance_video_url": (
        "https://nhkworld-vh.akamaihd.net/i/nhkworld/english/news/"
        "ataglance/{0}/master.m3u8?set-akamai-hls-revision=5"
    ),
}
