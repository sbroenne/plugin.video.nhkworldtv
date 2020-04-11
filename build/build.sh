#!/bin/bash
# Build NK World TV for Kodi Leia (18.5+)

# Requires that ENV variable PLUGIN_VERSION is set (e.g. 0.0.1)
echo "Building NHK World TV version: $PLUGIN_VERSION"
echo "Kodi $KODI_VERSION"
echo "XBMC Python Version $XBMC_PYTHON_VERSION"
# Clean-up
rm -rf $KODI_VERSION
rm -rf $KODI_VERSION/dist
# Cleanuo DEV artifacts
mkdir $KODI_VERSION
cp -r ../plugin.video.nhkworldtv $KODI_VERSION
rm -rf $KODI_VERSION/plugin.video.nhkworldtv/tests
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/api_json.js
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/*.pyc
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/*.pyo
rm -f $KODI_VERSION/plugin.video.nhkworldtv/tests
rm -f $KODI_VERSION/plugin.video.nhkworldtv/lib/routing.py

# Set the plugin version in addon.xml
# This uses GNU SED - so if your are on Mac, you need to install this and change your path accordingly
sed -i "s/{PLUGIN_VERSION}/$PLUGIN_VERSION/g" $KODI_VERSION/plugin.video.nhkworldtv/addon.xml
# Set the XMBC Python Version (different for Leia and Matrix)
sed -i "s/{XBMC_PYTHON_VERSION}/$XBMC_PYTHON_VERSION/g" $KODI_VERSION/plugin.video.nhkworldtv/addon.xml

# Create distribution folder
mkdir $KODI_VERSION/dist
cd $KODI_VERSION/dist

# Pack plug-in with create_repository
../../create_repository.py ../plugin.video.nhkworldtv
cp ./plugin.video.nhkworldtv/plugin.video.nhkworldtv-$PLUGIN_VERSION.zip plugin.video.nhkworldtv-$PLUGIN_VERSION-$KODI_VERSION.zip

# Copy resources so that the Install Plug-in dialogi in Kodi can display them
mkdir plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.jpeg plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.jpg plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.png plugin.video.nhkworldtv/resources

# Clean addon.xml - created by create_repository but not needed here
rm -f addons*
cd ../..
