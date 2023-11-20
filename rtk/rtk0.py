import serial

serial_port = serial.Serial('COM9', 57600)

while True:
    data = serial_port.readline()
    print(data)

