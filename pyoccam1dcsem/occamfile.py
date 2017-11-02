#!/usr/bin/env python
"""
    Copyright: 2017 Voudenay Geophysics Ltd
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

import pandas as pd
from numpy import zeros,sqrt,log10
import matplotlib.pyplot as plt

def removelines(l):
	c=['0']
        while ''.join(c)[0]!='#':
                c=l.pop(0)
		if len(c)==0: c=['0']
	l=[c]+l
	return l

class OccamFile:

	def __init__(self,filename="RUNFILE"):
		a=[ line.split() for line in file(filename) ]
		# Drop first lines
		a=removelines(a)
		self.transmitpos=self.__dataframe(a)
		self.transmitpos['rx']=self.transmitpos.index+1
		self.transmitpos.set_index('Y',inplace=True)
                # Drop the no longer necessary lines
                a=removelines(a)
		nfreq=int(a.pop(0)[2])
		self.freql=[]
		for i in range(nfreq):
			self.freql.append(a.pop(0)[0])
                # Drop the no longer necessary lines
		a=removelines(a)
		self.recpos=self.__dataframe(a,colheader=False)
                # Drop the no longer necessary lines
                a=removelines(a)
		self.datadf=self.__dataframe(a)
		self.types=self.datadf['TYPE'].unique()
		self.nfreq=self.datadf['FREQ#'].nunique()
		self.ntransmit=self.datadf['TX#'].nunique()
		self.nrec=self.datadf['RX#'].nunique()

	def __dataframe(self,a,colheader=True,floatdata=True):
		nlines=int(a.pop(0)[2])
		if colheader:
                	colnames=[ str(i) for i in a.pop(0) ]
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
		return row['E1']**2+row['E2']**2

	def __logAmp(self,row):
		return log10(sqrt(row['squaredAmp']))

	def __DeltalogAmp(self,row):
                return 2.0*(abs(row['E1'])*row['DeltaE1']+ \
			abs(row['E2'])*row['DeltaE2'])/row['squaredAmp']
	
	def plotlogAmp(self,name):
		self.eedf.set_index('TX#',inplace=True)
		for i in range(self.nfreq):
			pltdata=self.transmitpos['rx'].map(self.eedf[self.eedf['FREQ#']==i+1]['logAmp']).dropna()
			plt.scatter(pltdata.index,pltdata.values)
		plt.legend(self.freql)
		plt.title(name)
		plt.show()
