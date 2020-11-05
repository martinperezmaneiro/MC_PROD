import os
import glob

from jobtools import checkmakedir

from config import *

city_input = dict(zip(cities[1:], cities[:-1]))


###################################
######### CREATE DIRS #############
###################################
proddir   = basedir + loc + "/prod/"
jobsdir   = basedir + loc + "/jobs/"
configdir = basedir + loc + "/config/"
logsdir   = basedir + loc + "/logs/"
checkmakedir(jobsdir)
checkmakedir(configdir)
checkmakedir(logsdir)
for city in cities: checkmakedir(proddir + city)


###################################
######### CREATE JOBS #############
###################################
jobtemplate = jobTemplates_dir + jobTemplate_filename_structure
jobTemplate = open(jobtemplate).read()
for file_in in files_in:
	n = get_file_number(file_in)
	city_commands = ""

    ## check if job already exists ####
    job  = jobsdir + f"/{n}.job"
    if os.path.exists(job): continue

    #### create job ####
	for i, city in enumerate(cities):
		if i != 0:
			file_in = proddir + city_input[city] + "/" + production_filename_structure.format(city=city_input[city], n=n, tag=tag)
		file_out    = proddir + city             + "/" + production_filename_structure.format(city=city            , n=n, tag=tag)

		#### create city config ####
		configtemplate = configTemplates_dir + configTemplate_filename_structure.format(city=city)
		configTemplate = open(configtemplate).read()
		config = configdir + city + f"_{n}.conf"
		with open(config, "w") as configfile:
			configfile.write(configTemplate.format(files_in=file_in,
												   file_out=file_out,
												   detector_db=detector_db))

		city_commands += f"city {city} {config}\n"

	with open(job, "w") as jobfile:
		jobfile.write(jobTemplate.format(jobname     = f"{n}",
                                         logfilename = logsdir + f"{n}.log",
                                         errfilename = logsdir + f"{n}.err",
                                         cities  = city_commands,
                                         config  = config))
