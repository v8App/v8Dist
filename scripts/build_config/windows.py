import subprocess
from pathlib import Path

gn_args_release = {
    'is_debug': 'false',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'is_clang': 'false',
    'dcheck_always_on': 'false',
    'v8_static_library': 'true',
    'v8_enable_pointer_compression_shared_cage ': 'false',
}

gn_args_debug = {
    'is_debug': 'true',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'is_clang': 'false',
    'v8_enable_backtrace': 'true',
    'v8_enable_slow_dchecks': 'false',
    'v8_optimized_debug': 'false',
    'v8_static_library': 'true',
    'v8_enable_pointer_compression_shared_cage ': 'false',
    'enable_iterator_debugging': 'true'
}

build_v8_modules = [
    'v8_compiler',
    'v8_base_without_compiler',
    'v8_libplatform',
    'v8_libbase',
    'torque_generated_initializers',
    'torque_generated_definitions',
    'v8_bigint',
    'v8_heap_base',
    'v8_heap_base_headers',
    'v8_snapshot',
    'v8_turboshaft',
    'cppgc_base',
    'inspector'
]

# We rename them to .a since bazel doesn't like the .lib extension
copy_v8_libs = {
    'libchrome_zlib.a': [
        'obj/third_party/zlib/google/compression_utils_portable'
        'obj/third_party/zlib/zlib',
        'obj/third_party/zlib/zlib_adler32_simd',
        'obj/third_party/zlib/zlib_arm_crc32',
        'obj/third_party/zlib/zlib_inflate_chunk_simd',
    ],
    'libcppgc_base.a': [
        'obj/cppgc_base'
    ],
    'libcrdtp_platform.a': [
        'obj/third_party/inspector_protocol/crdtp_platform'
    ],
    'libcrdtp.a': [
        'obj/third_party/inspector_protocol/crdtp'
    ],
    'libicui18n.a': [
        'obj/third_party/icu/libicui18n'
    ],
    'libicuuc.a': [
        'obj/third_party/icu/libicuuc'
    ],
    'libinspector_string_conversions.a': [
        'obj/src/inspector/inspector_string_conversions'
    ],
    'libinspector.a': [
        'obj/src/inspector/inspector'
    ],
    'libtorque_generated_definitions.a': [
        'obj/torque_generated_definitions'
    ],
    'libtorque_generated_initializers.a': [
        'obj/torque_generated_initializers'
    ],
    'libv8_base_without_compiler.a': [
        'obj/v8_base_without_compiler'
    ],
    'libv8_bigint.a': [
        'obj/v8_bigint'
    ],
    'libv8_compiler.a': [
        'obj/v8_compiler'
    ],
    'libv8_heap_base.a': [
        'obj/v8_heap_base'
    ],
    'libv8_libbase.a': [
        'obj/v8_libbase'
    ],
    'libv8_libplatform.a': [
        'obj/v8_libplatform'
    ],
    'libv8_snapshot.a': [
        'obj/v8_snapshot'
    ],
    'libv8_turboshaft.a': [
        'obj/v8_turboshaft'
    ],
}


package_v8_libs = {
    # these don't get bundled into the zlib one so we have to manually add them
    'zlib_extra.a': [
        'obj/third_party/zlib/zlib_adler32_simd/*.obj',
        'obj/third_party/zlib/zlib_crc32_simd/*.obj',
        'obj/third_party/zlib/zlib_inflate_chunk_simd/*.obj',
    ]
}

vs_vc_path = None
vc_env_cmd = None


def package_lib(arch, build_dir, module_dirs, lib_name):
    global vs_vc_path, vc_env_cmd

    if len(module_dirs) == 0:
        print(f'{lib_name} passed an empty list of directories to merge')

    if arch == 'x86_64':
        arch = 'amd64'
    if arch == 'x86_32':
        arch = 'x86'

    if vs_vc_path is None:
        vs_vc_path = subprocess.run(['C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vswhere.exe',
                                     '-latest', '-property', 'installationPath'], shell=True, capture_output=True)
        vs_vc_path = vs_vc_path.stdout.decode('utf-8').strip()
        vc_env_cmd = Path(vs_vc_path) / Path('VC/Auxiliary/Build/vcvarsall.bat')

    run_args = [vc_env_cmd, arch, 'store', '10.0.22621.0', '&', 'lib', '/OUT:' + str(lib_name)]
    run_args.extend(module_dirs)
    result = subprocess.run(run_args, shell=True, cwd=build_dir, capture_output=True)
    if result.returncode != 0:
        return False
    return True
