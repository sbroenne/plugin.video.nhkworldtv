# Test Coverage

## Test Strategy

All API-related tests are **INTEGRATION TESTS** with real API calls.
Unit tests are only used for pure logic/utility functions with no external dependencies.

## Integration Tests (23 tests - Real API calls)

File: `tests/test_integration_nhk_api.py`

### VOD Endpoints (10 tests)
- ✅ Homepage on-demand episodes
- ✅ Program list
- ✅ Latest episodes
- ✅ Episode detail with video URL
- ✅ Categories
- ✅ Most watched episodes
- ✅ All VOD endpoints accessible
- ✅ Episode images present
- ✅ Episode field structure validation
- ✅ Video URL format and accessibility

### Schedule/EPG Endpoints (3 tests)
- ✅ EPG endpoint with dynamic date
- ✅ Current program detection
- ✅ Schedule field structure validation
- ✅ Program thumbnails

### News Endpoints (3 tests)
- ✅ News homepage
- ✅ At-a-Glance news
- ✅ All news endpoints accessible

### Live Stream (2 tests)
- ✅ Live stream URL accessible
- ✅ HLS playlist validation

### API Completeness (2 tests)
- ✅ All endpoints defined in nhk_api.py
- ✅ All endpoints return 200 status

## Unit Tests (19 tests - Logic only, no API calls)

### Episode Class Logic (7 tests)
- Episode creation
- Thumbnail URL construction
- Video info parsing
- Time calculations
- Duration calculations
- Plot formatting

### Utility Functions (7 tests)
- Episode name formatting
- Time conversion
- URL path construction
- Timestamp parsing
- Plot formatting

### API Configuration (1 test)
- Endpoint definitions validation

### URL Utilities (3 tests)
- API request parameter parsing
- JSON parsing
- NHK website URL construction

## Total Coverage

- **Integration Tests**: 23 (Real API validation)
- **Unit Tests**: 19 (Pure logic)
- **Total**: 42 tests, 100% passing ✅

## Running Tests

```bash
# All tests
pipenv run pytest plugin.video.nhkworldtv/tests/ -v

# Integration tests only (slower, requires network)
pipenv run pytest plugin.video.nhkworldtv/tests/test_integration_nhk_api.py -v

# Unit tests only (fast, no network)
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib*.py -v
```

## Key Principles

1. **No mocked API tests** - Mocks provide false confidence
2. **Integration tests validate real APIs** - Catch endpoint changes immediately
3. **Unit tests for logic only** - Fast, deterministic, no external dependencies
4. **100% API coverage** - Every endpoint validated with real calls
