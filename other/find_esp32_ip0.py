import socket

# Create a UDP socket to listen on all interfaces and port 14550
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 14550))

print("Listening for UDP packets on port 14550...")

try:
    while True:
        data, addr = udp_socket.recvfrom(1024)  # Adjust buffer size as needed
        print(f"Received packet from {addr[0]}:{addr[1]}")
except KeyboardInterrupt:
    print("Listening stopped.")

udp_socket.close()