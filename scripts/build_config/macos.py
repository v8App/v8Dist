import os.path
import subprocess
from pathlib import Path

gn_args_release = {
    'is_debug': 'false',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'dcheck_always_on': 'false',
    'use_custom_libcxx': 'false',
    'v8_static_library': 'true',
    'v8_enable_pointer_compression_shared_cage ': 'false',
    "v8_use_libm_trig_functions":"false",
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
    'v8_static_library': 'true',
    'v8_enable_pointer_compression_shared_cage ': 'false',
    'enable_iterator_debugging': 'true',
    "v8_use_libm_trig_functions": "false",
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

copy_v8_libs = {
    'obj/third_party/zlib/libchrome_zlib.a': 'libchrome_zlib.a',
    'obj/third_party/zlib/google/libcompression_utils_portable.a': 'libcompression_utils_portable.a',
    'obj/libcppgc_base.a': 'libcppgc_base.a',
    'obj/third_party/inspector_protocol/libcrdtp_platform.a': 'libcrdtp_platform.a',
    'obj/third_party/inspector_protocol/libcrdtp.a': 'libcrdtp.a',
    'obj/third_party/icu/libicui18n.a': 'libicui18n.a',
    'obj/third_party/icu/libicuuc.a': 'libicuuc.a',
    'obj/src/inspector/libinspector_string_conversions.a': 'libinspector_string_conversions.a',
    'obj/src/inspector/libinspector.a': 'libinspector.a',
    'obj/libtorque_generated_definitions.a': 'libtorque_generated_definitions.a',
    'obj/libtorque_generated_initializers.a': 'libtorque_generated_initializers.a',
    'obj/libv8_base_without_compiler.a': 'libv8_base_without_compiler.a',
    'obj/libv8_bigint.a': 'libv8_bigint.a',
    'obj/libv8_compiler.a': 'libv8_compiler.a',
    'obj/libv8_heap_base.a': 'libv8_heap_base.a',
    'obj/libv8_libbase.a': 'libv8_libbase.a',
    'obj/libv8_libplatform.a': 'libv8_libplatform.a',
    'obj/libv8_snapshot.a': 'libv8_snapshot.a',
    'obj/libv8_turboshaft.a': 'libv8_turboshaft.a',

}

package_v8_libs = {
    # these don't get bundled into the zlib one so we have to manually add them
    'libzlib_extra.a': [
    'obj/third_party/zlib/zlib_adler32_simd/*.o' ,
    'obj/third_party/zlib/zlib_crc32_simd/*.o' ,
    'obj/third_party/zlib/zlib_arm_crc32/*.o' ,
    'obj/third_party/zlib/zlib_inflate_chunk_simd/*.o' ,
    ]
}


def package_lib(arch, build_dir, module_dirs, lib_name):
    args = ['ar', 'r', str(lib_name)]
    for mod_dir in module_dirs:
        if os.path.exists(build_dir / Path(mod_dir).parent):
            args.append(mod_dir)
    run_args = ''
    for arg in args:
        if type(arg) is not str:
            run_args += ' ' + str(arg)
        else:
            run_args += ' ' + arg
    result = subprocess.run(run_args, shell=True, cwd=build_dir, capture_output=True)
    return result.returncode == 0