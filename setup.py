#!/usr/bin/env python

from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install
from distutils.command.clean import clean
from os import system,chdir
import sys
import platform
import re
from pyoccam1dcsem import __version__

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
        chdir("pyoccam1dcsem")
        if platform.system()=="Linux":
       	    system("libtoolize")
        else:
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
        system("tail -1 setup.cfg | cut -d= -f2 > pyoccam1dcsem/prefix.foo")
        prefix=open("pyoccam1dcsem/prefix.foo","r").readlines()
        with open("pyoccam1dcsem/prefix.py","w") as fout:
            fout.write("prefix=\"{}\"\n".format(prefix[0].rstrip()))

class clean_(clean):
    def run(self):
        system("rm -rf build")
        chdir("pyoccam1dcsem")
        system("make clean")
        system("rm -f prefix.*")

class install_(install):
    def run(self):
        chdir("pyoccam1dcsem")
        system("make install")

setup(
    name='pyOccam1DCSEM',
    version=__version__,
    packages=['pyoccam1dcsem'],
    author='Christophe Ramananjaona',
    author_email='isloux AT yahoo.co.uk',
    url='https://github.com/isloux/pyOccam1DCSEM',
    license='GNU General Public License v3',
    long_description=open('README.txt').read(),
    classifiers=["Programming Language :: Python",
        "Programming Language :: Fortran"],
    cmdclass={'configure': configure, 'clean': clean_,'lib': install_}
)
