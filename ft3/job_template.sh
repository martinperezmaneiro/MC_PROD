#!/bin/bash

#SBATCH --job-name {jobname}
#SBATCH --output   {output}
#SBATCH --error    {error}
#SBATCH --ntasks   {tasks_per_job}
#SBATCH --time     {job_time}
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu 3G

source $STORE/refactor_ic_setup.sh

{tasks}
wait
