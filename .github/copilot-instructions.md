# GitHub Copilot Instructions for NHK World TV Kodi Plugin

## Project Overview

This is a **Kodi addon** for streaming NHK World TV content (live TV, on-demand videos, and news programs). The plugin is written in Python 3.12 and uses the NHK World API to fetch content.

### Key Technologies

- **Python 3.12** with Pipenv for dependency management
- **Kodi API** (xbmc, xbmcgui, xbmcplugin, xbmcaddon) via kodistubs
- **Requests** library with caching for API calls
- **Pytest** for unit testing
- **Playwright** for analyzing NHK website and API extraction

## Code Style & Best Practices

### Python Standards

- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation (no tabs)
- Line length: **88 characters** (Black formatter standard)
- Use **type hints** where possible for better code clarity
- Write **docstrings** for all public functions and classes

### Kodi-Specific Guidelines

- Always use `xbmc.log()` for logging with appropriate log levels
- Handle errors gracefully - Kodi should never crash due to API failures
- Use `xbmcgui.Dialog` for user interactions (dialogs, notifications)
- Cache API responses to minimize network requests (60 minutes minimum)
- Always check if URLs exist before attempting to play media

### Error Handling

```python
# GOOD: Null-safe API response handling
def get_json(url, cached=True):
    request = get_url(url, cached)
    if request.status_code == 200:
        try:
            result = request.json()
            return result
        except ValueError:
            xbmc.log(f"Could not parse JSON from API: {url}")
            return None
    else:
        xbmc.log(f"Could not connect to API: {url}")
        return None

# GOOD: Safe dictionary access
api_result_json = url.get_json(api_url)
if api_result_json and "data" in api_result_json:
    data = api_result_json["data"]
else:
    xbmc.log("API returned no data")
    return []

# BAD: Direct access without null checking
api_result_json = url.get_json(api_url)["data"]  # Can raise TypeError!
```

## Project Structure

```
plugin.video.nhkworldtv/
├── lib/                    # Main library code
│   ├── nhk_api.py         # API endpoint definitions (hardcoded URLs)
│   ├── url.py             # HTTP request handling with retry logic
│   ├── plugin.py          # Main plugin logic and menu system
│   ├── vod.py             # Video-on-demand functionality
│   ├── episode.py         # Episode data handling
│   ├── ataglance.py       # At-a-glance news
│   ├── topstories.py      # Top stories news
│   ├── utils.py           # Utility functions
│   └── kodiutils.py       # Kodi helper utilities
├── tests/                 # Unit tests (pytest)
├── resources/             # Kodi addon resources (settings, translations)
└── main.py               # Plugin entry point
```

