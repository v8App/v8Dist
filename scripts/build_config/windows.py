import subprocess
from pathlib import Path

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
    'v8_enable_slow_dchecks': 'false',
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
    'v8_turboshaft',
    'cppgc_base',
    'inspector',
]

# We rename them to .a since bazel doesn't like the .lib extension
package_v8_libs = {
    "abseil.a": {
        "noarch": [
            "obj/third_party/abseil-cpp/absl/base/base/*.obj",
            "obj/third_party/abseil-cpp/absl/base/log_severity/*.obj",
            "obj/third_party/abseil-cpp/absl/base/malloc_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/base/raw_logging_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/base/spinlock_wait/*.obj",
            "obj/third_party/abseil-cpp/absl/base/strerror/*.obj",
            "obj/third_party/abseil-cpp/absl/base/throw_delegate/*.obj",
            "obj/third_party/abseil-cpp/absl/container/hashtablez_sampler/*.obj",
            "obj/third_party/abseil-cpp/absl/container/raw_hash_set/*.obj",
            "obj/third_party/abseil-cpp/absl/crc/cpu_detect/*.obj",
            "obj/third_party/abseil-cpp/absl/crc/crc32c/*.obj",
            "obj/third_party/abseil-cpp/absl/crc/crc_cord_state/*.obj",
            "obj/third_party/abseil-cpp/absl/crc/crc_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/debugging/debugging_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/debugging/demangle_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/debugging/examine_stack/*.obj",
            "obj/third_party/abseil-cpp/absl/debugging/failure_signal_handler/*.obj",
            "obj/third_party/abseil-cpp/absl/debugging/stacktrace/*.obj",
            "obj/third_party/abseil-cpp/absl/debugging/symbolize/*.obj",
            "obj/third_party/abseil-cpp/absl/hash/city/*.obj",
            "obj/third_party/abseil-cpp/absl/hash/hash/*.obj",
            "obj/third_party/abseil-cpp/absl/hash/low_level_hash/*.obj",
            "obj/third_party/abseil-cpp/absl/log/die_if_null/*.obj",
            "obj/third_party/abseil-cpp/absl/log/globals/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/check_op/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/conditions/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/fnmatch/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/format/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/globals/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/log_message/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/log_sink_set/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/nullguard/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/proto/*.obj",
            "obj/third_party/abseil-cpp/absl/log/internal/vlog_config/*.obj",
            "obj/third_party/abseil-cpp/absl/log/log_entry/*.obj",
            "obj/third_party/abseil-cpp/absl/log/log_sink/*.obj",
            "obj/third_party/abseil-cpp/absl/numeric/int128/*.obj",
            "obj/third_party/abseil-cpp/absl/profiling/exponential_biased/*.obj",
            "obj/third_party/abseil-cpp/absl/random/distributions/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/platform/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/pool_urbg/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/randen/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/randen_hwaes/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/randen_hwaes_impl/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/randen_slow/*.obj",
            "obj/third_party/abseil-cpp/absl/random/internal/seed_material/*.obj",
            "obj/third_party/abseil-cpp/absl/random/seed_gen_exception/*.obj",
            "obj/third_party/abseil-cpp/absl/random/seed_sequences/*.obj",
            "obj/third_party/abseil-cpp/absl/status/status/*.obj",
            "obj/third_party/abseil-cpp/absl/status/statusor/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/cord/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/cord_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/cordz_functions/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/cordz_handle/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/cordz_info/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/internal/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/str_format_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/string_view/*.obj",
            "obj/third_party/abseil-cpp/absl/strings/strings/*.obj",
            "obj/third_party/abseil-cpp/absl/synchronization/graphcycles_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/synchronization/kernel_timeout_internal/*.obj",
            "obj/third_party/abseil-cpp/absl/synchronization/synchronization/*.obj",
            "obj/third_party/abseil-cpp/absl/time/cctz/civil_time/*.obj",
            "obj/third_party/abseil-cpp/absl/time/cctz/time_zone/*.obj",
            "obj/third_party/abseil-cpp/absl/time/time/*.obj",
            "obj/third_party/abseil-cpp/absl/types/bind_optional_access/*.obj",
            "obj/third_party/abseil-cpp/absl/types/bad_variant_access/*.obj",
        ],
    },
    'libchrome_zlib.a': {
        'noarch':
            [
                'obj/third_party/zlib/google/compression_utils_portable/*.obj',
                'obj/third_party/zlib/zlib/*.obj',
                'obj/third_party/zlib/zlib_adler32_simd/*.obj',
                'obj/third_party/zlib/zlib_inflate_chunk_simd/*.obj',
            ],
        'x64': [
            'obj/third_party/zlib/zlib_crc32_simd/*.obj',
        ],
        'arm64':
            [
                'obj/third_party/zlib/zlib_arm_crc32/*.obj',
            ]
    },
    'libcppgc_base.a': [
        'obj/cppgc_base/*.obj'
    ],
    'libcrdtp_platform.a': [
        'obj/third_party/inspector_protocol/crdtp_platform/*.obj'
    ],
    'libcrdtp.a': [
        'obj/third_party/inspector_protocol/crdtp/*.obj'
    ],
    'libicui18n.a': [
        'obj/third_party/icu/icui18n/*.obj'
    ],
    'libicuuc.a': [
        'obj/third_party/icu/icuuc_private/*.obj'
    ],
    'libinspector.a': [
        'obj/src/inspector/inspector/*.obj'
    ],
    'libinspector_string_conversions.a': [
        'obj/src/inspector/inspector_string_conversions/*.obj'
    ],
    'libtorque_generated_definitions.a': [
        'obj/torque_generated_definitions/*.obj'
    ],
    'libtorque_generated_initializers.a': [
        'obj/torque_generated_initializers/*.obj'
    ],
    'libv8_base_without_compiler_0.a': [
        'obj/v8_base_without_compiler_0/*.obj'
    ],
    'libv8_base_without_compiler_1.a': [
        'obj/v8_base_without_compiler_1/*.obj'
    ],

    'libv8_bigint.a': [
        'obj/v8_bigint/*.obj'
    ],
    'libv8_compiler.a': [
        'obj/v8_compiler/*.obj'
    ],
    'libv8_heap_base.a': [
        'obj/v8_heap_base/*.obj'
    ],
    'libv8_libinit.a': [
        'obj/v8_init/*.obj'
    ],
    'libv8_libinitializers.a': [
        'obj/v8_initializers/*.obj'
    ],
    'libv8_libbase.a': [
        'obj/v8_libbase/*.obj'
    ],
    'libv8_libplatform.a': [
        'obj/v8_libplatform/*.obj'
    ],
    'libv8_snapshot.a': [
        'obj/v8_snapshot/*.obj'
    ],
    'libv8_turboshaft.a': [
        'obj/v8_turboshaft/*.obj'
    ],
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
