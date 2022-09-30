import os
import sys
import glob
import subprocess

from time import sleep

def checkmakedir(path):
    if os.path.isdir(path):
        print('hey, directory already exists!:\n' + path)
    else:
        os.makedirs(path)
        print('creating directory...\n' + path)

def check_jobs(cmd, nmin=10, wait=1):
    j = nmin
    while j>nmin-1:
        j = subprocess.run(cmd, shell=True, capture_output=True)
        j = int(j.stdout)
        sleep(wait)

def check_exists(file):
    return os.path.isfile(file)
