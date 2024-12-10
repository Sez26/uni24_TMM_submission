%% FFT analysis of c component
% Fs = 1/(12*60*60);    % Sampling frequency 1 per hour!!                    
% T = 1/Fs;             % Sampling period       
% L = n;                % Length of signal
% t = (0:L-1)*T;        % Time vector
% 
% c_FFT = fft(c);
% P2 = abs(c_FFT/L);
% P1 = P2(1:L/2+1);
% P1(2:end-1) = 2*P1(2:end-1);
% 
% f = Fs/L*(0:(L/2));
% plot(f,P1) 
n =100;
s = 4;
c = zeros(n,1);
c(1) = 0.5;
for t = 2:n
    c_sum = 0;
    for j = 1:(s/2)
        c_sum = c_sum + cos((2*pi*j/s) * c(t-1));
    end
    c(t) = c_sum;
end

figure;
plot(c)