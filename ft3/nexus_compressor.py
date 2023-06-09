import os
import glob
import tables as tb
from config import *
from invisible_cities.io.dst_io import load_dst, df_writer

compr_dir = nexus_dir.replace('/nexus/', '/nexus_compr/')
os.makedirs(compr_dir, exist_ok=True)

nexus_files = nexus_dir + '*.h5'
files = sorted(glob.glob(nexus_files), key = lambda x: int(x.split('_')[-2]))

for f in files:
    cdst = load_dst(f, 'MC', 'configuration')
    hdst = load_dst(f, 'MC', 'hits')
    pdst = load_dst(f, 'MC', 'particles')
    spdst = load_dst(f, 'MC', 'sns_positions')
    srdst = load_dst(f, 'MC', 'sns_response')

    fname = f.split('/')[-1]
    with tb.open_file(compr_dir + fname, 'w') as h5out:
        df_writer(h5out, cdst, 'MC', 'configuration', compression = 'ZLIB4', str_col_length = 256)
        df_writer(h5out, hdst, 'MC', 'hits', compression = 'ZLIB4')
        df_writer(h5out, pdst, 'MC', 'particles', compression = 'ZLIB4')
        df_writer(h5out, spdst, 'MC', 'sns_positions', compression = 'ZLIB4')
        df_writer(h5out, srdst, 'MC', 'sns_response', compression = 'ZLIB4')

    