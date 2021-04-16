fileID = fopen('T.bin','r');
B = fread(fileID,8000);
fclose(fileID);

signal = B;
%plot(signal);
y = B;

mysig =  B;
plot(mysig);

n = 8;
d = size(mysig,1)/n

for i=1:n
    startbit = (i-1)*d + 1;
    endbit = i*d;
    E(i) = sum(mysig(startbit:endbit));
end;
E>110000