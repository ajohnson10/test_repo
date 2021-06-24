import serial
import time
from datetime import datetime

bytes_per_packet = 7
timeout_seconds = 2

def send_datalogger_command(command2send):
	serialport.write("a") # Command header byte 1
	time.sleep(0.001)
	serialport.write("6") # Command header byte 2
	time.sleep(0.001)
	serialport.write(command2send[0]) # Command byte
	time.sleep(0.001)
	serialport.write(command2send[1]) # Command data byte 1
	time.sleep(0.001)
	serialport.write(command2send[2]) # Command data byte 2
	return;

outputfile = open("output.txt", "a+")

print("Datalogger Interface for PI3")
command1 = raw_input("C = Continue, S = Set Sample Rate, R = Set Channel to Read:")
if(command1=="R"):
	print("Enter new channel enable register value in hex (LSB = Ch0)")
	print("Example: '25' = 0b00100101 = Enable 0, 2, and 5")
	command2 = raw_input("Enter new value:")
	send_datalogger_command("g" +  command2)
	time.sleep(0.2)

serialport = serial.Serial(port='/dev/ttyS0', baudrate=9600, timeout=timeout_seconds)

if(serialport.isOpen() == True):
	serialport.close()

now = datetime.now()
outputfile.write("Datalogger Output,")
#outputfile.write(date.today())
outputfile.write(now.strftime("%d/%m/%Y %H:%M:%S") + "\n")
outputfile.write("Time,Channel,Reading\n")

int_start_cap = 0

serialport.open()

def read_datalogger(reg2read):
	send_datalogger_command(reg2read + "00")
	rcv = serialport.read(size=bytes_per_packet)
	return rcv;

#channel_reg = read_datalogger("c")
#print("Channel Enable Register = " + channel_reg)

#serialport.write("a6a00")
#send_datalogger_command("a00")

#serialport.write("a") # Send real time data to serial port
#time.sleep(0.01)
#serialport.write("6") # Send real time data to serial port
#time.sleep(0.01)
#serialport.write("a") # Send real time data to serial port
#time.sleep(0.01)
#serialport.write("0") # Send real time data to serial port
#time.sleep(0.01)
#serialport.write("0") # Send real time data to serial port
#time.sleep(0.01)

missed_samples = 0 # This is appended to the last column of the written data

print("Listening on serial 0")
try:
	while True:
		#serialport.write(".")
#		rcv = serialport.read(size=bytes_per_packet)
		rcv = serialport.readline()
		serialport.flush()
#		print rcv
		#print("--")
		try:
			if(rcv[0]=='b' and rcv[1]=='7'):
#				print("Data received")
				if(rcv[2]=='g'):
#					#int_data = int(rcv[4] + rcv[5])
#					print("Data on Ch " + rcv[3] + " = " + rcv[4] + rcv[5] + rcv[6] + rcv[7])
#					print(int_data)
					print(rcv)
					now = datetime.now()
					outputfile.write(now.strftime("%H:%M:%S") + "," + rcv[4] + "," + str(missed_samples) + "," + rcv[5] + rcv[6] + rcv[7] + rcv[8] + "\n")
					if(missed_samples > 0):
						print("Missed Samples = " + str(missed_samples))
					missed_samples = 0
			else:
				print("Received: " + rcv)
				missed_samples += 1
				print(missed_samples)
		except:
			exception_counter = 1
#			print("Buffer Empty")

except KeyboardInterrupt:
	serialport.close()
	outputfile.close()


