# Local Build Instructions

You can build this plug-in for both Kodi Leia and Matrix. There is a build file for each version. The plug-in has been tested on both versions.

The plugin version is determine from the latest Git Tag (e.g. *v1.0.0*). You can also hard-code it in the build file (can be useful for dev purposes)

## Build for Leia

This is how you would build for Kodi Leia

```bash
chmod u+x build_leia.sh
./build_leia.sh
```

The output can then be found in the respective [dist](./leia/dist/) folder.
