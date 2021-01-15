#!/bin/bash
# Build NK World TV for Kodi Leia (18.5+)

# Set the git tag
export GIT_TAG=$(git describe --abbrev=0)
# Set plugin version
export PLUGIN_VERSION=${GIT_TAG:1}

# Get the Kodi version specific variables
source $KODI_VERSION.env

# Requires that ENV variable PLUGIN_VERSION is set (e.g. 0.0.1)
echo "Building NHK World TV version: $PLUGIN_VERSION"
echo "Kodi version: $KODI_VERSION"

echo "1. Pre-build clean-up"
# Clean-up
rm -rf $KODI_VERSION
rm -rf $KODI_VERSION/dist
# Cleanup DEV artifacts
mkdir $KODI_VERSION
cp -r ../plugin.video.nhkworldtv $KODI_VERSION
rm -rf $KODI_VERSION/plugin.video.nhkworldtv/tests
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/api_json.js
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/*.pyc
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/*.pyo
rm -f $KODI_VERSION/plugin.video.nhkworldtv/tests
rm -f $KODI_VERSION/plugin.video.nhkworldtv/nhk_world_cache.sqlite
rm -rf $KODI_VERSION/plugin.video.nhkworldtv/.pytest*
rm -rf $KODI_VERSION/plugin.video.nhkworldtv/.vscode

echo "2. envsubst addon.xml"
# Substitute the env variable reference in addon.xml with the env variables 
envsubst < $KODI_VERSION/plugin.video.nhkworldtv/addon_template.xml > $KODI_VERSION/plugin.video.nhkworldtv/addon.xml
rm -f $KODI_VERSION/plugin.video.nhkworldtv/addon_template.xml

echo "3. Packing the plugin"
# Create distribution folder
mkdir $KODI_VERSION/dist
cd $KODI_VERSION/dist

# Pack plug-in with create_repository
../../create_repository.py ../plugin.video.nhkworldtv
cp ./plugin.video.nhkworldtv/plugin.video.nhkworldtv-$PLUGIN_VERSION.zip plugin.video.nhkworldtv-$PLUGIN_VERSION-$KODI_VERSION.zip

echo "4. Copying addtional resources"
# Copy resources so that the Install Plug-in dialog in Kodi can display them
mkdir plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.jpeg plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.jpg plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.png plugin.video.nhkworldtv/resources

echo "5. Post-build clean-up"
# Clean addon.xml - created by create_repository but not needed here
rm -f addons*
cd ../..

echo "6. Done"
