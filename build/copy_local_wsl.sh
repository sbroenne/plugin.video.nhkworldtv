#!/bin/bash
# Copies the Plugin from the dist folder to the local Kodi directory - used for local development on Windows 10 WSL2 (Ubuntu)

# Set the git tag
export GIT_TAG=$(git describe --tags --abbrev=0)
# Set plugin version
export PLUGIN_VERSION=${GIT_TAG:1}


# Requires that ENV variable PLUGIN_VERSION is set (e.g. 0.0.1)
echo "Building NHK World TV version: $PLUGIN_VERSION"

echo "1. Pre-build clean-up"
# Clean-up everything
rm -rf dist

# Create Plugin directory
export DEST_DIR=dist/plugin.video.nhkworldtv
export SOURCE_DIR='../plugin.video.nhkworldtv'
echo "Plugin source: $SOURCE_DIR"
echo "Plugin destination: $DEST_DIR"

# Creating target
mkdir dist
mkdir $DEST_DIR
mkdir $DEST_DIR/lib
mkdir $DEST_DIR/resources

# Copying resources
echo "2. Copying resources from $SOURCE_DIR to $DEST_DIR"
cp $SOURCE_DIR/addon.xml $DEST_DIR
cp $SOURCE_DIR/LICENSE $DEST_DIR
cp $SOURCE_DIR/main.py $DEST_DIR
cp $SOURCE_DIR/lib/*.py $DEST_DIR/lib
cp -r $SOURCE_DIR/resources $DEST_DIR

# Set the local path (you need to adjust this)
local_kodi=/c/Users/stefa/AppData/Roaming/Kodi
# Change the <reuselanguageinvoker> to false - only needed for debugging
sed -i "s/>true</>false</g" dist/plugin.video.nhkworldtv/addon.xml
# Delete existing add on folder
rm -rf $local_kodi/addons/plugin.video.nhkworldtv
# Copy the new build
cp -r dist/plugin.video.nhkworldtv $local_kodi/addons