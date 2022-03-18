#!/bin/bash

#SBATCH --job-name {jobname}
#SBATCH --output   {output}
#SBATCH --error    {error}
#SBATCH --ntasks   {tasks_per_job}
#SBATCH --time      01:00:00
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu 3G

{tasks}
wait
