from oscilloscope import *
import pylab as pl
import time

osc = oscilloscope("10.51.0.65");

osc.stop();
time.sleep(1);
podaciKanal1 = osc.getDataNoStop("channel1", properTime=True);
podaciKanal2 = osc.getDataNoStop("channel2", properTime=True);

Fs = 1/(podaciKanal1[0][1] - podaciKanal1[0][0]);
# print (podaciKanal1[0], podaciKanal1[1])
# pl.plot(podaciKanal1[0], podaciKanal1[1])
# pl.show();

np.save('data2/a20ms_PFE', podaciKanal1);
np.save('data/axxxxx20ms_PFE', podaciKanal2);