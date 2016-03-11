"""Module for all array formating functions."""
import numpy as np
from math import floor


def truncate(EEG_data, nb_min, truncation_beginning=0, fs=250):
    """Truncate EEG data.
    Args:
        EEG_data (np array)
        nb_min (int): duration of the output signal that we want
        truncation_beginning (int): second at which truncaction should start
        fs (int): EEG sampling frequency
    Returns:
        EEG_trunc (np array)
    """
    nb_points = nb_min * 60 * fs
    if truncation_beginning*fs+nb_points-1 < len(EEG_data):
        EEG_trunc = EEG_data[
            truncation_beginning*fs: truncation_beginning*fs+nb_points-1]
    else:
        print("The number of minutes required is greater than total duration")
        EEG_trunc = EEG_data[truncation_beginning*fs:]

    return EEG_trunc


def exp_smoothing(signal, exp_smoothing_coeff=0.3):
    """Perform exponential smoothing on input signal.
    Args:
        signal (np array)
        exp_smoothing_coeff (int)
    Returns
        smoothed_data (np array)
    """
    smoothed_data = np.zeros((len(signal), 1), dtype=float, order='C')
    smoothed_data[0] = signal[0]
    for i in range(len(signal)-1):
        smoothed_data[i+1] = (1-exp_smoothing_coeff)*smoothed_data[i] +\
            exp_smoothing_coeff*signal[i+1]
    return smoothed_data


def mean_smoothing(signal, win_size):
    """Perform mean smoothing on 1Hz input signal.
    Args:
        signal (np array): input data at 1Hz
        win_size (int): window size in sec
    Returns:
        averaged_signal (np array)
    """
    averaged_signal = np.zeros((len(signal), 1))
    for i in range(win_size):
        averaged_signal[i] = signal[i]
    for i in range(len(signal)-win_size):
        averaged_signal[i+win_size] = np.mean(signal[i:i+win_size])
    return(averaged_signal)


def array_dilation(signal, nb_pts):
    """Dilate an alpha power STEREO array to a given size."""
    original_size = len(signal)
    size_ratio = int(floor(nb_pts/original_size))
    dilated_array = np.zeros((nb_pts, 2))
    for i in range(original_size-1):
        for j in range(size_ratio):
            dilated_array[i*size_ratio+j][0] = signal[i][0] \
                + (signal[i+1][0]-signal[i][0]) * j / size_ratio
            dilated_array[i*size_ratio+j][1] = signal[i][1] \
                + (signal[i+1][1]-signal[i][1]) * j / size_ratio
    return dilated_array


def polynome(array):
        """Return polynomial function from coeffs array."""
        def calcul(t):
            """Return f(t)."""
            resultat = 0
            for i in range(len(array)):
                resultat += array[len(array)-i-1] * t**i
            return resultat
        return calcul


def get_fs_acc(EEG_data, mvt_data, fs):
    """Return accelerometer frequency.
    Args:
        EEG_data (np array)
        mvt_data (np array)
        fs (int): EEF sampling frequency
    Returns:
        fs_acc (int): accelerometer frequency in Hz
    """
    fs_acc = 5   # 5 Hz by default, migth be 50Hz

    if int(len(EEG_data)/len(mvt_data)) == 50:
        fs_acc = 5  # Normal
    elif int(len(EEG_data)/len(mvt_data)) == 5:
        fs_acc = 50
    elif int(len(EEG_data)/len(mvt_data)) == 1:
        fs_acc = 250
    else:
        print(
            "There is a problem with accelerometer frequency",
            len(EEG_data)/len(mvt_data))

    return fs_acc