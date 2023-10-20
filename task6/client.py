import os
import time
import subprocess

directory = './example'

def process_file(filename):
    os.system('sshpass -p "password" scp -P 10022 ' + filename +  ' username@localhost:/home/username')

while True:
    for filename in os.listdir(directory):
        if filename.endswith('.cpp'):
            filepath = os.path.join(directory, filename)
            process_file(filepath)
    time.sleep(1) 
