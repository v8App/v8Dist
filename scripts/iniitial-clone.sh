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
if [[ $? -ne 0 ]]; then
    echo "Failed tochange to ${TOP}"
    exit 1
fi

#source in the setup of v8 on the host machine
BUILD_ROOT=${TOP}
source ${TOP}/scripts/setup-v8.sh

echo ""
echo ""
echo "You will want to add this this path '${TOP}/depot_tools' to your PATH variable through an export or in your shell config."