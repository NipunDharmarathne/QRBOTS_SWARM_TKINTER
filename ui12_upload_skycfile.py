from tkinter import *
from pymavlink import mavutil
import socket
import time
import math
import threading
import os
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
from math import asin, atan2, cos, degrees, radians, sin
from tkinter import filedialog
import zipfile
import json

def calculate_distance_and_bearing(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    angle = math.atan2(x2 - x1, y2 - y1)
    angle_degrees = math.degrees(angle)
    return distance, angle_degrees

# func to get coordinates of the point #############################################################################
def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)

drone_home_positions = []

def upload_file():
    contentShowOrientation = showOrientation.get("1.0", "end-1c")
    float_contentShowOrientation = float(contentShowOrientation)
    showOrientationVal = float_contentShowOrientation
    print(showOrientationVal)

    contentShowOrigin = showOrigin.get("1.0", "end-1c")
    print(showOrientationVal)

    lat1_1_str, lon1_1_str = contentShowOrigin.split()
    lat1_1 = float(lat1_1_str)
    lon1_1 = float(lon1_1_str)

    skyc_file_path = filedialog.askopenfilename()
    json_file_name = 'show.json'

    if skyc_file_path:
        label.config(text=skyc_file_path)

        with zipfile.ZipFile(skyc_file_path, 'r') as zip_file:
            # Check if the JSON file exists in the zip file
            if json_file_name in zip_file.namelist():
                # Extract the JSON file from the zip file
                with zip_file.open(json_file_name) as json_file:
                    # Read and parse the JSON data
                    data = json.load(json_file)

        # Extract home positions of drones
        global drone_home_positions
        drone_home_positions.clear()
        map_widget.delete_all_marker()

        for drone in data['swarm']['drones']:
            home_position = drone['settings']['home']
            drone_home_positions.append(home_position)

        # Now, 'drone_home_positions' contains a list of home positions
        print("Home Positions of Drones:")
        for i, position in enumerate(drone_home_positions, 1):
            print(f"Drone {i}: {position}")
            distance, bearing = calculate_distance_and_bearing(drone_home_positions[0][:2], position[:2])
            print(distance, bearing)
            lat, lon = get_point_at_distance(lat1_1, lon1_1, distance/1000, bearing)
            map_widget.set_marker(lat, lon, icon=location_image)

    else:
        map_widget.delete_all_marker()
        label.config(text="No file selected")




# window #############################################################################
master = Tk()
master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), master.winfo_screenheight()))
master.wm_state("zoomed")
master.configure(bg="grey6")
master.title("QRBOTS")

# map #############################################################################
right_frame = Frame(master, bg='grey')
right_frame.grid(row=0, rowspan=25, column=2, padx=3, pady=3, sticky="nw")

# path for the database to use
script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "offline_tiles_nyc.db")

# create map widget and only use the tiles from the database, not the online server (use_database_only=True)
map_widget = TkinterMapView(right_frame, width=1000, height=700, corner_radius=0, use_database_only=False,
                            max_zoom=19, database_path=database_path)
map_widget.pack(fill="both", expand=True)
map_widget.set_position(7.25963, 80.59915)
map_widget.set_zoom(19)

current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
location_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "location.png")).resize((4, 7)))


def add_marker_event(coords, showOrientationVal):
    print("Add marker:", coords)
    print(drone_home_positions)
        
    lat1_1 = coords[0]
    lon1_1 = coords[1]

    for i, position in enumerate(drone_home_positions, 1):
        print(f"Drone {i}: {position}")
        distance, bearing = calculate_distance_and_bearing(drone_home_positions[0][:2], position[:2])
        print(distance, bearing)
        lat, lon = get_point_at_distance(lat1_1, lon1_1, distance/1000, bearing+showOrientationVal)
        map_widget.set_marker(lat, lon, icon=location_image)




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
esp32_ip_list = []
udpout_connection_list = []

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

'''/// BUTTON COMMANDS //////////////////////////////////////////////'''
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

def getShowOrientation():
    contentShowOrientation = showOrientation.get("1.0", "end-1c")
    float_contentShowOrientation = float(contentShowOrientation)
    showOrientationVal = float_contentShowOrientation
    print(showOrientationVal)

    contentShowOrigin = showOrigin.get("1.0", "end-1c")
    lat1_1_str, lon1_1_str = contentShowOrigin.split()
    lat1_1 = float(lat1_1_str)
    lon1_1 = float(lon1_1_str)
    print("Latitude:", lat1_1)
    print("Longitude:", lon1_1)

    map_widget.delete_all_marker()
    add_marker_event([lat1_1, lon1_1], showOrientationVal)

label = Label(master, text="No file selected", fg="white", bg="grey6")
label.grid(row = 5, column = 0, columnspan=2, sticky = N)

upload_button = Button(master, text="Upload File", bg="cyan4", command=upload_file)
upload_button.grid(row = 6, column = 0, columnspan=2, sticky = N)

showOriginLabel = Label(master, text = "   Show Origin:", fg="white", bg="grey6")
showOriginLabel.grid(row = 7, column = 0, sticky = W)

showOrigin = Text(master, height=1, width=22)
showOrigin.insert("1.0", "7.2597843 80.5991768")
showOrigin.grid(row = 7, column = 1)

showOrientationLabel = Label(master, text = "   Show Orientation:", fg="white", bg="grey6")
showOrientationLabel.grid(row = 8, column = 0, sticky = W)

showOrientation = Text(master, height=1, width=22)
showOrientation.insert("1.0", "0.0")
showOrientation.grid(row = 8, column = 1, sticky = N)

updateShowOriginOrientation = Button(master, text = "UPDATE", bg="cyan4", command=getShowOrientation)
updateShowOriginOrientation.grid(row = 9, column = 0, columnspan=2, sticky = N)


b1 = Button(master, text = "ARM ALL", height=3, width=25, bg="springgreen3", command=armAll)
b1.grid(row = 10, column = 0, sticky = W)

b2 = Button(master, text = "DISARM ALL", height=3, width=25, bg="cyan4", command=disarmAll)
b2.grid(row = 10, column = 1, sticky = W)

b3 = Button(master, text = "TAKE OFF ALL", height=3, width=25, bg="chartreuse2", command=takeOffAll)
b4 = Button(master, text = "LAND ALL", height=3, width=25, bg="chocolate1", command=landAll)
b5 = Button(master, text = "RTL ALL", height=3, width=25, bg="goldenrod1", command=rtlAll)
b6 = Button(master, text = "SHOW ALL", height=3, width=25, bg="tomato", command=showAll)
b7 = Button(master, text = "LIGHT ALL", height=3, width=25, bg="olivedrab1", command=lightsAll)

# arranging button widgets
b3.grid(row = 11, column = 0, sticky = W)
b4.grid(row = 11, column = 1, sticky = W)
b5.grid(row = 12, column = 0, sticky = W)
b6.grid(row = 12, column = 1, sticky = W)
b7.grid(row = 13, column = 0, sticky = W)



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

    frame_inner.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

''''///////////////////////////'''

yawVals = []

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
    the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

    while True:
        msg = the_connection.recv_match(type='ATTITUDE', blocking=True)
        
        if msg is not None:    
            for i in range(len(esp32_ip_list)):
                if msg.get_srcSystem() == i + 1:
                    # print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")
                    yawVals[i].config(text=f"{msg.yaw * 180 / math.pi:.2f}")


receive_thread = threading.Thread(target=listen_func)
def start_receive_thread():
    receive_thread.start()

'''////////////////////////////////////////'''

mainloop()
