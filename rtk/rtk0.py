import serial

serial_port = serial.Serial('COM8', 57600)

while True:
    data = serial_port.readline()
    print(data)

