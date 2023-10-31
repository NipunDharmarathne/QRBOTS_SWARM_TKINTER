import tkinter as tk
import socket
import time

def create_udp_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 14550))
    return server_socket

def receive_data(socket, source_ip_list):
    start_time = time.time()
    while time.time() - start_time < 3:
        data, addr = socket.recvfrom(1024)

        if addr[0] not in source_ip_list:
            source_ip_list.append(addr[0])

        # print(f"Source IP: {addr[0]}")
   
    print("Unique Source IP Addresses:")
    for ip in source_ip_list:
        print(ip)

def start():
    receive_data(server_socket, source_ip_list)

source_ip_list = []
server_socket = create_udp_socket()

# Create the main tkinter window
root = tk.Tk()
root.title("Start/Stop Loop")

# Create buttons to start and stop the loop
start_button = tk.Button(root, text="Start Loop", command=start)
start_button.pack()

# Start the tkinter main loop
root.mainloop()
