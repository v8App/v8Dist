# v8Dist
v8App's repository for building v8 distributions

Clone the repository then run setup.py it will setup the repo for being able to build v8.

To build run the build-v8.py and specify the following arguments:
* --build-root (Usually the top of the repository unless you want it to build elsewhere)
* one or more of --macos, --ios, --windows, --android, --linux
* optionally specify the --arch as one of x64, arm, arm32, arm64. Defaults to x64

Currently only windows has been fully tested.