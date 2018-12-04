# Parallel Test Code
# This code is an example for running parallel code with RR while reducing the impact on the time it takes to receive data.
# Motivating example: AR tag detection takes ~10 Hz between image capturing and processing. We would like to run a much faster control loop that uses a RR function call to obtain the most recent tag pose data. This function will be called at the faster rate (and therefore will be constant between certain control loops), but the control loop can run faster than the tag detection function.

import RobotRaconteur as RR
import thread
import threading
import numpy
import time

# Define function that takes significant computation time outside of the object class, and pass the object as an argument
def runTestFunc(obj):
    while True:
        time.sleep(1) # Here, time.sleep represents the computationally intensive function we wish to run in parallel
        with obj._lock: # Do not implement a lock until the computationally intensive function has finished, if possible. Note that this also applies to any subfunctions the computationally expensive function may call.
             obj.testVal +=1 # Fake function increases test value by 1

class RRparallelTest_impl:
    def __init__(self):
        self._lock = threading.RLock()
        self.testVal = 0

    def getTestVal(self):
        with self._lock:
            return self.testVal

def main():
    RR.RobotRaconteurNode.s.UseNumPy = True
    RR.RobotRaconteurNode.s.NodeName = "RRParallel"
    parallelTestService = RRparallelTest_impl()

    t = RR.TcpTransport()
    t.StartServer(8338)
    RR.RobotRaconteurNode.s.RegisterTransport(t)

    # Start running computationally expensive function in parallel
    updateTestVal = threading.Thread(target=runTestFunc,args = (parallelTestService,))
    updateTestVal.setDaemon(True)
    updateTestVal.start()

    try:
        with open('RRparallelTest.robdef','r') as f:
            service_def = f.read()
    except:
        print("error1")
    try:
        RR.RobotRaconteurNode.s.RegisterServiceType(service_def)
    except:
        print("error2") 
    try:
        RR.RobotRaconteurNode.s.RegisterService("parallelTestServ","edu.rpi.paralleltest.parallelTestServ",parallelTestService)
        print("Connect at tcp://localhost:8338/RRParallel/parallelTestServ")
        raw_input("press enter to quit...\r\n")
    except:
         print("error3")

    RR.RobotRaconteurNode.s.Shutdown()

if __name__=='__main__':
    main()
