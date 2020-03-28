# NHK World TV Kodi Plugin

## Disclaimer

This plug-in is a fan project and not related in any way to NHK! I built this plugin because NHK does not support Android TV (yet).

## Overview

NHK World TV is a plug-in that displays most of the content from [NHK World Japan](https://www3.nhk.or.jp/nhkworld/en/live/) in Kodi in the highest possible quality (1080p).

The plugin is optimized for an Internet connection with at least 10 MBIT. NHK still uses H.264 so that requires a lot of bandwidth.

Originally it started as a fork of **Misty's** [Best Of NHK plug-in](https://forum.kodi.tv/showthread.php?tid=196657) but shares almost zero code with it nowadays.  His plug-in also provides addtional content like NHK on Youtube - check it out - it is worth it!

**Thank you Misty, awesome work!**

The design goal for the NHK World TV plug-in is to eventually be included in the official Kodi repo and to include **only** content from the NHK World web site with the focus on the video-on-demand section - in hest best possible quality.

If you like to add the other content that can be found in Best Of NHK, please feel free to clone - I will **not** accept PRs for adding content sources outside of NHK World itself.

## How-to Install

You can install a beta version of the plugin by installing the [NHK World TV Development Repository](https://github.com/sbroenne/kodirepo/tree/master/repository.sbroenne). The plug-in will auto-update itself regularly.

You can also manually download [the plug-in as a ZIP file](https://github.com/sbroenne/kodirepo/tree/master/plugin.video.nhkworldtv). In this case, you will need to manually peforms updates.

## Performance

"Snappiness" was one of my design goals when developing this plug-in. For example, most calls to NHK are cached for a while so that navigation is faster (defaults to three hours)

The plug-in also uses companion cloud service to speed up video play-back because these NHK APIs are very slow. You can disabe this in Settings if you do not want to use this - the only downside is that starting playback of video will take a bit longer and that you will use a bit of UI functionality (e.g. Kodi will not store how much of a program you have already watched)

You can find the source code for the cloud service at [NHK World TV Azure Backend](https://github.com/sbroenne/nhkworldtv-backend).

The cache runs on Azure implemented as Azure Functions backed by Cosmos DB. It gets updated with new episodes multiple times per day.

## Known Issues

1. After the **initial** installation, you might encounter an error when stating the plug-in. Simply start again - this will fix the issue. This is caused by a bug in a third party component. It will occur only once.

2. After the **initial** installation and after **each update**, the start of the plug-in can take a litte while - subsequent starts should be faster.

3. If you have a problem **after an update**, simply stop Kodi and start it again. This will usually fix it. This is caused by a bug in Kodi when you re-use the Pyhton language invoker - which the plug-in does sice it improves performance dramatically.

## Current Development Status

The plug-in is largely feature complete. You are able to:

- watch the live stream in HD
- access the full on-demand programs in HD, including categories, playlists, etc.
- check the latest Top-Stories & At A Glance stories (in SD)
- access a "mini EPG"/live schedule with the upcoming shows - if the program is available on-demand, you can play it as well.

Automatic timezone support is implemented and has been tested on MacOs, Windows and Android TV.

Most of the NHK API is parsed and **not** hard-coded so this should make the plug-in more resilient to changes on the NHK web site.

The plug-in is localized but translation only exists for English (GB).

## Future Development

Main open topics are:

- Implement CI/CD via github actions
- code fixes to comply with the Kodi plugin guidelines
- more unit tests for fringe cases
- preparations to be able to submit the plugin to the official Kodi repo

## Bugs & Issues

If you find a bug, or want to fix something directly, that would be awesome! Just use github and open an issue!
