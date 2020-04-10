#!/bin/bash
# Build NK World TV for Kodi Leia (18.5+)

# Requires that ENV variable PLUGIN_VERSION is set (e.g. 0.0.1)
echo "Building NHK World TV version: $PLUGIN_VERSION"

# Clean-up
rm -rf leia
rm -rf leia/dist
# Cleanuo DEV artifacts
mkdir leia
cp -r ../plugin.video.nhkworldtv leia
rm -rf leia/plugin.video.nhkworldtv/tests
#rm -f leia/plugin.video.nhkworldtv/*.pyc
rm -f leia/plugin.video.nhkworldtv/lib/*.pyc
rm -f leia/plugin.video.nhkworldtv/tests
rm -f leia/plugin.video.nhkworldtv/lib/routing.py

# Set the plugin version in addon.xml
# This uses GNU SED - so if your are on Mac, you need to install this and change your path accordingly
sed -i "s/{PLUGIN_VERSION}/$PLUGIN_VERSION/g" leia/plugin.video.nhkworldtv/addon.xml

# Create distribution folder
mkdir leia/dist
cd leia/dist

# Pack plug-in with create_repository
../../create_repository.py ../plugin.video.nhkworldtv
# Copy resources so that the Install Plug-in dialogi in Kodi can display them
mkdir plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.jpeg plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.jpg plugin.video.nhkworldtv/resources
cp ../plugin.video.nhkworldtv/resources/*.png plugin.video.nhkworldtv/resources

# Clean addon.xml - created by create_repository but not needed here
rm -f addons*
cd ../..
