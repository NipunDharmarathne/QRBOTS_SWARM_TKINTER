import socket

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 14550))

# Create a list to store the unique source IP addresses
source_ip_list = []

try:
    while True:
        # Receive data and the address of the sender
        data, addr = server_socket.recvfrom(1024)

        # Check if the sender's IP address is not already in the list
        if addr[0] not in source_ip_list:
            source_ip_list.append(addr[0])

        # Print the source IP address (if needed)
        # print(f"Source IP: {addr[0]}")

except KeyboardInterrupt:
    print("Received KeyboardInterrupt. Exiting.")

server_socket.close()

# Print the source IP list
print("Unique Source IP Addresses:")
for ip in source_ip_list:
    print(ip)
