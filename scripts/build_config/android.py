import subprocess
from pathlib import Path

# None os this has been tested for android so WIP
gn_args_release = {
    'is_debug': 'false',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'is_clang': 'false',
    'dcheck_always_on': 'false',
}

gn_args_debug = {
    'is_debug': 'true',
     'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'is_clang': 'false',
    'v8_enable_backtrace': 'true',
    'v8_enable_slow_dchecks': 'true',
    'v8_optimized_debug': 'false',
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
    'v8_compiler.lib':'v8_compiler',
    'v8_base_without_compiler.lib':'v8_base_without_compiler',
    'v8_libplatform.lib':'v8_libplatform',
    'v8_libbase.lib':'v8_libbase',
    'torque_generated_initializers.lib':'torque_generated_initializers',
    'torque_generated_definitions.lib':'torque_generated_definitions',
    'v8_bigint.lib':'v8_bigint',
    'v8_heap_base.lib':'v8_heap_base',
    'v8_snapshot.lib':'v8_snapshot',
    'cppgc_base.lib':'cppgc_base',
    'libcrdtp.lib':'third_party/inspector_protocol/crdtp',
    'libcrdpt_platform.lib':'third_party/inspector_protocol/crdtp_platform',
    'libzlib.lib':[
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
    'libcppgc_base.lib':'cppgc_base',
}

vs_vc_path = None
vc_env_cmd = None


def package_lib(arch, module_path, lib_name):
    pass

