# Development Guide

Complete guide for developing the NHK World TV Kodi plugin.

## Table of Contents

- [Quick Start](#quick-start)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# Clone and setup
git clone https://github.com/sbroenne/plugin.video.nhkworldtv.git
cd plugin.video.nhkworldtv

# Install dependencies
pipenv install --dev
pipenv run build/install_packages.sh  # Install routing package

# Run tests
make test

# Format and lint
make format lint

# Build plugin
build/build.sh
```

## Development Environment

### Required Software

- **Python 3.12+**: Required for Kodi Omega/Piers compatibility
- **Pipenv**: Dependency management
- **Git**: Version control
- **VS Code** (recommended): Configured with all extensions

### Python Dependencies

**Runtime Dependencies** (Pipfile):
- `requests >= 2.32.3`: HTTP client
- `pytz >= 2024.2`: Timezone handling
- `routing`: Kodi URL routing (manual install)

**Development Dependencies** (Pipfile):
- `pytest >= 8.0.0`: Test framework
- `pytest-cov >= 6.0.0`: Coverage reporting
- `ruff >= 0.8.0`: Linter & formatter
- `mypy >= 1.13.0`: Type checking

### VS Code Setup

The repository includes complete VS Code configuration in `.vscode/`:

**settings.json** - Auto-format on save, testing, type checking
**launch.json** - Debug configurations:
- Debug Python File
- Debug Pytest (Current File)
- Debug Pytest (All Tests)

**extensions.json** - Recommended extensions:
- Python (ms-python.python)
- Ruff (charliermarsh.ruff)
- Mypy Type Checker (ms-python.mypy-type-checker)
- Test Explorer UI (hbenl.vscode-test-explorer)
- GitLens (eamodio.gitlens)
- Even Better TOML (tamasfe.even-better-toml)

**Features**:
- ✅ Auto-format on save with Ruff
- ✅ Integrated testing with Test Explorer
- ✅ Type checking on save
- ✅ IntelliSense with auto-imports
- ✅ Debug breakpoints for Python and tests

### Configuration Files

**pyproject.toml** - Modern Python project configuration (PEP 518):
- Ruff linter/formatter settings
- pytest configuration
- mypy type checking rules
- Coverage settings

**Makefile** - Common development commands:
```bash
make install      # Install all dependencies
make format       # Auto-format code with Ruff
make lint         # Check code quality
make type-check   # Run mypy type checking
make test         # Run all tests
make test-cov     # Tests with HTML coverage report
make clean        # Remove caches and build artifacts
make all          # Run everything: format, lint, type-check, test
```

**.editorconfig** - Universal editor settings:
- 4 spaces indentation for Python
- Unix line endings (LF)
- UTF-8 encoding
- Trim trailing whitespace
- 88 character line length

**.gitignore** - Excludes:
- Python caches (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`)
- Build artifacts (`dist/`, `build/`, `*.pyc`)
- IDE files (`.vscode/` kept for team consistency)
- Coverage reports (`htmlcov/`, `.coverage`)

## Project Structure

```
plugin.video.nhkworldtv/
├── .github/
│   ├── workflows/           # GitHub Actions (tests, releases)
│   └── copilot-instructions.md  # AI coding assistant rules
├── .vscode/                 # VS Code configuration
│   ├── settings.json        # Editor, formatting, testing
│   ├── launch.json          # Debug configurations
│   └── extensions.json      # Recommended extensions
├── build/                   # Build scripts
│   ├── build.sh             # Create plugin ZIP
│   ├── copy_local_wsl.sh    # Deploy to local Kodi (WSL)
│   └── install_packages.sh  # Install routing package
├── docs/                    # Documentation
│   ├── README.md            # Main documentation
│   ├── build.md             # Build instructions
│   ├── DEVELOPMENT.md       # This file
│   └── SUBMISSION.md        # Kodi repo submission info
├── plugin.video.nhkworldtv/ # Main plugin
│   ├── main.py              # Entry point
│   ├── addon.xml            # Plugin metadata
│   ├── lib/                 # Core modules
│   │   ├── plugin.py        # Main plugin logic
│   │   ├── nhk_api.py       # API endpoints
│   │   ├── url.py           # HTTP client with caching
│   │   ├── vod.py           # Video-on-demand
│   │   ├── episode.py       # Episode data model
│   │   ├── ataglance.py     # At-a-glance news
│   │   ├── topstories.py    # Top stories news
│   │   ├── utils.py         # Utility functions
│   │   └── kodiutils.py     # Kodi helper functions
│   ├── resources/
│   │   ├── settings.xml     # Plugin settings UI
│   │   ├── language/        # Translations (en_GB)
│   │   └── media/           # Icons, fanart
│   └── tests/               # Unit & integration tests
│       ├── test_lib_*.py    # Unit tests per module
│       └── test_integration_nhk_api.py  # API integration tests
├── .editorconfig            # Universal editor config
├── .gitignore               # Git exclusions
├── Makefile                 # Quick commands
├── Pipfile                  # Python dependencies
├── Pipfile.lock             # Locked dependency versions
├── pyproject.toml           # Modern Python config (Ruff, pytest, mypy)
└── README.md                # Project overview
```

