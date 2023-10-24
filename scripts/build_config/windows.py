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
    'v8_enable_pointer_compression_shared_cage ':'false',
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
    'enable_iterator_debugging':'true'
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

package_v8_libs = {
    'v8_compiler.a': 'v8_compiler',
    'v8_base_without_compiler_0.a': 'v8_base_without_compiler_0',
    'v8_base_without_compiler_1.a': 'v8_base_without_compiler_1',
    'v8_libplatform.a': 'v8_libplatform',
    'v8_libbase.a': 'v8_libbase',
    'torque_generated_initializers.a': 'torque_generated_initializers',
    'torque_generated_definitions.a': 'torque_generated_definitions',
    'v8_bigint.a': 'v8_bigint',
    'v8_heap_base.a': 'v8_heap_base',
    'v8_snapshot.a': 'v8_snapshot',
    'v8_turboshaft.a': 'v8_turboshaft',
    'cppgc_base.a': 'cppgc_base',
    'libcrdtp.a': 'third_party/inspector_protocol/crdtp',
    'libcrdpt_platform.a': 'third_party/inspector_protocol/crdtp_platform',
    'libzlib.a': [
        'third_party/zlib/zlib',
        'third_party/zlib/zlib_adler32_simd',
        'third_party/zlib/zlib_crc32_simd',
        'third_party/zlib/zlib_inflate_chunk_simd',
        'third_party/zlib/google/compression_utils_portable',
    ],
    'libicu.a': [
        'third_party/icu/icui18n',
        'third_party/icu/icuuc_private'
    ],
    'libcppgc_base.a': 'cppgc_base',
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
