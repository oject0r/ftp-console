import json
import ftplib as fl
import os
import requests
import argparse as ap

def start():
    print('''
███████╗████████╗██████╗      ██████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██╗     ███████╗
██╔════╝╚══██╔══╝██╔══██╗    ██╔════╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██║     ██╔════╝
█████╗     ██║   ██████╔╝    ██║     ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     █████╗
██╔══╝     ██║   ██╔═══╝     ██║     ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██╔══╝
██║        ██║   ██║         ╚██████╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝          ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝
By OJector
    ''')
    input('Press any key, to continue')

    if os.name == 'nt': # for windows
      os.system('cls')
    else: # for mac and linux
      os.system('clear')
preprefix = '' # yeah, it's prefix before prefix

connection = None # connection object storage
hostgl = ''

parser = ap.ArgumentParser() # parse arguments
parser.add_argument('-cmd', dest='command', required=False)
parser.add_argument('-f', dest='file', required=False)
args = parser.parse_args()

def check_for_exists(file): # here we check file for existing on server
    flist = connection.nlst() # get file list
    if file in flist: # if file in file list
        return True
    else: # if not
        return False

def main(cmd):
    global preprefix
    global connection
    global hostgl
    if cmd.startswith('connect'):
        if connection == None:
            command = cmd.split(';') # argument splitter
            if len(command) >= 3:
                host = command[0].split(' ', 1)[1] # get host by splitting
                login = command[1] # get login by splitting (again)
                password = command[2] # get password by splitting (again)
                try: # try to get connection.
                    connection = fl.FTP()
                    connection.connect(host, 21)# create connection
                    connection.login(login,password) # login
                    preprefix = f'{host}/'
                    hostgl = host
                    print(f'Connected successfully to {host} as {login}')
                except Exception as e: # if something went wrong, we catch this
                    print('Error occured, while trying to connect ('+str(e)+')')
            else:
                print('Missing required arguments.') # if arguments is missing
        else:
            print('Allready has a connection! Enter the "disconnect" command, to disconnect') # if allready has a connection
    elif cmd.startswith('disconnect'):
        if connection != None:
            preprefix = ''
            connection = None
            hostgl = None
            print(f'Disconnected successfully from "{hostgl}"')
        else:
            print('Allready disconnected')
    elif cmd.startswith('echo'): # echo command (print)
        if len(cmd.split(' ', 1)) >= 2:
            print(cmd.split(' ', 1)[1])
        else:
            print('Missing required arguments.')
    elif cmd.startswith(' '): # ignore symbols
        pass
    elif not cmd: # elif cmd == '' (nothing)
        pass
    elif cmd.startswith('listfile') or cmd.startswith('dir'):
        if connection: # if connection is positive
            try: # trying to get file list
                files = connection.nlst()
                cntr = 1
                for file in files:
                    print(f'{str(cntr)}. '+file) # printing it
                    cntr += 1
            except Exception as e: # exception for it (if no perms, or we hasn't have files in directory)
                print(f'Error ({str(e)})')
        else: # if we hasn't connection
            print('You does not have connection! Please, connect it by using "connect" command')


    elif cmd.startswith('execf'):
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                fname = cmd.split(' ', 1)[1]
                if os.path.exists(fname): # if filename exists
                    with open(fname, 'r') as f: # open file and split it
                        cmdlist = f.read().replace('\n','').split('$')
                    for CMD in cmdlist: # for loop
                        main(CMD) # execute command
                else: # if filename doesn't exist
                    print('File doesn`t exist!')
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('#'): # comment in file
        pass
    elif cmd.startswith('dfile'): # download file
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                filename = cmd.split(' ', 1)[1] # get arguments
                if check_for_exists(filename):
                    with open(filename, 'wb+') as f:
                        connection.retrbinary(f"RETR {filename}", f.write) # save file
                else:
                    print('File doesn`t exist!')
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('ufile'): # upload file
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                filename = cmd.split(' ', 1)[1]
                if os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        connection.storbinary(f'STOR {filename}', f) # upload file
                else:
                    print('File doesn`t exist!')
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('delete'):
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                filename = cmd.split(' ', 1)[1]
                if check_for_exists(filename):
                    connection.delete(filename)
                else:
                    print('File doesn`t exist!')
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('mkdir'):
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                dirname = cmd.split(' ', 1)[1]
                connection.mkd(str(dirname))
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('rename'):
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                command = cmd.split(';') # argument splitter
                before = command[0].split(' ', 1)[1]
                after = command[1]
                connection.rename(before, after) # rename the file
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('cd'): # if change directory command
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                a = cmd.split(' ', 1)[1] # get path
                if a != '..':
                    if check_for_exists(a):
                        connection.cwd(a)
                        preprefix = f'{hostgl}{str(connection.pwd())}'
                    else:
                        print('Directory not found')
                else:
                    connection.cwd(a)
                    preprefix = f'{hostgl}{str(connection.pwd())}'
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')
    elif cmd.startswith('rmdir'):
        if connection:
            if len(cmd.split(' ', 1)) >= 2:
                directory = cmd.split(' ', 1)[1] # get directory
                files = list(connection.nlst(directory)) # get files in directory
                for f in files: # delete all files in folder
                    if f[-3:] == "/.." or f[-2:] == '/.': continue
                    connection.delete(f)
                connection.rmd(directory) # now removing the directory fully
            else:
                print('Missing required arguments.')
        else:
            print('You does not have connection! Please, connect it by using "connect" command')

    elif cmd.startswith('help'):
        if len(cmd.split(' ', 1)) == 1:
            print('''
██╗  ██╗███████╗██╗     ██████╗     ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
██║  ██║██╔════╝██║     ██╔══██╗    ████╗ ████║██╔════╝████╗  ██║██║   ██║
███████║█████╗  ██║     ██████╔╝    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
██╔══██║██╔══╝  ██║     ██╔═══╝     ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
██║  ██║███████╗███████╗██║         ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝         ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝

--------------------------------------------------------------------

[] - optional argument
() - required argument

help - Shows this text
connect (host);(login);(password) - Create a connection, to work with console
disconnect - Delete connection
echo (text) - Echo (print) a text
dir - Shows current directory
execf (filename) - Execute a script from file
dfile (filename) - Download file
ufile (filename) - Upload file
delete (filename) - Delete file
mkdir (dirname) - Create a directory (folder)
rename (before);(after) - Rename a file
cd (dirname) - Change working directory (folder)
rmdir (dirname) - Delete directory (folder)
            ''')

    else: # if command not found
        print('Command not found')




if not args.command: # if we didn't got the command from terminal
    if os.path.exists('OnBoot.ftp'): # if we has On Boot file
        with open('OnBoot.ftp', 'r') as f: # open file and split it
            cmdlist = f.read().replace('\n','').split('$')
        print('On Boot Logs {') # logging for on boot
        for CMD in cmdlist: # for loop

            main(CMD) # execute command
        print('}')
    start()
    if not args.file:
        while True:
            Cmd = input(preprefix+'>') # ask user for a command
            main(Cmd)
    else:
        if os.path.exists(args.file):
            with open(args.file, 'r') as f:
                cmdlist = f.read().replace('\n','').split('$')
            for CMD in cmdlist: # for loop
                main(CMD) # execute command
        else:
            print('Not find filename')
else: # if we got the command from terminal
    cmdlist = args.command
    cmdlist = cmdlist.split('$')
    for Cmd in cmdlist:
        main(Cmd)
