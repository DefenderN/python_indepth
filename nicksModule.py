import fnmatch
import os
import subprocess
import sys
import molsys
from molsys.util import slicer
import numpy as np
import weaver
import shutil


def buildSupercellTopologyFilesFromCommandLine():
    
    
    # Missing arguments handling
    E = """Make sure to execute this file with proper arguments:

            [pythonVersion] [thisfilename.py] [topologyfile.mfpx] x y z
    EXAMPLE: python3 thisfilename.py topologyFile.mfpx 4 5-8 10"""

    T = """topology.mfpx file as second argument and x, y and z as 3rd, 4th and 5th arguments are missing. \n"""
    D = """x, y, and z dimensions as arguments are missing. \n"""
    
    if len(sys.argv) < 2:
        raise ValueError(T + E)
    elif len(sys.argv) < 5:
        raise ValueError(D + E)

    #1 read topology file given from input
    topologyFile = sys.argv[1]

    #2 get dimensions from input
    xDim = sys.argv[2].split("-")
    yDim = sys.argv[3].split("-")
    zDim = sys.argv[4].split("-")

    xMin = int(xDim[0])
    xMax = xMin if len(xDim) == 1 else int(xDim[1])

    yMin = int(yDim[0])
    yMax = yMin if len(yDim) == 1 else int(yDim[1])

    zMin = int(zDim[0])
    zMax = zMin if len(zDim) == 1 else int(zDim[1])

    #3 Create a .mfpx file for every dimension given and save it in the current directory.
    
    #cwd = os.getcwd()
    #subDirectory = cwd + "/new"
    #os.mkdir(subDirectory)
    
    
    for x in range(xMin,xMax+1):
        for y in range(yMin,yMax+1):
            for z in range(zMin,zMax+1):
                print("making Blueprint of size {} {} {}".format(x,y,z))
                fullBlueprint = __makeFullOrthorombicNCBlueprint(x,y,z,topologyFile)
                name = "orthorombicBP_{}_{}_{}.mfpx".format(x,y,z)
                fullBlueprint.write(name)
                #shutil.move(name, subDirectory)
                
    return

def __makeFullOrthorombicNCBlueprint(x,y,z,topologyFile):

    """Creates the full-sized blueprint of a nanocrystallite (NC) by providing the number of paddlewheel units
       in each dimension and a topology.mfpx file.
       
    Args:
        x: number of paddle-wheels in x-Dimension
        y: number of paddle-wheels in y-Dimension
        z: number of paddle-wheels in z-Dimension
        topologyFile: A topology.mfpx file being in the same directory

    Returns:
        A mol object representing the NC blueprint
    """

    molObject = molsys.mol.from_file(topologyFile)
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
    return molObject

def addBBtoAllFilesInCurrentDir(metalBB, linker1, linker2, stub1, stub2):
        
    bpFiles = __findFullBlueprintFiles()
    for file in bpFiles:
        print("Adding BBs to file:" + file)
        __addBBtoBP(file,metalBB,linker1,linker2,stub1,stub2)
        # assignParams(bpFiles)
    return

def __findFullBlueprintFiles():
    """Finds all generated blueprint files in pwd that match the ending *_*_*_*.mfpx.

    Returns:
        list: A list containing all filenames of FullBlueprintFiles
    """
    fileNames = []
    
    files = os.scandir()
    for file in files:
        if fnmatch.fnmatchcase(file.name, "*_*_*_*.mfpx"):
            print(file.name)
            fileNames.append(file.name)
            
    print(fileNames)
    return fileNames

def __addBBtoBP(topoFile, metalBB, linker1, linker2, stub1, stub2):
    
    #1 Instanciate Framework
    f = weaver.framework("tempFramework")
    
    #2 Read topologyFile
    f.read_topo(topoFile)
    
    #3 Assign BBs
    f.assign_bb("o", metalBB, specific_conn = [['1','3'],['2','4']])
    f.assign_bb('1',linker1,linker=True)
    f.assign_bb('2',linker2,linker=True)
    f.assign_bb("3", stub1)
    f.assign_bb("4", stub2)
    
    #4 ???
    f.scale_net([13.5,13.5,9])
    f.scan_orientations(25)
    
    #5 Generate Framework
    f.generate_framework([0]*len(f.norientations))
    
    #6 write file
    f.write_framework(os.path.splitext(topoFile)[0] + "_withBBs.mfpx")
    return



def assignParams(bpFilesWithAtoms):
    
    path=os.getcwd()

    mfpx_files = bpFilesWithAtoms
    
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
    
    
        # atype with bash command (mofplus)
        
    
        # fragmentize with bash command
    
        # run fix_atypes_frags.py
    
        # querey parameters
    
        # fix_dut8nc_fpar --> fixes something
    return
