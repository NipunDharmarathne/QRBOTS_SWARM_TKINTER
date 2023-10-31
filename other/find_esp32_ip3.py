import socket

def create_udp_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 14550))
    return server_socket

def receive_data(socket, source_ip_list):
    try:
        while True:
            data, addr = socket.recvfrom(1024)

            if addr[0] not in source_ip_list:
                source_ip_list.append(addr[0])

            print(f"Source IP: {addr[0]}")
            
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Exiting.")
    finally:
        socket.close()

def main():
    source_ip_list = []
    server_socket = create_udp_socket()
    receive_data(server_socket, source_ip_list)

    print("Unique Source IP Addresses:")
    for ip in source_ip_list:
        print(ip)

if __name__ == "__main__":
    main()
