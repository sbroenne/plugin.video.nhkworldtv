# Kodi Repository Submission Update - November 2025

This document summarizes the changes made to update the plugin for submission to the official Kodi repository.

## What Was Updated

### 1. GitHub Actions Workflows

#### `.github/workflows/addon_submit.yml`

- ✅ Updated from `nexus` to support `omega` and `piers` branches
- ✅ Added branch selection via workflow_dispatch input
- ✅ Added validation step with `kodi-addon-checker` before submission
- ✅ Updated to use official `xbmc/kodi-addon-submitter` tool
- ✅ Improved error handling and git configuration

#### `.github/workflows/addon_repo_push.yml`

- ✅ Updated from `nexus` to support `omega` and `piers` branches
- ✅ Added branch selection via workflow_dispatch input
- ✅ Added validation step before pushing
- ✅ Updated tooling to modern versions

#### `.github/workflows/release.yml`

- ✅ Added validation job that runs before building release
- ✅ Updated to validate against Omega branch
- ✅ Enhanced release notes with changelog and compatibility info
- ✅ Updated Python setup action to v5

#### `.github/workflows/addon-checker.yml` (NEW)

- ✅ Created new workflow for automatic validation on PRs and pushes
- ✅ Validates against both Omega and Piers branches
- ✅ Runs on all main branch changes to catch issues early

### 2. Addon Configuration

#### `plugin.video.nhkworldtv/.kodiignore` (NEW)

- ✅ Created to exclude development files from addon packaging
- ✅ Excludes test files, cache files, SVG files, and development artifacts
- ✅ Ensures clean submission without warnings

### 3. Documentation

#### `docs/SUBMISSION.md` (NEW)

Comprehensive submission guide including:

- ✅ Prerequisites and validation requirements
- ✅ GitHub secrets setup instructions
- ✅ Three submission methods (automated, semi-automated, manual)
- ✅ Troubleshooting common issues
- ✅ Links to official Kodi resources
- ✅ Current status and compatibility information

#### `README.md`

- ✅ Added link to new submission guide

## Key Changes Summary

### From (Old)

- Targeted: Kodi Nexus (v20) - outdated
- Tool: romanvm/kodi-addon-submitter (old fork)
- No validation before submission
- Manual branch specification
- No PR validation workflow

### To (Current)

- Targets: Kodi Omega (v21) and Piers (v22) - current versions
- Tool: xbmc/kodi-addon-submitter (official)
- Automatic validation with kodi-addon-checker
- User-friendly branch selection dropdown
- Automatic PR validation on all changes

## How to Use

### Option 1: Automated Submission (Recommended)

1. Go to **Actions** → **Submit addon to Kodi repo**
2. Click **Run workflow**
3. Select branch: `omega` or `piers`
4. Click **Run workflow**

The action will validate and create a PR automatically.

### Option 2: Manual Validation

```bash
# Validate locally before submission
pipenv run kodi-addon-checker --branch=omega plugin.video.nhkworldtv
```

### Option 3: Completely Manual

Follow the detailed instructions in `docs/SUBMISSION.md`.

## Prerequisites

Ensure these GitHub secrets are set:

- `GH_TOKEN` - Personal Access Token with repo scope
- `EMAIL` - Your email for git commits

## Validation Results

Current validation status (November 2025):

- ✅ Addon structure: Valid
- ✅ XML validation: Valid
- ✅ Assets (icon, fanart, screenshots): Valid
- ✅ PO files: Valid
- ⚠️ Warnings: 45 (mostly cache files - now excluded via .kodiignore)

## Next Steps

1. **Test the workflow**: Run the addon-checker workflow to verify it passes
2. **Update version**: Bump version in `addon.xml` if needed
3. **Submit**: Use the automated workflow to submit to official repository
4. **Monitor**: Watch the PR for feedback from Kodi team

## Important Notes

- The official Kodi repository uses separate branches for each version
- Omega (v21) is the minimum supported version for this addon
- Piers (v22) is the latest version
- All dependency versions must exist in the Kodi repository mirror
- The addon must pass kodi-addon-checker validation to be accepted

## References

- [Official Submission Guide](https://kodi.wiki/view/Submitting_Add-ons)
- [Kodi repo-plugins](https://github.com/xbmc/repo-plugins)
- [kodi-addon-checker](https://github.com/xbmc/addon-check)
- [Our Detailed Guide](docs/SUBMISSION.md)

## Compatibility Matrix

| Kodi Version | Branch | Status      | Supported |
| ------------ | ------ | ----------- | --------- |
| Nexus (v20)  | nexus  | End of Life | ❌ No     |
| Omega (v21)  | omega  | Current     | ✅ Yes    |
| Piers (v22)  | piers  | Latest      | ✅ Yes    |

---

**Date**: November 8, 2025
**Updated by**: GitHub Copilot
**Status**: Ready for submission
