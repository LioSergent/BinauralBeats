# -*- coding: utf-8 -*-
"""Formating data from first experiment.
Conditions:
* 10 minutes lying down in bed with eyes closed
* one minute of silence followed by 3 three-minutes sessions.

canal 0: E1
canal 1: C3
canal 2: T7
canal 3: O1
canal 4: leave

140 and 152 Hz

Hypothesis of ear symetry in binaural beats.
"""

import h5py
import numpy as np
from matplotlib import pyplot as plt
from math import floor, sqrt
import array_functions as array

f = h5py.File("vincent.h5", "r")

fs = 256

debuts = [256*60, 256*60*14, 256*60*37, 256*60*50]
fins = [
    256*60 + 256*60*10, 256*60*14 + 256*60*10,
    256*60*37 + 256*60*10, 256*60*50 + 256*60*10
]


def SO_fft_window_rel(EEG_data, fs=250):
    """Return alpha power after fft on the EEG data.
    Args:
        EEG_data (np array)
        fs (int): sampling frequency in Hz.
    Returns:
        alpha (np array): alpha power of the EEG_data
    """
    n = len(EEG_data)
    fft = abs(np.fft.fft(EEG_data, n=None, axis=-1)[:n / 2 + 1])
    pow_fft = fft**2
    # relative band power
    tot_pow = np.sum(pow_fft)
    alpha = sqrt(
        np.sum(pow_fft[int(8 * n * 2 / fs):int(12 * n * 2 / fs)])/tot_pow)
    theta = sqrt(
        np.sum(pow_fft[int(4 * n * 2 / fs):int(8 * n * 2 / fs)])/tot_pow)

    return alpha, theta


def alpha_power(EEG_data, win_len, exp_smoothing_coeff, fs=250):
    """Return alpha relative power on a sliding window at 1 Hz.
    Args:
        EEG_data (np array)
        win_len (int): floating window length in sec
        exp_smoothing_coeff (float)
        fs (int): EEG sampling frequency in Hz
    Returns:
        alpha_smoothed (np array): relative alpha power at 1 Hz.
    """
    npts_win = fs * win_len
    alpha = []

    # For computational reasons we calculate the powers at each second
    for i in range(int(floor(len(EEG_data)/fs))-win_len):
        sig_win = EEG_data[i*fs: i*fs+npts_win-1]
        fft_w = SO_fft_window_rel(sig_win, fs)[1]
        alpha.append(fft_w)
    # Now append zeros at the beginning of all the channels
    zeros = np.zeros((win_len, ))
    alpha = np.concatenate((zeros, alpha), axis=0)

    # Smooth it a bit
    alpha_smoothed = array.mean_smoothing(
        array.exp_smoothing(alpha, exp_smoothing_coeff),
        win_len)

    return alpha_smoothed


def my_plot(EEG_data, i, label, win_len, exp_smoothing_coeff):
    plt.figure(i)
    plt.plot(EEG_data)
    plt.title(label)
    plt.show()
    plt.plot(alpha_power(EEG_data, win_len, exp_smoothing_coeff))
    plt.title("puissance alpha de "+label)
    plt.axvline(x=1*60, linewidth=4, color="r")
    plt.axvline(x=4*60, linewidth=4, color="r")
    plt.axvline(x=7*60, linewidth=4, color="r")
    plt.show()
    plt.specgram(EEG_data, NFFT=256*10, Fs=256)
    plt.axvline(x=1*60, linewidth=4, color="r")
    plt.axvline(x=4*60, linewidth=4, color="r")
    plt.axvline(x=7*60, linewidth=4, color="r")
    plt.show()


mon_port_bin = f[u'signal_0'][u'sig'][debuts[0]:fins[0]]
mon_port_bin2 = f[u'signal_0'][u'sig'][debuts[1]:fins[1]]
port_bin_mon = f[u'signal_0'][u'sig'][debuts[2]:fins[2]]
test = f[u'signal_0'][u'sig'][debuts[3]:fins[3]]

my_plot(mon_port_bin, 1, "mon_port_bin", 10, 1)
my_plot(mon_port_bin2, 2, "mon_port_bin2", 10, 1)
my_plot(port_bin_mon, 3, "port_bin_mon", 10, 1)
my_plot(test, 4, "test", 10, 1)


"""
# Lionel veut que je lui calcule une fft

# Ok data is between 51000 and 51000+8*60*250
EEG_data = f2[51000:51000 + 8*250*60]
plt.figure(2)
plt.plot(EEG_data)
plt.ylim([-50, 50])
plt.title("EEG signal")
# plt.xlim(x_lims)
plt.show()

silence = SO_fft_window_rel(EEG_data[0:2*60*250])
monaural_1f = SO_fft_window_rel(EEG_data[2*60*250:4*60*250])
monaural_2f = SO_fft_window_rel(EEG_data[4*60*250:6*60*250])
binaural = SO_fft_window_rel(EEG_data[6*60*250:8*60*250])

alpha_slide = alpha_power(EEG_data, 10, 0.1)

plt.figure(4)
plt.plot(alpha_slide)
plt.axvline(x=2*60, linewidth=4, color="r")
plt.axvline(x=4*60, linewidth=4, color="r")
plt.axvline(x=6*60, linewidth=4, color="r")
plt.axvline(x=8*60, linewidth=4, color="r")
plt.show()

plt.figure(1)
plt.plot(f[u'signal_1'][u'sig'][:256*60*60*1])
plt.title("signal_1")
# plt.ylim([-5, 5])
# plt.xlim([x_lims[0]/5, x_lims[1]/5])
plt.show()

plt.figure(2)
plt.plot(f[u'signal_2'][u'sig'][:256*60*60*1])
plt.title("signal_2")
# plt.ylim([-5, 5])
# plt.xlim([x_lims[0]/5, x_lims[1]/5])
plt.show()

plt.figure(3)
plt.plot(f[u'signal_3'][u'sig'][:256*60*60*1])
# plt.ylim([-5, 5])
# plt.xlim([x_lims[0]/5, x_lims[1]/5])
plt.show()

plt.figure(4)
plt.plot(f[u'signal_4'][u'sig'][:256*60*60*1])
# plt.ylim([-5, 5])
# plt.xlim([x_lims[0]/5, x_lims[1]/5])
plt.show()
"""