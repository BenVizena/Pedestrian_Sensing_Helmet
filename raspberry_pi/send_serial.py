import serial
import random
import time

class Serial_Class():
    ser = ''
    create_serial_connection_called = False

    @staticmethod
    def create_serial_connection(device = '/dev/ttyUSB0', baud_rate = 9600):
        Serial_Class.ser = serial.Serial(device, baud_rate)
        Serial_Class.create_serial_connection_called = True
#        print(Serial_Class.create_serial_connection_called)

    @staticmethod
    def write_to_serial(message_in):
#        print('this is it: ')
#        print(Serial_Class.create_serial_connection_called)
        if Serial_Class.create_serial_connection_called == False:
            print('NEED TO CALL "create_serial_connection" BEFORE "write_to_serial"!')
        else:
	    message = str(message_in);
	    if len(message) > 3:
		print('message too large to send!')
	    else:
		while len(message) < 3:
		    message = '0' + message

	        Serial_Class.ser.write(message)
        	print("WROTE " + message + " TO SERIAL")



def main():
    
    Serial_Class.create_serial_connection()
#    Serial_Class.write_to_serial(random.randint(0, 101))

    while True:
        who = random.randint(0, 100)
        Serial_Class.write_to_serial(who)
#        print(who)
        time.sleep(2)

if __name__ == "__main__": main()
