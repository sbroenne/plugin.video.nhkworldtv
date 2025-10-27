"""
NHK Cache API - gets episode VOD information from the companion Azure service
"""
import xbmc

from . import url


def get_program_metdadata_cache():
    """
    Load the VOD program URLs from a json file that is generated every few hours
    by the [Azure Cache for NHK World TV Kodi Plugin](https://github.com/sbroenne/nhkworldtv-backend)
    service.

    This file is stored in Azure Blob Storage and will speed up resolving of episodes dramatically.


    Returns:
        {dict} -- A JSON dict with the cache items or None if the request failed
    """
    cache_file = "https://nhkworldtv.blob.core.windows.net/program-list-v2/cache.json"

    cache = url.get_json(cache_file)
    if cache is not None:
        xbmc.log(
            f"cache_api.get_program_metdadata_cache: Got {len(cache)} episodes from Azure Blob Storage"
        )
    else:
        xbmc.log(
            "cache_api.get_program_metdadata_cache: Failed to retrieve cache from Azure Blob Storage"
        )
    return cache
