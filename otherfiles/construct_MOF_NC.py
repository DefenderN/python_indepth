import os
import weaver
import numpy as np
import copy

for n in range(2,10):

    #instanciate framework
    f = weaver.framework('test-MOF')
    #read topo file
    f.read_topo('../pcu_3c_3_3_%d.mfpx'%(n))
    #assign bbs
    f.assign_bb('0','BBs/ZnPWL6.mfpx',specific_conn = [['1','3'],['2','4']])
    f.assign_bb('1','BBs/bdc.mfpx',linker=True)
    f.assign_bb('2','BBs/dabco.mfpx',linker=True)
    f.assign_bb("3", "BBs/ph-stub.mfpx")
    f.assign_bb("4", "BBs/dabco-stub.mfpx")
    
    # ???
    f.scale_net([13.5,13.5,9])
    f.scan_orientations(25)
    
    # ???
    f.generate_framework([0]*len(f.norientations))
    # write files
    f.write_framework('NC%s.mfpx'%(n))
#    os.system('change_com.py NC%s.mfpx' %(n))
#    os.system('mv NC%s.mfpx nanocrystallites_dut128'%(n))



