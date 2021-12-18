#!/usr/bin/env python3
"""
    Copyright: 2016-2020 Isloux Geophysics Ltd, Voudenay Geophysics Ltd
    Copyright: 2021 Christophe Ramananjaona
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>

    Module containng the class definition for an electric dipole
"""

__all__ = ['Dipole']

from ._dipole import *

class Dipole:
    """
    Class definition for electric dipole modelling
    """
    def __init__(self):
        """! Constructor with path to shared library
        """
        c_initialiseDpl1D()

    @property
    def ntx(self):
        return c_get_nTx()
    @property
    def nfreq(self):
        return c_get_nFreq()
        
    def callDipole1d(self,iTx=1,iFreq=1):
        """! Computes the electromagnetic for a given transmitter and frequency
        iTx Transmitter index
        iFreq Frequency index
        """
        c_CallDipole1D(iTx, iFreq)

    def __del__(self):
        """! Destructor for the object Dipole """
        c_close_outfile()
