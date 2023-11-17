import serial
import socket

def fragment_and_send(data, udp_socket, esp32_ip, esp32_port, chunk_size=128):
    # Calculate the number of chunks
    num_chunks = (len(data) + chunk_size - 1) // chunk_size

    # Send each chunk
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size
        chunk = data[start_idx:end_idx]

        udp_socket.sendto(chunk, (esp32_ip, esp32_port))
        print(chunk)


serial_port = serial.Serial('COM9', 57600)
esp32_ip = '192.168.0.12'  #broadcast
esp32_port = 14555 

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = serial_port.readline()
    # udp_socket.sendto(data, (esp32_ip, esp32_port))
    # print(data)
    fragment_and_send(data, udp_socket, esp32_ip, esp32_port)

