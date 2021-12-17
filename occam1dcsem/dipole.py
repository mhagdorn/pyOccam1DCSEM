#!/usr/bin/env python3
"""
    Copyright: 2016-2020 Isloux Geophysics Ltd, Voudenay Geophysics Ltd
    Copyright: 2021 Christophe Ramananjaona
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>

    Module containng the class definition for an electric dipole
"""

from ctypes import cdll,c_int
from sys import version_info
from os import environ
import platform
import re
from .occamfile import OccamFile
from .prefix import prefix

class Dipole:
    """
    Class definition for electric dipole modelling
    """
    def __init__(self,libpath="/usr/local/lib"):
        """! Constructor with path to shared library
        libpath Path to the shared library
        """
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
        """! Computes the electromagnetic for a given transmitter and frequency
        iTx Transmitter index
        iFreq Frequency index
        """
        self.flib.c_CallDipole1D(c_int(iTx),c_int(iFreq))

    def finalise(self):
        """! Destructor for the object Dipole """
        self.flib.c_close_outfile()

def main():
    """! Default test main program for the module running from the default RUNFILE """
    libpath=prefix+"/lib"
    ccmfl=OccamFile("RUNFILE")
    dpl=Dipole(libpath)
    for ifreq in range(dpl.nfreq):
        for itx in range(dpl.ntx):
            dpl.callDipole1d(itx+1,ifreq+1)
    dpl.finalise()

if __name__=="__main__":
    main()
