# Written by Oliver Heilmann
# 14/03/2019

# This code takes the mouse pixel readings (from the USB port). This thread can be
# initiated in the main body code and will run in the background. See fetch_optic.py
# for more information on how to fetch the optical flow measurements.

# Optical Flow Mouse is Redragon M601 Centrophorus-3200 DPI
# However any mouse can be used with a USB port

import struct, math, os, errno
from threading import Thread

'''
25.4 mm = 1 inch
Mouse has 1200 DPI ie 1200/25.4 DPmm
ie 25.4/1200= 0.021167 mm per dot
'''
file = open( "/dev/input/mice", "rb" );
DPI=3200; mm_dot=25.4/DPI;
grad=1/0.2935   # calculated through testings(see OptFlow_Cali.xlsx for further details)
const=0.6469    # as above
class Point:
    x = 0.0
    y = 0.0

def getMouseEvent():
    buf = file.read(3);
    x,y = struct.unpack( "bb", buf[1:] );
    dis = Point();
    dis.x = x; dis.y = y;
    return dis;

class Optical_Flow(Thread):
    def __init__(self):
        self.point_x = 0; self.point_y = 0;
        self.stx=0; self.sty=0;
        self.has_been_called=False
        self.terminationRequired = False
        Thread.__init__(self)

    def position(self):
        return [self.stx,self.sty]
    
    def stop(self):
        self.terminationRequired = True
        print ("stopping")

    def reset(self):
        self.stx=0; self.sty=0;
        self.point_x = 0; self.point_y = 0;
        self.has_been_called=True
        print('Optic Kernel Reset to [0,0]')
        pass
    
    def run(self):
        while (not self.terminationRequired):
            try:
                if self.has_been_called==False:
                    dis = getMouseEvent();
                    self.point_x = self.point_x + ((grad * dis.x)-const);   # using scaling from experimentation
                    self.point_y = self.point_y + ((grad * dis.y)-const);
                    dist_x=self.point_x*(mm_dot); dist_y=self.point_y*(mm_dot); # convert to mm
                    self.stx=dist_x; self.sty=dist_y
                    #print('%d %d' % (dist_x,dist_y))   # print distance in command window
                elif self.has_been_called==True:
                    self.has_been_called=False
            except:
                print ('An Error Occurred in opticalflow.py')
                file.close();
                break
            
# FUNCTIONS TO USE IN MAIN SCRIPT
# initiate thread: optic=Optical_Flow()
# optic.start()
# optic.position()
# optic.reset()
