import fnmatch
import os
import subprocess
import sys
import molsys
from molsys.util import slicer
import numpy as np
import weaver
import shutil

def makeOrthorombicSupercellFilesFromCommandLine():
    # TODO:Add description of this function
    
    def validateInput():
        E = """Make sure to execute this file with proper arguments:

        [pythonVersion] [thisfilename.py] [topologyfile.mfpx] x y z
        EXAMPLE: python3 thisfilename.py topologyFile.mfpx 4 5-8 10"""

        T = """topology.mfpx file as second argument and x, y and z as 3rd, 4th and 5th arguments are missing. \n"""
        D = """x, y, and z dimensions as arguments are missing. \n"""
    
        if len(sys.argv) < 2:
            raise ValueError(T + E)
        elif len(sys.argv) < 5:
            raise ValueError(D + E)
        return

    # Raises error message if arguments in the command line are missing.
    validateInput()
    
    # Read topology file and x,y,z dimensions from command line input.
    topologyFile = sys.argv[1]
    xDimInput    = sys.argv[2].split("-")
    yDimInput    = sys.argv[3].split("-")
    zDimInput    = sys.argv[4].split("-")  
    
    # Extract the dimensions from input.
    # Sets the maximum value to the minimum value if no maximum value is provided.
    xDim = [int(xDimInput[0]), int(xDimInput[0]) if len(xDimInput) == 1 else int(xDimInput[1])]
    yDim = [int(yDimInput[0]), int(yDimInput[0]) if len(yDimInput) == 1 else int(yDimInput[1])]
    zDim = [int(zDimInput[0]), int(zDimInput[0]) if len(zDimInput) == 1 else int(xDimInput[1])]

    newFileNames = makeOrthorombicSupercellFiles(topologyFile,xDim,yDim,zDim)
    return newFileNames

def makeOrthorombicSupercellFiles(topologyFileName, xDim: list, yDim: list, zDim: list):
    """Makes multiple supercell files by calling @makeOrthorombicSupercellFile.

    Args:
        topologyFileName : A topology.mfpx file being in the same directory.
        xDim (list): Dimensions of number of paddlewheel units in x direction.
        yDim (list): Dimensions of number of paddlewheel units in y direction.
        zDim (list): Dimensions of number of paddlewheel units in z direction.
    Returns:
        A list of names of the newly made orthorombic supercell files.
    """
    
    #Calculate minimum and maximum values for x,y and z.
    xMin = int(xDim[0])
    xMax = xMin if len(xDim) == 1 else int(xDim[1])

    yMin = int(yDim[0])
    yMax = yMin if len(yDim) == 1 else int(yDim[1])

    zMin = int(zDim[0])
    zMax = zMin if len(zDim) == 1 else int(zDim[1])

    # Make multiple supercell files

    newFileNames = []

    for x in range(xMin,xMax+1):
        for y in range(yMin,yMax+1):
            for z in range(zMin,zMax+1):
                newFileName = makeOrthorombicSupercellFile(topologyFileName,x,y,z)
                newFileNames.append(newFileName)

    return newFileNames

def makeOrthorombicSupercellFile(topologyFileName, x, y, z):
    """Creates a supercell with the dimensions [x,y,z] by providing a topology.mfpx file
    and the number of paddlewheel units in each dimension.
       
    Args:
        topologyFileName: A topology.mfpx file being in the same directory.
        x: number of paddle-wheels in x-Dimension
        y: number of paddle-wheels in y-Dimension
        z: number of paddle-wheels in z-Dimension
    Returns:
        A string of the name of the newly made orthorombic supercell file.
    """
    
    print("making orthorombic supercell of size {} {} {}".format(x,y,z))
    molObject = molsys.mol.from_file(topologyFileName)
    size =[x,y,z]

    # do not change
    size = np.array(size, "d")
    cut = 0.1
    supercell = size + np.array([4,4,4], "d")
    orig = size / 2.0

    fx = float(x)
    fy = float(y)
    fz = float(z)

    s = slicer(molObject)

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

    molObject = s(supercell=supercell.astype(int).tolist(),orig=orig,max_dist=2.0)
    newFileName = "orthorombicSupercell_{}_{}_{}.mfpx".format(x,y,z)
    molObject.write(newFileName)
    return newFileName

def addBBsToSupercellFiles(supercellFileNames, metalBB, BB1, BB2, BB1stub, BB2stub):
    for supercellFile in supercellFileNames:
        addBBsToSupercellFile(supercellFile, metalBB, BB1, BB2, BB1stub, BB2stub)
    return

def addBBsToSupercellFile(supercellFile, metalBB, BB1, BB2, BB1stub, BB2stub):
    
    #1 Instanciate Framework
    f = weaver.framework("test-MOF")
    
    #2 Read supercellFile
    f.read_topo(supercellFile)
    
    #3 Assign BBs
    f.assign_bb("0", metalBB, specific_conn = [['1','3'],['2','4']])
    f.assign_bb('1',BB1,linker=True)
    f.assign_bb('2',BB2,linker=True)
    f.assign_bb("3", BB1stub)
    f.assign_bb("4", BB2stub)
    
    #4 ???
    f.scale_net([13.5,13.5,9])    
    f.scan_orientations(25)
    
    
    #5 Generate Framework
    f.generate_framework([0]*len(f.norientations))
    
    #6 write file
    f.write_framework(os.path.splitext(supercellFile)[0] + "_withBBs.mfpx")
    return

def assignParamsToMfpxFile(mfpxFileName):
    
    #1 Bash command 
    print("Initiate bash cmd atype {}".format(mfpxFileName))
    atypeOutput = subprocess.getoutput("atype {}".format(mfpxFileName))
    #2 Bash command
    print("Initiate bash cmd fragmentize {}".format(mfpxFileName))
    fragmentizeOutput = subprocess.getoutput("fragmentize {}".format(mfpxFileName))
    
    #3 Fix atom types
    fixAtypesFragments(mfpxFileName)
    #4 Get ff-params
    queryFFParametersOutput = subprocess.getoutput("""query_parameters {} 'MOF-FF JULIAN-FF' fit""".format(mfpxFileName))
    
    #5 Fix mistakes in fpar file
    fixDut8ncfpar(mfpxFileName)
    
    return

def fixAtypesFragments(mfpxFileName):
    print("fixAtypesFragments called on filename {}".format(mfpxFileName))
    os.system("sed -i -e s/dab1/dab/g {}".format(mfpxFileName))
    os.system("sed -i -e s/n3_c3/n4_c3x1 {}".format(mfpxFileName))
    return

def fixDut8ncfpar(mfpxFileName):

    fparFileName = mfpxFileName.split(".")[0]+ ".fpar"
    print("fixDut8ncfpar called on filename {}".format(fparFileName))
    f = open(fparFileName)
    text = f.read()
    f.close()

    text=text.replace("     $o1_0","0.00000000" )
    text=text.replace("0.60000000      1.12504570           # gaussian->(n4_c3x1@dab)|dabco","0.00000000      1.12504570           # gaussian->(n4_c3x1@dab)|dabco")

    f=open(mfpxFileName.rsplit('.',1)[0]+'.par',"w")
    f.write(text)
    print("write "+ mfpxFileName.rsplit('.',1)[0]+'.par')
    f.close()
    
    return

