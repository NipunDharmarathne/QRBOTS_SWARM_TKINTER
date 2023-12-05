from tkinter import *
from tkinter.ttk import Combobox
from pymavlink import mavutil
import socket
import time
import math
import threading
import serial.tools.list_ports

import map_functions
import rtk_functions
import other_functions
import button_functions

drone_home_positions = []   # positions of drones [x, y, z] obtained from skyc file
markers_skyc = []           # markers in the map set according to the drone_home_positions in skyc file


# window #############################################################################
master = Tk()
master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
master.wm_state("zoomed")
master.configure(bg="grey6")
master.title("QRBOTS")

# map #############################################################################
right_frame = Frame(master, bg='grey')
right_frame.grid(row=0, rowspan=25, column=2, padx=3, pady=3, sticky="nw")


map_widget = map_functions.create_map_widget(right_frame)
location_skyc, location_drone = map_functions.load_images()


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

# scan button ##################################################################
def scan():
    receive_data()

scan = Button(master, text = "SCAN", bg="springgreen3", command=scan)
scan.grid(row = 2, column=0, columnspan=2)

# Listen messages ############################################################
frame1 = Frame(master)
frame1.grid(row=3, column=0, columnspan=2, sticky="nsew")

# Specify the width and height for the canvas
canvas1 = Canvas(frame1, width=300, height=100)
canvas1.grid(row=0, column=0, sticky="nsew")
scrollbar1 = Scrollbar(frame1, orient="vertical", command=canvas1.yview)
scrollbar1.grid(row=0, column=1, sticky="ns")

frame1.grid_rowconfigure(0, weight=1)
frame1.grid_columnconfigure(0, weight=1)

canvas1.config(yscrollcommand=scrollbar1.set)

frame1_inner = Frame(canvas1)
canvas1.create_window((0, 0), window=frame1_inner, anchor="nw")

frame1_inner.update_idletasks()
canvas1.config(scrollregion=canvas1.bbox("all"))

# start button ##################################################################
def start():
    create_labels(frame1_inner)
    start_receive_thread()

start = Button(master, text = "START", bg="springgreen3", command=start)
start.grid(row = 4, column=0, columnspan=2)

'''/// BACKEND ////////////////////////////////////////////////////////////////////////////////////////////////////'''
esp32_ip_list = []              # list to keep track of esp32 ips sending data to gui
udpout_connection_list = []     # mavlink udpout connections set according to esp32_ip_list
markers_drones = []             # markers in the map to show real time location of drones

def create_udp_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 14550))
    udp_socket.settimeout(3.0)
    return udp_socket

def receive_data():
    global esp32_ip_list
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

    global markers_drones
    for i in range(len(esp32_ip_list)):
        markers_drones.append(map_widget.set_marker(0, 0, icon=location_drone, icon_anchor="s", text=i+1, text_color="#000000", font="Tahoma 6 bold"))
    print(markers_drones)

'''/// BUTTON COMMANDS //////////////////////////////////////////////'''

def getShowOrientation():
    contentShowOrientation = showOrientation.get()
    float_contentShowOrientation = float(contentShowOrientation)
    showOrientationVal = float_contentShowOrientation
    print(showOrientationVal)

    contentShowOrigin = showOrigin.get()
    lat1_1_str, lon1_1_str = contentShowOrigin.split()
    lat1_1 = float(lat1_1_str)
    lon1_1 = float(lon1_1_str)
    print("Latitude:", lat1_1)
    print("Longitude:", lon1_1)
    map_functions.add_marker_event([lat1_1, lon1_1], showOrientationVal, map_widget, location_skyc, drone_home_positions, markers_skyc)

selected_port = ""  
selected_baudrate = 921600

def sendRTKmessages():
    start_rtk_thread()

def on_select_portsdropdown(event):
    global selected_port
    selected_port = portsdropdown_var.get()
    print(f"Selected item: {selected_port}")

def on_select_baudratedropdown(event):
    global selected_baudrate
    selected_baudrate = baudratedropdown_var.get()
    print(f"Selected item: {selected_baudrate}")

portsdropdown_var = StringVar()
portsoptions = other_functions.get_available_ports()
portsdropdown = Combobox(master, textvariable=portsdropdown_var, values=portsoptions, state="readonly")
portsdropdown.set("Select Port")  # Set the default value
portsdropdown.bind("<<ComboboxSelected>>", on_select_portsdropdown)  # Bind the event handler
portsdropdown.grid(row = 5, column = 0, sticky = EW)

baudratedropdown_var = StringVar()
baudrateoptions = ["921600", "57600", "9600"]
baudratedropdown = Combobox(master, textvariable=baudratedropdown_var, values=baudrateoptions, state="readonly")
baudratedropdown.set("921600")  # Set the default value
baudratedropdown.bind("<<ComboboxSelected>>", on_select_baudratedropdown)  # Bind the event handler
baudratedropdown.grid(row = 5, column = 1, sticky = EW)

Button(master, text = "SEND RTK MESSAGES", bg="cyan4", command=sendRTKmessages).grid(row = 6, column = 0, columnspan=2, sticky=N)

label = Label(master, text="No file selected", fg="white", bg="grey6")
label.grid(row = 7, column = 0, columnspan=2, sticky = N)


Label(master, text = " Show Origin:", fg="white", bg="grey6").grid(row = 9, column = 0, sticky = W)

def on_enter_showOrigin(event):
    getShowOrientation()

def on_enter_showOrientation(event):
    getShowOrientation()

