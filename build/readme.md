# Local Build Instructions

You can build this plug-in for both Kodi Leia and Matrix. There is a build file for each version. The plug-in has been tested on both versions. Since Matrix has been released, I only release Matrix versions in my repo.

The plugin version is determined from the latest Git Tag (e.g. _v1.0.0_). You can also hard-code it in the build file (can be useful for dev purposes)

## Prerequisites

Pipenv is used to install the required [Python packages](../Pipfile) where possible. There is a Pipfile for Python version 2.7 and 3.8. You need to rename it to **Pipfile** before you can use Pipenv.

### Packages not in PyPi

I use two packages (kodi-six and routing) that are not in PyPi. You need to manually install them once with the [install_packages script](./install_packages.sh) - this only needs to be done once.

```bash
pipenv run ./install_packages.sh
```

## Build for Matrix

This is how you would build for Kodi Matrix

```bash
chmod u+x build_matrix.sh
./build_matrix.sh
```

The output can then be found in the respective [dist](./leia/matrix) folder.

## Copy to local WSL 2 on Windows 10/11 Kodi

I develop on Windows 11 with WSL v2.

The [copy_local_wsl script](./copy_local_wsl.sh) will install the content of the [dist](./leia/matrix) folder to the local Kodi installation folder so you can update the plug-in easily while developing. This script works **only on Windows 10 using WSL2 as the development environment** but but should be easy to adapt to your environment.

## GitHub Actions

I created two actions for building a release and for running unit tests on GitHub.
