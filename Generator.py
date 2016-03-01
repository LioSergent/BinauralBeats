# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 10:48:48 2016

@author: tox9
"""

import pyaudio
import numpy as np

p = pyaudio.PyAudio()

print "Hello"

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
f = 220.0   
f2 = 880     # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samplesL = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
samplesR = (np.sin(2*np.pi*np.arange(fs*duration)*f2/fs)).astype(np.float32)

samples=np.zeros(fs*duration*2).astype(np.float32)

samples[::2]=samplesL
samples[1::2]=samplesR


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively) 
stream.write(volume*samples)

stream.stop_stream()
stream.close()


p.terminate()