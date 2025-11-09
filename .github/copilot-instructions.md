# GitHub Copilot Instructions for NHK World TV Kodi Plugin

## Project Context

**What**: Kodi addon for streaming NHK World TV (live TV, on-demand videos, news)
**Tech Stack**: Python 3.12, Kodi API (xbmc/xbmcgui/xbmcplugin), Requests with in-memory caching, Pytest
**Current Status**: Submitted to official Kodi repo - [PR #4718](https://github.com/xbmc/repo-plugins/pull/4718)
**Kodi Versions**: Omega (v21), Piers (v22)

## Critical Rules (Always Follow)

### 1. ⚠️ MANDATORY: Check Kodi Repository for Dependency Versions FIRST

**🔴 BEFORE making ANY dependency changes, ALWAYS verify versions against the Kodi repository.**

The Kodi addon repository at https://mirrors.kodi.tv/addons/omega/ is the **ONLY** source of truth for dependency versions.

**Mandatory Workflow**: `Kodi Repository → addon.xml → Pipfile`

**Step-by-step process**:
1. **FIRST**: Check https://mirrors.kodi.tv/addons/omega/ for available versions
2. **THEN**: Update `plugin.video.nhkworldtv/addon.xml` to match Kodi repository
3. **FINALLY**: Update `Pipfile` to match `addon.xml`

**Critical Notes**:
- Binary addons (e.g., `inputstream.adaptive`) have platform-specific directories in repo (e.g., `inputstream.adaptive+android-aarch64/`) but are referenced without platform suffix in `addon.xml`
- Script modules use `script.module.*` prefix in repository (e.g., `script.module.requests/`)
- **NEVER** assume a version exists without verification
- **NEVER** update dependencies based on Dependabot/security alerts without checking Kodi repo first
- If a version doesn't exist in Kodi repo, it **cannot** be used

**Current verified dependencies** (as of January 2025):
- script.module.requests: 2.31.0 ✅ ([verify](https://mirrors.kodi.tv/addons/omega/script.module.requests/))
- script.module.pytz: 2023.3.0 ✅ ([verify](https://mirrors.kodi.tv/addons/omega/script.module.pytz/))
- script.module.routing: 0.2.3 ✅ ([verify](https://mirrors.kodi.tv/addons/omega/script.module.routing/))
- script.module.tzlocal: 5.0.1 ✅ ([verify](https://mirrors.kodi.tv/addons/omega/script.module.tzlocal/))
- inputstream.adaptive: 21.5.16 ✅ ([verify](https://mirrors.kodi.tv/addons/omega/inputstream.adaptive+android-aarch64/))

### 2. Error Handling Pattern

**ALWAYS use null-safe patterns:**

```python
# CORRECT: Null-safe API access
api_result = url.get_json(api_url)
if api_result and "items" in api_result:
    data = api_result["items"]
else:
    xbmc.log("API returned no data")
    return []

# WRONG: Direct access without checking
data = url.get_json(api_url)["items"]  # Can raise TypeError!
```

### 3. NHK API Architecture

**Current API**: `api.nhkworld.jp/showsapi/v1/` (October 2025 migration)
**Authentication**: None required (public endpoints)
**Video URLs**: Provided directly in API responses (no scraping needed)

All endpoints are hardcoded in `nhk_api.py`:

```python
NHK_API_BASE = "https://api.nhkworld.jp/showsapi/v1/"
NHK_BASE = "https://www3.nhk.or.jp"
LANG = "en"

rest_url = {
    'homepage_ondemand': f"{NHK_API_BASE}{LANG}/video_episodes?limit=20",
    'get_programs': f"{NHK_API_BASE}{LANG}/video_programs",
    'get_episode_detail': f"{NHK_API_BASE}{LANG}/video_episodes/{{0}}",
    'live_stream_url_1080p': "https://media-tyo.hls.nhkworld.jp/hls/w/live/o-master.m3u8",
    'live_stream_url': "https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8",
}
```

**API Response Format (New vs Old)**:

| Old API         | New API         | Notes                       |
| --------------- | --------------- | --------------------------- |
| `data.episodes` | `items`         | Top-level array             |
| `vod_id`        | `id`            | Episode identifier          |
| `title_clean`   | `title`         | Episode title               |
| Unix timestamp  | ISO 8601 string | Date format                 |
| N/A             | `video.url`     | Video URL included directly |

## Code Style

**Python Standards**:

- PEP 8 style, 4 spaces indentation, 88 char line length
- Type hints where possible
- Docstrings for all public functions/classes
- All configured in `pyproject.toml`

**Development Tools (2025)**:

- **Ruff**: Modern linter & formatter (replaces Black, isort, flake8, pylint)
  - Run: `make format` or `pipenv run ruff format .`
  - Auto-fix: `pipenv run ruff check --fix .`
- **mypy**: Type checking
  - Run: `make type-check` or `pipenv run mypy plugin.video.nhkworldtv/lib`
- **pytest**: Testing with coverage
  - Run: `make test` or `make test-cov`
- **Makefile**: Quick commands for common tasks
  - `make all` - Format, lint, type-check, and test in one command

**VS Code Integration**:
- Auto-format on save (Ruff)
- Integrated testing (Test Explorer)
- Type checking (mypy)
- All configured in `.vscode/settings.json`

**Kodi-Specific**:

- Use `xbmc.log()` for logging (appropriate log levels)
- Handle errors gracefully - never crash Kodi
- Cache API responses (60 minutes minimum)
- Always check URLs exist before playback

**Naming Conventions**:

- Test files: `test_lib_<module_name>.py`
- Modules: `lowercase_with_underscores`
- Constants: `UPPER_CASE_WITH_UNDERSCORES`
- Functions: `lowercase_with_underscores`
- Classes: `PascalCase`

## Project Structure

```
plugin.video.nhkworldtv/
├── lib/
│   ├── nhk_api.py      # API endpoints (hardcoded URLs)
│   ├── url.py          # HTTP requests with retry logic
│   ├── plugin.py       # Main plugin logic and menus
│   ├── vod.py          # Video-on-demand
│   ├── episode.py      # Episode data handling
│   ├── ataglance.py    # At-a-glance news
│   ├── topstories.py   # Top stories news
│   ├── utils.py        # Utility functions
│   └── kodiutils.py    # Kodi helper utilities
├── tests/              # Pytest unit tests
├── resources/          # Settings, translations, media
└── main.py            # Entry point
```

**Removed modules** (PR #140): `api_keys.py`, `nhk_api_parser.py`, `cache_api.py`, `news_programs.py`, `first_run_wizard.py`

## Common Tasks

### Add API Endpoint

1. Add to `nhk_api.rest_url` dictionary in `nhk_api.py`
2. Use via `url.get_json(nhk_api.rest_url['endpoint_name'])`
3. Add null safety checks
4. Write unit tests

### Get Episode List

```python
from lib import vod, url, nhk_api

api_result = url.get_json(nhk_api.rest_url["get_latest_episodes"])
if api_result and "items" in api_result:
    episodes = vod.process_episodes(api_result["items"])
else:
    episodes = []
```

### Add Menu Item

```python
from lib import kodiutils
import xbmcgui, xbmcplugin

li = xbmcgui.ListItem(label="Menu Title")
li.setArt({'thumb': thumb_url, 'fanart': fanart_url})
xbmcplugin.addDirectoryItem(
    handle=kodiutils.get_handle(),
    url=url,
    listitem=li,
    isFolder=True
)
```

### Debug Logging

```python
import xbmc
xbmc.log(f"API URL: {api_url}", xbmc.LOGDEBUG)
xbmc.log(f"Error: {error_message}", xbmc.LOGERROR)
```

## Testing

**Run tests**:

```bash
# Quick command
make test

# All tests with verbose output
pipenv run pytest plugin.video.nhkworldtv/tests/ -v

# With coverage
make test-cov
# or manually:
pipenv run pytest plugin.video.nhkworldtv/tests/ --cov=plugin.video.nhkworldtv/lib --cov-report=html -v

# Specific test file
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib_url.py -v
```

**Current status**: All 178 tests passing, 76% coverage

**Test organization**:
- `test_lib_*.py` - Unit tests for each module
- `test_integration_nhk_api.py` - Integration tests for API endpoints
- All tests use mocking to avoid live API calls where appropriate

**When debugging API issues**:

1. Check endpoints in `nhk_api.py`
2. Verify URLs are correct
3. Check for null responses
4. Add proper error handling
5. Test with `test_integration_nhk_api.py`

## Stream Information

- **Live Stream**: 1080p primary (media-tyo.hls.nhkworld.jp), 720p fallback (masterpl.hls.nhkworld.jp)
- **VOD Streams**: 1080p primary with 720p fallback
- **Codec**: H.264 Main Profile, AAC-LC audio, HLS adaptive streaming
- **Kodi Compatibility**: ✅ Excellent - all codecs fully supported

## Git Workflow

**Branch naming**: `feature/description`, `fix/description`

**Commit format**:

```
<type>: <short description>

<optional detailed description>

Issue number reference
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

**PR Guidelines**: Link to issue, mark as draft if WIP, include test results, document API changes

## Important URLs

- NHK World: https://www3.nhk.or.jp/nhkworld/
- API Base: https://api.nhkworld.jp/showsapi/v1/
- Live Stream (1080p): https://media-tyo.hls.nhkworld.jp/hls/w/live/o-master.m3u8
- Live Stream (720p): https://masterpl.hls.nhkworld.jp/hls/w/live/master.m3u8
- Repository: https://github.com/sbroenne/plugin.video.nhkworldtv
- Official PR: https://github.com/xbmc/repo-plugins/pull/4718
- Kodi Mirror: https://mirrors.kodi.tv/addons/omega/

## Development Environment

**.vscode/** contains:

- `settings.json` - Python, testing, formatting config (Ruff, mypy)
- `launch.json` - Debug configurations
- `extensions.json` - Recommended VS Code extensions

**pyproject.toml** contains:

- Ruff configuration (linter & formatter rules)
- pytest configuration
- mypy type checking configuration
- Coverage settings

**Makefile** provides quick commands:

- `make format` - Auto-format code with Ruff
- `make lint` - Check code quality
- `make type-check` - Run mypy type checking
- `make test` - Run all 178 tests
- `make test-cov` - Tests with HTML coverage report
- `make all` - Run everything (format, lint, type-check, test)

## Quick Decision Guide

**When to update dependencies**: Check Kodi repository → Update addon.xml → Update Pipfile
**When API call fails**: Always check for null, log error, return empty list/dict
**When adding features**: Write tests first, ensure null safety, update documentation
**When tests fail**: Check API endpoints, verify response format, ensure null-safe dict access
**When deploying**: All tests must pass, version number updated, changelog in addon.xml

## When to Ask for Help

- NHK API endpoints change significantly
- Authentication requirements reintroduced
- Major architectural changes needed
- Breaking Kodi API changes discovered
