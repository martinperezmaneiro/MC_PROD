import os
import re
import glob
import subprocess
from time import sleep
from config import *

def check_jobs(cmd, nmin=10, wait=1):
    j = nmin
    while (j>nmin-1):
        j = subprocess.run(cmd, shell=True, capture_output=True)
        j = int(j.stdout)
        sleep(wait)
        if (j == nmin): sleep(10*wait)

jobfilenames = glob.glob(os.path.join(jobs_dir, "job_*.sh"))

if __name__ == "__main__":

    get_file_number = lambda name: int(re.findall("[0-9]+", name.split("/")[-1])[0])

    jobfilenames = sorted(jobfilenames, key=get_file_number)

    for jobfilename in jobfilenames:
        check_jobs(queue_state_command, nmin=queue_limit)

        cmd = joblaunch_command.format(jobfilename=jobfilename)
        subprocess.run(cmd, shell=True)
