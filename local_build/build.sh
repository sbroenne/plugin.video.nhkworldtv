#!/bin/bash
rm -rf plugin.video.nhkworldtv
rm -f *zip
rm -rf ../../zips/plugin.video.nhkworldtv/

mkdir plugin.video.nhkworldtv
mkdir  ../../zips/plugin.video.nhkworldtv/
cp ../addon.xml plugin.video.nhkworldtv
cp ../changelog.txt plugin.video.nhkworldtv
cp ../LICENSE plugin.video.nhkworldtv
cp ../main.py plugin.video.nhkworldtv
cp -r ../resources plugin.video.nhkworldtv
cp -r ../lib plugin.video.nhkworldtv
7za a -tzip plugin.video.nhkworldtv-0.0.5.zip plugin.video.nhkworldtv

cp ../addon.xml ../../zips/plugin.video.nhkworldtv/
cp ../resources/icon.png ../../zips/plugin.video.nhkworldtv/
cp ../resources/fanart.jpg ../../zips/plugin.video.nhkworldtv/

cp -r *.zip ../../zips/plugin.video.nhkworldtv/
rm -rf plugin.video.nhkworldtv
rm -rf *.zip