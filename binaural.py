""" Generate a sequence of silence, monaural 1 f, monaural 2 f,
and binaural of 2 min each."""


import numpy as np
from scipy.io.wavfile import write

nb_min = 2
fs = 44100

# create 4 arrays of 2 minutes each
silence = np.zeros((nb_min*60*fs, 2))
