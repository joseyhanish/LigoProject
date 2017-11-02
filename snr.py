# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:45:44 2017

@author: joskh
"""

import numpy as np

def snr(signal):
    print np.amax(signal)
    print np.std(signal)
    return np.amax(signal)/ \
        np.std(signal[:signal.index(np.amax(signal))-3]+signal[signal.index(np.amax(signal))+3:])
    
if __name__ == '__main__':
    test = [0,1,0,1,0,1,3,4,5,4,3,0,1,0,1,0]
    print snr(test)
    