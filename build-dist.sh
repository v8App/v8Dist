#!/usr/bin/env bash

# the flags for distributions to build
BUILD_LINUX=0
BUILD_ANDROID=0
BUILD_MAC_OS=0
BUILD_IOS=0

TOP="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source ${TOP}/scripts/functions

#if we are running an automated build then run with out interaction
QUIET=0
if [[ ! -z $1 ]] && [[ $1 == "--no-interaction" ]]; then
    QUIET=1
fi

#are we on Linux or Mac OS X
OSX=`uname -a | grep Darwin | wc -l`
V8_VERSION=`cat ${TOP}/v8Version`

#regardless of whether we are running on linux or mac os we'll use docker to build the linux and android distributions
DOCKER=1
docker -v /dev/null
if [[ $? -ne 0 ]]; then
    DOCKER=0
fi

if [[ ${OSX} -eq 1 ]]; then
    BUILD_MAC_OS=1
    BUILD_IOS=1
    if [[ ${QUIET} -eq 0 ]]; then
        ANSWER=0
        ask_for_yes_no ANSWER "Do you wish to build MacOS builds?"
        if [[ $? -ne 0 ]]; then
            echo "Failed to get answer"
            exit 1
        fi
        if [[ ${ANSWER} -eq 0 ]]; then
            BUILD_MAC_OS=0
        fi
        ANSWER=0
        ask_for_yes_no ANSWER "Do you wish to build iOS builds?"
        if [[ $? -ne 0 ]]; then
            echo "Failed to get answer"
            exit 1
        fi
        if [[ ${ANSWER} -eq 0 ]]; then
            BUILD_IOS=0
        fi
    fi
fi

# if docker is not available skip building android and linux
if [[ ${DOCKER} -eq 1 ]]; then
    BUILD_LINUX=1
    BUILD_ANDROID=1
    if [[ ${QUIET} -eq 0 ]]; then
        ANSWER=0
        ask_for_yes_no ANSWER "Do you wish to build Linux builds?"
        if [[ $? -ne 0 ]]; then
            echo "Failed to get answer"
            exit 1
        fi
        if [[ ${ANSWER} -eq 0 ]]; then
            BUILD_LINUX=0
        fi
        ANSWER=0
        ask_for_yes_no ANSWER "Do you wish to build Android builds?"
        if [[ $? -ne 0 ]]; then
            echo "Failed to get answer"
            exit 1
        fi
        if [[ ${ANSWER} -eq 0 ]]; then
            BUILD_ANDROID=0
        fi

    fi
fi

if [[ ${BUILD_MAC_OS} -eq 0 ]] && [[ ${BUILD_IOS} -eq 0 ]] && [[ ${BUILD_LINUX} -eq 0 ]] && [[ ${BUILD_ANDROID} -eq 0 ]]; then
    echo "Found nothing to build"
    exit 0
fi

if [[ ${BUILD_MAC_OS} -eq 1 ]]; then
    source ${TOP}/builders/build-macos.sh
fi

if [[ ${BUILD_IOS} -eq 1 ]]; then
    source ${TOP}/builders/build-ios.sh
fi

if [[ ${BUILD_ANDROID} -eq 1 ]]; then
    source ${TOP}/builders/build-android.sh
fi

if [[ ${BUILD_LINUX} -eq 1 ]]; then
    source ${TOP}/builders/build-ubuntu.sh
    source ${TOP}/builders/build-debian.sh
fi

echo "Done building distributions"