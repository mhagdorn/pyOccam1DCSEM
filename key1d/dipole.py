#!/usr/bin/env python
"""
    Copyright 2016 Isloux
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

from ctypes import cdll
from sys import version_info
import platform

class Dipole:
    
    def __init__(self,libpath="/usr/local/lib/"):
	package="key1d"
	pyv="python"+str(version_info[0])+"."+str(version_info[1])
	if platform.system()=="Linux":
	# Disabled for now
	#    libpath+=pyv+"/dist-packages/"+package
	    suffix=".so.0.0.1"
	else:
	    suffix=".0.dylib"
        self.flib=cdll.LoadLibrary(libpath+"liboccam1dcsem"+suffix)
	inverse=False
        self.flib.c_initialiseDpl1D(inverse)
    
    def callDipole1d(self,iTx=1,iFreq=1):
        self.flib.c_CallDipole1D(iTx,iFreq)

def main():
    libpath="/home/christophe/Documents/Informatique/lib/"
    dpl=Dipole(libpath)
    dpl.callDipole1d()

if __name__=="__main__":
    main()
