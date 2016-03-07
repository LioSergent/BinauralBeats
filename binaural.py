""" Generate a sequence of silence, monaural 1 f, monaural 2 f,
and binaural of 2 min each."""


import numpy as np
from scipy.io.wavfile import write, read


nb_min = 2
fs = 44100
f1 = 240
f2 = 254
f3 = (f1+f2)/2
# f4 = 420

# create 4 arrays of 2 minutes each
silence = np.zeros((nb_min*60*fs, 2))
monaural_1f = np.zeros((nb_min*60*fs, 2))
monaural_2f = np.zeros((nb_min*60*fs, 2))
binaural = np.zeros((nb_min*60*fs, 2))

print("generating frequencies")

F_1 = (np.cos(2*np.pi*np.arange(fs*nb_min*60)*f1/fs)).astype(np.float32)
F_2 = (np.cos(2*np.pi*np.arange(fs*nb_min*60)*f2/fs)).astype(np.float32)
F_3 = (np.cos(2*np.pi*np.arange(fs*nb_min*60)*f3/fs)).astype(np.float32)
# F_4 = (np.cos(2*np.pi*np.arange(fs*nb_min*60)*f4/fs)).astype(np.float32)

print("generating sounds")

monaural_1f[::, 0] = F_3
monaural_1f[::, 1] = F_3

monaural_2f[::, 0] = (F_2 + F_1)/2
monaural_2f[::, 1] = (F_2 + F_1)/2

binaural[::, 0] = F_2
binaural[::, 1] = F_1

print("on a peine deux les trucs")

data = np.append(silence, monaural_1f, axis=0)
data = np.append(data, monaural_2f, axis=0)
data = np.append(data, binaural, axis=0)

# scale data to get integers
scaled = np.int16(data/np.max(np.abs(data)) * 32767)
print("writing .wav")
write("4_periods_2_min" + '.wav', 44100, scaled)

