function [] = bin2wav(name_in, name_out, a, b)
fileID = fopen(name_in,'r');
B = fread(fileID,10000);
fclose(fileID);
plot(B);

y = B(a:b);
%plot(y);

audiowrite(name_out,y/max(y),192000);
end