showOrigin = Entry(master, width=22)
showOrigin.insert(0, "7.2597843 80.5991768")
showOrigin.grid(row=9, column=1, sticky=EW)
showOrigin.bind("<Return>", on_enter_showOrigin)

Label(master, text = " Show Orientation:", fg="white", bg="grey6").grid(row = 10, column = 0, sticky = W)

showOrientation = Entry(master, width=22)
showOrientation.insert(0, "0.0")
showOrientation.grid(row=10, column=1, sticky=EW)
showOrientation.bind("<Return>", on_enter_showOrientation)

Button(master, text="Upload File", bg="cyan4", command=lambda: map_functions.upload_file(markers_skyc, drone_home_positions, showOrigin, showOrientation, label, map_widget, location_skyc)).grid(row = 8, column = 0, columnspan=2, sticky = N)



Button(master, text = "ARM ALL", height=3, width=25, bg="springgreen3", command=lambda: button_functions.armAll(udpout_connection_list)).grid(row = 12, column = 0, sticky = NSEW)
Button(master, text = "DISARM ALL", height=3, width=25, bg="cyan4", command=lambda: button_functions.disarmAll(udpout_connection_list)).grid(row = 12, column = 1, sticky = NSEW)
Button(master, text = "TAKE OFF ALL", height=3, width=25, bg="chartreuse2", command=lambda: button_functions.takeOffAll(udpout_connection_list)).grid(row = 13, column = 0, sticky = NSEW)
Button(master, text = "LAND ALL", height=3, width=25, bg="chocolate1", command=lambda: button_functions.landAll(udpout_connection_list)).grid(row = 13, column = 1, sticky = NSEW)
Button(master, text = "RTL ALL", height=3, width=25, bg="goldenrod1", command=lambda: button_functions.rtlAll(udpout_connection_list)).grid(row = 14, column = 0, sticky = NSEW)
Button(master, text = "SHOW ALL", height=3, width=25, bg="tomato", command=lambda: button_functions.showAll(udpout_connection_list)).grid(row = 14, column = 1, sticky = NSEW)
Button(master, text = "LIGHT ALL", height=3, width=25, bg="olivedrab1", command=lambda: button_functions.lightsAll(udpout_connection_list)).grid(row = 15, column = 0, sticky = NSEW)

'''/////////////////////////////////////////////////'''

def create_labels_and_buttons(frame):
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

''''///////////////////////////'''

yawVals = []
pitchVals = []
rollVals = []

def create_labels(frame):
    # Clear the frame by destroying all its children widgets
    for widget in frame.winfo_children():
        widget.destroy()
        
    for i in range(len(esp32_ip_list)):
        droneIP = Label(frame, text=esp32_ip_list[i])
        yaw = Label(frame, text="Yaw:")
        pitch = Label(frame, text="Pitch:")
        roll = Label(frame, text="Roll:") 
        yawVal = Label(frame, text="0.00")
        pitchVal = Label(frame, text="0.00")
        rollVal = Label(frame, text="0.00") 

        yawVals.append(yawVal)
        pitchVals.append(pitchVal)
        rollVals.append(rollVal)

        droneIP.grid(row=i, column=0, padx=1, pady=1, sticky="w")
        yaw.grid(row=i, column=1, padx=1, pady=1, sticky="e")
        yawVal.grid(row=i, column=2, padx=1, pady=1, sticky="e")
        pitch.grid(row=i, column=3, padx=1, pady=1, sticky="e")
        pitchVal.grid(row=i, column=4, padx=1, pady=1, sticky="e")
        roll.grid(row=i, column=5, padx=1, pady=1, sticky="e")
        rollVal.grid(row=i, column=6, padx=1, pady=1, sticky="e")

    frame1_inner.update_idletasks()
    canvas1.config(scrollregion=canvas1.bbox("all"))


def listen_func():
    global markers_drones
    the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

    while True:
        msg = the_connection.recv_match(type='ATTITUDE', blocking=True)
        
        if msg is not None:    
            for i in range(len(esp32_ip_list)):
                if msg.get_srcSystem() == i + 1:
                    # print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")
                    yawVals[i].config(text=f"{msg.yaw * 180 / math.pi:.2f}")
                    pitchVals[i].config(text=f"{msg.pitch * 180 / math.pi:.2f}")
                    rollVals[i].config(text=f"{msg.roll * 180 / math.pi:.2f}")

        msgGPS = the_connection.recv_match(type='GPS_RAW_INT', blocking=True)
        if msgGPS is not None:
            for i in range(len(esp32_ip_list)):
                if msgGPS.get_srcSystem() == i + 1:
                    markers_drones[i].set_position(msgGPS.lat/10000000.0, msgGPS.lon/10000000.0)
            # print(msgGPS)
            print(msgGPS.lat/10000000.0, msgGPS.lon/10000000.0)

            # if msg.get_srcSystem() == 1:
            #     marker_1.set_position(msgGPS.lat/10000000.0, msgGPS.lon/10000000.0)
            # elif msg.get_srcSystem() == 2:
            #     marker_2.set_position(msgGPS.lat/10000000.0, msgGPS.lon/10000000.0)

def listen_rtk():
    print(selected_port.split(':', 1)[0].strip(), selected_baudrate)
    serial_port = serial.Serial(selected_port.split(':', 1)[0].strip(), selected_baudrate)
    
    while True:
        data = serial_port.readline()
        print(data)
        rtk_functions.encode(data)

receive_thread = threading.Thread(target=listen_func)
def start_receive_thread():
    receive_thread.start()

rtk_thread = threading.Thread(target=listen_rtk)
def start_rtk_thread():
    rtk_thread.start()

'''////////////////////////////////////////'''

mainloop()
