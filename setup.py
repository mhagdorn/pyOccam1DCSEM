#!/usr/bin/env python

from skbuild import setup


setup(
    name='pyOccam1DCSEM',
    version="7.3.0",
    packages=['occam1dcsem'],
    author='Christophe Ramananjaona',
    author_email='isloux AT yahoo.co.uk',
    url='https://github.com/isloux/pyOccam1DCSEM',
    license='GNU General Public License v3',
    long_description=open('README.txt').read(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Fortran"],
    cmake_args=['-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON'],
)
