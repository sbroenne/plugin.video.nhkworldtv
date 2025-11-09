"""
URL / Request handling
"""

from __future__ import annotations

import time

import requests
import xbmc
import xbmcaddon
from requests.models import Response

from . import nhk_api

# Get Plug-In path
ADDON = xbmcaddon.Addon()
PLUGIN_PATH = ADDON.getAddonInfo("path")

# Cache configuration (60 minutes)
URL_CACHE_MINUTES = 60

# Simple in-memory cache
# Format: {url: (response_text, expiry_timestamp)}
_response_cache: dict[str, tuple[str, float]] = {}


def _get_cache_key(url: str, params: dict | None = None) -> str:
    """Generate cache key from URL and parameters"""
    if params:
        # Sort params for consistent cache keys
        param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"{url}?{param_str}"
    return url


def _get_cached_response(url: str, params: dict | None = None) -> str | None:
    """Get cached response if available and not expired"""
    cache_key = _get_cache_key(url, params)
    if cache_key in _response_cache:
        content, expiry = _response_cache[cache_key]
        if time.time() < expiry:
            xbmc.log(f"Cache hit for: {url}", xbmc.LOGDEBUG)
            return content
        else:
            # Expired, remove from cache
            del _response_cache[cache_key]
            xbmc.log(f"Cache expired for: {url}", xbmc.LOGDEBUG)
    return None


def _cache_response(url: str, content: str, params: dict | None = None):
    """Cache response with expiration time"""
    cache_key = _get_cache_key(url, params)
    expiry = time.time() + (URL_CACHE_MINUTES * 60)
    _response_cache[cache_key] = (content, expiry)
    xbmc.log(f"Cached response for: {url}", xbmc.LOGDEBUG)


# Instantiate request session
session = requests.Session()
# Act like a browser
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/88.0.4324.182"
session.headers.update({"User-Agent": user_agent})


def check_url_exists(url: str) -> bool:
    """Check if a URL exists or it returns a 404

    Arguments:
        url: URL to check

    Returns:
        False if 404, True otherwise
    """
    # Don't cache existence checks
    request = session.get(url)
    return bool(request.status_code != 404)


def get_json(url: str, cached: bool = True) -> dict | None:
    """Get JSON object from a URL with improved error handling

    Args:
        url: URL to retrieve
        cached: Use request_cache. Defaults to True.

    Returns:
        JSON dictionary or None if request fails
    """
    request = get_url(url, cached)
    if request.status_code == 200:
        try:
            result: dict | None = request.json()
            xbmc.log(f"Successfully loaded JSON from API: {url}")
            return result
        except ValueError:
            # Failure - no way to handle - probably an issue with the NHK API
            xbmc.log(f"Could not parse JSON from API: {url}")
            return None
    else:
        # Failure - could not connect to site
        xbmc.log(f"Could not connect to API: {url}")
        return None


def get_api_request_params(url: str) -> dict | None:
    """Returns the API request parameters for the NHK API

    Args:
        url: Url

    Returns:
        Empty dict for API URLs (no auth needed), None for others
    """

    # Check if this is an NHK API URL
    if nhk_api.NHK_API_BASE in url or nhk_api.NHK_BASE in url:
        # API key is no longer required per commit 05d1548
        request_params: dict | None = {}
    else:
        request_params = None

    return request_params


def request_url(url: str, cached: bool = True) -> Response:
    """HELPER: Request URL with handling basic error conditions

    Args:
        url ([str]): URL to retrieve
        cached (bool, optional): Use in-memory cache. Defaults to True.

    Returns:
        [response]: Response object - can be None
    """

    request_params = get_api_request_params(url)

    try:
        # Check cache first if caching is enabled
        if cached:
            cached_content = _get_cached_response(url, request_params)
            if cached_content:
                # Create a fake response object from cached content
                request = Response()
                request.status_code = 200
                # Use encoding instead of direct content access
                request.encoding = "utf-8"
                # pylint: disable=protected-access
                request._content = cached_content.encode("utf-8")
                return request

        # Make actual request
        if request_params is not None:
            request = session.get(url, params=request_params)
        else:
            request = session.get(url)

        # Cache successful responses
        if cached and request.status_code == 200:
            _cache_response(url, request.text, request_params)

        return request
    except requests.ConnectionError:
        # Could not establish connection at all
        request = Response()
        request.status_code = 10001
    return request


def get_url(url: str, cached: bool = True) -> Response:
    """Get a URL with automatic retries
        NHK sometimes have intermittent problems with 502 Bad Gateway

    Args:
        url: URL to retrieve
        cached: Use in-memory cache. Defaults to True.

    Returns:
        Response object
    """

    # maximum number of retries
    max_retries = 3
    current_try = 1

    while current_try <= max_retries:
        # Make an API Call
        xbmc.log(f"Fetching URL:{url} ({current_try} of {max_retries})")

        request = request_url(url, cached)
        status_code = request.status_code

        if status_code == 200:
            # Call was successful
            xbmc.log(f"Successfully fetched URL: {url} - Status {status_code}")
            break

        elif status_code == 502:
            # Bad Gateway - can be retried
            if current_try == max_retries:
                # Max retries reached - still could not get url
                xbmc.log(
                    f"FATAL: Could not get URL {url} after {current_try} retries",
                    xbmc.LOGDEBUG,
                )
                break
            else:
                # Try again - this usually fixes the error
                xbmc.log(
                    f"Temporary failure fetching URL: {url} with Status {status_code})",
                    xbmc.LOGDEBUG,
                )

                # Wait for 1s before the next call
                time.sleep(1)
        else:
            # Other HTTP error - FATAL, do not retry
            xbmc.log(
                f"FATAL: Could not get URL: {url} - HTTP Status Code {status_code}",
                xbmc.LOGDEBUG,
            )
            break

        current_try = current_try + 1

    return request


def get_nhk_website_url(path: str) -> str:
    """Return a full URL from the partial URLs in the JSON results

    Args:
        path: Partial URL path

    Returns:
        Full URL
    """
    nhk_website = nhk_api.NHK_BASE
    return nhk_website + path
