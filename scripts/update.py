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

if os.path.exists(top + '/depot_tools') is False:
    print("depot_tools is not installed use setup instead")
    sys.exit(1)

with open(top + '/v8Version', 'r') as f:
    v8_version = f.read()

depot_env = os.environ.copy()
# we want it at the front
if host_os == 'Windows':
    depot_env['PATH'] = top + '/depot_tools;' + depot_env['PATH']
    depot_env['DEPOT_TOOLS_WIN_TOOLCHAIN'] = '0'
else:
    depot_env['PATH'] = top + '/depot_tools:' + depot_env['PATH']

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

ret_code = subprocess.run(
    generate_run_args(['gclient', 'sync', '-D', '--gclientfile=.v8_gclient', '--with_branch_heads', '--with_tags'],
                      arg_as_list),  shell=True, cwd=top, env=depot_env)
if ret_code.returncode != 0:
    print('Failed to do gclient sync for v8')
    sys.exit(1)

print('Finished setup')
