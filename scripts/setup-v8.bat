@echo off

rem allow the the build root to be passed in other wise it's exported or
rem imported from being called
if not "%~1"=="" set BUILD_ROOT=%1

echo "This script will install google's depot tools and then clone the v8App in the current directory '%BUILD_ROOT%'."

cd %BUILD_ROOT%
if %ERRORLEVEL% neq 0 echo "Failed to change to %BUILD_ROOT%." && exit 1

curl -o .\depot_tools.zip https://storage.googleapis.com/chrome-infra/depot_tools.zip 
if %ERRORLEVEL% neq 0 echo "Failed to download the depot tools." && exit 1

mkdir depot_tools
if %ERRORLEVEL% neq 0 echo "Failed to create the depot_tools folder." && exit 1

tar -xf .\depot_tools.zip -C .\depot_tools
if %ERRORLEVEL% neq 0 echo "Failed to extract the depot tools." && exit 1

PATH %BUILD_ROOT%\depot_tools;%PATH%;

cd %BUILD_ROOT\depot_tools%
if %ERRORLEVEL% neq 0 echo "Failed to change to depot tools." && exit 1

set DEPOT_TOOLS_WIN_TOOLCHAIN=0

rem update depot tools
gclient sync --gclientfile=.v8_gclient --with_branch_heads --with_tags
if %ERRORLEVEL% neq 0 echo "Failed to update depot tools." && exit 1

cd %BUILD_ROOT%
if %ERRORLEVEL% neq 0 echo "Failed to change back to %BUILD_ROOT%." && exit 1

echo "Fetching v8"
rem gclient sync --gclientfile=.v8_gclient --with_branch_heads --with_tags
gclient fetch v8
if %ERRORLEVEL% neq 0 echo "Failed to sync the v8 repository." && exit 1

set /p V8_VERSION=%BUILD_ROOT%\v8Version

cd %BUILD_ROOT%\v8
if %ERRORLEVEL% neq 0 echo "Failed to change to v8." && exit 1

git checkout %V8_VERSION%
if %ERRORLEVEL% neq 0 echo "Failed to check out v8 version %V8_VERSION%." && exit 1

gclient sync
if %ERRORLEVEL% neq 0 echo "Failed to sync v8." && exit 1

:end