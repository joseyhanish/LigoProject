# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:45:44 2017

@author: joskh
"""

import numpy as np
from readligo import loaddata
import matplotlib.pyplot as plt

def snr_old(signal):
    print np.amax(signal)
    print np.std(signal)
    return np.amax(signal)/ \
        np.std(signal[:signal.index(np.amax(signal))-3]+signal[signal.index(np.amax(signal))+3:])

def snr(strain_data):
    "Don't use this; I need to fix it."
    fourier_domain_strain = list(np.absolute(np.fft.fft(strain_data)))
    print np.amax(fourier_domain_strain)
    print np.std(fourier_domain_strain[:fourier_domain_strain.index(np.amax(fourier_domain_strain))-3]\
        +fourier_domain_strain[fourier_domain_strain.index(np.amax(fourier_domain_strain))+3:])
    return np.amax(fourier_domain_strain)/ \
        np.std(fourier_domain_strain[:fourier_domain_strain.index(np.amax(fourier_domain_strain))-3]\
        +fourier_domain_strain[fourier_domain_strain.index(np.amax(fourier_domain_strain))+3:])

def plot_frequency_spectrum(strain_data, dt):
    fourier = np.fft.rfft(strain_data)
    print np.shape(fourier)
    amplitudes = np.absolute(fourier)
    freqs = np.fft.rfftfreq(len(strain_data), dt)
    plt.figure(figsize=(10,10))
    plt.plot(freqs[1:], amplitudes[1:])
#    plt.xlim(0, 30)
    plt.show()
    
#    print freqs[1] - freqs[0]
    plt.figure(figsize=(10,10))
    plt.plot(freqs[1200:16000], amplitudes[1200:16000])
    
    # Whiten the data
    
    
if __name__ == '__main__':
#    test = [0,1,0,1,0,1,3,4,5,4,3,0,1,0,1,0]
#    print snr_old(test)
    
    filename = r'C:\Users\joskh\Documents\2017Fall\ast376r\LOSC_Event_tutorial\LOSC_Event_tutorial\L-L1_LOSC_4_V1-1167559920-32.hdf5'
    strain, time, chan_dict = loaddata(filename)
    if strain is None or time is None or chan_dict is None:
        print 'Loading data failed'
        quit()
    print 'len(strain) = {}'.format(len(strain))
    print 'len(time) = {}'.format(len(time))
    dt = time[1] - time[0]
    
#    print snr(strain)
    
    print '\n'
    plot_frequency_spectrum(strain, dt)
    