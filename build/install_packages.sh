#!/bin/bash
# Install packackes thar are not in PyPi. This only needs to be done once.
# You need to run this in a Python virtual environment: pipenv run ./install_packages.sh

# $ PYTHON version is set by the Github Action - only need to set it for local development
if [ -z $PYTHON_VERSION ]
then
    export PYTHON_VERSION=3.12
fi

echo "PYTHON VERSION: $PYTHON_VERSION"
rm -rf prereq
mkdir prereq
cd prereq

# Install routing.py
cd .. 
export SITE_PACKAGES="$(pipenv --venv)/lib/python$PYTHON_VERSION/site-packages/"
echo "Site Packages Directory: $SITE_PACKAGES"
cp routing/routing.py $SITE_PACKAGES
