#!/bin/bash
# Build NK World TV for Kodi
echo "Building NHK World TV"

echo "1. Pre-build clean-up"
cd ..

# Clean-up exisiting ZIPs
rm -f plugin*.zip

# Creating plugin zip in base directory"
echo "2. Creating plugin zip"
pipenv run submit-addon -z -s plugin.video.nhkworldtv

cd build