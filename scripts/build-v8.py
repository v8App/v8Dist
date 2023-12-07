from __future__ import annotations

import argparse
import json
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
dist_dir = build_root / Path('dists')
os.makedirs(build_dir_root, exist_ok=True)

with open(build_root / 'v8Version') as f:
    v8_version = f.read()

v8_version = v8_version.strip()

host_os = platform.system()
arg_as_list = False
if host_os == 'Windows':
    arg_as_list = True


def generate_run_args(in_args: list, as_list: bool) -> list | str:
    if as_list:
        return in_args
    ret_args = ''
    for arg in in_args:
        if type(arg) is not str:
            ret_args += ' ' + str(arg)
        else:
            ret_args += ' ' + arg
    return ret_args


github_token = None
if 'GITHUB_API_TOKEN' in os.environ:
    github_token = os.environ['GITHUB_API_TOKEN']
    has_curl = subprocess.run(generate_run_args(['curl', '--version'], arg_as_list), shell=True)
    if has_curl.returncode != 0:
        print(
            "Must have curl installed in order to upload releases. If you just want to "
            "build remove the GITHUB_API_TOKEN environment var")
        sys.exit(1)

if github_token is None or len(github_token) == 0:
    # just to make sure it's None
    github_token = None
    print('Github token not found release distribution uploads will not be done')


def setup_v8_target_oss(arch, gn_args):
    # host_arch = platform.machine().lower()

    # if host_arch in ['amd64', 'x86_64']:
    #    host_arch = 'x64'
    # elif host_arch in ['arm64']:
    #    host_arch = 'arm64'

    # quotes are important here
    gn_args['v8_target_cpu'] = f'"{arch}"'
    gn_args['target_cpu'] = f'"{arch}"'

    return gn_args


def core_build(arch, build, gn_args, build_v8_modules, copy_v8_libs, package_v8_modules, package_lib,
               platform_env=None):
    if platform_env is None:
        platform_env = {}
    build_name = f'{v8_version}_{build}'
    v8_root = build_root / Path('v8')
    rel_build_dir = Path('out.gn') / Path(build)
    build_dir = v8_root / Path('out.gn') / Path(build)
    core_dist_dir = build_root / Path(f'dists/{build_name}')

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(core_dist_dir, exist_ok=True)

    dst_arg_file = build_dir / Path('args.gn')
    with open(dst_arg_file, 'w') as arg_file:
        for arg_name, arg_value in gn_args.items():
            arg_file.writelines(f'{arg_name} = {arg_value}\n')

    env = os.environ.copy()
    if env is not None:
        env.update(platform_env)
    if host_os == 'Windowa':
        seperator = ';'
    else:
        seperator = ':'

    env['PATH'] = str(Path(f'{build_root}/depot_tools').resolve()) + seperator + os.environ['PATH']

    proc = subprocess.run(generate_run_args(['gn', 'gen', build_dir], arg_as_list), shell=True, env=env, cwd=v8_root)
    if proc.returncode != 0:
        print("Failed to generate the build files")
        return
    proc = subprocess.run(generate_run_args(['ninja', '-C', rel_build_dir, *build_v8_modules], arg_as_list), shell=True,
                          env=env, cwd=v8_root)
    if proc.returncode != 0:
        print('Failed to build v8 modules')
        return

    for lib_name, module_dirs in package_v8_modules.items():
        print(f'packaging library {lib_name}')
        if type(module_dirs) is str:
            module_dirs = [module_dirs]
        full_module_dir = []
        for module_dir in module_dirs:
            full_module_dir.append(Path(module_dir))

        if not package_lib(arch, build_dir, full_module_dir, (core_dist_dir / Path(f'{lib_name}'))):
            print(f"Failed to package {lib_name} library")
            return
    # package the compiled v8 libs
    for lib_path, lib_name in copy_v8_libs.items():
        print(f'copying library {lib_name}')
        shutil.copyfile((build_dir / Path(lib_path)), (core_dist_dir / Path(lib_name)))

    shutil.copyfile((build_dir / Path(f'icudtl.dat')), (core_dist_dir / Path(f'icudtl.dat')))
    shutil.copyfile((build_dir / Path(f'snapshot_blob.bin')), (core_dist_dir / Path(f'snapshot_blob.bin')))

    print(f'zipping up the libraries for {build_name}')
    with zipfile.ZipFile(build_root / Path('dists') / Path(f'{build_name}.zip'), 'w',
                         zipfile.ZIP_DEFLATED) as lib_zip_ref:
        files = os.listdir(core_dist_dir)
        for file in files:
            if file.startswith('.'):
                continue
            lib_zip_ref.write(core_dist_dir / Path(file), arcname=Path(core_dist_dir.name) / Path(file))