**Removed modules** (as of PR #140):

- `api_keys.py` - API keys no longer required (authentication removed)
- `nhk_api_parser.py` - Dynamic API parsing removed (URLs now hardcoded)
- `cache_api.py` - Azure cache removed
- `news_programs.py` - Consolidated into other modules
- `first_run_wizard.py` - First-run wizard removed

## NHK API Architecture

### API Structure (As of October 28, 2025)

**NHK migrated to a new API**: `api.nhkworld.jp/showsapi/v1/` (October 2025)

**All API endpoints are hardcoded** in `nhk_api.py`:

Key constants in `nhk_api.py`:

- `NHK_API_BASE = "https://api.nhkworld.jp/showsapi/v1/"`
- `NHK_BASE = "https://www3.nhk.or.jp"`
- `LANG = "en"`

All endpoints are defined in the `rest_url` dictionary:

```python
rest_url = {
    # VOD endpoints (new showsapi v1)
    'homepage_ondemand': f"{NHK_API_BASE}{LANG}/video_episodes?limit=20",
    'get_programs': f"{NHK_API_BASE}{LANG}/video_programs",
    'get_latest_episodes': f"{NHK_API_BASE}{LANG}/video_episodes?limit=23",
    'get_episode_detail': f"{NHK_API_BASE}{LANG}/video_episodes/{{0}}",

    # Live stream
    'live_stream_url': "https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8",

    # News (still uses old endpoints)
    'homepage_news': f"{NHK_BASE}/nhkworld/data/en/news/all.json",
    # ... etc
}
```

### New API Response Format

**Key differences from old API**:

| Old API             | New API              | Notes                                |
| ------------------- | -------------------- | ------------------------------------ |
| `data.episodes`     | `items`              | Top-level array                      |
| `vod_id`            | `id`                 | Episode identifier                   |
| `title_clean`       | `title`              | Episode title                        |
| `sub_title_clean`   | `subtitle`           | Episode subtitle                     |
| `description_clean` | `description`        | Episode description                  |
| `image`, `image_l`  | `images.landscape[]` | Image array with multiple sizes      |
| Unix timestamp      | ISO 8601 string      | Date format (`2021-08-18T01:55:00Z`) |
| **Not available**   | `video.url`          | **Video URL provided directly!**     |

### Video URL Resolution

**Major simplification**: The new API provides video URLs directly in episode detail responses!

```python
# New API - video URL in episode detail response
api_result = url.get_json(nhk_api.rest_url['get_episode_detail'].format(episode_id))
if api_result and 'video' in api_result:
    video_url = api_result['video']['url']  # Direct HLS URL!
    # Example: https://masterpl.hls.nhkworld.jp/hls/w/602403620251026001/master.m3u8
```

**No more player.js scraping needed!** Previously, the plugin had to:

1. Scrape `player.js` to extract API URL and token
2. Make separate request to media information API
3. Parse nested response for video URL

Now it's just one API call with the video URL included directly.

### Authentication Status

**API keys are NO LONGER REQUIRED**. The new NHK API works without authentication for all public endpoints.

### Making API Requests

Use `url.get_json()` which handles caching and error handling:

```python
from lib import url, nhk_api

# New API format - returns items array directly
api_result = url.get_json(nhk_api.rest_url['get_latest_episodes'])
if api_result and "items" in api_result:
    episodes = api_result["items"]
else:
    # Handle null response gracefully
    episodes = []
```

**Dual format support**: The code handles both old and new API formats for backward compatibility during migration.

## Testing Strategy

### Running Tests

```bash
# Run all tests with verbose output
pipenv run pytest plugin.video.nhkworldtv/tests/ -v

# Run with coverage
pipenv run pytest plugin.video.nhkworldtv/tests/ --cov=plugin.video.nhkworldtv/lib --cov-report=html -v

# Run specific test file
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib_url.py -v
```

### Test Requirements

- All new functions should have corresponding unit tests
- Tests should use mocked Kodi API calls (xbmc, xbmcgui, etc.)
- API tests should handle both successful and failed responses
- Test for null safety and error conditions

### Playwright for Website Analysis

```bash
# Analyze NHK website and extract API information
npx playwright test tests/analyze_nhk_api.spec.ts
```

**IMPORTANT - NHK HTTP/1.1 Requirement**:
NHK does not support HTTP/2. The Playwright configuration forces HTTP/1.1:

- `playwright.config.ts` - Uses `--disable-http2` flag in launch args
- `playwright-mcp-config.json` - MCP server config with HTTP/1.1 enforcement
- `.vscode/mcp.json` - MCP server uses the config file

**Verified Working** (October 28, 2025):

- ✅ Playwright MCP server successfully accesses NHK website with HTTP/1.1
- ✅ Can navigate to `https://www3.nhk.or.jp/nhkworld/`
- ✅ Page snapshots work correctly
- ✅ No HTTP/2 errors when properly configured

Use Playwright MCP server tools to:

- `mcp_playwright_browser_navigate` - Navigate to NHK website pages
- `mcp_playwright_browser_snapshot` - Get accessibility snapshot of current page
- `mcp_playwright_browser_network_requests` - Monitor API calls made by the page
- `mcp_playwright_browser_take_screenshot` - Screenshot pages for documentation
- `mcp_playwright_browser_evaluate` - Execute JavaScript to extract data from page

## MCP Servers Available

### GitHub MCP Server

Use for:

- Creating issues
- Managing pull requests
- Searching code across repositories
- Reviewing commits and branches

### Playwright MCP Server

**Configured with HTTP/1.1** (NHK requirement) - **VERIFIED WORKING**

Use for:

- `mcp_playwright_browser_navigate` - Navigate to NHK website (HTTP/1.1 working)
- `mcp_playwright_browser_snapshot` - Extract accessible page structure
- `mcp_playwright_browser_evaluate` - Execute JavaScript to extract API data
- `mcp_playwright_browser_network_requests` - Monitor API calls
- `mcp_playwright_browser_console_messages` - Capture browser console output
- `mcp_playwright_browser_take_screenshot` - Screenshot pages

**Installation**: Chrome browser must be installed first:

```bash
npx playwright install chrome
```

## Common Tasks

### Adding a New API Endpoint

1. Add endpoint URL to `nhk_api.rest_url` dictionary in `nhk_api.py`
2. Use via `url.get_json(nhk_api.rest_url['endpoint_name'])`
3. Add null safety checks for response
4. Write unit tests

### Debugging API Issues

1. Use Playwright MCP to navigate to NHK website
2. Monitor network requests for working API calls with `mcp_playwright_browser_network_requests`
3. Extract headers or cookies if needed
4. Verify endpoint URLs match those in `nhk_api.py`
5. Check for null responses and empty data arrays

### Fixing Test Failures

1. Identify root cause (API change, authentication, data structure)
2. Update API endpoint URLs if changed
3. Add proper error handling for null responses
4. Update test expectations if API structure changed
5. Ensure all dict access is null-safe

## File Naming Conventions

- Test files: `test_lib_<module_name>.py`
- Library modules: Lowercase with underscores (e.g., `nhk_api_parser.py`)
- Constants: UPPER_CASE_WITH_UNDERSCORES
- Functions: lowercase_with_underscores
- Classes: PascalCase

## Git Workflow

### Branch Naming

- Features: `feature/description`
- Bugfixes: `fix/description`
- API fixes: `fix-nhk-api-description`

### Commit Messages

```
<type>: <short description>

<detailed description if needed>

Issue #<number>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

### PR Guidelines

- Link to related issue
- Mark as draft if work in progress
- Include test results
- Document API changes

## Important URLs

- NHK World: https://www3.nhk.or.jp/nhkworld/
- New API Base: https://api.nhkworld.jp/showsapi/v1/
- Old API Config: https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api2.json (deprecated)
- Live Stream: https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8
- Repository: https://github.com/sbroenne/plugin.video.nhkworldtv

## VS Code Configuration

The project has optimized VS Code settings in `.vscode/`:

- **settings.json** - Python, testing, and formatting configuration
- **launch.json** - Debug configurations for addon and tests
- **tasks.json** - Common development tasks
- **mcp.json** - MCP server configurations (GitHub, Playwright)

## Current Work (October 28, 2025)

**✅ ALL TESTS PASSING**: **57/57 (100%)**

**Completed Fixes** (October 28, 2025):

1. ✅ **API Migration to showsapi/v1**

   - Migrated from `nwapi.nhk.jp` to `api.nhkworld.jp/showsapi/v1/`
   - Updated all endpoint URLs in `nhk_api.py`
   - Removed API key authentication (no longer required)

2. ✅ **Response Format Handling**

   - Updated code to handle new API format (`items` vs `data.episodes`)
   - Added field name mapping (`id` vs `vod_id`, `title` vs `title_clean`)
   - Fixed image structure handling (`images.landscape[]` array)

3. ✅ **Video URL Resolution Simplification**

   - **Major improvement**: Video URLs now provided directly in `video.url` field
   - Removed complex player.js scraping logic (fallback still exists for old API)
   - Single API call instead of multi-step resolution process

4. ✅ **Timestamp Format Compatibility**

   - Fixed ISO 8601 string (`2021-08-18T01:55:00Z`) vs Unix timestamp handling
   - Added type checking in `Episode.broadcast_start_date` setter

5. ✅ **Stream Compatibility Verification**
   - **Live Stream**: H.264 Main Profile, 720p, AAC-LC audio, HLS adaptive streaming
   - **VOD Streams**: H.264 Main Profile Level 3.1, 720p @ 29.97fps, AAC-LC audio
   - **Kodi Compatibility**: ✅ Excellent - all codecs fully supported

**Test Results**: All 57 tests passing (up from 0 at start of session)

## When to Ask for Help

- If NHK API endpoints change significantly and break multiple tests
- If authentication requirements are reintroduced
- If major architectural changes are needed
- If breaking changes to Kodi API are discovered

## Quick Reference

### Get Episode List

```python
from lib import vod, url, nhk_api

api_url = nhk_api.rest_url["get_latest_episodes"]
api_result = url.get_json(api_url)

if api_result and "data" in api_result:
    episodes = vod.process_episodes(api_result["data"])
else:
    # Handle error gracefully
    episodes = []
```

### Add Menu Item

```python
from lib import kodiutils
import xbmcgui, xbmcplugin

li = xbmcgui.ListItem(label="Menu Item Title")
li.setArt({'thumb': thumb_url, 'fanart': fanart_url})
xbmcplugin.addDirectoryItem(
    handle=kodiutils.get_handle(),
    url=url,
    listitem=li,
    isFolder=True
)
```

### Log Debugging Info

```python
import xbmc

xbmc.log(f"API URL: {api_url}", xbmc.LOGDEBUG)
xbmc.log(f"Error: {error_message}", xbmc.LOGERROR)
```
