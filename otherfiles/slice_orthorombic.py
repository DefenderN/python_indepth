import molsys
from molsys.util import slicer
import numpy as np

m = molsys.mol.from_file('pcu_2c_tertiary.mfpx')

# define the size of the nanoparticle in all directions (x,y,z) in multiples of the unitcell here
# should be multiples of 2
# NOTE: the size is the number of paddle wheel units in each dimension)
# This script creates multiple (i) .mfpx files with the dimensions x,y,z

for i in range(2,10):

    # TODO: Choose your dimensions for the NC
    x = 3
    y = 3
    z = i

    m = molsys.mol.from_file('pcu_2c_tertiary.mfpx')
    size = [x,y,z]
    # do not change
    size = np.array(size, "d")
    cut = 0.1
    supercell = size + np.array([4,4,4], "d")
    orig = size / 2.0

    fx = float(x)
    fy = float(y)
    fz = float(z)

    s = slicer(m)

    s.set_plane([1,0,0], dist=fx/2+0.1, name="xp", symm=False)
    s.set_plane([1,0,0], dist=-fx/2+0.9, name="xm", symm=False)
    s.set_plane([0,1,0], dist=fy/2+0.1, name="yp", symm=False)
    s.set_plane([0,1,0], dist=-fy/2+0.9, name="ym", symm=False)
    s.set_plane([0,0,1], dist=fz/2+0.1, name="zp", symm=False)
    s.set_plane([0,0,1], dist=-fz/2+0.9, name="zm", symm=False)

    s.set_stub("0", "h", "3", 0.4, plane_name="xp")
    s.set_stub("0", "h", "3", 0.4, plane_name="xm")
    s.set_stub("0", "h", "3", 0.4, plane_name="yp")
    s.set_stub("0", "h", "3", 0.4, plane_name="ym")
    s.set_stub("0", "i", "4", 0.5, plane_name="zp")
    s.set_stub("0", "i", "4", 0.5, plane_name="zm")

    m = s(supercell=supercell.astype(int).tolist(),orig=orig,max_dist=2.0)

    m.write('pcu_3c_3_3_%d.mfpx'% (i,))


