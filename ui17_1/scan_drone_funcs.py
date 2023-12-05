import socket
import time
from pymavlink import mavutil
from tkinter import *

def create_udp_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 14550))
    udp_socket.settimeout(3.0)
    return udp_socket

def receive_data(frame, canvas, esp32_ip_list, udpout_connection_list, numDrones, map_widget, location_drone, markers_drones):
    esp32_ip_list.clear()
    udpout_connection_list.clear()

    udp_socket = create_udp_socket()
    
    try:
        start_time = time.time()
        while True:
            if time.time() - start_time >= 3:
                break  # Exit the loop after 3 seconds
            try:
                data, addr = udp_socket.recvfrom(1024)
                if addr[0] not in esp32_ip_list:
                    esp32_ip_list.append(addr[0])
                # print(f"Received packet from {addr[0]}:{addr[1]}")
            except socket.timeout:
                print("No packet received within the timeout.")
    except KeyboardInterrupt:
        print("Listening stopped.")
    finally:
        udp_socket.close()
    
    esp32_ip_list = sorted(esp32_ip_list, key=lambda x: (int(x.split('.')[-1]), x))
    print("ESP32 IPs:", esp32_ip_list)

    numDrones.config(text=len(esp32_ip_list))

    for source_ip in esp32_ip_list:
        connection = mavutil.mavlink_connection('udpout:' + source_ip + ':14555')
        udpout_connection_list.append(connection)
    
    create_labels_and_buttons(frame, canvas, esp32_ip_list, udpout_connection_list)
    print("UDPOUT Connections:", udpout_connection_list)

    for i in range(len(esp32_ip_list)):
        markers_drones.append(map_widget.set_marker(0, 0, icon=location_drone, icon_anchor="s", text=i+1, text_color="#000000", font="Tahoma 6 bold"))
    print(markers_drones)




def create_labels_and_buttons(frame, canvas, esp32_ip_list, udpout_connection_list):
    # Clear the frame by destroying all its children widgets
    for widget in frame.winfo_children():
        widget.destroy()
        
    def arm_button_command(ip):
        print(f"ARM button clicked for {ip}")
        index = esp32_ip_list.index(ip)
        udpout_connection_list[index].mav.sys_status_send(11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    def disarm_button_command(ip):
        # Add the action you want to perform when the DISARM button is clicked for the given IP
        print(f"DISARM button clicked for {ip}")
        index = esp32_ip_list.index(ip)
        udpout_connection_list[index].mav.sys_status_send(12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    
    def takeoff_button_command(ip):
        # Add the action you want to perform when the TAKE OFF button is clicked for the given IP
        print(f"TAKE OFF button clicked for {ip}")
        index = esp32_ip_list.index(ip)
        udpout_connection_list[index].mav.sys_status_send(13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    def light_button_command(ip):
        # Add the action you want to perform when the LIGHT button is clicked for the given IP
        print(f"LIGHT button clicked for {ip}")

    if len(esp32_ip_list) > 0:
        for i in range(len(esp32_ip_list)):
            # print(f"IP address {i}: {esp32_ip_list[i]}")
            droneIP = Label(frame, text=esp32_ip_list[i])
            arm = Button(frame, text="ARM", bg="springgreen3", command=lambda ip=esp32_ip_list[i]: arm_button_command(ip))
            disarm = Button(frame, text="DISARM", bg="cyan3", command=lambda ip=esp32_ip_list[i]: disarm_button_command(ip))
            light = Button(frame, text="LIGHT", bg="olivedrab1", command=lambda ip=esp32_ip_list[i]: light_button_command(ip))
            takeOff = Button(frame, text="TAKE OFF", bg="chocolate1", command=lambda ip=esp32_ip_list[i]: takeoff_button_command(ip))

            droneIP.grid(row=i, column=0, padx=1, pady=1, sticky="w")
            arm.grid(row=i, column=1, padx=1, pady=1, sticky="e")
            disarm.grid(row=i, column=2, padx=1, pady=1, sticky="e")
            light.grid(row=i, column=3, padx=1, pady=1, sticky="e")
            takeOff.grid(row=i, column=4, padx=1, pady=1, sticky="e")
    else:
        errMsg = Label(frame, text="Unable to establish a connection.")
        errMsg.grid(row=0, column=0, padx=1, pady=1, sticky="w")

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
