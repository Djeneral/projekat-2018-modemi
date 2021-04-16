from pylab import *
import vxi11
import time
import progressbar
class preamble:
    def __init__(self, preambleString):
        dat = preambleString.split(",");
        self.format = int(dat[0]);
        self.type = int(dat[1]);
        self.points = int(dat[2]);
        self.count = int(dat[3]);
        self.xincrement = double(dat[4]);
        self.xorigin = double(dat[5]);
        self.xreference = double(dat[6]);
        self.yincrement = double(dat[7]);
        self.yorigin = double(dat[8]);
        self.yreference = double(dat[9]);

class oscilloscope:
    channel1 = "channel1";
    channel2 = "channel2";
    channel3 = "channel3";
    channel4 = "channel4";
    
    def __init__(self, IP = "192.168.0.19"):
        self.osc = vxi11.Instrument(IP);
    def reset(self):
        self.osc.write("*rst");
    def stop(self):
        self.osc.write("stop");
    def run(self):
        self.osc.write("run");
    def single(self):
        self.osc.write("trigger:sweep single");
    def getDataNoStop(self, channel, properTime = True, trackProgress = True):
        self.osc.write("wav:source {0}".format(channel));
        self.osc.write("wav:mode max");
        self.osc.write("wav:format byte");
        
        pream = preamble(self.osc.ask("wav:preamble?"));
        start = 0;
        data="";
        if(trackProgress):
            print channel + " data:"

        while(pream.points - start - 2.5e+5 > 0):
            self.osc.write("wav:start {0}".format(start+1));
            self.osc.write("wav:stop {0}".format(start + int(2.5e+5)));
            data = data + (self.osc.ask_raw("wav:data?")[11:-1]);
            start = start + int(2.5e+5);
        self.osc.write("wav:start {0}".format(start+1));
        self.osc.write("wav:stop {0}".format(pream.points));
        data = data + self.osc.ask_raw("wav:data?")[11:-1];
        datapnts = [];
        for i in data:
            datapnts.append(ord(i));
        datapnts = double(datapnts);
        datapnts = datapnts - pream.yreference - pream.yorigin;
        y = datapnts*pream.yincrement;
        if(properTime):
            x = arange(-pream.points*pream.xincrement/2.0 + pream.xorigin, pream.points*pream.xincrement/2.0 + pream.xorigin, pream.xincrement);
        else:
            x = arange(0.0, pream.points*pream.xincrement, pream.xincrement);
        
        return [x, y];
    
    def getDouble(self, command):
        raw = self.osc.ask(command);
        return double(raw);
        
    def autorangeY(self, channel):
        val = 1
        while True:
            val = self.getDouble(
                "measure:item? vpp, {0}".format(channel));
            self.write("{0}:range {1}".format(channel, val*1.2));
            time.sleep(0.3);
            newVal = self.getDouble("measure:item? vpp,{0}".format(channel));
            if abs(val-newVal)/val < 0.1:
                break;

    def setrangeX(self, frequency, nPeriod):
        period = nPeriod/double(frequency)/12.0;
        self.osc.write("timebase:scale {0}".format(period));
                       
    def write(self, cmd):
        self.osc.write(cmd);

    def setrangeY(self, channel, amplitude):
        self.write("{0}:range {1}".format(channel, amplitude*1.2));
        time.sleep(0.3);
    def ask(self, question):
	    return self.osc.ask(question);
    
    def trigSingleBlocking(self):
        self.run();
        self.single();
        time.sleep(0.1);
        while(self.ask("trigger:status?") != "STOP"):
            time.sleep(0.1);
    def setDivPosition(self, channel, position):
        range = self.getDouble("{0}:range?".format(channel));
        self.write("{0}:offset {1}".format(channel, range/8*position));
    def channel(self, channel):
        if (channel in [1,2,3,4]):
            return "channel{0}".format(channel);

