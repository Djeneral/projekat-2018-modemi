function [out] = add(in1, in2, net)
c = max(in1,in2);
in1 = in1/(c*2);
in2 = in2/(c*2);
out = net([in1,in2]')*(c*2);
end

