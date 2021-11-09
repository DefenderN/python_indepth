#! /home/vertiefer/miniconda3/envs/molsys_nogcc/bin/python3
import os
import sys

fpar=sys.argv[1]
f=open(fpar)
text=f.read()
f.close()

text=text.replace("     $o1_0","0.00000000" )
text=text.replace("0.60000000      1.12504570           # gaussian->(n4_c3x1@dab)|dabco","0.00000000      1.12504570           # gaussian->(n4_c3x1@dab)|dabco")

f=open(fpar.rsplit('.',1)[0]+'.par',"w")
f.write(text)
f.close()

