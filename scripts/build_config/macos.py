import subprocess
from pathlib import Path

gn_args_release = {
    'is_debug': 'false',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'dcheck_always_on': 'false',
    'use_custom_libcxx': 'false',
}

gn_args_debug = {
    'is_debug': 'true',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'v8_enable_backtrace': 'true',
    'v8_enable_slow_dchecks': 'true',
    'v8_optimized_debug': 'false',
    'use_custom_libcxx': 'false',
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
    'cppgc_base',
    'inspector'
]

package_v8_libs = {
    'v8_compiler.lib': 'v8_compiler',
    'v8_base_without_compiler.lib': 'v8_base_without_compiler',
    'v8_libplatform.lib': 'v8_libplatform',
    'v8_libbase.lib': 'v8_libbase',
    'torque_generated_initializers.lib': 'torque_generated_initializers',
    'torque_generated_definitions.lib': 'torque_generated_definitions',
    'v8_bigint.lib': 'v8_bigint',
    'v8_heap_base.lib': 'v8_heap_base',
    'v8_snapshot.lib': 'v8_snapshot',
    'cppgc_base.lib': 'cppgc_base',
    'libcrdtp.lib': 'third_party/inspector_protocol/crdtp',
    'libcrdpt_platform.lib': 'third_party/inspector_protocol/crdtp_platform',
    'libzlib.lib': [
        'third_party/zlib/zlib',
        'third_party/zlib/zlib_adler32_simd',
        'third_party/zlib/zlib_inflate_chunk_simd',
        'third_party/zlib/zlib_crc32_simd',
        'third_party/zlib/google/compression_utils_portable',
    ],
    'libicu.lib': [
        'third_party/icu/icui18n',
        'third_party/icu/icuuc_private'
    ],
    'libcppgc_base.lib': 'cppgc_base',
}

vs_vc_path = None
vc_env_cmd = None


def package_lib(arch, build_dir, module_dirs, lib_name):
    args = ['ar', 'r', str(lib_name), '*.a']
    args.extend(module_dirs)
    run_args = ''
    for arg in args:
        if type(arg) is not str:
            run_args += ' ' + str(arg)
        else:
            run_args += ' ' + arg
    result = subprocess.run(run_args, shell=True, cwd=build_dir, capture_output=True)
    if result.returncode != 0:
        return False
    return True
