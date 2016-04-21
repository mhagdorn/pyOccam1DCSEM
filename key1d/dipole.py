#!/usr/bin/env python
"""
    Copyright 2016 Isloux
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

from ctypes import cdll

class Dipole:
    
    def __init__(self,libpath="/usr/local/lib/"):
        self.flib=cdll.LoadLibrary(libpath+"liboccam1dcsem.0.dylib")
        self.flib.c_initialiseDpl1D()
    
    def callDipole1d(self,iTx=1,iFreq=1):
        self.flib.c_CallDipole1D(iTx,iFreq)

def main():
    libpath="/Users/christophe/Documents/Informatique/Python/Key1d/key1d/lib/"
    dpl=Dipole(libpath)
    dpl.callDipole1d()

if __name__=="__main__":
    main()
