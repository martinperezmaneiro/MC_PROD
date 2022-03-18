"""
Assumes tasks are created at /path/tasks/ with filenames tasks_
"""

import os
import re
import glob
from math   import ceil
from config import *

job_task = "srun --ntasks 1 {task} &" + os.linesep
job_end  = "wait"                     + os.linesep

if __name__ == "__main__":

    get_file_number = lambda name: int(re.findall("[0-9]+", name.split("/")[-1])[0])

    task_filenames = sorted( glob.glob(os.path.join(tasks_dir, "task_*.sh"))
                           , key=get_file_number)
    ntasks   = len(task_filenames)
    nbatches = ceil(ntasks/tasks_per_job)

    print(f"Creating {tag} jobs..")

    jobTemplate = open(job_template).read()

    # write jobs
    for batch in range(0, nbatches):
        tasks_in_batch = task_filenames[batch*tasks_per_job:(batch+1)*tasks_per_job]

        tasks = ""
        for task in tasks_in_batch:
            tasks += "srun --ntasks 1 " + task + "\n"

        # write to file
        filename = os.path.join(jobs_dir, f"job_{batch+1}.sh")
        with open(filename, "x") as outfile:
            outfile.write(jobTemplate.format(jobname= str(batch+1) + "_" + tag
                                            , output = os.path.join(logs_dir, str(batch+1)+".out")
                                            , error  = os.path.join(logs_dir, str(batch+1)+".err")
                                            , tasks_per_job = len(tasks_in_batch)
                                            , tasks         = tasks))

    print(f"{nbatches} jobs created")
