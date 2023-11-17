import serial
import socket

serial_port = serial.Serial('COM9', 57600)
esp32_ip = '192.168.0.12'  #broadcast
esp32_port = 14555 

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = serial_port.readline()
    udp_socket.sendto(data, (esp32_ip, esp32_port))
    print(data)

