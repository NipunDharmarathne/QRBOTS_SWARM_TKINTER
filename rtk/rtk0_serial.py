import serial

serial_port = serial.Serial('COM8', 921600)
out_port = serial.Serial('COM2', 921600)

while True:
    data = serial_port.readline()
    out_port.write(data)
    print(data)

