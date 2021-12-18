import occam1dcsem

ccmfl=occam1dcsem.OccamFile("RUNFILE")
dpl=occam1dcsem.Dipole()

print(occam1dcsem.__version__)
print(dpl.ntx)
print(dpl.nfreq)

for ifreq in range(dpl.nfreq):
    for itx in range(dpl.ntx):
        dpl.callDipole1d(itx+1,ifreq+1)
