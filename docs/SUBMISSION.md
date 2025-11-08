# Submitting NHK World TV Plugin to Official Kodi Repository

This guide explains how to submit the plugin to the official Kodi add-on repository.

## Prerequisites

Before submitting, ensure:

1. **All tests pass**: Run `pipenv run pytest plugin.video.nhkworldtv/tests/ -v`
2. **Addon passes validation**: The `addon-checker.yml` workflow validates your addon automatically
3. **Version number is updated**: Update version in `plugin.video.nhkworldtv/addon.xml`
4. **Changelog is updated**: Add changes to the `<news>` section in `addon.xml`
5. **Assets are present**: Ensure icon.png, fanart.jpg, and screenshots are in `resources/`

## GitHub Secrets Required

Set up these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

- `GH_TOKEN`: Personal Access Token with `repo` scope
- `EMAIL`: Your email address for git commits

## Validation Process

### Automatic Validation

Every push to main and pull request automatically runs `kodi-addon-checker` for both Omega and Piers branches. Check the Actions tab to see results.

### Manual Local Validation

```bash
# Install kodi-addon-checker
pip install kodi-addon-checker

# Validate for Kodi Omega (v21)
kodi-addon-checker --branch=omega plugin.video.nhkworldtv

# Validate for Kodi Piers (v22)
kodi-addon-checker --branch=piers plugin.video.nhkworldtv
```

## Submission Methods

### Method 1: Automated Submission (Recommended)

Use the GitHub Actions workflow to automatically create a PR to the official repository:

1. Go to **Actions** tab in your GitHub repository
2. Select **"Submit addon to Kodi repo"** workflow
3. Click **"Run workflow"**
4. Select target branch:
   - `omega` for Kodi v21
   - `piers` for Kodi v22
5. Click **"Run workflow"** button

The workflow will:

- Validate your addon with `kodi-addon-checker`
- Fork the official `xbmc/repo-plugins` repository
- Create a branch with your addon
- Submit a pull request to the official repository

### Method 2: Manual Submission

If you prefer manual control:

#### Step 1: Install kodi-addon-submitter

```bash
pip install git+https://github.com/xbmc/kodi-addon-submitter.git
```

#### Step 2: Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Step 3: Set GitHub Token

```bash
export GH_USERNAME="your-github-username"
export GH_TOKEN="your-github-token"
export EMAIL="your.email@example.com"
```

#### Step 4: Submit to Kodi Repository

For **Kodi Omega (v21)**:

```bash
submit-addon -r repo-plugins -b omega --pull-request plugin.video.nhkworldtv
```

For **Kodi Piers (v22)**:

```bash
submit-addon -r repo-plugins -b piers --pull-request plugin.video.nhkworldtv
```

### Method 3: Completely Manual (Fork and PR)

1. Fork https://github.com/xbmc/repo-plugins
2. Clone your fork locally
3. Checkout the appropriate branch (`omega` or `piers`)
4. Copy your addon folder to the repository root
5. Create a commit with format: `[plugin.video.nhkworldtv] 1.5.0`
6. Push to your fork
7. Open a pull request to the official repository

## After Submission

1. **Monitor your PR**: The official Kodi team will review your submission
2. **Automated checks run**: GitHub Actions will run `kodi-addon-checker` on your PR
3. **Address feedback**: Respond to any review comments
4. **Wait for merge**: Once approved, your addon will be merged and available in the official repository

## Common Issues

### Validation Errors

If `kodi-addon-checker` reports errors:

1. Read the error message carefully
2. Fix the issue in your code
3. Update version number
4. Re-run validation locally
5. Submit updated version

### Dependency Version Mismatches

Check that all dependency versions in `addon.xml` exist in the Kodi repository:

- Visit: https://mirrors.kodi.tv/addons/omega/
- Verify each `<import>` version exists

### PR Rejected

Common reasons for rejection:

- Duplicate functionality (another similar addon exists)
- Copyright/legal issues
- Code quality concerns
- Missing or incorrect metadata

## References

- [Official Kodi Add-on Submission Guide](https://kodi.wiki/view/Submitting_Add-ons)
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development)
- [xbmc/repo-plugins Repository](https://github.com/xbmc/repo-plugins)
- [Kodi Add-on Checker](https://github.com/xbmc/addon-check)
- [Contributing Guidelines](https://github.com/xbmc/repo-plugins/blob/master/CONTRIBUTING.md)

## Current Status

As of November 2025:

- **Current Kodi Versions**: Omega (v21), Piers (v22)
- **Plugin Version**: Check `addon.xml` for current version
- **Python Version**: Python 3.12
- **Minimum Kodi Version**: Omega (v21)

## Questions?

- [Kodi Forum Thread](https://forum.kodi.tv/showthread.php?tid=353215)
- [GitHub Issues](https://github.com/sbroenne/plugin.video.nhkworldtv/issues)
