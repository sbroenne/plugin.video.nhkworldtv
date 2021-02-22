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
# Clean-up everything
rm -rf $KODI_VERSION

# Create Plugin directory
export DEST_DIR=$KODI_VERSION/plugin.video.nhkworldtv
export SOURCE_DIR='../plugin.video.nhkworldtv'
echo "Plugin source: $SOURCE_DIR"
echo "Plugin destination: $DEST_DIR"

# Creating target
mkdir $KODI_VERSION
mkdir $DEST_DIR
mkdir $DEST_DIR/lib
mkdir $DEST_DIR/resources

# Copying resources
echo "2. Copying resources from $SOURCE_DIR to $DEST_DIR"
cp $SOURCE_DIR/addon_template.xml $DEST_DIR
cp $SOURCE_DIR/LICENSE $DEST_DIR
cp $SOURCE_DIR/main.py $DEST_DIR
cp $SOURCE_DIR/lib/*.py $DEST_DIR/lib
cp -r $SOURCE_DIR/resources $DEST_DIR

echo "3. envsubst addon.xml"
# Substitute the env variable reference in addon.xml with the env variables 
envsubst < $DEST_DIR/addon_template.xml > $DEST_DIR/addon.xml
rm -f $DEST_DIR/addon_template.xml

echo "4. Packing the plugin"
# Create distribution folder
mkdir $KODI_VERSION/dist
cd $KODI_VERSION/dist

# Pack plug-in with create_repository
python3 ../../create_repository.py $SOURCE_DIR

# Only used by the Github release action
cp ./plugin.video.nhkworldtv/plugin.video.nhkworldtv-$PLUGIN_VERSION.zip plugin.video.nhkworldtv-$PLUGIN_VERSION-$KODI_VERSION.zip

echo "5. Copying addtional resources"
# Copy resources so that the Install Plug-in dialog in Kodi can display them

mkdir plugin.video.nhkworldtv/resources
cp $SOURCE_DIR/resources/*.jpeg plugin.video.nhkworldtv/resources
cp $SOURCE_DIR/resources/*.jpg plugin.video.nhkworldtv/resources
cp $SOURCE_DIR/resources/*.png plugin.video.nhkworldtv/resources

echo "6. Post-build clean-up"
# Clean addon.xml - created by create_repository but not needed here
rm -f addons*
cd ../..

echo "6. Done"
