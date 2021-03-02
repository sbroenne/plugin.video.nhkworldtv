# NHK World TV Kodi Plugin

## Disclaimer

This plug-in is a fan project and not related in any way to NHK! I built this plugin because NHK does not support Android TV (yet).

## Overview

NHK World TV is a plug-in that displays most of the content from [NHK World Japan](https://www3.nhk.or.jp/nhkworld/en/live/) in Kodi in the highest possible quality (1080p) where available.

Tested on Kodi 18.6+ and 19 with the default Estuary skin.

## How-to Install

### Kodi 19 / Matrix (current Kodi version)

You can install the current Matrix version of the plugin by installing the [NHK World TV Development Repository ZIP file](https://github.com/sbroenne/kodirepo/tree/master/repository.sbroenne/repository.sbroenne-0.0.13.zip). The plug-in will auto-update itself regularly from this repo.

You can also download the Leia version from a [releases](https://github.com/sbroenne/plugin.video.nhkworldtv/releases/download/v1.0.0/plugin.video.nhkworldtv-1.0.0.zip) but you need to install this as ZIP file and it will not auto-update.

### Video Quality

NHK provides streams via Akamai in 720p and 1080p - the plug-in defaults to 1080p where available.

If you encounter buffering issues, you can fall-back to 720p by changing the 'Use 720p instead of 1080p' addon-setting.

Default setting is **off** (play 1080P where available).

### Design Goals

#### Inclusion in the official Kodi Repo

The design goal for the NHK World TV plug-in is to be included in the official Kodi repo and to include **only** content from the NHK World web site with the focus on the video-on-demand section - in hest best possible quality.

If you like to add the other content that can be found in Best Of NHK, please feel free to clone - I will **not** accept PRs for adding content sources outside of NHK World itself.

#### Performance

"Snappiness" was one of my design goals when developing this plug-in. For example, most calls to NHK are cached (requests-cache) for a while so that navigation is faster (defaults to two hours)

The plug-in also uses companion cloud service to speed up video play-back because these NHK APIs are very slow. 
You can disabe this in Settings if you do not want to use this - the only downside is that starting playback of video will take a bit longer and that you will loose a bit of UI functionality (e.g. Kodi will not store how much of a program you have already watched)

You can find the source code for the cloud service at [NHK World TV Azure Backend](https://github.com/sbroenne/nhkworldtv-backend).

The cache runs on Azure and is implemented as Azure Functions backed by Cosmos DB. It gets updated with new episodes multiple times per day.

## Known Issues

1. After the **initial** installation and after **each update**:

   1. The start of the plug-in can take a litte while - subsequent starts should be faster.

2. If you have a problem **after an update**, simply exit Kodi and start it again - or start a different plug-in. This will usually fix it. This is caused by Kodi when you re-use the Pyhton language invoker - which the plug-in does since it improves performance dramatically.

## Current Development Status

The plug-in is feature complete. You are able to:

- watch the live stream in HD
- access the full on-demand programs in HD, including programs, categories, playlists, etc.
- check the latest Top-Stories & At A Glance stories (in SD)
- access a "mini EPG"/live schedule with the upcoming shows - if the program is available on-demand, you can watch-ondemand it as well.
- watch the NHK News Programs like NEWSLINE or NEWSLINE IN DEPTH

Most of the NHK API is parsed and **not** hard-coded so this should make the plug-in more resilient to changes on the NHK web site. I also run scheduled unit tests on Github to alert me on breaking changes.

The plug-in is localized but translation only exists for English (GB). It is also Python3-compatible (by using python-future and kodi-six).

## Future Development

Main open topics are:

- None

## Local Development

You will find scripts to build the plugin in locally in the [build](./build/) folder. [More Information](./build/readme.md)

## Bugs & Issues

If you find a bug, or want to fix something directly, that would be awesome! Just use Github and open an issue! Thank you!

## Origins

Originally it started as a fork of **Misty's** [Best Of NHK plug-in](https://forum.kodi.tv/showthread.php?tid=196657) but shares zero code with it nowadays. His plug-in also provides addtional content like NHK on Youtube - check it out - it is worth it!
**Thank you Misty, awesome work!**
