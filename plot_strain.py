#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:22:01 2017

@author: nathaniellargent
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
import readligo as rl


# Open the File
fileName = 'L-L1_LOSC_4_V1-931160064-4096.hdf5'
dataFile = h5py.File(fileName, 'r')

# Explore the file
for key in dataFile.keys():
    print key 
    
# Read in strain data
strain = dataFile['strain']['Strain'].value
ts = dataFile['strain']['Strain'].attrs['Xspacing']

# Print out some meta data
print "\n\n"
metaKeys = dataFile['meta'].keys()
meta = dataFile['meta']
for key in metaKeys:
    print key, meta[key].value
    

# Create a time vector
gpsStart = meta['GPSstart'].value
duration = meta['Duration'].value
gpsEnd   = gpsStart + duration

time = np.arange(gpsStart, gpsEnd, ts)

# Plot the time series
numSamples = 10000
plt.plot(time[0:numSamples], strain[0:numSamples])
plt.xlabel('GPS Time (s)')
plt.ylabel('L1 Strain')
plt.ion()

# Load LIGO data from a single file
strain, time, chan_dict = rl.loaddata('L-L1_LOSC_4_V1-931160064-4096.hdf5', 'L1')

# Work with a directory of data files
start = 842656000
stop =  842670000
segList = rl.getsegs(start, stop, 'L1', flag='CBCLOW_CAT2')


# Plot a few seconds of each "good" segment
N = 10000
for (begin, end) in segList:
    # -- Use the getstrain() method to load the data
    strain, meta, dq = rl.getstrain(begin, end, 'L1')

    # -- Make a plot
    plt.figure()
    ts = meta['dt']
    rel_time = np.arange(0, end-begin, meta['dt'])
    plt.plot(rel_time[0:N], strain[0:N])
    plt.xlabel('Seconds since GPS ' + str(begin) )
plt.show()