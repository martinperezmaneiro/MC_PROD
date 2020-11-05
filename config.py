import os
import glob

basedir = os.path.expandvars("$PWD/data")
loc = "/prueba"
tag = "tag"

indir  =  basedir + "/nexus/"
cities = ["detsim", "hypathia", "penthesilea", "esmeralda"] # order is important

detector_db = "next100"
queue_limit = 199


# directory of job and config Templates.
# Following above, configTemplat_dir must contain "{city}Template.conf" files
# and jobTemplate_dir must contain "jobTemplate.sh"
# configuration templates are such that files_in, files_out and detector_db
# have to be introduced. files_in and files_out are automatically filled
jobTemplates_dir    = os.path.expandvars("$PWD/templates/")
configTemplates_dir = os.path.expandvars("$PWD/templates/")

# jobTemplates_dir    = os.path.expandvars("$HOME/IC_PRODUCTION")
# configTemplates_dir = os.path.expandvars("$HOME/IC_PRODUCTION/configTemplates")


# WARNING: Modifying this setting will require code changes below.
# Do not modify this settings if you do not know what you are doing
production_filename_structure     = "{city}_{n}_{tag}.h5"
configTemplate_filename_structure = "{city}Template.conf"
jobTemplate_filename_structure    = "jobTemplate.sh"

get_file_number = lambda filename: int(filename.split("/")[-1].split("_")[1])
def check_filename_structure(filename):
    name  = filename.split("/")[-1]
    # check length
    assert len(name.split("_")) == len(production_filename_structure.split("_"))
    # check file number
    assert name.split("_")[1].isdigit()
    # check tag
    assert name.split("_")[2] == tag + ".h5"


############################
###### input files #########
############################
files_in = glob.glob(indir + "/*.h5")
for file_in in files_in: check_filename_structure(file_in)
files_in.sort(key=get_file_number)


###########################
###### JOB LAUNCH #########
###########################
# commands (system dependent)
queue_state_command = "squeue |grep usciegdl |wc -l"
joblaunch_command   = "sbatch {filename}"
