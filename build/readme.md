# Local Build Instructions

You can build this plug-in for both Kodi Leia and Matrix. There is a build file for each version. The plug-in has been tested on both versions.

The plugin version is determined from the latest Git Tag (e.g. *v1.0.0*). You can also hard-code it in the build file (can be useful for dev purposes)

## Prerequsites

Pipenv is used to install the required [Python packages](../Pipfile) where possible.

### GNU Sed

I am developing on a Mac so you will need to adapt this to your environment. Because of this I also use GNU sed insted of the default MacOsX sed - without it the build scripts will **not** work. I use Homebrew to install it and then change my $PATH to make it the default.

### Packages not in PyPi

I use two packages (kodi-six and routing) that are not in PyPi. You need to manually install them once with the [install_packages script](./install_packages.sh) - this only needs to be done once.

```bash
chmod u+x install_packages.sh
pipenv run ./install_packages.sh
```

## Build for Leia

This is how you would build for Kodi Leia

```bash
chmod u+x build_leia.sh
./build_leia.sh
```

The output can then be found in the respective [dist](./leia/dist/) folder.

## Copy to local MacOsX Kodi

The [copy_local_macosx script](./copy_local_macosx.sh) will install the content of the [dist](./leia/dist/) folder to the local Kodi installation folder so you can update the plug-in easily while developing. This script works **only on MacOsX** but but should be easy to adapt to your environment.

## Copy to local WSL 2 on Windows 10 Kodi

The [copy_local_wsl script](./copy_local_wsl.sh) will install the content of the [dist](./leia/dist/) folder to the local Kodi installation folder so you can update the plug-in easily while developing. This script works **only on Windows 10 using WSL2 as the development environment** but but should be easy to adapt to your environment.
