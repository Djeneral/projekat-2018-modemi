from pylab import *

indat = np.load("data2/15ms_PFE.npy");

Fs = 1/(indat[0][1]-indat[0][0]);

print Fs

T = 0.020;
f1 = 38.6e+3;
f0 = 39.4e+3;

def demodulate(y_filtered, inbin):
	cos0 = np.cos(np.array(np.arange(0, T, 1 / float(Fs))) * 2 * np.pi * f0);
	sin0 = np.sin(np.array(np.arange(0, T, 1 / float(Fs))) * 2 * np.pi * f0);
	cos1 = np.cos(np.array(np.arange(0, T, 1 / float(Fs))) * 2 * np.pi * f1);
	sin1 = np.sin(np.array(np.arange(0, T, 1 / float(Fs))) * 2 * np.pi * f1);
	
	out = []
	muts0 = np.zeros(len(y_filtered))
	mutc0 = np.zeros(len(y_filtered))
	mutc1 = np.zeros(len(y_filtered))
	muts1 = np.zeros(len(y_filtered))

	
	
	for i in range (0, int(len(y_filtered))):
		mutc0[i] = y_filtered[i]*cos0[i % len(cos0)]
		muts0[i] = y_filtered[i]*sin0[i % len(sin0)]
		
		mutc1[i] = y_filtered[i]*cos1[i % len(cos1)]
		muts1[i] = y_filtered[i]*sin1[i % len(sin1)]
	for i in range(0, inbin-1):
		print i
		mutic0 = mutc0[(i * int(Fs * T)) : ((i + 1) * int(Fs * T) + 1)]
		mutis0 = muts0[(i * int(Fs * T)) : ((i + 1) * int(Fs * T) + 1)]
		mutic1 = mutc1[(i * int(Fs * T)) : ((i + 1) * int(Fs * T) + 1)]
		mutis1 = muts1[(i * int(Fs * T)) : ((i + 1) * int(Fs * T) + 1)]
		
		print indat[0][indat[0][:-1]>0][i*int(Fs*T)]
		#print(mut.shape)
		mut0 = sqrt(sum(mutic0)**2 + sum(mutis0)**2)
		mut1 = sqrt(sum(mutic1)**2 + sum(mutis1)**2)
		print mut0, mut1
		if mut0>mut1:
			out.append(0)
		else:
			out.append(1)
	
	return out
	
np.savetxt("data2/DEMtest_PFE_20ms", demodulate(indat[1][indat[0][:-1]>0], 32+1) )
