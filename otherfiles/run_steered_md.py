import molsys
import pylmps
import ncvol

name='DH-nano_6_latopt'
m = molsys.mol.from_ff(name)

pl = pylmps.pylmps(name)
pl.setup(mol=m, kspace=False,bcond=0,use_pdlp=True)

pl.MD_init('heat_up', ensemble='nvt', T=[10,300], thermo='hoover', tnstep=500, startup=True, relax=[0.05],traj=['xyz','cell','vel'], dump=False)
pl.MD_run(50000)

pl.MD_init('equil', ensemble='nvt', T=300, thermo='hoover', tnstep=500, startup=False, relax=[0.1],traj=['xyz','cell','vel'], dump=False)
pl.MD_run(100000)

#switch on volume restraint
pdlp=name+'.pdlp'

pl = pylmps.pylmps(name)

ncv = ncvol.ncvol(["zn2p", "co2"],mode='US',k=0.002,Vref = 145199.367309,nstep=100)
# put the callback into the gloabl namespace
callback = ncv.callback

pl.add_external_potential(ncv, callback="callback")

pl.setup(pdlp=pdlp,restart='equil',restart_vel=True,ff="file", bcond=0, kspace=False, origin="center",use_pdlp=True)


pl.MD_init('constant_Vref',T=300.0,startup=False,ensemble='nvt',thermo='hoover',relax=[0.1],tnstep=500,dump=False,traj=['xyz','cell','vel'])
pl.MD_run(10000)

ncv.Vrefs=[145000,75000,700000]
pl.MD_init('ramp_Vref',T=300.0,startup=False,ensemble='nvt',thermo='hoover',relax=[0.1],tnstep=100,dump=False,traj=['xyz','cell','vel'])
pl.MD_run(700000)



