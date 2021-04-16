fileID = fopen('T.bin','r');
B = fread(fileID,10000);
fclose(fileID);

signal = B(1850:4450);
%plot(signal);

[y Fs] = audioread('output10010.wav');
y = y(1:2500);

br = 0;
for i=1:2:5000
    br = br+1;
    x(i) = y(br);
end;

for i=2:2:4999
    x(i) = (x(i-1)+x(i+1))/2;
end;
plot(x);

audiowrite('output10010B.wav',x/max(x),192000);
