# Written by Oliver Heilmann
# 16/04/2019

# This code accesses the incoming becaon data from the Arduino. The .ino script
# for the Arduino outputs text which must be decoded into the useful [x,y,z]
# information. Not only does this dramatically reduce the computational load
# on the Raspberry Pi, but it also increases the rate of beacon
# data transfer.

# See Hedgehog_UART.ino for more details on the Arduino script.

# FUNCTIONS TO USE IN MAIN SCRIPT
# initiate thread: beacon=Beacon_Arduino()
# beacon.start()
# beacon.stop()

import serial as sl
import time
import sys
import pdb
from threading import Thread

class Beacon_Arduino(Thread):
    def __init__(self):
        self.ser =sl.Serial('/dev/ttyACM0',115200)
        self.location=[0,0,0]
        self.x=0; self.y=0; self.z=0
        self.has_been_called=False
        self.terminationRequired = False
        Thread.__init__(self)

    def position(self):
        return self.location
    
    def stop(self):
        self.terminationRequired = True
        print ("stopping")
    
    def run(self):
        while (not self.terminationRequired):
            try:
                ser_bytes=self.ser.readline()
                if ser_bytes.find('x')!=-1 and ser_bytes.find('y')!=-1 and ser_bytes.find('z')!=-1:
                    sort=ser_bytes.split(":")
                    if len(sort)==4 and sort[0]!='':
                        str_x=sort[0].split('x'); self.x=float(str_x[1])
                        str_y=sort[1].split('y'); self.y=float(str_y[1])
                        str_z=sort[2].split('z'); self.z=float(str_z[1])
                        self.location=[self.x,self.y,self.z]
                        print(self.location)
                        time.sleep(0.1)
                        #pdb.set_trace()
            except:
                print ('An Error Occurred in Beacons_from_Ard.py')
                break
beacon=Beacon_Arduino()
beacon.start()
