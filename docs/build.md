# Local Build Instructions

Minimum supported Kodi version is Matrix and Python 3.12.

## Prerequisites

Pipenv is used to install the required [Python packages](../Pipfile). I use Ubuntu 24.04 / WSL as my dev platform.

```bash
sudo apt install pipenv
pipenv install -d
```

### Packages not in PyPi

I use a package (routing) which is not in PyPi. You need to manually install it **once** with the [install_packages script](../build/install_packages.sh).

```bash
pipenv run ../build/install_packages.sh
```

## Build plugin

I use [Kodi Addon Submitter](https://github.com/xbmc/kodi-addon-submitter) to create the plugin ZIP file

```bash
chmod u+x ../build/build.sh
../build/build.sh
```

The resulting ZIP file can then be found in the project root folder.

## Copy to local WSL 2 on Windows 11 Kodi

I develop on Windows 11 with WSL v2.

The [copy_local_wsl script](../build/copy_local_wsl.sh) will copy the plugin to the [dist](../build/dist) folder & from there copy it to the local Kodi installation folder so you can update the plug-in easily while developing. This script works **only on Windows 11 using WSL2 as the development environment** but but should be easy to adapt to your environment.

You will need to modify the *local_kodi* variable to match your local path.

## GitHub Actions

I created [two actions](../.github) for building a release and for running unit tests on GitHub.
