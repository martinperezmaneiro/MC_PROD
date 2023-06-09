import os
import glob

vols = sorted(glob.glob(os.path.expandvars('$LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/*/')))
vols = [v.split('/')[-2] for v in vols]

prev = 'volumes'


for v in vols:
    post = 'volumes/' + v
    os.system("sed -i 's\/{prev}/\/{post}/\g' config.py".format(prev = prev, post = post))
    prev = post
    os.system('sed -n 5p config.py')
    
    #os.system('mv $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/config $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/ref_config'.format(vol = v))
    #os.system('mv $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/nexus $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/prod/'.format(vol = v)) 
    #os.system('mkdir $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/prod/ref_prod'.format(vol = v))
    #for c in ['sophronia', 'esmeralda', 'beersheba', 'isaura']:
    #    os.system('mv $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/prod/{city}/ $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/prod/ref_prod/'.format(vol = v, city = c))
    #os.system('rm $LUSTRE/NEXT100/data/full_prod/214Bi/prod/volumes/{vol}/logs/*'.format(vol = v))
    os.system('python nexus_compressor.py &')
    #os.system('python create_task_files.py')
    #os.system('python create_job_files.py')
    #os.system('python job_launcher.py')

os.system("sed -i 's\/{prev}/\/{post}/\g' config.py".format(prev = prev, post = 'volumes'))

