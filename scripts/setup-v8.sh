#!/usr/bin/env bash

# allow the build root to be passed in otherwise it's exported or comes
# from the file being sourced into a script
if [[ ! -z $1 ]]; then
    BUILD_ROOT=$1
fi

V8_VERSION=`cat ${BUILD_ROOT}/v8Version`

echo "This script will install google's depot tools and then clone the v8App in the current directory '${BUUILD_ROOT}'."

git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
if [[ $? -ne 0 ]]; then
    echo "Failed to clone the depot_tools"
    exit 1
fi

export PATH=${PATH}:${BUILD_ROOT}/depot_tools

cd ${BUILD_ROOT}/depot_tools
if [[ $? -ne 0 ]]; then
    echo "Failed to cd to the depot_tools"
    exit 1
fi

#now update depot_tools
echo "Updating depot_tools"
gclient --version
if [[ $? -ne 0 ]]; then
    echo "Failed to update depot_tools"
    exit 1
fi

cd ${BUILD_ROOT}
if [[ $? -ne 0 ]]; then
    echo "Failed to change back to ${BUILD_ROOT}"
    exit 1
fi

echo "Fetching v8"
gclient sync --gclientfile=.v8_gclient --with_branch_heads --with_tags
if [[ $? -ne 0 ]]; then
    echo "Failed to sync the v8 repository"
    exit 1
fi

# get a specific version
cd v8
echo "Checking out ${V8_VERSION}"
git checkout ${V8_VERSION}
