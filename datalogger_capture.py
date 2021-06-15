import serial
import time
from datetime import datetime

outputfile = open("output.txt", "a+")

print("Datalogger Interface for PI3")
serialport = serial.Serial(port='/dev/ttyS0', baudrate=19200, timeout=1)

if(serialport.isOpen() == True):
	serialport.close()

now = datetime.now()
outputfile.write("Datalogger Output")
#outputfile.write(date.today())
outputfile.write(now.strftime("%d/%m/%Y %H:%M:%S"))

int_start_cap = 0

serialport.open()

serialport.write("a") # Send real time data to serial port
time.sleep(0.01)
serialport.write("6") # Send real time data to serial port
time.sleep(0.01)
serialport.write("a") # Send real time data to serial port
time.sleep(0.01)
serialport.write("0") # Send real time data to serial port
time.sleep(0.01)
serialport.write("0") # Send real time data to serial port
time.sleep(0.01)

print("Listening on serial 0")
try:
	while True:	
#  		serialport.write(".")
		rcv = serialport.read(size=100)
		serialport.flush()
		print rcv
		print("--")
		if(rcv[1]=='C' and rcv[2]=='H'):
			outputfile.write("@" + rcv[4] + ":" + rcv[6] + rcv[7] + rcv[8] + rcv[9] + rcv[10])

except KeyboardInterrupt:
	serialport.close()
	outputfile.close()


