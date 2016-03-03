import numpy as np;
from scipy.io.wavfile import write

def pink(N, depth=80):
    """ N-length vector with (approximate) pink noise
    pink noise has 1/f PSD """
    a = []
    s = iterpink(depth)
    for n in range(N):
        a.append(s.next())
    return a

def iterpink(depth=20):
    """Generate a sequence of samples of pink noise.
    pink noise generator
    from http://pydoc.net/Python/lmj.sound/0.1.1/lmj.sound.noise/
    Based on the Voss-McCartney algorithm, discussion and code examples at
    http://www.firstpr.com.au/dsp/pink-noise/
    depth: Use this many samples of white noise to calculate the output. A
    higher number is slower to run, but renders low frequencies with more
    correct power spectra.
    Generates a never-ending sequence of floating-point values. Any
    continuous
    set of these samples will tend to have a 1/f power spectrum.
    """
    values = np.random.randn(depth)
    smooth = np.random.randn(depth)
    source = np.random.randn(depth)
    sumvals = values.sum()
    i = 0
    while True:
        yield sumvals + smooth[i]
        # advance the index by 1. if the index wraps, generate noise to use
        # in
        # the calculations, but do not update any of the pink noise values.
        i += 1
        if i == depth:
            i = 0
            smooth = np.random.randn(depth)
            source = np.random.randn(depth)
            continue
        # count trailing zeros in i
        c = 0
        while not (i >> c) & 1:
            c += 1
            # replace value c with a new source element
            sumvals += source[i] - values[c]
            values[c] = source[i]

total_time = 5  # duration of wav file in seconds
dur_stim = 4.5  # duration of stimulus (at full power) in seconds
dur_ramps = 0.025  # duration of ramp up / ramp down phases
freq = 44100  # encoding frequency in Hz
nb_pts = int(freq * (dur_stim + 2 * dur_ramps))
nb_pts_ramp = int(freq * dur_ramps)
type_noise = 'pink'  # among 'pink', 'white'

# container for data
data = np.zeros(freq * total_time)

if type_noise == 'white':
    data[:nb_pts] = np.random.uniform(-1,1, nb_pts)
elif type_noise == 'pink':
    data[:nb_pts] = np.array(pink(nb_pts))
# smooth ramp up and down
data[:nb_pts_ramp] *= 1. * np.arange(nb_pts_ramp) / nb_pts_ramp
data[nb_pts - nb_pts_ramp:nb_pts] *= 1 - 1. * np.arange(nb_pts_ramp) / nb_pts_ramp

# scale data to get integers
scaled = np.int16(data/np.max(np.abs(data)) * 32767)
write(type_noise + '.wav', 44100, scaled)

# plot sound
import pylab as plt
plt.plot(data)
plt.show()


