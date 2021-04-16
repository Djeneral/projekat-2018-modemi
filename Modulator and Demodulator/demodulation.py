class Demod(object):


    def __init__(self, f1 = 38600, f0 = 39400, Fs = 100000, T = 0.0005, Amp = 5,  F = 39100  ):
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
        cos = np.cos(2 * np.pi * self.f0 * (np.arange(0, len(y_filtered)/len(inbin), 1 / float(self.Fs))))
        out = []
        mut = np.zeros(len(y_filtered))
        for i in range (0, int(len(y_filtered))):
            mut[i] = y_filtered[i]*cos[i]

        for i in range(0, len(inbin)):
            mut = mut[i * int(self.Fs * self.T): (i + 1) * int(self.Fs * self.T)]
            if scipy.integrate.simps(mut) > 0:
                out.append(0)
            else:
                out.append(1)
