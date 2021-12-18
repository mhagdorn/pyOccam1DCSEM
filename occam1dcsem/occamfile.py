#!/usr/bin/env python3
"""
    Copyright: 2017-2020 Voudenay Geophysics Ltd
    Copyright: 2021 Christophe Ramananjaona
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>

    Module containing the class definition for the OccamFile class.
    The class is used to read and write files in the 'Occam' format
"""

import pandas as pd
from numpy import zeros,sqrt,log10
import matplotlib.pyplot as plt
import re
from .version import __version__

def removelines(l):
    """! Remove the commented lines startying with #. """
    c=['0']
    while ''.join(c)[0]!='#':
        c=l.pop(0)
        if len(c)==0:
            c=['0']
        elif c[0]=="Dipole1D_1.1":
            c=[]
            l.pop(0)
            break
    if len(c)==0:
        return l
    else:
        return [c]+l

def removecol(l):
    """! Remove the comments after the !. """
    o=[]
    for i in l:
        if len(i)>0:
            j=0
            while i[j]!='!':
                if j<len(i)-1:
                    j+=1
                    f=j
                else:
                    f=j+1
                    break
            o.append(i[:f])
    return o

class OccamFile:

    def __init__(self,filename="RUNFILE"):
        """! Constructor.
        filename Occam format input filename
        """
        with open(filename,"r") as f:
            a=[ line.split() for line in f.readlines() ]
        # Transmistter positions
        # Drop first lines
        a=removelines(a)
        a=removecol(a)
        self.transmitpos=self.__dataframe(a)
        self.transmitpos['rx']=self.transmitpos.index+1
        self.transmitpos.set_index('Y',inplace=True)
        # Drop the no longer necessary lines
        a=removelines(a)
        # Frequencies
        inputline=a.pop(0)
        if len(inputline)==1:
            nfreq=int(inputline[0])
        else:
            nfreq=int(inputline[2])
        self.freql=[]
        for i in range(nfreq):
            self.freql.append(a.pop(0)[0])
        # Drop the no longer necessary lines
        a=removelines(a)
        a.pop(0)
        # Do not read the layers
        #
        # Drop the no longer necessary lines
        a=removelines(a)
        self.recpos=self.__dataframe(a,colheader=False)
        # Drop the no longer necessary lines
        if a.pop(0)[0]=='#':
            a=removelines(a)
            # CSEM data
            self.datadf=self.__dataframe(a)
            self.types=self.datadf['TYPE'].unique()
            self.nfreq=self.datadf['FREQ#'].nunique()
            self.ntransmit=self.datadf['TX#'].nunique()
            self.nrec=self.datadf['RX#'].nunique()

    def __dataframe(self,a,colheader=True,floatdata=True):
        """! Creates a dataframe from rows and columns of data.
        a List of list containing the data
        colheader Indicatess if the input list contains headers
        floatdata Indicates if the input data are of type float
        """
        inputline=a.pop(0)
        if len(inputline)==1:
            nlines=int(inputline[0])
        else:
            nlines=int(inputline[2])
        if colheader:
            colnames=[ str(i) for i in a.pop(0) ]
            if colnames[0]=='#':
                colnames.pop(0)
        else:
            colnames=['X','Y','Z']
        ncol=len(colnames)
        if floatdata:
            posa=zeros((nlines,ncol),dtype='float')
        else:
            posa=zeros((nlines,ncol),dtype='int')
        for i in range(nlines):
            for j in range(ncol):
                if floatdata:
                    posa[i,j]=float(a[i][j])
                else:
                    posa[i,j]=int(a[i][j])
        return pd.DataFrame(posa,columns=colnames)

    def compAmplitude(self):
        """! Copmutes amplitudes from real and impaginary. """
        if len(self.types)>2:
            raise Warning("There are more than two data types.")
        self.datadf['E1']=0.0
        self.datadf['E2']=0.0
        self.datadf['DeltaE1']=0.0
        self.datadf['DeltaE2']=0.0
        self.datadf.apply(self.__fillinfields,axis=1)
        self.datadf.drop('TYPE',axis=1,inplace=True)
        self.eedf=self.datadf.groupby(['FREQ#','TX#','RX#']).sum().reset_index()
        self.eedf['squaredAmp']=self.eedf.apply(self.__Ampsquared,axis=1)
        self.eedf['logAmp']=self.eedf.apply(self.__logAmp,axis=1)
        self.eedf['DeltalogAmp']=self.eedf.apply(self.__DeltalogAmp,axis=1)
        self.eedf.drop(['DATA','SD_ERROR','E1','E2','DeltaE1','DeltaE2','squaredAmp'],axis=1,inplace=True)
        for i in ['FREQ#','TX#','RX#']:
            self.eedf[i]=self.eedf[i].astype(int)

    def __fillinfields(self,row):
        if row['TYPE']==self.types[0]:
            row['E1']=row['DATA']
            row['DeltaE1']=row['SD_ERROR']
        else:
            row['E2']=row['DATA']
            row['DeltaE2']=row['SD_ERROR']
        return row

    def __Ampsquared(self,row):
        """! Copmutes the squared amplitude from the real and imaginary. """
        return row['E1']**2+row['E2']**2

    def __logAmp(self,row):
        """! Copmutes the log10 of the amplitude from the squared amplitude. """
        return log10(sqrt(row['squaredAmp']))

    def __DeltalogAmp(self,row):
        """! Copmutes the standard deviation of the log10 of the amplitude. """
        return 2.0*(abs(row['E1'])*row['DeltaE1']+abs(row['E2'])*row['DeltaE2'])/row['squaredAmp']

    def plotlogAmp(self,name):
        """! Plots the log10 of the amplitude. 
        name Title of the plot
        """
        self.eedf.set_index('TX#',inplace=True)
        for i in range(self.nfreq):
            pltdata=self.transmitpos['rx'].map(self.eedf[self.eedf['FREQ#']==i+1]['logAmp']).dropna()
            plt.scatter(pltdata.index,pltdata.values)
            plt.legend(self.freql)
            plt.title(name)
            plt.show()