### Key Modules

**plugin.py** (51% coverage):
- Main plugin logic and menu system
- Route handlers for Kodi navigation
- Difficult to test without complex Kodi mocking

**nhk_api.py** (100% coverage):
- Hardcoded API endpoint URLs
- No logic, just constants

**url.py** (99% coverage):
- HTTP client with retry logic
- In-memory caching (60 minutes default)
- Session management

**vod.py** (95% coverage):
- Process VOD episodes
- Extract episode metadata
- Image URL handling

**episode.py** (100% coverage):
- Episode data model
- Time difference calculations
- Playability checks

**utils.py** (100% coverage):
- Date/time formatting
- URL helpers
- General utilities

**kodiutils.py**:
- Kodi-specific helpers
- Settings management
- Directory info

## Development Workflow

### Standard Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes** with auto-format on save in VS Code

3. **Run quality checks**:
   ```bash
   make format  # Auto-format and fix
   make lint    # Check remaining issues
   make type-check  # Type checking
   ```

4. **Write tests** for new functionality

5. **Run tests**:
   ```bash
   make test     # Quick test run
   make test-cov # With coverage report
   ```

6. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

7. **Push and create PR**:
   ```bash
   git push origin feature/my-feature
   ```

### Commit Message Format

Follow conventional commits:

```
<type>: <short description>

<optional detailed description>

<optional issue reference>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks
- `style`: Code style changes (formatting)

**Examples**:
```
feat: add 1080p stream support

Implements fallback from 1080p to 720p streams
when high quality is unavailable.

Closes #42
```

```
fix: handle null API responses in episode list

Added null safety checks to prevent crashes
when NHK API returns empty responses.
```

## Testing

### Test Organization

**Unit Tests** (`test_lib_*.py`):
- One file per module
- Mock external dependencies
- Fast execution
- Test individual functions

**Integration Tests** (`test_integration_nhk_api.py`):
- Test real API endpoints
- Verify API contract
- Detect breaking changes
- Slower execution

### Running Tests

**All tests**:
```bash
make test
# or
pipenv run pytest plugin.video.nhkworldtv/tests/ -v
```

**Specific test file**:
```bash
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib_url.py -v
```

**Specific test function**:
```bash
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib_url.py::test_get_json -v
```

**With coverage**:
```bash
make test-cov
# Opens htmlcov/index.html automatically
```

**Watch mode** (re-run on file changes):
```bash
pipenv run pytest-watch plugin.video.nhkworldtv/tests/
```

### Writing Tests

**Example unit test**:
```python
def test_format_date():
    """Test date formatting utility"""
    from lib import utils
    
    result = utils.format_date("2025-11-09T10:00:00Z")
    assert result == "Nov 9, 2025"
```

**Example with mocking**:
```python
from unittest.mock import patch

def test_get_episodes_with_api_error():
    """Test episode list handles API errors gracefully"""
    from lib import vod
    
    with patch('lib.url.get_json', return_value=None):
        result = vod.get_episode_list("program_id")
        assert result == []  # Should return empty list, not crash
