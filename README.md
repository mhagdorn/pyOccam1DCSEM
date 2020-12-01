# pyOccam1DCSEM
1D electromagnetic dipole modelling using Python module distribution of Kerry Key's Occam 1D CSEM code
(forward modelling only)

Installation:
> python3 setup.py configure --prefix=<lib_installation_path>

> python3 setup.py lib

> pip3 install .

Clean build:
> python3 setup.py clean

Usage:
> export LD_LIBRARY_PATH="<lib_installation_path>:LD_LIBRARY_PATH"

> python3 -m pyoccam1dcsem.dipole
