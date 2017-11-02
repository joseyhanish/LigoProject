#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:43:11 2017

@author: hayleyjellison
"""

import json, urllib
dataset = 'S5'
GPSstart = 825155213   # start of S5
GPSend   = 825232014   # end of S5
detector = 'H2'

urlformat = 'https://losc.ligo.org/archive/links/{0}/{1}/{2}/{3}/json/'
url = urlformat.format(dataset, detector, GPSstart, GPSend)
print "Tile catalog URL is ", url

r = urllib.urlopen(url).read()    # get the list of files
tiles = json.loads(r)             # parse the json

print tiles['dataset']
print tiles['GPSstart']
print tiles['GPSend']

output_list = open('files', 'w')
for file in tiles['strain']:
    if file['format'] == 'hdf5':
        print "found file from ", file['UTCstart']
        print>>output_list, file['url']

output_list.close()

import os, urllib
import numpy
import readligo

Sec = 4096      # samples per second
Hour = 4096     # seconds per file
FoldTime = 32   # seconds for folding
detector = 'H2' # which detector to use

# First we get a list of all the files that are already processed
try:
    f = open('filesdone')
    donelist = f.readlines()
    f.close()
except:
    donelist = []

# Now open the list of files that are to be processed
for line in open('files').readlines():
    if line in donelist: continue    # already processed

# Now build the URL for each file
# Example line 815792128/H-H1_LOSC_4_V1-815886336-4096.hdf5
    tok = line.strip().split('/')     
    url = 'https://losc.ligo.org/archive/data/S5/' + line.strip()
    filename = tok[1]

    tol = filename.split('-')   #  H   H2_LOSC_4_V1   843599872    4096.hdf5
    gpstime = int(tol[2])

    try:
        foldsum = numpy.load('foldsum.npy')   # load the sum output file 
        foldnum = numpy.load('foldnum.npy')   # load the file of how many 
    except:
        foldsum = numpy.zeros(FoldTime*Sec, numpy.float32)  # or make a new one with zeros
        foldnum = numpy.zeros(FoldTime, numpy.int32)  


    print "Fetching data file from ", url
    r = urllib.urlopen(url).read()
    f = open('cache/' + filename, 'w')   # write it to the right filename
    f.write(r)
    f.close()

    strain, time, chan_dict = readligo.loaddata('cache/' + filename, detector)
# Lets only count the CAT4 (best) data
    okmask = chan_dict['CBCHIGH_CAT4']
    
    secs = 0
    for t in range(0,Hour):
        if okmask[t]:
            m = (gpstime + t) % FoldTime            # second of the fold
            foldsum[m*Sec:(m+1)*Sec] += strain[t*Sec:(t+1)*Sec]  # vector coadd operation
            foldnum[m] += 1
            secs += 1
    print "     %d seconds processed, fold from %d to %d" % (secs, foldnum.min(), foldnum.max())

    try:
        numpy.save('foldsum.npy', foldsum)     # save the output file
        numpy.save('foldnum.npy', foldnum)     # save the output file
        f = open('filesdone', 'a')         # mark the file as done
        print>>f, line.strip()
        f.close()
        os.system("rm cache/*")                     # delete the processed file
    except Exception, e:
        print "Something went wrong", e

import numpy
import scipy.io.wavfile
Sec = 4096
foldsum = numpy.load('foldsum.npy')
foldnum = numpy.load('foldnum.npy')
print "Found %d seconds" % len(foldnum)
for i in range(len(foldnum)):   # Make the average
    foldsum[i*Sec:(i+1)*Sec] /= foldnum[i]
scaled = numpy.int16(numpy.sqrt(foldsum/numpy.max(numpy.abs(foldsum))) * 32767)
scipy.io.wavfile.write('fold.wav' , Sec, scaled)