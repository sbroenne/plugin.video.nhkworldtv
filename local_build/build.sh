#!/bin/bash
rm -rf plugin.video.nhkworldtv
rm -f *zip
mkdir plugin.video.nhkworldtv
cp ../addon.xml plugin.video.nhkworldtv
cp ../changelog.txt plugin.video.nhkworldtv
cp ../license.txt plugin.video.nhkworldtv
cp ../icon.png plugin.video.nhkworldtv
cp ../default.py plugin.video.nhkworldtv
cp -r /lib plugin.video.nhkworldtv
cp -r ../resources plugin.video.nhkworldtv
7za a -tzip plugin.video.nhkworldtv-1.0.1.zip plugin.video.nhkworldtv

cp ../addon.xml ../../zips/plugin.video.nhkworldtv/
cp ../changelog.txt ../../zips/plugin.video.nhkworldtv/
cp ../icon.png ../../zips/plugin.video.nhkworldtv/

cp -r *.zip ../../zips/plugin.video.nhkworldtv/
rm -rf plugin.video.nhkworldtv
rm -rf *.zip