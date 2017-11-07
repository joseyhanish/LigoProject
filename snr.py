# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:45:44 2017

@author: joskh
"""

import numpy as np
from readligo import loaddata

def snr_old(signal):
    print np.amax(signal)
    print np.std(signal)
    return np.amax(signal)/ \
        np.std(signal[:signal.index(np.amax(signal))-3]+signal[signal.index(np.amax(signal))+3:])

def snr(strain_data):
    fourier_domain_strain = list(np.absolute(np.fft.fft(strain_data)))
    print np.amax(fourier_domain_strain)
    print np.std(fourier_domain_strain[:fourier_domain_strain.index(np.amax(fourier_domain_strain))-3]\
        +fourier_domain_strain[fourier_domain_strain.index(np.amax(fourier_domain_strain))+3:])
    return np.amax(fourier_domain_strain)/ \
        np.std(fourier_domain_strain[:fourier_domain_strain.index(np.amax(fourier_domain_strain))-3]\
        +fourier_domain_strain[fourier_domain_strain.index(np.amax(fourier_domain_strain))+3:])
    
if __name__ == '__main__':
#    test = [0,1,0,1,0,1,3,4,5,4,3,0,1,0,1,0]
#    print snr_old(test)
    
    filename = r'C:\Users\joskh\Documents\2017Fall\ast376r\LOSC_Event_tutorial\LOSC_Event_tutorial\L-L1_LOSC_4_V1-1167559920-32.hdf5'
    strain, time, chan_dict = loaddata(filename)
    if strain is None or time is None or chan_dict is None:
        print 'Loading data failed'
        quit()
#    print 'len(strain) = {}'.format(len(strain))
#    print 'len(time) = {}'.format(len(time))
    print snr(strain)
    