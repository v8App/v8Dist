import argparse
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser(description="Builds v8 for the specified platform")
parser.add_argument('--build-root', type=str, required=True, dest='build_root',
                    help='The build root, usually the v8Dist repository')

platforms = parser.add_argument_group('Platforms', 'At least one platform must be specified')
platforms.add_argument('--macos', action='store_true', help='Specifies to build the mac os version of the library')
platforms.add_argument('--ios', action='store_true', help='Specifies to build the ios version of the library')
platforms.add_argument('--windows', action='store_true', help='Specifies to build the windows version of the library')
platforms.add_argument('--android', action='store_true', help='Specifies to build the android version of the library')
platforms.add_argument('--linux', action='store_true', help='Specifies to build the linux version of the library')

parser.add_argument('--arch', type=str, choices=['x64', 'arm', 'arm32', 'arm64'],
                    default='x64', help='Specifies to architecture to build for. '
                                        'Defaults to x64 for all platforms but ios which defaults to arm64')
args = parser.parse_args()

if not args.macos and not args.ios and not args.windows and not args.android and not args.linux:
    parser.print_help()
    sys.exit(1)
# require at least python 3.4
if sys.version_info.major < 3 and (sys.version_info.major == 3 and sys.version_info.minor < 4):
    print('Require atr least python >= 3.4')
    sys.exit(1)
build_root = Path(args.build_root).resolve()
build_dir_root = build_root / Path('v8/out.gn')
os.makedirs(build_dir_root, exist_ok=True)

with open(build_root / 'v8Version') as f:
    v8_version = f.read()

v8_version = v8_version.strip()

host_os = platform.system()


def setup_v8_target_oss(arch, gn_args):
    host_arch = platform.machine().lower()

    if host_arch in ['amd64', 'x86_64']:
        host_arch = 'x64'
    elif host_arch in ['arm64']:
        host_arch = 'arm64'

    # quotes are important here
    gn_args['target_cpu'] = f'"{host_arch}"'
    gn_args['v8_target_cpu'] = f'"{arch}"'

    return gn_args


def core_build(build, arch, package_lib, gn_args, build_v8_modules, package_v8_modules, obj_ext, platform_env=None):
    if platform_env is None:
        platform_env = {}
    build_name = f'{v8_version}_{build}'
    v8_root = build_root / Path('v8')
    rel_build_dir = Path('out.gn') / Path(build)
    build_dir = v8_root / Path('out.gn') / Path(build)
    dist_dir = build_root / Path(f'dists/{build_name}')

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(dist_dir, exist_ok=True)

    dst_arg_file = build_dir / Path('args.gn')
    with open(dst_arg_file, 'w') as arg_file:
        for arg_name, arg_value in gn_args.items():
            arg_file.writelines(f'{arg_name} = {arg_value}\n')

    env = os.environ.copy()
    if env is not None:
        env.update(platform_env)
    env['PATH'] = str(Path(f'{build_root}/depot_tools').resolve()) + ';' + os.environ['PATH']

    proc = subprocess.run(['gn', 'gen', build_dir], shell=True, env=env, cwd=v8_root)
    if proc.returncode != 0:
        print("Failed to generate the build files")
        return
    proc = subprocess.run(['ninja', '-C', rel_build_dir, *build_v8_modules], shell=True, env=env, cwd=v8_root)
    if proc.returncode != 0:
        print('Failed to build v8 modules')
        return

    # package the compiled v8 libs
    for lib_name, module_dirs in package_v8_modules.items():
        print(f'packaging library {lib_name}')
        if type(module_dirs) is str:
            module_dirs = [module_dirs]
        full_module_dir = []
        for module_dir in module_dirs:
            full_module_dir.append(Path(module_dir) / Path(obj_ext))

        if not package_lib(arch, (build_dir / Path('obj')), full_module_dir, (dist_dir / Path(f'{lib_name}'))):
            print(f"Failed to package {lib_name} library")
            return

    shutil.copyfile((build_dir / Path(f'icudtl.dat')), (dist_dir / Path(f'icudtl.dat')))
    shutil.copyfile((build_dir / Path(f'snapshot_blob.bin')), (dist_dir / Path(f'snapshot_blob.bin')))

    print(f'zipping up the libraries for {build_name}')
    with zipfile.ZipFile(build_root / Path(f'{build_name}.zip'), 'w', zipfile.ZIP_DEFLATED) as lib_zip_ref:
        files = os.listdir(dist_dir)
        for file in files:
            if file.startswith('.'):
                continue
            lib_zip_ref.write(dist_dir / Path(file), arcname=Path(dist_dir.name) / Path(file))


def build_macos(host, arch):
    from build_config.macos import gn_args_debug, gn_args_release, package_lib, package_v8_libs, build_v8_modules
    if host != 'Darwin':
        print('Skipping macos build as we are not on a MacOs host')
        return

    if arch != 'arm64' and arch != 'x64':
        print('macos can only be built for arm64 or x64')
        return

    core_build(f'macos-{arch}-release', arch, package_lib, setup_v8_target_oss(arch, gn_args_release), build_v8_modules,
               package_v8_libs, '*.o')
    core_build(f'macos-{arch}-debug', arch, package_lib, setup_v8_target_oss(arch, gn_args_debug), build_v8_modules,
               package_v8_libs, '*.o')


def build_ios(host, arch):
    from build_config.ios import gn_args_debug, gn_args_release, package_lib, package_v8_libs, build_v8_modules
    if host != 'Darwin':
        print('Skipping ios build as we are not on a MacOs host')
        return

    if arch != 'arm64' and arch != 'x64':
        print('ios can only be built for arm64 or x64 simulator')
        return

    core_build(f'ios-{arch}-release', arch, package_lib, setup_v8_target_oss(arch, gn_args_release), build_v8_modules,
               package_v8_libs, '*.o')
    core_build(f'ios-{arch}-debug', arch, package_lib, setup_v8_target_oss(arch, gn_args_debug), build_v8_modules,
               package_v8_libs, '*.o')


def build_windows(host, arch):
    from build_config.windows import gn_args_debug, gn_args_release, package_lib, package_v8_libs, build_v8_modules
    if host != 'Windows':
        print('Skipping ios build as we are not on a Windows host')
        return

    env = {
        'DEPOT_TOOLS_WIN_TOOLCHAIN': '0'
    }

    core_build(f'win-{arch}-release', arch, package_lib, setup_v8_target_oss(arch, gn_args_release), build_v8_modules,
               package_v8_libs, '*.obj', env)
    #core_build(f'win-{arch}-debug', arch, package_lib, setup_v8_target_oss(arch, gn_args_debug), build_v8_modules,
    #           package_v8_libs, '*.obj', env)


def build_android(host, arch):
    print('TODO')
    return


def build_linux(host, arch):
    print('TODO')
    return


if args.macos:
    build_macos(host_os, args.arch)

if args.ios:
    build_ios(host_os, args.arch)

if args.windows:
    build_windows(host_os, args.arch)

if args.android:
    build_android(host_os, args.arch)

if args.linux:
    build_linux(host_os, args.arch)

# pack the include directory for the version
print('zipping up the v8 includes directory')
with zipfile.ZipFile(build_root / Path(f'v8-{v8_version}-includes.zip'), 'w', zipfile.ZIP_DEFLATED) as zip_ref:
    v8_path = build_root / Path('v8/include')
    for folder_name, sub_folders, file_names in os.walk(v8_path):
        zip_path = Path(folder_name).relative_to(build_root / Path('v8'))
        for file_name in file_names:
            zip_ref.write(Path(folder_name) / Path(file_name), arcname=zip_path / Path(file_name))
