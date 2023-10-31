import socket
import time

# Create a UDP socket to listen on all interfaces and port 14550
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 14550))

print("Listening for UDP packets on port 14550...")

# Set a 3-second timeout for the socket
udp_socket.settimeout(3.0)

try:
    start_time = time.time()
    while True:
        if time.time() - start_time >= 3:
            break  # Exit the loop after 3 seconds
        try:
            data, addr = udp_socket.recvfrom(1024)  # Adjust buffer size as needed
            print(f"Received packet from {addr[0]}:{addr[1]}")
        except socket.timeout:
            print("No packet received within the timeout.")
except KeyboardInterrupt:
    print("Listening stopped.")
finally:
    udp_socket.close()
