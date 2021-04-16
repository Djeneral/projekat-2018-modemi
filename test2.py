import pylab as plt
from scipy.io import wavfile
import numpy as np
import scipy.signal

refsig = np.load("Ref_testic1.npy")
#refsig = refsig.astype(np.float)/2**8

insig = np.load("Out_testic1.npy")

#insig = insig.astype(np.float)/2**8

plt.plot(refsig);
plt.show();
Fs = 1/(insig[0][1] - insig[0][0])
print Fs

f, t, Sxx = scipy.signal.spectrogram(insig[1], Fs)
plt.pcolormesh(t, f, 20*np.log10(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
f, t, Sxx = scipy.signal.spectrogram(refsig[1], Fs)
plt.pcolormesh(t, f, 20*np.log10(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()