```

**Test naming conventions**:
- File: `test_lib_<module_name>.py`
- Function: `test_<functionality>_<condition>`
- Use descriptive names that explain what's being tested

### Current Test Coverage

**Overall**: 76% (178 tests)

**By Module**:
- episode.py: 100%
- utils.py: 100%
- nhk_api.py: 100%
- url.py: 99%
- vod.py: 95%
- plugin.py: 51% (route handlers difficult to test)

**Coverage Goals**:
- ✅ All business logic: 100%
- ✅ Data models: 100%
- ✅ Utility functions: 100%
- ⚠️ Plugin routes: 51% (acceptable - requires Kodi mocking)

## Code Quality

### Linting & Formatting

**Ruff** (2025 Modern Standard):
- Replaces Black, isort, flake8, pylint, autoflake
- Fast (10-100x faster than alternatives)
- Comprehensive rule set
- Auto-fix capabilities

**Configuration** (pyproject.toml):
```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "N", "UP", "B", "C4", "SIM", "PTH", "RUF"]
```

**Usage**:
```bash
# Auto-format
make format
# or
pipenv run ruff format .

# Check for issues
make lint
# or
pipenv run ruff check .

# Auto-fix issues
pipenv run ruff check --fix .
```

### Type Checking

**mypy** configuration (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Gradual typing
```

**Usage**:
```bash
make type-check
# or
pipenv run mypy plugin.video.nhkworldtv/lib
```

**Best Practices**:
- Add type hints to new functions
- Use `Optional[T]` for nullable values
- Document complex types in docstrings
- Gradual adoption (not enforced on existing code)

### Pre-commit Checks

Before committing, run:
```bash
make all  # Format, lint, type-check, test
```

Or individually:
```bash
make format      # Auto-format code
make lint        # Check code quality
make type-check  # Type checking
make test        # Run all tests
```

## Debugging

### VS Code Debugging

**Debug Current Python File**:
1. Open file in editor
2. Set breakpoints (click left gutter)
3. Press `F5` or Run > Start Debugging
4. Select "Python Debugger: Current File"

**Debug Specific Test**:
1. Open test file
2. Set breakpoint in test
3. Press `F5`
4. Select "Python Debugger: Pytest (Current File)"

**Debug All Tests**:
1. Press `F5`
2. Select "Python Debugger: Pytest (All Tests)"

### Logging

**Kodi logging**:
```python
import xbmc

# Log levels
xbmc.log("Debug message", xbmc.LOGDEBUG)
xbmc.log("Info message", xbmc.LOGINFO)
xbmc.log("Warning message", xbmc.LOGWARNING)
xbmc.log("Error message", xbmc.LOGERROR)

# Format strings
xbmc.log(f"API URL: {api_url}", xbmc.LOGDEBUG)
xbmc.log(f"Processing {len(items)} items", xbmc.LOGINFO)
```

**Viewing Kodi logs**:
- Linux: `~/.kodi/temp/kodi.log`
- Windows: `%APPDATA%\Kodi\kodi.log`
- macOS: `~/Library/Logs/kodi.log`

**Test debugging**:
```python
def test_something():
    result = my_function()
    print(f"Result: {result}")  # Visible with pytest -v
    assert result == expected
```

## Common Tasks

### Add New API Endpoint

1. **Add endpoint to nhk_api.py**:
   ```python
   rest_url = {
       # ... existing endpoints ...
       'new_endpoint': f"{NHK_API_BASE}{LANG}/new_path",
   }
   ```

2. **Use in code**:
   ```python
   from lib import url, nhk_api
   
   api_result = url.get_json(nhk_api.rest_url['new_endpoint'])
   if api_result and "items" in api_result:
       # Process data
       pass
   ```

3. **Add test**:
   ```python
   def test_new_endpoint():
       from lib import nhk_api
       assert 'new_endpoint' in nhk_api.rest_url
       assert nhk_api.rest_url['new_endpoint'].startswith('https://')
   ```

### Add New Menu Item

1. **Add route in plugin.py**:
   ```python
   @plugin.route('/new_menu')
   def show_new_menu():
       """Display new menu"""
       items = get_menu_items()
       for item in items:
           li = xbmcgui.ListItem(label=item['title'])
           xbmcplugin.addDirectoryItem(
               handle=kodiutils.get_handle(),
               url=plugin.url_for(play_item, item_id=item['id']),
               listitem=li,
               isFolder=False
           )
       xbmcplugin.endOfDirectory(kodiutils.get_handle())
   ```

