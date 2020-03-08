import nhk_api_parser

# NHK World API - parsed from api.js
# FIXME: Some URLs cannot be found in api.js and are therefor static
rest_url = {
    'homepage_ondemand':
    nhk_api_parser.get_homepage_ondemand_url(),
    'homepage_news':
    nhk_api_parser.get_homepage_news_url(),
    'get_livestream':
    nhk_api_parser.get_livestream_url(),
    'get_programs':
    nhk_api_parser.get_programs_url(),
    'get_programs_episode_list':
    nhk_api_parser.get_programs_episode_list_url(),
    'get_categories':
    nhk_api_parser.get_categories_url(),
    'get_categories_episode_list':
    nhk_api_parser.get_categories_episode_list_url(),
    'get_playlists':
    nhk_api_parser.get_playlists_url(),
    'get_playlists_episode_list':
    nhk_api_parser.get_playlists_episode_list_url(),
    'get_latest_episodes':
    nhk_api_parser.get_all_episodes_url('23'),
    'get_most_watched_episodes':
    nhk_api_parser.get_most_watched_episodes_url(),
    'get_all_episodes':
    nhk_api_parser.get_all_episodes_url('all'),
    'get_episode_detail':
    nhk_api_parser.get_episode_detail_url(),
    # Not in api.js
    'get_news_xml':
    'https://www3.nhk.or.jp/nhkworld/data/en/news/movie/{0}.xml',
    'news_url':
    'https://nhkworld-vh.akamaihd.net/i/nhkworld/upld/medias/en/news/{0},L,H,Q.mp4.csmil/master.m3u8?set-akamai-hls-revision=5',
    'live_stream_url':
    'https://nhkwlive-ojp.akamaized.net/hls/live/2003459/nhkwlive-ojp/index_4M.m3u8',
    'nhkworldtv-backend':
    'https://nhkworldtv.azurewebsites.net/api/GetVideoUrl/{0}',
     'video_url':
    'https://movie-s.nhk.or.jp/ws/ws_program/api/67f5b750-b419-11e9-8a16-0e45e8988f42/apiv/5/mode/json?v={0}',
    'episode_url':
    'https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/definst/{0}/chunklist.m3u8'
}
