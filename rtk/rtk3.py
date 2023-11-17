import serial
import socket

max_packet_size = 1400  # Adjust based on your network's MTU

serial_port = serial.Serial('COM9', 57600)
esp32_ip = '192.168.0.12'  #broadcast
esp32_port = 14555 

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = serial_port.readline()
    chunks = [data[i:i+max_packet_size] for i in range(0, len(data), max_packet_size)]

    for chunk in chunks:
        udp_socket.sendto(chunk, (esp32_ip, esp32_port))

