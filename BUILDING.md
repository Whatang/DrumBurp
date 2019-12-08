# Building DrumBurp

## Release Builds

DrumBurp is automatically built by [GitHub Actions](https://github.com/features/actions) on a push to the [repository](https://github.com/Whatang/DrumBurp). Pushes with a tag create a [new release](https://github.com/Whatang/DrumBurp/releases). This ensures a consistent environment for the builds, and enables quick releases of new content.

The definitions of the GitHub Actions build workflows are kept in `.github/workflows`. The scripts used by these workflows are in the `build/` directory. All DrumBurp source code is in `src/`.

## Development Builds

When developing DrumBurp locally, you should try to replicate the release build environment as much as possible. You can do this by running the appropriate `install_*` scripts in the `build` directory. It is recommended that you first create an appropriate Python virtual environment and execute the install script in it, so that your system and build environments stay clean.

You should also execute `pip install -r requirements-dev.txt` in your virtual environment to get the necessary development packages installed.

## Release Process

DrumBurp development uses the Git Flow model of branching. Development should all happen on, or branched from, the `develop` branch. Small tweaks can happen directly on this branch, larger dev efforts should be branched off into `feature/` branches.

When you are at the point of wanting to push a new release, follow these steps.

1. Check everything in to the `develop` branch.
2. Run the appropriate `build_*` scripts from the `build/` directory to check that the build works.
3. Check that DrumBurp installs and works correctly from those builds. It is a good idea to check that the builds run OK in a clean VM.
4. Run [versionflow](https://pypi.org/project/versionflow/) to bump the version number and create a tagged commit on `master`.
5. Push `master` (and `develop`) to the GitHub repo.
6. Sit back and watch a new version get built and released!

## Versioning

DrumBurp uses semantic versioning to keep track of its version numbers. Version numbers are stored in a number of places:

* `DBVersionNum.py` - used by DrumBuro to know what the current version is.
* `build\DrumBurp.nsi` - used by the Windows build script to appropriately label built executables.
* `.versionflow` - the configuration file for the version handling utility.
* In the tag on the master branch which labels the commit for the corresponding release.

There is no need to ever update these by hand: [versionflow](https://pypi.org/project/versionflow/) takes care of this to keep them consistent, as long as you always use it when creating a release.

DrumBurp also uses `versionflow`'s features to understand development versions: when running from a dev repo, `versionflow` will adjust the version number DrumBurp gets to indicate the commit that is running.
