#!/bin/bash
# Install packackes thar are not in PyPi. This only needs to be done once.
# export PYTHON_VERSION=2.7
echo "PYTHON VERSION: $PYTHON_VERSION"
rm -rf prereq
mkdir prereq
cd prereq

# Install Kodi-Six
wget https://github.com/romanvm/kodi.six/archive/master.zip
unzip master.zip
rm -f master.zip
cd kodi.six-master
python setup.py install
cd ..
rm -rf kodi.six-master

# Install routing.py
cd .. 
cp routing/routing.py $(pipenv --venv)/lib/python$PYTHON_VERSION/site-packages
