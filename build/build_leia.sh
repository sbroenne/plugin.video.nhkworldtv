#!/bin/bash
# Build NK World TV for Kodi Leia (18.5+)
# Set the git tag
export GIT_TAG=$(git describe --abbrev=0)
# Set plugin version
export PLUGIN_VERSION=${GIT_TAG:1}
# Set the Kodi version
export KODI_VERSION=leia
# XBMC Python Version
export XBMC_PYTHON_VERSION="2.26.0"
. ./build.sh