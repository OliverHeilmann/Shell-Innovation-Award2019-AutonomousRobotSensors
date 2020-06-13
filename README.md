# Project Summary
Myself and four others built an autonomous robot for our Masters project. Being nominated for the *Shell Innovation Award*, we presented to a pannel of judges from Shell. It was announced, at our final university design show that we were the winners of this competition. See the following website for more information about our project, the design show and the competition.

http://uosdesign.org/designshow2019/project/robot-localisation/

## The Design
<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/ExplodedView.png">
   <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/Testing2.png"> 
   <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/Testing1.png">
</p>

## Top Level Wiring Diagram
<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/WiringDiagram.png">
</p>

# Using Sensor Functions (Top Level)
Marvelmind ultrasonic beacon system, BNO055 IMU, Optical flow sensor (from computer mouse via USB to Raspberry Pi)

## Beacon Commands (import marvelmind_cy_mm):
1) Create Thread: hedge = MarvelmindHedge(tty = "/dev/ttyACM0", adr=4, debug=False)
2) Start Thread: hedge.start()
3) Fetch Position: hedge.position() #Note: as [x,y,z]

<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/Beacon.png">
</p>

## Optical Flow Commmands (import opticalflow):
1) Create Thread: optic = Optical_Flow()
2) Start Thread: optic.start()
3) Fetch Position: optic.position() #Note: as [dx,dy]
4) Reset Position: optic.reset()	 #Note: as [0,0]
5) Stop Readings: optic.stop() #Note: kernal cannot be started again after

<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/OpticalFlow.png">
</p>

## IMU Commands (import BNO055):
1) Create Thread: bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=18)
2) Start Thread: bno.connect_IMU() #Note: this is a custom function to subvert bug when initialising
3) Fetch Position: bno.position() #Note: as [heading,roll,pitch,sys,gyro,accel,mag], 3:end are calibration
4) Calibrate Sensors: bno.calibrate() # See notes below:

<p align="center">
  <img width="750" src="https://github.com/OliverHeilmann/Shell-Innovation-Award2019-AutonomousRobotSensors/blob/master/GDP%20Github%20Figures/IMU.png">
</p>

### Calibration Instructions:
Once bno.calibrate() has been called then calibration begins. The order is [gyro, accelerometer, magnometer, system]
1) Gyro: leave still
2) Accelerometer: 45 deg turns on every axis
3) Magnometer: figure of 8s in air (up and down not forwards and back)
4) System: leave still in starting position


### For the IMU to work one must do the following: 
1) Follow the instructions on the following weblink: https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/overview
2) Use commands in the terminal: 
3) sudo apt-get update 
4) sudo apt-get install -y build-essential python-dev python-smbus python-pip git
5) cd ~ 
6) git clone https://github.com/adafruit/Adafruit_Python_BNO055.git 
7) cd Adafruit_Python_BNO055 
8) sudo python setup.py install

## You will also need to go into your Pi 3B+ config files to setup the IMU to use MINIUART:
1) Enable Serial Port, Disable Serial Console (Preferences, R.Pi Config, Interfaces)
2) Write enable_uart=1 (write 'sudo nano /boot/config.txt' in terminal and add line/ change 0 -> 1)
3) Disable serial port 'ttyAMAO' with 'sudo systemctl disable serial-getty@ttyAMA0.service'
4) dtoverlay=pi3-miniuart-bt  #To swap bluetooth and serial ports 
5) sudo reboot

For detailed explination on the above steps visit:
https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3/
