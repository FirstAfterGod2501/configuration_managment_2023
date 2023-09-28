import argparse
import os
import sys
import tarfile
import zipfile
import shutil

cwd = "/"


def pwd():
    print(os.getcwd().split("_virtual")[1]+'/')


def ls():
    files = os.listdir('.')
    for file in files:
        print(file)


def cd(directory):
    try:
        if (directory == "../" or directory == ".." or "//" in directory) and "virtual" in os.getcwd().split("/")[-1]:
            print("you are in the root directory")
            return
        os.chdir(directory)
    except FileNotFoundError:
        print(f'Directory {directory} does not exist.')
        return
    except NotADirectoryError:
        print(f'{directory} is not a directory.')
        return


def cat(filename):
    try:
        with open(filename, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f'File {filename} does not exist.')


parser = argparse.ArgumentParser(description='vshell command line emulator.')
parser.add_argument('archive', help='Path to the archive file.')
args = parser.parse_args()

try:
    if args.archive.endswith('.tar'):
        os.mkdir(args.archive.replace(".tar", "") + "_virtual")
        os.chdir(args.archive.replace(".tar", "") + "_virtual")
        cwd = os.getcwd()
        shutil.copy("../" + args.archive, ".")
        archive = tarfile.open(args.archive, 'r')
        archive.extractall()
        os.remove(args.archive)
    elif args.archive.endswith('.zip'):
        os.chdir(args.archive.replace(".zip", "") + "_virtual")
        os.chdir(args.archive.replace(".zip", "") + "_virtual")
        archive = zipfile.ZipFile(args.archive, 'r')
        archive.extractall()
    else:
        print('Unsupported archive format. Supported formats: tar, zip.')
        sys.exit(1)
except FileNotFoundError:
    print(f'File {args.archive} does not exist.')
    sys.exit(1)
except tarfile.ReadError:
    print(f'Unable to open archive {args.archive}.')
    sys.exit(1)
except zipfile.BadZipFile:
    print(f'Unable to open zip archive {args.archive}.')
    sys.exit(1)

while True:
    command = input('> ').strip().split()

    if len(command) == 0:
        continue

    if command[0] == 'pwd':
        pwd()
    elif command[0] == 'ls':
        ls()
    elif command[0] == 'cd':
        if len(command) > 1:
            cd(command[1])
        else:
            print('No directory specified.')
    elif command[0] == 'cat':
        if len(command) > 1:
            cat(command[1])
        else:
            print('No filename specified.')
    elif command[0] == 'exit':
        break
    else:
        print('Unknown command.')

shutil.rmtree(cwd)
archive.close()
