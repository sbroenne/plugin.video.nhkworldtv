# Local Build Instructions

Minimum supported Kodi version is Omega (v21) and Python 3.12.

## Development Setup

### Prerequisites

Install system dependencies:

```bash
sudo apt install pipenv  # Ubuntu/Debian
```

### Python Environment Setup

1. **Install all dependencies** (including dev tools):

   ```bash
   pipenv install --dev
   ```

   This installs:
   - Runtime dependencies: requests, pytz, routing
   - Dev dependencies: pytest, pytest-cov, ruff, mypy

2. **Install routing package** (not in PyPI):

   ```bash
   pipenv run build/install_packages.sh
   ```

   Only needed once after initial setup.

### Development Tools (2025 Modern Stack)

The project uses modern Python tooling configured in `pyproject.toml`:

- **Ruff**: Fast linter & formatter (replaces Black, isort, flake8, pylint)
- **mypy**: Type checking
- **pytest**: Testing framework with 178 tests (76% coverage)
- **Makefile**: Quick commands for common tasks

**Quick Commands:**

```bash
make format      # Auto-format and fix code style
make lint        # Check code quality
make type-check  # Run type checking
make test        # Run all tests
make test-cov    # Run tests with coverage report
make all         # Run everything: format, lint, type-check, test
```

**Manual Commands:**

```bash
# Format code
pipenv run ruff format .
pipenv run ruff check --fix .

# Lint code
pipenv run ruff check .

# Type checking
pipenv run mypy plugin.video.nhkworldtv/lib

# Run tests
pipenv run pytest plugin.video.nhkworldtv/tests/ -v

# Coverage report
pipenv run pytest plugin.video.nhkworldtv/tests/ --cov=plugin.video.nhkworldtv/lib --cov-report=html
```

### VS Code Setup

The repository includes complete VS Code configuration:

- **Auto-format on save** with Ruff
- **Integrated testing** (Test Explorer)
- **Type checking** with mypy
- **Debug configurations** for Python and pytest

**Recommended Extensions** (see `.vscode/extensions.json`):
- Python (ms-python.python)
- Ruff (charliermarsh.ruff)
- Mypy Type Checker (ms-python.mypy-type-checker)
- Test Explorer
- GitLens

VS Code will prompt to install these when you open the project.

## Build Plugin

Use [Kodi Addon Submitter](https://github.com/xbmc/kodi-addon-submitter) to create the plugin ZIP file:

```bash
chmod u+x build/build.sh
build/build.sh
```

The resulting ZIP file will be in the project root folder.

## Deploy to Local Kodi (WSL2 on Windows 11)

The [copy_local_wsl script](../build/copy_local_wsl.sh) copies the plugin to `dist/` and then to your local Kodi installation.

**Note**: This script is specific to Windows 11 with WSL2 but can be adapted to your environment.

Edit the `local_kodi` variable to match your Kodi installation path:

```bash
chmod u+x build/copy_local_wsl.sh
build/copy_local_wsl.sh
```

## Testing

### Run All Tests

```bash
pipenv run pytest plugin.video.nhkworldtv/tests/ -v
```

**Current Status**: 178 tests, 76% coverage

### Run Specific Tests

```bash
# Single test file
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib_url.py -v

# Single test function
pipenv run pytest plugin.video.nhkworldtv/tests/test_lib_url.py::test_get_json -v
```

### Coverage Report

```bash
# Generate HTML report
pipenv run pytest plugin.video.nhkworldtv/tests/ --cov=plugin.video.nhkworldtv/lib --cov-report=html -v

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## GitHub Actions

Two automated workflows:

1. **Build Release** - Creates plugin ZIP on tags
2. **Unit Tests** - Runs all 178 tests on every push

See [.github/workflows/](../.github/workflows/) for details.

## Troubleshooting

### Import Errors

If you see import errors, ensure the routing package is installed:

```bash
pipenv run build/install_packages.sh
```

### Test Failures

1. Check that all dependencies are installed: `pipenv install --dev`
2. Verify Python version: `pipenv run python --version` (should be 3.12+)
3. Clear caches: `pipenv clean` then `pipenv install --dev`

### VS Code Not Finding Interpreter

Update the Python interpreter path in `.vscode/settings.json`:

```bash
# Get virtualenv path
pipenv --venv

# Update settings.json with the path + /bin/python
```