2. **Add to main menu** (if needed):
   ```python
   @plugin.route('/')
   def index():
       # ... existing menu items ...
       add_menu_item(
           label="New Menu",
           url=plugin.url_for(show_new_menu),
           is_folder=True
       )
   ```

### Update Dependencies

**Check Kodi repository first**:
```bash
# Visit https://mirrors.kodi.tv/addons/omega/
# Find the available version
```

**Update addon.xml**:
```xml
<requires>
    <import addon="xbmc.python" version="3.0.2"/>
    <import addon="script.module.requests" version="2.32.3"/>
    <!-- Add/update dependency -->
</requires>
```

**Update Pipfile** to match:
```toml
[packages]
requests = ">=2.32.3"
```

**Install**:
```bash
pipenv update
pipenv run build/install_packages.sh  # If updating routing
```

### Build and Deploy

**Build plugin ZIP**:
```bash
chmod u+x build/build.sh
build/build.sh
```

**Deploy to local Kodi** (WSL2 on Windows 11):
```bash
# Edit build/copy_local_wsl.sh to set your Kodi path
chmod u+x build/copy_local_wsl.sh
build/copy_local_wsl.sh
```

**Test in Kodi**:
1. Navigate to Add-ons
2. Select "My Add-ons"
3. Select "Video Add-ons"
4. Find "NHK World TV"
5. Test functionality

## Troubleshooting

### Import Errors

**Symptom**: `ModuleNotFoundError: No module named 'routing'`

**Solution**:
```bash
pipenv run build/install_packages.sh
```

### Test Failures After Ruff Formatting

**Symptom**: Syntax errors or unexpected test failures

**Solution**:
```bash
# Check what changed
git diff

# Run linter to find issues
make lint

# Manually fix any problems
# Then re-run tests
make test
```

### VS Code Not Finding Modules

**Symptom**: Import errors in VS Code but tests pass

**Solution**:
```bash
# Get virtualenv path
pipenv --venv

# Update .vscode/settings.json:
{
  "python.defaultInterpreterPath": "/path/to/venv/bin/python"
}

# Reload VS Code
# Cmd/Ctrl + Shift + P > "Developer: Reload Window"
```

### Coverage Report Not Generating

**Symptom**: `make test-cov` doesn't create HTML report

**Solution**:
```bash
# Manual coverage generation
pipenv run pytest plugin.video.nhkworldtv/tests/ \
  --cov=plugin.video.nhkworldtv/lib \
  --cov-report=html \
  -v

# Check htmlcov/ directory was created
ls -la htmlcov/

# Open manually if needed
xdg-open htmlcov/index.html  # Linux
open htmlcov/index.html       # macOS
```

### Kodi Cache Issues

**Symptom**: Changes not appearing in Kodi

**Solution**:
1. Exit Kodi completely
2. Clear addon cache:
   ```bash
   rm -rf ~/.kodi/addons/plugin.video.nhkworldtv/
   ```
3. Reinstall plugin
4. Start Kodi

### API Changes Detected

**Symptom**: Integration tests failing

**Solution**:
1. Check API response format:
   ```bash
   curl https://api.nhkworld.jp/showsapi/v1/en/video_episodes?limit=1
   ```
2. Compare with expected format in tests
3. Update code to handle new format
4. Update tests to match new API
5. Document changes in commit message

### Performance Issues

**Symptom**: Slow plugin navigation

**Solution**:
1. Check cache settings in `url.py`
2. Verify cache is working:
   ```python
   # Add debug logging
   xbmc.log(f"Cache hit: {cache_key}", xbmc.LOGDEBUG)
   ```
3. Increase cache duration if needed
4. Profile slow operations

## Additional Resources

- [Kodi Python API Documentation](https://codedocs.xyz/xbmc/xbmc/)
- [NHK World Website](https://www3.nhk.or.jp/nhkworld/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/sbroenne/plugin.video.nhkworldtv/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sbroenne/plugin.video.nhkworldtv/discussions)
- **Kodi Forum**: [NHK World TV Thread](https://forum.kodi.tv/)

---

**Last Updated**: November 2025
**Plugin Version**: See `addon.xml`
**Minimum Kodi**: Omega (v21)
