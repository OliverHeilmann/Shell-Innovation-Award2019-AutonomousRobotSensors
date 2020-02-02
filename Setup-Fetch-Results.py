from marvelmind_cy_mm import MarvelmindHedge
from opticalflow import Optical_Flow
import BNO055
from time import sleep

# Initiate IMU Thread
optic = Optical_Flow()
hedge = MarvelmindHedge(tty = "/dev/ttyACM0", adr=4, debug=False)
bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=18)

#SETUP PHASE FOR SENSORS
def Setup():
    hedge.start()
    optic.start()
    bno.connect_IMU()
    sleep(2)
    
#FETCH RESULTS FROM SENSORS
def fetch_beacon():
    state = hedge.position()
    return state

def fetch_optic():
    state=optic.position()
    return state

def fetch_IMU():
    state=bno.position()
    return state

#OTHER IMPORTANT FUNCTIONS
def reset_optic():
    optic.reset()
    pass

def calibrate_IMU():
    bno.calibrate()
    pass