def generate_runfile(source,freq,layers,rec,name,air_resistivity=1.0e12):
    """! Generates a 'Occam' input file from given parameters:
    source  list of dictionaries providing the source positions and orientations
    freq    list of frequencies
    layers  list of dictionaries describing the layers
    rec     list of dictionaries providing the receiver positions
    name    string providing the name of the created file
    air_resistivity optional air resistivity value in ohm.m
    """
    with open("RUNFILE","w") as outfile:
        outfile.write("Version: pyOccam1DCSEM {}\n".format(__version__))
        outfile.write("Output Filename: {}.csem\n".format(name))
        outfile.write("CompDerivatives: no\n")
        outfile.write("# TRANSMITTERS: {}\n".format(len(source)))
        outfile.write("X\tY\tZ\tROTATION\tDIP\n")
        for i in source:
            outfile.write("{}\t{}\t{}\t{}\t{}\n".format(i['X'],i['Y'],i['Z'], \
                    i['ROTATION'],i['DIP']))
        outfile.write("# FREQUENCIES: {}\n".format(len(freq)))
        for i in freq:
            outfile.write("{}\n".format(i))
        outfile.write("# LAYERS: {}\n".format(len(layers)+1))
        str_air_rho=re.sub("e","d",str(air_resistivity))
        outfile.write("-100000\t{}\t! The top depth of the first layer is not used in the code. In this example the first layer is air (1d12 ohm-m)\n".format(str_air_rho))
        for i in layers:
            outfile.write("{}\t{}\n".format(i['top'],i['rho']))
        outfile.write("# RECEIVERS: {}\n".format(len(rec)))
        for i in rec:
            outfile.write("{}\t{}\t{}\n".format(i['x'],i['y'],i['z']))

if __name__=="__main__":
    source=[{'X':0.0,'Y':0.0,'Z':1000.0,'ROTATION':90.0,'DIP':0.0}]
    nu=[0.01,0.02,0.05,0.1,0.2,0.5,1.0,2.0,5.0,10.0]
    layers=[{'top':0.0,'rho':5.0}]
    rec=[{'x':0.0,'y':0.0,'z':0.0}]
    name="helloworld"
    generate_runfile(source,nu,layers,rec,name)
