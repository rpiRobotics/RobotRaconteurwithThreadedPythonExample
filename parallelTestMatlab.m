% Parallel Test Script

clear variables; close all; clc

parallelTest = RobotRaconteur.Connect('tcp://192.168.1.136:8338/RRParallel/parallelTestServ');

num_samples = 10000;
Tf = 10; % final time/test length

ttemp = 0;
t = zeros(1,num_samples);
testvals = zeros(1,num_samples);
k = 1;
tic 
while ttemp<Tf
    ttemp = toc;
    testvals(k) = parallelTest.getTestVal();
    t(k) = ttemp;
    k = k+1;
end

idx = find(t,1,'last');
t = t(1:idx);
testvals = testvals(1:idx);

figure(1)
plot(t,testvals,'b','LineWidth',2)
xlabel('Time (s)')
ylabel('Test Value')

figure(2)
plot(diff(t),'b','LineWidth',2)
xlabel('Sample Rate (s)')