# 1. NHK World TV Kodi Plugin

- [1. NHK World TV Kodi Plugin](#1-nhk-world-tv-kodi-plugin)
  - [1.1. Disclaimer](#11-disclaimer)
  - [1.2. Overview](#12-overview)
  - [1.3. How-to Install](#13-how-to-install)
  - [1.4. Design Goals](#14-design-goals)
    - [1.4.1. Inclusion in the official Kodi Repo](#141-inclusion-in-the-official-kodi-repo)
    - [1.4.2. Performance](#142-performance)
  - [1.5. Known Issues](#15-known-issues)
  - [1.6. Current Development Status](#16-current-development-status)
  - [1.7. Future development roadmap](#17-future-development-roadmap)
  - [1.8. Local development environment](#18-local-development-environment)
  - [1.9. Bugs \& Issues](#19-bugs--issues)
  - [1.10. Origins](#110-origins)

## 1.1. Disclaimer

This plug-in is a fan project and not related in any way to NHK! I built this plugin because NHK does not support Android TV (yet).

## 1.2. Overview

NHK World TV is a plug-in that displays most of the content from [NHK World Japan](https://www3.nhk.or.jp/nhkworld/en/live/) in Kodi.

- **Full HD (1080p) streaming** - Live TV and on-demand content with automatic 720p fallback
- Browse and search through all programs
- Live schedule / EPG
- Top Stories and At a Glance news
- Uses new NHK World API (`api.nhkworld.jp/showsapi/v1/`)

Content is retrieved and played directly from the NHK World web site or their content delivery network using the new NHK World API (`api.nhkworld.jp/showsapi/v1/`).

## 1.3. How-to Install

The plugin is available through the [NHK World TV Development Repository](https://github.com/sbroenne/kodirepo). Install the [repository ZIP file](https://github.com/sbroenne/kodirepo/raw/main/repository.sbroenne/repository.sbroenne-0.0.16.zip) first, then install the plugin from the repository. The plug-in will **auto-update** itself regularly.

**Official Kodi Repository Status**: ✅ **PR submitted** - [PR #4718](https://github.com/xbmc/repo-plugins/pull/4718) is under review for inclusion in the official Kodi repository (Omega v21 and Piers v22).

## 1.4. Design Goals

### 1.4.1. Inclusion in the official Kodi Repo

The design goal for the NHK World TV plug-in is to be included in the official Kodi repo and to include **only** content from the NHK World web site with the focus on the video-on-demand section - in the best possible quality.

**Current Status**: ✅ Submitted - [PR #4718](https://github.com/xbmc/repo-plugins/pull/4718) is under review for Kodi Omega (v21) and Piers (v22). See [SUBMISSION.md](SUBMISSION.md) for the submission process.

If you like to add the other content that can be found in Best Of NHK, please feel free to clone - I will **not** accept PRs for adding content sources outside of NHK World itself.

### 1.4.2. Performance

"Snappiness" was one of my design goals when developing this plug-in. API calls to NHK are cached in memory for a while so that navigation is faster (defaults to 60 minutes).

Episodes are resolved dynamically when you select them for playback.

## 1.5. Known Issues

If you have a problem **after an update**, simply exit Kodi and start it again - or start a different plug-in. This will usually fix it. This is caused by Kodi when you re-use the Python language invoker - which the plug-in does since it improves performance dramatically.

## 1.6. Current Development Status

The plug-in is feature complete and stable.

**Recent Updates (October 2025):**

- Migrated to new NHK World API (`api.nhkworld.jp/showsapi/v1/`)
- Removed authentication requirements (API now public)
- Simplified video URL resolution (URLs provided directly by API)
- API endpoints are hardcoded constants which makes the plug-in more maintainable
- Scheduled unit tests run on Github to alert on breaking changes

The plug-in is localized but translation only exists for English (GB). It runs on Kodi Omega (v21) and Piers (v22).

## 1.7. Future development roadmap

Current priorities:

#- Monitor for NHK API changes

No major feature work planned - the plugin is feature complete. If you have an idea, simply create an issue.

## 1.8. Local development environment

You will find scripts to build the plugin in locally in the [build](../build/) folder. [More Information](build.md)

## 1.9. Bugs & Issues

If you find a bug, or want to fix something directly, that would be awesome! Just use Github and open an issue! Thank you!

## 1.10. Origins

Originally it started as a fork of **Misty's** [Best Of NHK plug-in](https://forum.kodi.tv/showthread.php?tid=196657) but shares zero code with it nowadays. His plug-in also provides additional content like NHK on YouTube - check it out - it is worth it!

**Thank you Misty, awesome work!**

It is not related in any way to the **NHK Live** plugin in the official addon repo.
