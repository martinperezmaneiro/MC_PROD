import os
import glob

basedir = os.path.expandvars("$PWD/../data")
loc = "/prueba"
tag = "tag"
detector_db = "next100"

indir  =  basedir + "/nexus/"
cities = ["detsim", "hypathia", "dorothea"] # order is important

queue_limit   = 30
tasks_per_job = 5

task_template = os.path.expandvars("$PWD/task_template.sh")
job_template  = os.path.expandvars("$PWD/job_template.sh")

configTemplates_dir = os.path.expandvars("$PWD/../templates/NEXT100/")
configTemplate_filename_structure = "{city}Template.conf"
production_filename_structure     = "{city}_{n}_{tag}.h5"

get_file_number = lambda filename: int(filename.split("/")[-1].split("_")[1])

############################
###### output dirs #########
############################
def create_out_dirs():
    prod_dir   = basedir + loc + "/prod/"
    tasks_dir  = basedir + loc + "/tasks/"
    jobs_dir   = basedir + loc + "/jobs/"
    config_dir = basedir + loc + "/config/"
    logs_dir   = basedir + loc + "/logs/"
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


###########################
###### JOB LAUNCH #########
###########################
# commands (system dependent)
queue_state_command = "squeue |grep usciegdl |wc -l"
joblaunch_command   = "sbatch {filename}"
