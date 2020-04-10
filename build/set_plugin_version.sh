#!/bin/bash

# Set the git tag
export GIT_TAG=$(git describe --abbrev=0)
# Set plugin version
export PLUGIN_VERSION=${GIT_TAG:1}
