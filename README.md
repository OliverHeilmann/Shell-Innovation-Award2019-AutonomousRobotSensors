# AutonomousRobot-Sensors
Marvelmind ultrasonic beacon system, BNO055 IMU, Optical flow sensor (from computer mouse via USB to Raspberry Pi)

## Beacon Commands (import marvelmind_cy_mm):
Create Thread: hedge = MarvelmindHedge(tty = "/dev/ttyACM0", adr=4, debug=False)
Start Thread: hedge.start()
Fetch Position: hedge.position() #Note: as [x,y,z]

## Optical Flow Commmands (import opticalflow):
Create Thread: optic = Optical_Flow()
Start Thread: optic.start()
Fetch Position: optic.position() #Note: as [dx,dy]
Reset Position: optic.reset()	 #Note: as [0,0]
Stop Readings: optic.stop() #Note: kernal cannot be started again after

## IMU Commands (import BNO055):
Create Thread: bno = BNO055.BNO055(serial_port='/dev/ttyS0', rst=18)
Start Thread: bno.connect_IMU() #Note: this is a custom function to subvert bug when initialising
Fetch Position: bno.position() #Note: as [heading,roll,pitch,sys,gyro,accel,mag], 3:end are calibration
Calibrate Sensors: bno.calibrate() # See notes below:

## Calibration Instructions:
Once bno.calibrate() has been called then calibration begins. The order is [gyro, accelerometer, magnometer, system]
	a) Gyro: leave still
	b) Accelerometer: 45 deg turns on every axis
	c) Magnometer: figure of 8s in air (up and down not forwards and back)
	d) System: leave still in starting position


### For the IMU to work one must do the following: 
1a) Follow the instructions on the following weblink: https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/overview
1b) Use commands in the terminal: 
sudo apt-get update 
sudo apt-get install -y build-essential python-dev python-smbus python-pip git
cd ~ 
git clone https://github.com/adafruit/Adafruit_Python_BNO055.git 
cd Adafruit_Python_BNO055 
sudo python setup.py install

## You will also need to go into your Pi 3B+ config files to setup the IMU to use MINIUART:
2a) Enable Serial Port, Disable Serial Console (Preferences, R.Pi Config, Interfaces)
2b) Write enable_uart=1 (write 'sudo nano /boot/config.txt' in terminal and add line/ change 0 -> 1)
2c) Disable serial port 'ttyAMAO' with 'sudo systemctl disable serial-getty@ttyAMA0.service'
2d) dtoverlay=pi3-miniuart-bt  #To swap bluetooth and serial ports 
2e) sudo reboot

For detailed explination on the above steps visit:
https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3/
