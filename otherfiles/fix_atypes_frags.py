#! /home/vertiefer/miniconda3/envs/molsys_nogcc/bin/python3
import os
import sys

mfpx=sys.argv[1]

os.system('sed -i -e s/dab1/dab/g '+mfpx)
os.system('sed -i -e s/n3_c3/n4_c3x1/g '+mfpx)

# os.system("sed -i -e 's/co2cent/co2    /g' " +mfpx)
