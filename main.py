import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
#from scipy.io import wavfile
#import scipy.signal.signaltools as sigtool
#import scipy#.signal as signal
#import filter
#import mls
#import binascii
import random
#import pandas as pd
#import wave
class Mod (object):

    def __init__(self, f1 = 38600, f0 = 39400, Fs = 384000, T = 0.015, Amp = 5, F = 39100 ):  # sep_sequence = [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0] ):
        self.f1 = f1
        self.f0 = f0
        self.Fs = Fs
        self.T = T
        self.Amp = Amp
        self.F = F
        #self.presequence = [ 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        # (15, 0, 15)
        #self.sep_sequence = sep_sequence

    def listtobin(self, words):
        bits = [[ord(ch) for ch in word] for word in words]
        result = []
       # result.extend(presequence)
        for word in words:
            for ch in word:
                bits = bin(ord(ch))[2:]
                bits = '00000000'[len(bits):] + bits
                result.extend([int(b) for b in bits])
           # if len(words)>1:
        #result.extend([0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0 ])#[0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0])
        return (result)


    def modulate_fsk(self, bit_arr):

        t = np.arange(0,float(len(bit_arr))*float(self.T),1/float(self.Fs), dtype=np.float) # generise niz brojeva od 0 do trajanja duzine poruke sa korakom koji je jednak vremenskoj udaljenosti izmedju dve tacke
        m = []
        self.Amp = 5
        for bit in bit_arr:
            if bit == 0:
                m=np.hstack((m,np.multiply(np.ones(int(self.Fs*self.T)),self.f0))) #pravi niz popunjen jedinicama duzine koja je jednaka broju tacaka u jednom bitu i mnozi taj niz sa potrebnom frekvencijom
            else:
                m=np.hstack((m,np.multiply(np.ones(int(self.Fs*self.T)),self.f1)))

        y=np.zeros(0)
        y=self.Amp * np.cos(2*np.pi*np.multiply(m,t)) #generise niz ciji su clanovi kordinate tacaka na y osi
        #pl.plot(y)
        #pl.show()

        return (y)

    def modulate_psk(self, inbin):

        for i in range(0, len(inbin)):
            inbin[i] = 2 * inbin[i] - 1
        t = np.linspace(0, len(inbin), len(inbin) * self.T * self.Fs)
        sig = np.repeat(inbin, self.Fs * self.T)
        wave = self.Amp *np.sqrt(self.T)*(np.sin(2*np.pi*self.F*t)).astype(np.float)
        psk_wave = sig * wave

        return (psk_wave)

    def modulate_ask(self, bit_arr):
        t = np.linspace(0, len(bit_arr), len(bit_arr) * self.T * self.Fs)
        dd = np.repeat(bit_arr, self.Fs * self.T)
        y = dd * np.sin(2 * np.pi * self.F * t)
        return (y)

    def downsample(self, sent_signal,  bit_arr):
        signal = scipy.signal.resample(sent_signal, int(self.T*(len(bit_arr))*300000))
        signal = np.hstack((signal, np.zeros(len(signal)/2)))
        return signal

class Demod(object):


    def __init__(self, f1 = 38600, f0 = 39400, Fs = 1000000, T = 0.001, Amp = 5,  F = 39100  ):
        self.f1 = f1
        self.f0 = f0
        self.Fs = Fs
        self.T = T
        self.Amp = Amp
        self.F =F


    def correlate (self, sent_signal, rec_signal):
        corrsig = scipy.signal.correlate(sent_signal, rec_signal, mode='full')
        return corrsig

    def p_fsk(self, insig):

        def butter_highpass_filter(data, cutoff, fs, order=15): #order je maksimalni broj odlozenih inouta/outputa koji se koriste u izracunavanju trenutne filtrirane tacke signala
            b, a = scipy.signal.butter(order, 0.65, btype='high', analog=False) #polinomi u imeniocu i brojiocu bloka koijm se filtrira signal u sledecoj liniji
            y_filtered = scipy.signal.filtfilt(b, a, data) #linearni filtar koji prolayi kroz signal dva puta u rayicitim smerovima
            return y_filtered

        def butter_lowpass_filter(data, cutoff, fs, order=15):
            b, a = scipy.signal.butter(order, 0.85, btype='low', analog=False)
            y_filtered = scipy.signal.filtfilt(b, a, data)
            return y_filtered
        y_filtered = butter_highpass_filter(insig, 38000, self.Fs)
        y_filtered = butter_lowpass_filter(y_filtered, 40000, self.Fs)
        return (y_filtered)

    def demodulate(self, y_filtered, inbin):
        cos = np.cos(2 * np.pi * self.f0 * (np.arange(0,self.T, 1 / float(self.Fs))))
        print len(y_filtered)
        print len(cos)
        out = []
        mut = np.zeros(len(y_filtered))
        for i in range (0, int(len(y_filtered))):
            mut[i] = y_filtered[i]*cos[i % len(cos)]
        print len (mut)
        for i in range(0, (len(inbin)-1)):
            mut1 = mut[(i * int(self.Fs * self.T)) : ((i + 1) * int(self.Fs * self.T) + 1)]
            #print(mut.shape)
            if scipy.integrate.simps(mut1)>0:
                out.append(0)
            else:
                out.append(1)
        return out

Fs = 384000
T = 0.015
#t = 5
#n = int(t/T)
mess = ["PFE "]
filename = "data2/PFE_15ms.csv"
m = Mod()
d = Demod()

bin1 = m.listtobin(mess)
print bin1
#bin1 = np.random.random_integers(0, 1, n)
sent_signal = m.modulate_fsk(bin1)
print (len(sent_signal))
np.savetxt(filename, sent_signal)
np.savetxt("data2/PFE_15ms", bin1)


#sent_signal = m.downsample(sent_signal, bin1)
"""
Fs, refsig = wavfile.read("Ref_10010_1.wav")
refsig = refsig.astype(np.float)/2**8

Fs, insig = wavfile.read("Out_10010_1.wav")
print Fs
insig = insig.astype(np.float)/2**8
pl.plot(insig)
pl.show()
f, t, Sxx = scipy.signal.spectrogram(insig, Fs)
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
#insig = insig[21600:271700]
#insig = d.correlate(sent_signal, insig)

#pl.plot(insig)
#pl.show()
print(len(insig))
signal = d.p_fsk(insig)

bin2 = d.demodulate(insig, bin1)
print(bin2)



#signal = wave.open("hhhh_sent.wav", "w")
#signal.setparams((1, 2, Fs, 7601, "NONE", "not compresed"))


# pl.plot(signal)
# # pl.show()
#m.totxt(filename, sent_signal)
"""