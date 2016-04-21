#!/usr/bin/env python

from distutils.core import setup, Extension
from distutils.command.build import build as _build
from distutils.command.build import build
from os import system,chdir
import sys
from key1d import __version__

class build_(build):
    def run(self):
        caller = sys._getframe(2)
        caller_module = caller.f_globals.get('__name__','')
        caller_name = caller.f_code.co_name
        #if caller_module != 'distutils.dist' or caller_name!='run_commands':
        #    _build.run(self)
        #else:
        # HARD CODED FOR NOW
        prefix="/Users/christophe/Documents/Informatique/Python/Key1d/key1d/"
        #
        chdir("key1d")
        system("glibtoolize")
        system("aclocal")
        system("autoconf")
        system("automake --add-missing")
        system("autoconf")
        system("./configure --prefix="+prefix)
        system("make")

occam1dcsem=Extension(
    'occam1dcsem',
    sources=[],
    libraries=['liboccam1dcsem.0.dylib'],
    library_dirs=['/Users/christophe/Documents/Informatique/Python/Key1d/key1d/lib']
)

setup(
	name='Key1d',
	version=__version__,
	packages=['key1d'],
	author='Kerry Key, Christophe Ramananjaona',
	author_email='isloux AT yahoo.co.uk',
	url='https://github.com/isloux/Key1d',
	license='GNU General Public License v3',
	long_description=open('README.txt').read(),
	classifiers=["Programming Language :: Python",
		     "Programming Language :: Fortran"],
	cmdclass={'build': build_},
    ext_modules=[occam1dcsem]
)
