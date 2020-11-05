import os
import glob
production_filename_structure = "{city}_{n}_{tag}.h5"

indir = os.path.expandvars("$PWD/data/nexus/")
city  = "nexus"
tag   = "tag"

def get_file_number(filename):
    name = filename.split("/")[-1]
    return int(name.split(".")[2])

if __name__ == "__main__":

    files = glob.glob(indir + "/*")

    for file in files:
        n = get_file_number(file)

        newname = production_filename_structure.format(city=city, tag=tag, n=n)
        os.rename(file, indir + "/" + newname)
