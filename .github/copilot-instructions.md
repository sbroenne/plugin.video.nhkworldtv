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
│   ├── nhk_api.py         # API endpoint definitions
│   ├── nhk_api_parser.py  # Dynamic API URL generation from api.json
│   ├── api_keys.py        # API keys and base URLs
│   ├── url.py             # HTTP request handling with retry logic
│   ├── plugin.py          # Main plugin logic and menu system
│   ├── vod.py             # Video-on-demand functionality
│   ├── episode.py         # Episode data handling
│   ├── news_programs.py   # News program handling
│   ├── ataglance.py       # At-a-glance news
│   ├── topstories.py      # Top stories news
│   └── kodiutils.py       # Kodi helper utilities
├── tests/                 # Unit tests (pytest)
├── resources/             # Kodi addon resources (settings, translations)
└── main.py               # Plugin entry point
```

## NHK API Architecture

### API Discovery
The NHK API configuration is dynamically loaded from:
```
https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api2.json
```

This JSON file contains:
- API endpoint templates with placeholders (`{version}`, `{lang}`, etc.)
- Whether endpoints require API keys (`requireKey: true/false`)
- Available resources organized by prefix (vod, tv, news, radio, etc.)

### API Parser Flow
1. **Load API config** (`nhk_api_parser.get_api_from_nhk()`) at module initialization
2. **Build endpoint URLs** by replacing placeholders with actual values
3. **Make requests** through `url.py` with automatic retry and caching

### Current API Issue (Issue #138)
⚠️ **Many NHK API endpoints now return 403 Forbidden errors**, likely due to:
- Changed authentication requirements
- Missing or incorrect API keys
- Changed request headers/User-Agent requirements

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

### Playwright for API Investigation
```bash
# Analyze NHK website and extract API information
npx playwright test tests/analyze_nhk_api.spec.ts
```

Use Playwright MCP server tools to:
- Navigate to NHK website pages
- Extract JavaScript files containing API configurations
- Monitor network requests to identify working endpoints
- Screenshot pages for documentation

## MCP Servers Available

### GitHub MCP Server
Use for:
- Creating issues
- Managing pull requests
- Searching code across repositories
- Reviewing commits and branches

### Playwright MCP Server  
Use for:
- `Playwright_navigate` - Navigate to NHK website
- `playwright_get_visible_html` - Extract page HTML
- `Playwright_evaluate` - Execute JavaScript to extract API keys
- `Playwright_expect_response` / `Playwright_assert_response` - Monitor API calls
- `playwright_console_logs` - Capture browser console output

## Common Tasks

### Adding a New API Endpoint
1. Check if endpoint exists in `api2.json`
2. Add URL builder function in `nhk_api_parser.py`
3. Add endpoint to `nhk_api.rest_url` dictionary
4. Use via `url.get_json(nhk_api.rest_url['endpoint_name'])`
5. Add null safety checks for response
6. Write unit tests

### Debugging API Issues
1. Use Playwright to navigate to NHK website
2. Monitor network requests for working API calls
3. Extract headers, cookies, or authentication tokens
4. Check `api2.json` for `requireKey: true` endpoints
5. Look for API keys in JavaScript files on NHK site

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
- API Config: https://www3.nhk.or.jp/nhkworld/assets/api_sdk/api2.json
- API Base: https://nwapi.nhk.jp/nhkworld/
- Live Stream: https://nhkworld.webcdn.stream.ne.jp/
- Repository: https://github.com/sbroenne/plugin.video.nhkworldtv

## VS Code Configuration

The project has optimized VS Code settings in `.vscode/`:
- **settings.json** - Python, testing, and formatting configuration
- **launch.json** - Debug configurations for addon and tests
- **tasks.json** - Common development tasks
- **mcp.json** - MCP server configurations (GitHub, Playwright)

## Current Work (PR #139)

**Goal**: Fix test failures caused by NHK API authentication changes

**Status**: 19 failed tests, 7 errors due to 403 Forbidden responses

**Next Steps**:
1. Use Playwright MCP to extract API keys from NHK website
2. Update authentication in `url.py` request handling
3. Fix null pointer errors from failed API calls
4. Update tests to match any API structure changes

## When to Ask for Help

- If NHK API endpoints are completely inaccessible
- If authentication mechanism is unclear after investigation
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
