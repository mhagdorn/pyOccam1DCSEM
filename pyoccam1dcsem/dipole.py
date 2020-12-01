#!/usr/bin/env python
"""
    Copyright: 2016-2017 Isloux Geophysics Ltd, Voudenay Geophysics Ltd
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

from ctypes import cdll
from sys import version_info
from os import environ
import platform
import re

class Dipole:
    
    def __init__(self,libpath="/usr/local/lib"):
        print(libpath)
        package="pyoccam1dcsem"
        pyv="python"+str(version_info[0])+"."+str(version_info[1])
        if platform.system()=="Linux":
        # Disabled for now
        #    libpath+=pyv+"/dist-packages/"+package
            suffix=".so.0.0.1"
        else:
            suffix=".0.dylib"
        self.flib=cdll.LoadLibrary(libpath+"/liboccam1dcsem"+suffix)
        self.flib.c_initialiseDpl1D()
        self.ntx=self.flib.c_get_nTx()
        self.nfreq=self.flib.c_get_nFreq()
    
    def callDipole1d(self,iTx=1,iFreq=1):
        self.flib.c_CallDipole1D(iTx,iFreq)

    def finalise(self):
        self.flib.c_close_outfile()

def main():
    l=re.search(":",environ['LD_LIBRARY_PATH'])
    libpath=environ['LD_LIBRARY_PATH'][:l.end()-1]
    dpl=Dipole(libpath)
    for ifreq in range(dpl.nfreq):
        for itx in range(dpl.ntx):
            dpl.callDipole1d(itx+1,ifreq+1)
    dpl.finalise()

if __name__=="__main__":
    main()
