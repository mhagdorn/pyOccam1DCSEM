#!/usr/bin/env python
"""
    Copyright: 2017 Voudenay Geophysics Ltd
    Author: Christophe Ramananjaona <isloux AT yahoo.co.uk>
"""

import occamfile as occmfl
from sys import argv
from os.path import isfile

if len(argv)<2:
	raise Exception("Provide file name.")
if isfile(argv[1]):
	occamfile=occmfl.OccamFile(argv[1])
	occamfile.compAmplitude()
	occamfile.plotlogAmp(argv[1])
else:
	raise Exception("File not found.")
