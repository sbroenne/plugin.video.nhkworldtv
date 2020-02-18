# NHK World TV Kodi Plugin

## Disclaimer

This plug-in is a fan project and not related in any way to NHK!

## Overview

NHK World TV is a plug-in that displays most of the content from [NHK World Japam](https://www3.nhk.or.jp/nhkworld/en/live/) in Kodi in the highest possible quality (HD).

The plugin is optimized for an Internet connection with at least 10 MBIT. NHK still uses MP4 so that requires a lot of bandwidth.

Originally it started as a fork of Misty's [Best Of NHK plug-in](https://forum.kodi.tv/showthread.php?tid=196657) but shares almost no code with it nowadays.  His plug-in also provides addtional content like NHK on Youtube. Thank you Misty, awesome work!

The design goal for the NHK World TV plug-in is to eventually be included in the official Kodi repo and to include **only** content from the NHK World web site. If you like to add the other content that can be found in Best Of NHK, please feel free to clone - I will **not** accept PRs for adding content sources.

You can install the plugin by installing the [NHK World TV Development Repo](https://github.com/sbroenne/kodirepo/tree/master/repository.sbroenne). The github-repo also contains the plug-in as a ZIP file if you want to download & install it without the development repo.

## Current Development Status

The plug-in is largely feature complete. You are able to:

- watch the live stream in HD
- access the on-demand programs in HD, including categories, playlists, etc.
- check the latest Top-Stories
- acess a "mini EPG" with the upcoming status.

Automatic timezone support is implemented and has been tested on MacOs, Windows and Android TV.

## Future Development

Main open topics are:

- Implement CI/CD via github actions
- automatic parsing of NHK Api so that plugin becomes more resilient to API changes
- code fixes to comply with the Kodi plugin guidelines
- more unit test
- preparations to be able to submit the plugin to the official Kodi repo
- Integration with a PVR back-end

## Bugs & Issues

If you find a bug, or want to fix something directly, that would be awesome! Just use github!
