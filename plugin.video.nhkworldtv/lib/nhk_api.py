"""
NHK API URL Constants

All API endpoints are hardcoded here instead of being dynamically parsed.
This makes the codebase more maintainable and easier to update when NHK changes their API.
"""

# API Base URLs
NHK_API_BASE = "https://nwapi.nhk.jp/nhkworld/"
NHK_BASE = "https://www3.nhk.or.jp"

# Current API version for VOD endpoints
VOD_VERSION = "v7b"
# Current API version for TV/EPG endpoints  
TV_VERSION = "v7b"
# Language
LANG = "en"

# NHK World API endpoints
rest_url = {
    # VOD - On Demand endpoints
    'homepage_ondemand':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/mostwatch/all/{LANG}/all/all.json",
    
    'get_programs':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/program/all/{LANG}/voice/all.json",
    
    'get_programs_episode_list':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/episode/0/{LANG}/all/all.json",
    
    'get_categories':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/category/all/{LANG}/all/ondemand/all.json",
    
    'get_categories_episode_list':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/cat_esd/0/{LANG}/all/all.json",
    
    'get_latest_episodes':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/all/all/{LANG}/all/23.json",
    
    'get_most_watched_episodes':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/mostwatch/all/{LANG}/all/all.json",
    
    'get_all_episodes':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/all/all/{LANG}/all/all.json",
    
    'get_episode_detail':
    f"{NHK_API_BASE}vodesdlist/{VOD_VERSION}/vod_id/{{0}}/{LANG}/all/1.json",
    
    # TV - Live stream and EPG
    'get_livestream':
    f"{NHK_API_BASE}epg/{TV_VERSION}/world/now.json",
    
    'live_stream_url_720p':
    "https://master.nhkworld.jp/nhkworld-tv/playlist/live.m3u8",
    
    'live_stream_url_1080p':
    "https://master.nhkworld.jp/nhkworld-tv/playlist/live.m3u8",
    
    # News endpoints
    'homepage_news':
    f"{NHK_BASE}/nhkworld/data/en/news/all.json",
    
    'news_detail':
    f"{NHK_BASE}/nhkworld/data/en/news/{{0}}.json",
    
    'get_news_ataglance':
    f"{NHK_BASE}/nhkworld/en/news/ataglance/index.json",
    
    'news_video_url':
    "https://nhkworld-vh.akamaihd.net/i/nhkworld/upld/medias/en/news/{0},L,H,Q.mp4.csmil/master.m3u8?set-akamai-hls-revision=5",
    
    'ataglance_video_url':
    "https://nhkworld-vh.akamaihd.net/i/nhkworld/english/news/ataglance/{0}/master.m3u8?set-akamai-hls-revision=5",
    
    'news_program_config':
    f"{NHK_BASE}/nhkworld/common/assets/news/config/en.json",
    
    'news_program_xml':
    f"{NHK_BASE}/nhkworld/data/en/news/programs/{{0}}.xml",
    
    'news_programs_video_url':
    "https://vod-stream.nhk.jp/nhkworld/upld/medias/en/news/programs/{0}/index.m3u8",
    
    # Player and video endpoints
    'player_url':
    f"{NHK_BASE}/nhkworld/common/player/tv/vod/world/player/js/movie-content-player.js",
    
    'video_url':
    "https://movie-s.nhk.or.jp/ws/ws_program/api/67f5b750-b419-11e9-8a16-0e45e8988f42/apiv/5/mode/json?v={0}",
}
