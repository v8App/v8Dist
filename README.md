# v8Dist
v8App's repository for building v8 distributions

 ##Get the code
 
 Mac OS, Linux
 ```bash
curl https://raw.githubusercontent.com/v8App/v8Dist/main/scripts/iniitial-clone.sh | bash -s
```
Windows
```cmd
curl -o initial-clone.bat https://raw.githubusercontent.com/v8App/v8Dist/main/scripts/iniitial-clone.bat
initial-clone.bat

```
As part of the windows setup for V8, Visual Studio will need to be installed first as the script will run the installer to make sure required compoenents are installed. When the installer window comes up if you have a modify button then the components need to be installed so click on modify. If you have close then the components are installed. You can close the window after installation is finished. A specific version of the windows sdk debugger also needs to be installed you will get a pop asking if you want to modify your computer from winsdksetup.exe, allow and it'll install the debugger.