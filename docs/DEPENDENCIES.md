# Dependency Version Management

## Overview

All dependencies for this Kodi addon **MUST** match versions available in the official Kodi addon repository. This is a hard requirement for addon approval and distribution.

## Verification Process (Updated January 2025)

### Step 1: Always Check Kodi Repository First

Before making any dependency changes:

1. Navigate to https://mirrors.kodi.tv/addons/omega/
2. Search for the dependency:
   - Script modules: `script.module.<name>/`
   - Binary addons: `<name>+<platform>/` (e.g., `inputstream.adaptive+android-aarch64/`)
3. Verify the available versions
4. **ONLY** use versions that exist in the repository

### Step 2: Update addon.xml

Update `plugin.video.nhkworldtv/addon.xml` with verified versions:

```xml
<requires>
    <import addon="xbmc.python" version="3.0.0"/>
    <import addon="script.module.requests" version="2.31.0"/>
    <import addon="script.module.pytz" version="2023.3.0"/>
    <import addon="script.module.routing" version="0.2.3"/>
    <import addon="script.module.tzlocal" version="5.0.1"/>
    <import addon="inputstream.adaptive" version="21.5.16"/>
</requires>
```

### Step 3: Update Pipfile

Update `Pipfile` to match `addon.xml`:

```toml
[packages]
requests = "==2.31.0"
pytz = "==2023.3.0"
tzlocal = "==5.0.1"
```

**Note**: `routing` is Kodi-specific and doesn't need to be in Pipfile. `requests-cache` was removed in v1.5.0 (replaced with in-memory caching).

## Current Dependencies (Verified January 2025)

| Dependency | Version | Kodi Repo | Status |
|------------|---------|-----------|--------|
| script.module.requests | 2.31.0 | [Link](https://mirrors.kodi.tv/addons/omega/script.module.requests/) | ✅ Available |
| script.module.pytz | 2023.3.0 | [Link](https://mirrors.kodi.tv/addons/omega/script.module.pytz/) | ✅ Available |
| script.module.routing | 0.2.3 | [Link](https://mirrors.kodi.tv/addons/omega/script.module.routing/) | ✅ Available |
| script.module.tzlocal | 5.0.1 | [Link](https://mirrors.kodi.tv/addons/omega/script.module.tzlocal/) | ✅ Available |
| inputstream.adaptive | 21.5.16 | [Link](https://mirrors.kodi.tv/addons/omega/inputstream.adaptive+android-aarch64/) | ✅ Available |

**Note**: `script.module.requests-cache` was removed in v1.5.0 and replaced with lightweight in-memory caching.

## Handling Dependabot Alerts

**IMPORTANT**: When Dependabot or other security scanners report vulnerabilities:

1. ❌ **DO NOT** immediately update to the suggested version
2. ✅ **DO** check if the suggested version exists in Kodi repository
3. ✅ **DO** verify against https://mirrors.kodi.tv/addons/omega/
4. ❌ **DO NOT** use versions not available in Kodi repo

### Example: requests Vulnerability

If Dependabot suggests updating `requests` from 2.31.0 to 2.32.0:

1. Check https://mirrors.kodi.tv/addons/omega/script.module.requests/
2. Verify 2.32.0 exists
3. If YES: Update addon.xml and Pipfile
4. If NO: Cannot update, must wait for Kodi team

## Binary Addons

Binary addons like `inputstream.adaptive` have platform-specific builds:

```
inputstream.adaptive+android-aarch64/
inputstream.adaptive+android-armv7/
inputstream.adaptive+osx-arm64/
inputstream.adaptive+osx-x86_64/
inputstream.adaptive+windows-i686/
inputstream.adaptive+windows-x86_64/
```

In `addon.xml`, reference without platform suffix:

```xml
<import addon="inputstream.adaptive" version="21.5.16"/>
```

## Common Issues

### "Why can't I use the latest version?"

Kodi manages dependencies through its own repository. Even if a newer version exists on PyPI or GitHub, it must first be:
1. Packaged for Kodi
2. Tested against Kodi
3. Published to the Kodi repository

### "My dependency has a security vulnerability"

Security updates follow the same process:
1. Check if a patched version exists in Kodi repo
2. If YES: Update
3. If NO: Report to Kodi team and wait

### "Dependabot keeps creating PRs"

Configure `.github/dependabot.yml` to ignore updates or reduce frequency. See [GitHub's documentation](https://docs.github.com/en/code-security/dependabot).

## Version History

| Date | Change | Reason |
|------|--------|--------|
| Jan 2025 | All deps verified at current versions | Initial optimization work |
| Oct 2024 | Migration to new NHK API | API endpoint changes |
| 2023 | Initial versions set | Original development |

## Quick Reference Commands

```bash
# Check current versions in addon.xml
grep -A 10 "<requires>" plugin.video.nhkworldtv/addon.xml

# Check current versions in Pipfile
grep -A 10 "[packages]" Pipfile

# Verify a specific dependency in Kodi repo
curl -s https://mirrors.kodi.tv/addons/omega/script.module.requests/ | grep ".zip"
```

## Tools

- **Kodi Addon Repository Browser**: https://mirrors.kodi.tv/addons/omega/
- **Official Kodi Forum**: https://forum.kodi.tv/
- **Kodi Wiki - Add-on Development**: https://kodi.wiki/view/Add-on_development

## Automation

Consider creating a GitHub Action to:
1. Periodically check Kodi repo for new versions
2. Alert when dependencies can be safely updated
3. Validate addon.xml matches available versions

Example workflow location: `.github/workflows/dependency-check.yml`

## Support

For questions about:
- **Kodi dependency versions**: Ask in [Kodi Forums](https://forum.kodi.tv/)
- **This addon specifically**: Open an issue on GitHub
- **Security vulnerabilities**: Report via GitHub Security Advisories
