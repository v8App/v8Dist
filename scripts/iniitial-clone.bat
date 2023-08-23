@echo off

rem Copyright 2020 The v8App Authors. All rights reserved.
rem Use of this source code is governed by a MIT license that can be
rem found in the LICENSE file.

SET TOP=%~dp0
set TOP=%TOP:~0,-1%

rem check for git installed
git --version >NUL
if %ERRORLEVEL% neq 0 echo "Doesn't seem as id git is isntalled, as getting the git version faild." & exit 1

rem clone the repository
git clone https://github.com/v8App/v8Dist.git
if %ERRORLEVEL% neq 0 echo "Failed to clone the v8Dist repo." && exit 1

set TOP=%TOP%\v8Dist
cd "%TOP%"
if %ERRORLEVEL% neq 0 echo "Failed to change to %TOP%." && exit 1

set BUILD_ROOT=%TOP%
echo "running setup"
call %TOP%\scripts\setup-v8.bat
echo ""
echo ""
echo "You will want to add this this path '%TOP%\depot_tools' to your PATH variable."
