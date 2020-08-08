!/usr/bin/env bash

if [[ -z ${BUILD_ROOT} ]]; then
    echo "This script should be run from the build-dist.sh script"
    exit 1
fi
if [[ -z ${V8_VERSION} ]]; then
    echo "Failed to find the v8 version variable"
    exit 1
fi
pushd ${BUILD_ROOT}/v8

BUILDS=(macos-x64-debug macos-x64-release)
MODULES=(v8_compiler v8_base_without_compiler v8_libplatform v8_libbase v8_libsampler v8_snapshot v8_initializers v8_init torque_generated_initializers)
for build in ${BUILDS[@]}
do
    BUILD_DIR=${BUILD_ROOT}/v8/out.gn/${build}
    BUILD_NAME=v8-${V8_VERSION}_${build}
    DIST_DIR=${BUILD_ROOT}/dists/${BUILD_NAME}

    # create the build and dist directories
    mkdir -p ${BUILD_DIR}
    if [[ $? -ne 0 ]]; then
        echo "Failed to create directory ${BUILD_DIR}"
        exit 1
    fi
    mkdir -p ${DIST_DIR}
    if [[ $? -ne 0 ]]; then
        echo "Failed to create directory ${DIST_DIR}"
        exit 1
    fi

    # copy the args file over
    cp ${BUILD_ROOT}/args-gn-files/${build}.gn ${BUILD_DIR}/args.gn
    if [[ $? -ne 0 ]]; then
        echo "Failed to copy the args.gn file"
        exit 1
    fi

    # generate the build
    gn gen ${BUILD_DIR}/
    if [[ $? -ne 0 ]]; then
        echo "Failed to generate the build"
        exit 1
    fi
    # build the source
    ninja -C ${BUILD_DIR} ${MODULES[@]} inspector
    if [[ $? -ne 0 ]]; then
        echo "Failed to build the source"
        exit 1
    fi

    # copt the modules to the dist directory
    for module in ${MODULES[@]}
    do
        ar r ${DIST_DIR}/lib${module}.a ${BUILD_DIR}/obj/${module}/*.o
        if [[ $? -ne 0 ]]; then
            echo "Failed to create directory ${DIST_DIR}"
            exit 1
        fi
    done

    # we need a couple of other modules that are built as part of the above modules
    ar r ${DIST_DIR}/libinspector_protocol.a ${BUILD_DIR}/obj/third_party/inspector_protocol/crdtp/*.o ${BUILD_DIR}/obj/third_party/inspector_protocol/crdtp_platform/*.o
    if [[ $? -ne 0 ]]; then
        echo "Failed to generate the libinspector_protocol.a library"
        exit 1
    fi
    ar r ${DIST_DIR}/libzip.a ${BUILD_DIR}/obj/third_party/zlib/zlib/*.o ${BUILD_DIR}/obj/third_party/zlib/google/compression_utils_portable/*.o
    if [[ $? -ne 0 ]]; then
        echo "Failed to generate the libzip.a library"
        exit 1
    fi

    #add the include folder
    cp -r ${BUILD_ROOT}/v8/include ${DIST_DIR}/include
    if [[ $? -ne 0 ]]; then
        echo "Failed to copy the include directory"
        exit 1
    fi

    # change to the the directory just above the dist we just built then zip it
    pushd ${DIST_DIR}/..
    zip -r v8-${V8_VERSION}_${build}.zip ${BUILD_NAME}
    if [[ $? -ne 0 ]]; then
        echo "Failed to zip the distribution"
        exit 1
    fi
    popd
done

popd