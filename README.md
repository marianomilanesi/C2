# C2
Simple C2 that uses ssl sockets to communicate with the github api in order to exfil data, run OS commands and upload/download 64bit shellcode in order to inject it using syscalls.

Current modules:

ReverseShell: Only available with persistant stagers. Uploads commands to be executed, when the stager is executed the command will be downloaded and executed as well, the output will then be accessible via client.

Inject: Uploads the executable as shellcode, when the stager is executed the shellcode will be downlaoded and injected into the target process using syscall.

## Usage

 - Run pip install requirements
 - Run config.py and provide the requested information
 - Run C2.py
 
## Requirements 

 - Visual Studio 2019 (Make sure to have MSBuild.exe on the system PATH)
 - Python3
 
## TODO

 - Add more persistence methods
 - Implement more efficient way to exfil large files
 
## Credits

 - https://github.com/fela15/directInjectorPOC
