#!/usr/bin/env bash

if [[ -z ${BUILD_ROOT} ]]; then
    echo "This script should be run from the build-dist.sh script"
    exit 1
fi
if [[ -z ${V8_VERSION} ]]; then
    echo "Failed to find the v8 version variable"
    exit 1
fi

BUILDS=(macos-x64-debug macos-x64-release)
MODULES=(v8_compiler v8_base_without_compiler v8_libplatform v8_libbase v8_libsampler v8_snapshot v8_initializers v8_init torque_generated_initializers)
for build in ${BUILDS[@]}
do
    BUILD_DIR=${BUILD_ROOT}/v8/out.gn/${build}
    DIST_DIR=${BUILD_ROOT}/dists/${build}

    # create the build and dist directories
    mkdir -p ${BUILD_DIR}
    mkdir -p ${DIST_DIR}

    # copy the args file over
    cp ${BUILD_ROOT}/args-gn-files/${build} ${BUILD_DIR}/args.gn

    # build the source
    ninja -C ${BUILD_DIR} ${MODULES[@]} inspector

    # copt the modules to the dist directory
    for module in ${MODULES[@]}
    do
        cp ${BUILD_DIR}/obj/$module}/lib${module}.a $DIST_DIR}
    done

    # we need a couple of other modules that are built as part of the above modules
    ar r ${DIST_DIR}/libinspector_protocol.a ${BUILD_DIR}/obj/third_party/inspector_protocol/crdtp/*.o ${BUILD_DIR}/obj/third_party/inspector_protocol/crdtp_platform/*.o
    ar r ${DIST_DIR}/libzip.a ${BUILD_DIR}/obj/third_party/zlib/zlib/*.o ${BUILD_DIR}/obj/third_party/zliib/google/compression_utils_portable/*.o

    # change to the the directory just above the dist we just built then zip it
    pushd ${DIST_DIR}/..
    zip -r v8-${V8_VERSION}_${build}.zip ${build}
    popd
done