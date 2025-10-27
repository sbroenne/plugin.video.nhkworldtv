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

- Live Stream
- On demand programs (by program, latest and most watched, categories and playlist) - you can also browse and search through all programs - ONLY available in 720p
- Live schedule / "EPG"
- Top Stories and At a Glance
- News programs like NEWSLINE, NEWSLINE IN DEPTH and NEWSROOM TOKYO

Content is retrieved and played directly from the NHK World web site or their content delivery network.

NHK used to support 1080P but now (February 2024) only supports 720P.

The plug-in uses a [companion cloud cache service](https://github.com/sbroenne/nhkworldtv-backend) to speed up video play-back because these NHK APIs are very slow.

## 1.3. How-to Install

I submitted the plugin to the official Kodi repo but unfortunately this request was declined. The reason is that the they only accept one plugin per content provider.

For NHK World that is the **NHK Live** plugin.

You can install the plugin by **first** installing the [NHK World TV Development Repository ZIP file](https://github.com/sbroenne/kodirepo/raw/main/repository.sbroenne/repository.sbroenne-0.0.16.zip). The plug-in will **auto-update** itself regularly from this repo.

## 1.4. Design Goals

### 1.4.1. Inclusion in the official Kodi Repo

The design goal for the NHK World TV plug-in is to be included in the official Kodi repo and to include **only** content from the NHK World web site with the focus on the video-on-demand section - in hest best possible quality.

If you like to add the other content that can be found in Best Of NHK, please feel free to clone - I will **not** accept PRs for adding content sources outside of NHK World itself.

### 1.4.2. Performance

"Snappiness" was one of my design goals when developing this plug-in. For example, most calls to NHK are cached (requests-cache) for a while so that navigation is faster (defaults to two hours)

The plug-in uses a companion cloud service to speed up video play-back because these NHK APIs are very slow.

You can disable this in Settings if you do not want to use this - the only downside is that starting playback of video will take a bit longer and that you will loose a bit of UI functionality (e.g. Kodi will not store how much of a program you have already watched)

You can find the source code for the cloud service at [NHK World TV Azure Backend](https://github.com/sbroenne/nhkworldtv-backend).

The cache runs on Azure and is implemented as Azure Functions backed by Cosmos DB. It gets updated with new episodes multiple times per day.

## 1.5. Known Issues

If you have a problem **after an update**, simply exit Kodi and start it again - or start a different plug-in. This will usually fix it. This is caused by Kodi when you re-use the Python language invoker - which the plug-in does since it improves performance dramatically.

## 1.6. Current Development Status

The plug-in is feature complete and stable.

Most of the NHK API is parsed and **not** hard-coded so this should make the plug-in more resilient to changes on the NHK web site. I also run scheduled unit tests on Github to alert me on breaking changes.

The plug-in is localized but translation only exists for English (GB). It only runs on Kodi Nexus.

## 1.7. Future development roadmap

There are no main open topics.

## 1.8. Local development environment

You will find scripts to build the plugin in locally in the [build](../build/) folder. [More Information](build.md)

## 1.9. Bugs & Issues

If you find a bug, or want to fix something directly, that would be awesome! Just use Github and open an issue! Thank you!

## 1.10. Origins

Originally it started as a fork of **Misty's** [Best Of NHK plug-in](https://forum.kodi.tv/showthread.php?tid=196657) but shares zero code with it nowadays. His plug-in also provides additional content like NHK on YouTube - check it out - it is worth it!

**Thank you Misty, awesome work!**

It is not related in any way to the **NHK Live** plugin in the official addon repo.
