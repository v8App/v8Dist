from __future__ import annotations

import os
import platform
import subprocess
import sys


def wait_for_enter():
    if sys.version_info[0] == 2:
        raw_input('Press enter to continue')
    else:
        input('Press enter to continue')


def generate_run_args(args: list, as_list: bool) -> list | str:
    if as_list:
        return args
    return ' '.join(args)


host_os = platform.system()
arg_as_list = False
if host_os == 'Windows':
    arg_as_list = True

top = os.path.dirname(os.path.abspath(sys.argv[0]))

has_git = subprocess.run(generate_run_args(['git', '--version'], arg_as_list), shell=True, cwd=top, capture_output=True)
if has_git.returncode != 0:
    print("Must have git installed to run this script")
    sys.exit(1)

has_git = subprocess.run(generate_run_args(['git', 'rev-parse', '--show-toplevel'], arg_as_list), shell=True, cwd=top,
                         capture_output=True)
if has_git.returncode != 0:
    print("Failed to get the repositories top level directory. make sure you have git version >=1.7.0"
          " and make sure this script is in the v8Dist repository")
    sys.exit(1)

top = has_git.stdout.decode('utf-8').strip()

if host_os == "Windows":
    has_git = subprocess.run(['curl', '--version'], shell=True, cwd=top)
    if has_git.returncode != 0:
        print("Must have curl installed to run this script")
        sys.exit(1)

    print('Downloading depot_tools')
    ret_code = subprocess.run(
        ['curl', '-o', 'depot_tools.zip', 'https://storage.googleapis.com/chrome-infra/depot_tools.zip'], shell=True,
        cwd=top)
    if ret_code.returncode != 0:
        print("Failed to download depot_tools")
        sys.exit(1)

    print('Downloading winsdksetup.exe')
    ret_code = subprocess.run(['curl', '-o' 'winsdksetup.exe',
                               'https://download.microsoft.com/download/7/9/6/7962e9ce-cd69-4574-978c-1202654bd729/windowssdk/winsdksetup.exe'
                               ], shell=True, cwd=top)
    if ret_code.returncode != 0:
        print('Failed to download the winsdksetup.exe')
        sys.exit(1)

    vs_setup = 'C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\setup.exe'
    vs_where = 'C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vswhere.exe'

    ret_code = subprocess.run([vs_where, '-latest', '-property', 'productId'], shell=True, cwd=top, capture_output=True)
    if ret_code.returncode != 0:
        print('Failed to get the productId from vswhere.exe')
        sys.exit(1)
    product_id = ret_code.stdout.decode('utf-8').strip()

    ret_code = subprocess.run([vs_where, '-latest', '-property', 'channelID'], shell=True, cwd=top, capture_output=True)
    if ret_code.returncode != 0:
        print('Failed to get the channelId from vswhere.exe')
        sys.exit(1)
    channel_id = ret_code.stdout.decode('utf-8').strip()

    print("Installing required Visual Studio components")
    print('Visual Studio Installer will launch, click modify and if you see close then close and exit, '
          'otherwise click modify to install additional components needed')
    wait_for_enter()
    ret_code = subprocess.run([vs_setup, 'install', '--add', 'Microsoft.VisualStudio.Workload.NativeDesktop', '--add',
                               'Microsoft.VisualStudio.Component.VC.ATLMFC', '--includeRecommended', '--productId',
                               product_id, '--channelId', channel_id], shell=True, cwd=top, capture_output=True)
    if ret_code.returncode != 0:
        print("Failed to install the required Visual Studio components")
        sys.exit(1)

    print("Installing the windows desktop debugger")
    print('Allow the winsdksetup.exe to modify your computer.')
    wait_for_enter()
    ret_code = subprocess.run(['winsdksetup.exe', '/features', 'OptionId.WindowsDesktopDebuggers',
                               '/quiet', '/norestart'], shell=True, cwd=top)
    if ret_code.returncode != 0:
        print("Failed to install the windows desktop debugger")

    os.unlink(top + '/depot_tools.zip')
    os.unlink(top + '/winsdksetup.exe')
else:
    if os.path.exists(top+'/depot_tools') is False:
        ret_code = subprocess.run(
            generate_run_args(['git', 'clone', 'https://chromium.googlesource.com/chromium/tools/depot_tools.git'],
                              arg_as_list), shell=True, cwd=top)
        if ret_code.returncode != 0:
            print("Failed to clone the depot_tools repo")
            sys.exit(1)

depot_env = os.environ.copy()
# we want it at the front
if host_os == 'Windows':
    depot_env['PATH'] = top + '/depot_tools;' + depot_env['PATH']
    depot_env['DEPOT_TOOLS_WIN_TOOLCHAIN'] = '0'
else:
    depot_env['PATH'] = top + '/depot_tools:' + depot_env['PATH']

ret_code = subprocess.run(
    generate_run_args(['gclient', 'sync', '--gclientfile=.v8_gclient', '--with_branch_heads', '--with_tags'],
                      arg_as_list),  shell=True, cwd=top, env=depot_env)
if ret_code.returncode != 0:
    print('Failed to do initial gclient sync for v8')
    sys.exit(1)

#ret_code = subprocess.run(generate_run_args(['fetch', 'v8', ], arg_as_list),
#                          shell=True, cwd=top, env=depot_env)
#if ret_code.returncode != 0:
#    print('Failed to fetch v8')
#    sys.exit(1)

with open(top + '/v8Version', 'r') as f:
    v8_version = f.read()

ret_code = subprocess.run(generate_run_args(['git', 'fetch'], arg_as_list),
                          shell=True, cwd=top + '/v8', env=depot_env)
if ret_code.returncode != 0:
    print('Failed to fetch v8 updates')
    sys.exit(1)

ret_code = subprocess.run(generate_run_args(['git', 'checkout', "tags/"+v8_version], arg_as_list),
                          shell=True, cwd=top + '/v8', env=depot_env)
if ret_code.returncode != 0:
    print('Failed to checkout v8 version: ' + v8_version)
    sys.exit(1)

print('Finished setup')
