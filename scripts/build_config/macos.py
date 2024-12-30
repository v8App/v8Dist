import os.path
import subprocess
from pathlib import Path

gn_args_release = {
    'is_debug': 'false',
    'is_component_build': 'false',
    'v8_monolithic': 'false',
    'v8_use_external_startup_data': 'true',
    'dcheck_always_on': 'false',
    'use_custom_libcxx':'false',
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
    'libcppgc_base.a': [
        'obj/cppgc_base/*.o'
    ],
    'libm.a': [
        'obj/libm/*.o'
    ],
    'libinspector.a': [
        'obj/src/inspector/inspector/*.o'
    ],
    'libinspector_string_conversions.a': [
        'obj/src/inspector/inspector_string_conversions/*.o'
    ],
    "abseil.a": {
        "noarch": [
            "obj/third_party/abseil-cpp/absl/base/base/*.o",
            "obj/third_party/abseil-cpp/absl/base/log_severity/*.o",
            "obj/third_party/abseil-cpp/absl/base/malloc_internal/*.o",
            "obj/third_party/abseil-cpp/absl/base/raw_logging_internal/*.o",
            "obj/third_party/abseil-cpp/absl/base/spinlock_wait/*.o",
            "obj/third_party/abseil-cpp/absl/base/strerror/*.o",
            "obj/third_party/abseil-cpp/absl/base/throw_delegate/*.o",
            "obj/third_party/abseil-cpp/absl/container/hashtablez_sampler/*.o",
            "obj/third_party/abseil-cpp/absl/container/raw_hash_set/*.o",
            "obj/third_party/abseil-cpp/absl/crc/cpu_detect/*.o",
            "obj/third_party/abseil-cpp/absl/crc/crc32c/*.o",
            "obj/third_party/abseil-cpp/absl/crc/crc_cord_state/*.o",
            "obj/third_party/abseil-cpp/absl/crc/crc_internal/*.o",
            "obj/third_party/abseil-cpp/absl/debugging/debugging_internal/*.o",
            "obj/third_party/abseil-cpp/absl/debugging/demangle_internal/*.o",
            "obj/third_party/abseil-cpp/absl/debugging/examine_stack/*.o",
            "obj/third_party/abseil-cpp/absl/debugging/failure_signal_handler/*.o",
            "obj/third_party/abseil-cpp/absl/debugging/stacktrace/*.o",
            "obj/third_party/abseil-cpp/absl/debugging/symbolize/*.o",
            "obj/third_party/abseil-cpp/absl/hash/city/*.o",
            "obj/third_party/abseil-cpp/absl/hash/hash/*.o",
            "obj/third_party/abseil-cpp/absl/hash/low_level_hash/*.o",
            "obj/third_party/abseil-cpp/absl/log/die_if_null/*.o",
            "obj/third_party/abseil-cpp/absl/log/globals/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/check_op/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/conditions/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/fnmatch/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/format/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/globals/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/log_message/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/log_sink_set/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/nullguard/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/proto/*.o",
            "obj/third_party/abseil-cpp/absl/log/internal/vlog_config/*.o",
            "obj/third_party/abseil-cpp/absl/log/log_entry/*.o",
            "obj/third_party/abseil-cpp/absl/log/log_sink/*.o",
            "obj/third_party/abseil-cpp/absl/numeric/int128/*.o",
            "obj/third_party/abseil-cpp/absl/profiling/exponential_biased/*.o",
            "obj/third_party/abseil-cpp/absl/random/distributions/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/platform/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/pool_urbg/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/randen/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/randen_hwaes/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/randen_hwaes_impl/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/randen_slow/*.o",
            "obj/third_party/abseil-cpp/absl/random/internal/seed_material/*.o",
            "obj/third_party/abseil-cpp/absl/random/seed_gen_exception/*.o",
            "obj/third_party/abseil-cpp/absl/random/seed_sequences/*.o",
            "obj/third_party/abseil-cpp/absl/status/status/*.o",
            "obj/third_party/abseil-cpp/absl/status/statusor/*.o",
            "obj/third_party/abseil-cpp/absl/strings/cord/*.o",
            "obj/third_party/abseil-cpp/absl/strings/cord_internal/*.o",
            "obj/third_party/abseil-cpp/absl/strings/cordz_functions/*.o",
            "obj/third_party/abseil-cpp/absl/strings/cordz_handle/*.o",
            "obj/third_party/abseil-cpp/absl/strings/cordz_info/*.o",
            "obj/third_party/abseil-cpp/absl/strings/internal/*.o",
            "obj/third_party/abseil-cpp/absl/strings/str_format_internal/*.o",
            "obj/third_party/abseil-cpp/absl/strings/string_view/*.o",
            "obj/third_party/abseil-cpp/absl/strings/strings/*.o",
            "obj/third_party/abseil-cpp/absl/synchronization/graphcycles_internal/*.o",
            "obj/third_party/abseil-cpp/absl/synchronization/kernel_timeout_internal/*.o",
            "obj/third_party/abseil-cpp/absl/synchronization/synchronization/*.o",
            "obj/third_party/abseil-cpp/absl/time/cctz/civil_time/*.o",
            "obj/third_party/abseil-cpp/absl/time/cctz/time_zone/*.o",
            "obj/third_party/abseil-cpp/absl/time/time/*.o",
            "obj/third_party/abseil-cpp/absl/types/bind_optional_access/*.o",
            "obj/third_party/abseil-cpp/absl/types/bad_variant_access/*.o",
        ],
    },
    'libchrome_zlib.a': {
        'noarch':
            [
                'obj/third_party/zlib/google/compression_utils_portable/*.o',
                'obj/third_party/zlib/zlib/*.o',
                'obj/third_party/zlib/zlib_adler32_simd/*.o',
                'obj/third_party/zlib/zlib_inflate_chunk_simd/*.o',
            ],
        'x64': [
            'obj/third_party/zlib/zlib_crc32_simd/*.o',
        ],
        'arm64':
            [
                'obj/third_party/zlib/zlib_arm_crc32/*.o',
            ]
    },
    'libcrdtp_platform.a': [
        'obj/third_party/inspector_protocol/crdtp_platform/*.o'
    ],
    'libcrdtp.a': [
        'obj/third_party/inspector_protocol/crdtp/*.o'
    ],
    'libicui18n.a': [
        'obj/third_party/icu/icui18n/*.o'
    ],
    'libicuuc.a': [
        'obj/third_party/icu/icuuc_private/*.o'
    ],
    # not sure if the next 3 are needed or just for the torque binary
    'libtorque_base.a': [
        'obj/torque_base/*.o'
    ],
    'libtorque_generated_definitions.a': [
        'obj/torque_generated_definitions/*.o'
    ],
    'libtorque_generated_initializers.a': [
        'obj/torque_generated_initializers/*.o'
    ],
    'libv8_base_without_compiler.a': [
        'obj/v8_base_without_compiler/*.o'
    ],
    'libv8_bigint.a': [
        'obj/v8_bigint/*.o'
    ],
    'libv8_compiler.a': [
        'obj/v8_compiler/*.o'
    ],
    'libv8_heap_base.a': [
        'obj/v8_heap_base/*.o'
    ],
    'libv8_init.a': [
        'obj/v8_init/*.o'
    ],
    'libv8_initializers.a': [
        'obj/v8_initializers/*.o'
    ],
    'libv8_libbase.a': [
        'obj/v8_libbase/*.o'
    ],
    'libv8_libplatform.a': [
        'obj/v8_libplatform/*.o'
    ],
    'libv8_snapshot.a': [
        'obj/v8_snapshot/*.o'
    ],
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
