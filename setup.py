#!/usr/bin/env python

from distutils.core import setup, Extension
from distutils.command.build import build
from distutils.command.install import install
from distutils.command.clean import clean
from os import system,chdir
import sys
import re
from key1d import __version__

class configure(install):
    def run(self):
        s=''.join(sys.argv)
        l=re.search("--prefix=",s)
        prefix=""
        if l!=None:
            s=s[l.end():]
            l=re.search(" ",s)
            if l!=None:
                prefix=" --prefix="+s[:l.start()]
	    else:
		prefix=" --prefix="+s
        chdir("key1d")
        system("glibtoolize")
        system("aclocal")
        system("autoconf")
        system("automake --add-missing")
        system("autoconf")
        system("./configure"+prefix)
	chdir("..")
	system("grep -v 'prefix' setup.cfg > temp1cfg")
	sprefix="prefix="+s
	system("echo "+sprefix+" >> temp1cfg")
	system("mv temp1cfg setup.cfg")

class build_(build):
    def run(self):
        chdir("key1d")
        system("make")

class clean_(clean):
    def run(self):
	chdir("key1d")
	system("make clean")

class install_(install):
    def run(self):
	chdir("key1d")
	system("make")
	system("make install")
        install.run

#occam1dcsem=Extension(
#    'occam1dcsem',
#    sources=[],
#    libraries=['liboccam1dcsem.0.dylib'],
#    library_dirs=['lib']
#)

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
	cmdclass={'build': build_,'configure': configure, 'clean': clean_,
		      'install': install_}
#        ext_modules=[occam1dcsem]
)
