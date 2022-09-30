import os
import glob
from config import *

city_input = dict(zip(cities[1:], cities[:-1]))

filename_structure = "{dir}/{city}/" + production_filename_structure

if __name__ == "__main__":

	print("Creating tasks...")

	taskTemplate = open(task_template).read()
	for file_in in files_in:
		n = get_file_number(file_in)
		city_commands = ""

		task_filename = os.path.join(tasks_dir, f"task_{n}.sh")

	    #### create task ####
		for i, city in enumerate(cities):
			if i != 0:
				file_in = filename_structure.format(dir=prod_dir, city=city_input[city], n=n, tag=tag)
			file_out    = filename_structure.format(dir=prod_dir, city=city,             n=n, tag=tag)

			#### create city config ####
			configtemplate = configTemplates_dir + configTemplate_filename_structure.format(city=city)
			configTemplate = open(configtemplate).read()
			config = os.path.join(config_dir, city + f"_{n}.conf")
			with open(config, "w") as configfile:
				configfile.write(configTemplate.format( files_in=file_in
													  , file_out=file_out
													  , detector_db=detector_db))

			city_commands += f"city {city} {config}\n"

		# create task
		with open(task_filename, "w") as file:
			file.write(taskTemplate.format(cities = city_commands))
		os.chmod(task_filename, 0o744)

	print(f"{len(files_in)} tasks created")
