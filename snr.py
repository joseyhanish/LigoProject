# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:45:44 2017

@author: joskh
"""

import numpy as np
from readligo import loaddata
import matplotlib.pyplot as plt
from scipy.signal import convolve
from astropy.convolution import Box1DKernel
import matplotlib.mlab as mlab
from scipy.interpolate import interp1d


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

def plot_frequency_spectrum(strain_data, times, dt):
    fourier = np.fft.rfft(strain_data)
    amplitudes = np.absolute(fourier)
    freqs = np.fft.rfftfreq(len(strain_data), dt)
    plt.figure(figsize=(10,10))
    plt.plot(freqs[1:], amplitudes[1:])
    plt.title('Raw frequency-amplitude spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.savefig('RawFreqSpec.png')
    plt.show()
    
#    print freqs[1] - freqs[0]
    # Zoom in
    plt.figure(figsize=(10,10))
    plt.plot(freqs[1200:16000], amplitudes[1200:16000])
    plt.title('Raw frequency-amplitude spectrum - 20 Hz to 500 Hz ')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.savefig('RawFreqSpec20to500.png')
    plt.show()
    
    # Whiten the amplitudes by using mlab to get the psd
    # Find the psd
    pxx, freqs2 = mlab.psd(strain_data, Fs = 4096, NFFT = 4*4096)    
    psd = interp1d(freqs2, pxx) #returns a function
    # Plot the psd (to make sure it looks like the psd in the workbook)
    plt.figure(figsize=(10,10))
    plt.plot(freqs2[1:], np.sqrt(pxx[1:]))
    plt.title('Power Spectral Density')
    plt.savefig('PSD.png')
    plt.xlabel('Frequency')
    plt.show()
    
    plt.figure(figsize=(10,10))
    plt.loglog(freqs2[1:], np.sqrt(pxx[1:]))
    plt.title('Power Spectral Density - Log Scale')
    plt.xlim(20, 2000)
    plt.show()
    
    # Whiten the amplitudes
    norm = 1./np.sqrt(1./(dt*2))
    whitened_amplitudes = fourier / np.sqrt(psd(freqs)) * norm
#    whitened_amplitudes = np.absolute(whitened_amplitudes)
    
    # Plot the whitened frequency spectrum
    plt.figure(figsize=(10,10))
    plt.plot(freqs[1:], whitened_amplitudes[1:])
    plt.title('Whitened Frequency Spectrum')
    plt.savefig('WhitenedFreqSpec.png')
    plt.show()
    
    # Zoom in
    plt.figure(figsize=(10,10))
    plt.plot(freqs[1200:16000], whitened_amplitudes[1200:16000])
    plt.title('Whitened Frequency Spectrum - 20 Hz to 500 Hz')
    plt.savefig('WhitenedFreqSpec20to500.png')
    plt.show()
    
    # Bandpassing at 50 - 400 Hz
    bp_freqs, bp_amps = zip(*[p for p in zip(freqs, whitened_amplitudes) 
                            if p[0] > 20 and p[0] < 400])
    
    plt.figure(figsize=(10,10))
    plt.plot(bp_freqs, bp_amps)
    plt.title('Whitened Frequency Spectrum After Bandpassing')
    plt.show()
    
#    # Return the whitened amplitudes to the frequency-strain domain
#    whitened_strain = np.fft.irfft(bp_amps, len(strain_data))
#    plt.figure(figsize=(10,10))
#    plt.specgram(whitened_strain, NFFT=4*4096, Fs=4096)
#    plt.show()
    
    
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
    dt = time[1] - time[0]
    
#    print snr(strain)
    
    print '\n'
    plot_frequency_spectrum(strain, time, dt)
    