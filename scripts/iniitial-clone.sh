#!/usr/bin/env bash

# Copyright 2020 The v8App Authors. All rights reserved.
# Use of this source code is governed by a MIT license that can be
# found in the LICENSE file.

TOP="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

#check for git install
git --version >> /dev/null
if [[ $? -ne 0 ]]; then
    echo "Doesn't seem as if git is installed, as getting the version failed"
    exit 1
fi

#clone the repository
git clone https://github.com/v8App/v8Dist.git
if [[ $? -ne 0 ]]; then
    echo "Failed to clone the v8Dist repo"
    exit 1
fi

TOP=${TOP}/v8Dist
cd ${TOP}

#are we on Linux or Mac OS X
OSX=`uname -a | grep Darwin | wc -l`
V8_VERSION=`cat ${TOP}/v8Version`


echo "This script will install google's depot tools and then clone the v8App in the current directory '${TOP}'."

git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
if [[ $? -ne 0 ]]; then
    echo "Failed to clone the depot_tools"
    exit 1
fi

export PATH=${PATH}:${TOP}/depot_tools

cd ${TOP}/depot_tools
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

cd ${TOP}
if [[ $? -ne 0 ]]; then
    echo "Failed to change back to ${TOP}"
    exit 1
fi

echo "Fetching v8"
cd v8Dist
fetch v8
if [[ $? -ne 0 ]]; then
    echo "Failed to fetch the v8 repository"
    exit 1
fi

gclient sync --with_branch_heads --with_tags
if [[ $? -ne 0 ]]; then
    echo "Failed to sync the v8App repository"
    exit 1
fi

# get a specific version
cd v8
echo "Checking out ${V8_VERSION}"
git checkout ${V8_VERSION}

echo "/n/nYou will want to add this this path '${TOP}/depot_tools' to your PATH variable through an export or in your shell config."