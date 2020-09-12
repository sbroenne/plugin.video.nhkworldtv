#!/bin/bash
# Copies the Plugin from the dist folder to the local Kodi directory - used for local development on Windows 10 WSL2 (Ubuntu)
# Build the Plugin
. ./build_leia.sh
# Set the local path (you probably need to adjust this)
local_kodi=/mnt/c/Users/stefa/AppData/Roaming/Kodi
# Change the <reuselanguageinvoker> to false
sed -i "s/>true</>false</g" $KODI_VERSION/plugin.video.nhkworldtv/addon.xml
# Delete existing add on folder
rm -rf $local_kodi/addons/plugin.video.nhkworldtv
# Copy the new build
cp -r $KODI_VERSION/plugin.video.nhkworldtv $local_kodi/addons