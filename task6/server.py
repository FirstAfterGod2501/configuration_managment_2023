import os
import subprocess

results_directory = './result'

def process_results(filename):
    os.system('sshpass -p "password" scp ' +results_directory+'/out.txt first@10.0.2.2:/home/first/qemu/example')

while(True):
    for filename in os.listdir('.'):
        if('.cpp' in filename):
            os.system('g++ -O3 -std=c++23 main.cpp && ./a.out > result/out.txt')
            process_results(filename)

