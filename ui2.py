from tkinter import *
from pymavlink import mavutil
import socket
import time

# window #############################################################################
master = Tk()
master.configure(bg="grey6")
master.title("QRBOTS")

# num Drones #########################################################################
numDronesLabel = Label(master, text = "Number of Drones:", fg="white", bg="grey6")
numDronesLabel.grid(row = 0, column = 0, sticky = E)
numDrones = Label(master, text = "0", fg="white", bg="grey6")
numDrones.grid(row = 0, column = 1, sticky = W)

# Create a frame for the canvas and scrollbar ########################################
frame = Frame(master)
frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Specify the width and height for the canvas
canvas = Canvas(frame, width=300, height=100)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas.config(yscrollcommand=scrollbar.set)

frame_inner = Frame(canvas)
canvas.create_window((0, 0), window=frame_inner, anchor="nw")

def welcome_message(frame):
    welcomeMsg = Label(frame, text="Welcome to QRBOTS. Press SCAN button.")
    welcomeMsg.grid(row=0, column=0, padx=1, pady=1, sticky="w")

welcome_message(frame_inner)
frame_inner.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# scan, stop buttons #################################################################
def scan():
    receive_data(esp32_ip_list)

def start():
    the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

scan = Button(master, text = "SCAN", bg="springgreen3", command=scan)
master.rowconfigure(2, minsize=35)
scan.grid(row = 2, column=0, columnspan=2)



'''/// BACKEND ////////////////////////////////////////////////////////////////////////////////////////////////////'''
esp32_ip_list = []
udpout_connection_list = []

def create_udp_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 14550))
    udp_socket.settimeout(3.0)
    return udp_socket

def receive_data(esp32_ip_list):
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
    
    create_labels_and_buttons(frame_inner)
    print("UDPOUT Connections:", udpout_connection_list)


'''/// BUTTON COMMANDS //////////////////////////////////////////////'''
def arm0():
    udpout_connection_list[0].mav.sys_status_send(11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def armAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def disarmAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def takeOffAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def landAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def rtlAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def showAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(16, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def lightsAll():
    for connection in udpout_connection_list:
        connection.mav.sys_status_send(17, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)



b1 = Button(master, text = "ARM ALL", height=3, width=25, bg="springgreen3", command=armAll)
b1.grid(row = 3, column = 0, sticky = W)

b2 = Button(master, text = "DISARM ALL", height=3, width=25, bg="cyan3", command=disarmAll)
b2.grid(row = 3, column = 1, sticky = W)


b3 = Button(master, text = "TAKE OFF ALL", height=3, width=25, bg="chocolate1", command=takeOffAll)
b4 = Button(master, text = "LAND ALL", height=3, width=25, bg="goldenrod1", command=landAll)
b5 = Button(master, text = "RTL ALL", height=3, width=25, bg="tomato", command=rtlAll)
b6 = Button(master, text = "SHOW ALL", height=3, width=25, bg="tomato", command=showAll)
b7 = Button(master, text = "LIGHT ALL", height=3, width=25, bg="olivedrab1", command=lightsAll)


# arranging button widgets
b3.grid(row = 4, column = 0, sticky = W)
b4.grid(row = 4, column = 1, sticky = W)
b5.grid(row = 5, column = 0, sticky = W)
b6.grid(row = 5, column = 1, sticky = W)
b7.grid(row = 6, column = 0, sticky = W)



'''/////////////////////////////////////////////////'''

def create_labels_and_buttons(frame):
    # Clear the frame by destroying all its children widgets
    for widget in frame.winfo_children():
        widget.destroy()
        
    def arm_button_command(ip):
        # Add the action you want to perform when the ARM button is clicked for the given IP
        print(f"ARM button clicked for {ip}")
        arm0()

    def disarm_button_command(ip):
        # Add the action you want to perform when the DISARM button is clicked for the given IP
        print(f"DISARM button clicked for {ip}")

    def light_button_command(ip):
        # Add the action you want to perform when the LIGHT button is clicked for the given IP
        print(f"LIGHT button clicked for {ip}")

    def takeoff_button_command(ip):
        # Add the action you want to perform when the TAKE OFF button is clicked for the given IP
        print(f"TAKE OFF button clicked for {ip}")

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

    # for i in range(5):
    #     label = Label(frame, text=f"Label {i}")
    #     button = Button(frame, text=f"Button {i}")
    #     label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    #     button.grid(row=i, column=1, padx=10, pady=5, sticky="e")

    frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

''''///////////////////////////'''


mainloop()
