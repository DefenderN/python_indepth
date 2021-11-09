#! /usr/bin/python3

import os
import subprocess
import sys
import numpy

path=os.getcwd()

mfpx_files = [i for i in os.listdir(path) if i.rsplit('.')[-1]=='mfpx']
    
for mfpx in mfpx_files:
    fname=mfpx
    mfpx_file_path=os.path.join(path,fname)
    name=fname.rsplit('.',1)[0]
    namepath=os.path.join(path,name)

    if name in os.listdir(path):
        os.system('rm '+mfpx_file_path)
        print(name+': system is already assigned')
        continue

    atypeout = subprocess.getoutput('atype %s' % (mfpx_file_path))
    fragout = subprocess.getoutput('fragmentize %s' % (mfpx_file_path))
    os.system('python3 fix_atypes_frags.py %s' %(mfpx_file_path))
    queryout = subprocess.getoutput('query_parameters %s "MOF-FF JULIAN-FF" fit' % (mfpx_file_path))
    os.system('python3 fix_dut8_nc_fpar.py %s' %(namepath+'.fpar'))
    os.system('mkdir '+namepath)
    os.system('mv %s.* %s' % (namepath,namepath))
    print(name+' is assigned')




        


