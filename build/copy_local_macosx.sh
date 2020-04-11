#!/bin/bash
# Copies the Plugin from the dist folder to the local Kodi directory - used for local development
# Build the Plugin
. ./build_leia.sh
# Change the <reuselanguageinvoker> to false
sed -i "s/>true</>false</g" $KODI_VERSION/plugin.video.nhkworldtv/addon.xml
# Delete main code folder (lib)
rm -rf ~/Library/Application\ Support/Kodi/addons/plugin.video.nhkworldtv/lib
# Delete stored view modes
rm -rf ~/Library/Application\ Support/Kodi/userdata/Database/ViewModes6.db
cp -r $KODI_VERSION/plugin.video.nhkworldtv ~/Library/Application\ Support/Kodi/addons