def build_macos(host, arch):
    from build_config.macos import gn_args_debug, gn_args_release, copy_v8_libs, package_v8_libs, build_v8_modules, \
        package_lib
    if host != 'Darwin':
        print('Skipping macos build as we are not on a MacOs host')
        return

    if arch != 'arm64' and arch != 'x64':
        print('macos can only be built for arm64 or x64')
        return

    core_build(arch, f'macos-{arch}-release', setup_v8_target_oss(arch, gn_args_release), build_v8_modules,
               copy_v8_libs, package_v8_libs, package_lib)
    core_build(arch, f'macos-{arch}-debug', setup_v8_target_oss(arch, gn_args_debug), build_v8_modules,
               copy_v8_libs, package_v8_libs, package_lib)


def build_ios(host, arch):
    from build_config.ios import gn_args_debug, gn_args_release, package_v8_libs, build_v8_modules
    if host != 'Darwin':
        print('Skipping ios build as we are not on a MacOs host')
        return

    if arch != 'arm64' and arch != 'x64':
        print('ios can only be built for arm64 or x64 simulator')
        return

    # core_build(f'ios-{arch}-release', setup_v8_target_oss(arch, gn_args_release), build_v8_modules,
    #           package_v8_libs)
    # core_build(f'ios-{arch}-debug', setup_v8_target_oss(arch, gn_args_debug), build_v8_modules,
    #           package_v8_libs)


def build_windows(host, arch):
    from build_config.windows import gn_args_debug, gn_args_release, package_v8_libs, copy_v8_libs, build_v8_modules, \
        package_lib
    if host != 'Windows':
        print('Skipping ios build as we are not on a Windows host')
        return

    env = {
        'DEPOT_TOOLS_WIN_TOOLCHAIN': '0'
    }

    core_build(arch, f'win-{arch}-release', setup_v8_target_oss(arch, gn_args_release), build_v8_modules,
               copy_v8_libs, package_v8_libs, package_lib, env)
    core_build(arch, f'win-{arch}-debug', setup_v8_target_oss(arch, gn_args_debug), build_v8_modules,
               copy_v8_libs, package_v8_libs, package_lib, env)


# noinspection PyUnusedLocal
def build_android(host, arch):
    print('TODO')
    return


# noinspection PyUnusedLocal
def build_linux(host, arch):
    print('TODO')
    return


def make_github_call(url, method="GET", call_data=None):
    # since requests isn't a standard library we' use curl
    call_args = [
        'curl',
        "-L",
        "-X",
        method if method != "UPLOAD" else "POST",
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        "Authorization: Bearer " + github_token,
        "-H",
        "X-GitHub-Api-Version: 2022-11-28",
    ]
    if method == 'UPLOAD':
        call_args.append('-H')
        call_args.append('Content-Type: application/octet-stream')
        call_args.append('-H')
        call_args.append('Transfer-Encoding: chunked')

    base_url = 'https://api.github.com/repos/v8App/v8Dist/'
    call_args.append(base_url + url)
    if call_data is not None and method == "POST":
        call_args.append("-d")
        call_args.append(json.dumps(call_data))
    if method == "UPLOAD":
        call_args.append('--data-binary')
        call_args.append(call_data)
    call_args = generate_run_args(call_args, arg_as_list)
    ret_code = subprocess.run(call_args, shell=True, capture_output=True)
    if ret_code.returncode != 0:
        print('Failed to execute curl command to github url:' + base_url + url)
        sys.exit(1)
    response = json.loads(ret_code.stdout.decode('utf-8'))
    return response


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
with zipfile.ZipFile(dist_dir / Path(f'v8-{v8_version}-includes.zip'), 'w',
                     zipfile.ZIP_DEFLATED) as zip_ref:
    v8_path = build_root / Path('v8/include')
    for folder_name, sub_folders, file_names in os.walk(v8_path):
        zip_path = Path(folder_name).relative_to(build_root / Path('v8'))
        for file_name in file_names:
            zip_ref.write(Path(folder_name) / Path(file_name), arcname=zip_path / Path(file_name))

if github_token is not None:
    idx = 1
    release = None
    loop = True
    while loop:
        releases = make_github_call('releases?per_page=100%26page=' + str(idx))
        if len(releases) == 0 or (releases is dict and 'message' in releases):
            loop = False
            continue
        for g_release in releases:
            if g_release['tag_name'] == v8_version:
                release = g_release
                loop = False
        idx += 1
    if release is None:
        data = {
            'tag_name': v8_version,
            'name': v8_version,
            'draft': True,
            'generate_release_notes ': False,
            'body': 'Packaged prebuilt libraries for ' + v8_version
        }
        release = make_github_call('releases', "POST", data)
"""
    Can't do the uploads through the API keep getting 413 entity to large errors
    So we create the release only and have to go to the website and upload that way
    if release is None:
        print('Failed to create the release or find it')
        sys.exit(1)

    if 'upload_url' not in release or 'id' not in release:
        print('Failed to find the upload url or id in the release data:' + json.dumps(release))
        sys.exit(1)
    upload_url = release['upload_url'].replace('{?name,label}', '')
    release_id = release['id']
    dists = os.listdir(dist_dir)
    for dist in dists:
        if '.zip' in dist:
            url = upload_url+'?name='+dist
            make_github_call(url, 'UPLOAD', "@"+str(dist_dir/Path(dist)))
"""
print('Finished building')
