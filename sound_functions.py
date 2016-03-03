"""Functions around WAV files generation."""

import numpy as np
from scipy.io.wavfile import write, read
from math import floor
import array_functions as array


def set_to_size(array, duration, rate=44100):
    """Create an audio file of a given size by looping the input array.

    Args:
        array (np array)
        duration (int): output sound durations in sec
        rate (int): sampling rate

    Returns:
        looped_array (np array)

    """
    in_length = len(array)
    # First determine the number of complete loops
    nb_loops = int(floor(duration*44100/in_length))
    looped_array = np.array([[0, 0], [0, 0]])
    for i in range(nb_loops):
        looped_array = np.concatenate((looped_array, array), axis=0)
    # Now append the last incomplete part
    # Calculate the rest of the euclidian division of duration by len(array)
    eucl_rest = duration*44100 - nb_loops*in_length
    # Append the right number of zeros to looped_array
    looped_array = np.concatenate(
        (looped_array, np.zeros((eucl_rest, 2))),  axis=0)
    for i in range(eucl_rest):
        looped_array[nb_loops*in_length + i] = array[i]

    return looped_array


def create_SO_sound(
        sound_in, file_name_out, volume_control, sampling_rate=44100):
    """Create a wav file of the sleep onset duration controled in volume_control.

    Volume_control is generated from the sleep onset SO_metric with function
    generate volume control

    Args:
        sound_in (string): path to background music file
        file_name_out (string): path to output WAV file to create
        SO_metric (np array): sleep onset metric at 1Hz
        sampling_rate (int)

    Returns:
        Void
    """
    length = len(volume_control)  # This is the length in sec
    # Normalize volume_control
    volume_control = volume_control/np.amax(volume_control)
    # The volume control array is 1D
    # Let's turn it into 2D array to multiply it with our stereo wav array
    print("creating volume_control_stereo from volume_control")
    volume_control_stereo = np.zeros((length, 2))
    for i in range(length):
        volume_control_stereo[i][0] = volume_control[i]
        volume_control_stereo[i][1] = volume_control[i]

    # We need the audio file to be of the right duration
    print("setting audio file to right duration")
    array_in = read(sound_in)
    audio_in_stereo = set_to_size(array_in[1], length)

    # Volume_control should be at 1Hz; we want to turn it to 44100Hz
    print("dilating volume_control_stereo to audio size")
    volume_control_stereo = array.array_dilation(
        volume_control_stereo, len(audio_in_stereo))
    print("multiplying audio and volume control")
    audio_out_stereo = volume_control_stereo * audio_in_stereo

    # Write our WAV file
    print("writing WAV file")
    write(file_name_out, sampling_rate, audio_out_stereo)
