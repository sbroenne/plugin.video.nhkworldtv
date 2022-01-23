"""
NHK Cache API - gets episode VOD information from the companion Azure service
"""
import xbmc

from . import url

BASE_URL = "https://nhkw-mzvod.akamaized.net/www60/mz-nhk10/_definst_/mp4:mm/flvmedia/5905"


def get_program_metdadata_cache():
    """ 
    Load the VOD program URLs from a json file that is generated every few hours
    by the [Azure Cache for NHK World TV Kodi Plugin](https://github.com/sbroenne/nhkworldtv-backend)
    service.

    This file is delivered by the Azure CDN and will speed up resolving of episodes dramatically.


    Returns:
        {dict} -- A JSON dict with the cache items or None if the request failed
    """
    cache_file = "https://nhkworldtv.azureedge.net/program-list-v2/cache.json"

    cache = url.get_json(cache_file)
    xbmc.log(
        f"cache_api.get_program_metdadata_cache: Got {len(cache)} episodes from Azure CDN"
    )
    return cache
