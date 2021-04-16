function [outputArg1,outputArg2] = txt2csv(name_in, name_out, l_sig, l_0)

dots = num2str(l_sig + 2*l_0);
s_dots = strcat('DOTS:',' ', dots);

fileID = fopen(name_in,'r');
A = fscanf(fileID,'%f \n',[l_sig 1]);
fclose(fileID);

A = A-min(A);

A = A/max(A);
A = A*16000 - 8000;
A = round(A);

fid = fopen(name_out,'w');
fprintf( fid, '%s\n', 'RIGOL:DG1:CSV DATA FILE');
fprintf( fid, '%s\n', 'TYPE:Arb');
fprintf( fid, '%s\n', 'AMP:1.0000 Vpp');
fprintf( fid, '%s\n', 'PERIOD:1.06E-6 S');
fprintf( fid, '%s\n', s_dots);
fprintf( fid, '%s\n', 'MODE:Freq');
fprintf( fid, '%s\n', 'AFG Frequency:1000000.000000');
fprintf( fid, '%s\n', 'AWG N:0');
fprintf( fid, '%s\n ', 'x, y[V]');

for i=1:l_0
    fprintf( fid, '%s ', ', ');
    fprintf( fid, '%d\n', 0);
end;

for i=1:size(A,1)
    fprintf( fid, '%s ', ', ');
    fprintf( fid, '%d\n', A(i));
end;

for i=1:l_0
    fprintf( fid, '%s ', ', ');
    fprintf( fid, '%d\n', 0);
end;

fclose(fid);
end

