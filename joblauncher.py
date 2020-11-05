import glob
import subprocess

from jobtools import check_jobs

from config import queue_limit
from config import basedir
from config import loc
from config import queue_state_command
from config import joblaunch_command


jobsdir = basedir + loc + "/jobs/"
jobs = glob.glob(jobsdir + "/*")
jobs.sort(key=lambda filename: int(filename.split("/")[-1].split(".")[0]))


####################
##### LAUNCHER #####
####################
for job in jobs:

    check_jobs(queue_state_command, nmin=queue_limit)

    #### launch job ####
    cmd = joblaunch_command.format(filename = job)
    print("Launching job", job)
    subprocess.run(cmd)


#     #### launch job ####
#     os.system("sbatch" + " " + job)
#     sleep(0.01)
