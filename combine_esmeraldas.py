import os
import glob
import numpy as np
import tables

# --------------------------------------------------------------------
# combine_esmeralda.py
# Combine pytables from analyses over many esmeralda files.
# ---------------------------------------------------------------------

tag = "tlde"
indir  = os.path.expandvars("$LUSTRE/DEMOPP_Run9/MC/esmeralda/")
outdir = os.path.expandvars("$LUSTRE/DEMOPP_Run9/MC/") 

include_tracks = True
include_dst = True

# input/output files
get_file_number = lambda filename: int(filename.split("/")[-1].split("_")[1])
files_in = sorted(glob.glob(indir + "/*.h5"), key=get_file_number)
file_out = os.path.join(outdir, f"esmeralda_combined_{tag}.h5")

print("Combined esmeralda:", file_out)

# Open the final tables file.
fcombined = tables.open_file(file_out, "w", filters=tables.Filters(complib="blosc", complevel=9))
group_Summary = fcombined.create_group(fcombined.root, "Summary")
if(include_tracks):
    group_Tracking = fcombined.create_group(fcombined.root, "Tracking")
if(include_dst):
    group_DST = fcombined.create_group(fcombined.root, "DST")

# Open the first file.
f1 = tables.open_file(files_in[0], 'r')
summary_combined = f1.copy_node('/Summary', name='Events', newparent=group_Summary)
if(include_tracks):
    tracking_combined = f1.copy_node('/Tracking', name='Tracks', newparent=group_Tracking)
if(include_dst):
    dst_combined = f1.copy_node('/DST', name='Events', newparent=group_DST)
f1.close()

# Process nruns files.
for fname in files_in:

    print("-- Adding file {0}".format(fname));

    # Open the next file and extract the elements.
    fn = tables.open_file(fname, 'r')
    if("/Summary" in fn):
        summary_events = fn.root.Summary.Events
        summary_combined.append(summary_events.read())
    if(include_tracks and "/Tracking" in fn):
        tracking_tracks = fn.root.Tracking.Tracks
        tracking_combined.append(tracking_tracks.read())
    if(include_dst and "/DST" in fn):
        dst_events = fn.root.DST.Events
        dst_combined.append(dst_events.read())
    else:
        print(" --> Skipping file due to no table found")

    # Close the file.
    fn.close()

    # Flush the combined file.
    fcombined.flush()

# Close the combined hdf5 file.
print("Saving combined file:", file_out)
fcombined.close()
