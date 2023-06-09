import os
import glob
import numpy as np

basedir = os.path.expandvars("$LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/")
#basedir = os.path.expandvars("$LUSTRE/NEXT100/data/228Th/refactor_prod/")
#basedir = os.path.expandvars("$LUSTRE/NEXT100/data/kr_test_data/")

#loc = "prod"
tag = "214Bi"
#tag = "kr"
detector_db = "next100"

file_percentage = 0.1

indir  =  basedir + "prod/hypathia/" #the starting city
cities = ["sophronia", "esmeralda"] # order is important

queue_limit   = 30
tasks_per_job = 10
job_time = "5:59:00"

task_template = os.path.expandvars("$PWD/task_template.sh")
job_template  = os.path.expandvars("$PWD/job_template.sh")
############
############ REMEMBER TO CHANGE ENVIRONMENT LOADED IN THE JOB TEMPLATE ##################
############
configTemplates_dir = os.path.expandvars("$LUSTRE/NEXT100/config_templates/gonzalo_senior_228Th_prod/refactor_ic/")
#configTemplates_dir = os.path.expandvars("$LUSTRE/NEXT100/config_templates/kr_production/")
configTemplate_filename_structure = "{city}Template.conf"
production_filename_structure     = "{city}_{n}_{tag}.h5"

get_file_number = lambda filename: int(filename.split("/")[-1].split("_")[1])

############################
###### output dirs #########
############################
def create_out_dirs():
    prod_dir   = basedir + "/prod/"
    tasks_dir  = basedir + "/tasks/"
    jobs_dir   = basedir + "/jobs/"
    config_dir = basedir + "/config/"
    logs_dir   = basedir + "/logs/"
    os.makedirs( tasks_dir, exist_ok=True)
    os.makedirs(  jobs_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(  logs_dir, exist_ok=True)
    for city in cities: os.makedirs(prod_dir + city, exist_ok=True)
    return prod_dir, tasks_dir, jobs_dir, config_dir, logs_dir

prod_dir, tasks_dir, jobs_dir, config_dir, logs_dir = create_out_dirs()

############################
###### input files #########
############################
def check_filename_structure(filename):
    name  = filename.split("/")[-1]
    # check length
    assert len(name.split("_")) == len(production_filename_structure.split("_"))
    # check file number
    assert name.split("_")[1].isdigit()
    # check tag
    assert name.split("_")[2] == tag + ".h5"

files_in = glob.glob(os.path.join(indir, "*.h5"))
for file_in in files_in: check_filename_structure(file_in)
files_in = sorted(files_in, key=get_file_number)
nfiles = int(np.ceil(len(files_in) * file_percentage))
files_in = files_in[nfiles:]

###########################
###### JOB LAUNCH #########
###########################
# commands (system dependent)
queue_state_command = "squeue -r |grep usciempm |wc -l"
joblaunch_command   = "sbatch {jobfilename}"
