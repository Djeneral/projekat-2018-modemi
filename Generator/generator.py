import vxi11
import time
class generator(object):
    def __init__(self, IP):
        self.gen = vxi11.Instrument("192.168.0.15");
        
    def write(self, message):
        self.gen.write(message);
        time.sleep(0.1);
    def outputOn(self, channelNO):
        self.write("output{0}:state on".format(channelNO));
    def outputOff(self, channelNO):
        self.write("output{0}:state off".format(channelNO));
    def trigger(self):
        self.write("*trg");
    def reset(self):
        self.write("*rst");
    def ask(self, query):
		return self.gen.ask(query);

    def setVolatileWaveform(self, wavfrm, channel):
		length = len(wavfrm);
		if(length > 16384 | length < 8):
			print "{0} is not valid length for valid arb waveform".format(length);
			return -1
		wavString = "source{0}:data:dac VOLATILE".format(channel);
		for i in wavfrm:
			wavString += ",{0:d}".format(int(i));
		self.gen.write(wavString);
		
