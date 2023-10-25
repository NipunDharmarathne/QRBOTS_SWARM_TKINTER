from tkinter import *
from pymavlink import mavutil
import socket
import time

'''/// UI ////////////////////////////////////////////////////////////////////////////////////////////////////'''
master = Tk()
master.configure(bg="grey6")
master.title("QRBOTS")

# num Drones
numDronesLabel = Label(master, text = "Number of Drones:", fg="white", bg="grey6")
numDronesLabel.grid(row = 0, column = 0, sticky = E)
numDrones = Label(master, text = "0", fg="white", bg="grey6")
numDrones.grid(row = 0, column = 1, sticky = W)


def scan():
    receive_data(source_ip_list)

def start():
    the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')


# scan stop buttons
scan = Button(master, text = "SCAN", bg="springgreen3", command=scan)
master.rowconfigure(2, minsize=35)
scan.grid(row = 2, column=0, columnspan=2)

# button widget
b3 = Button(master, text = "LIGHT ALL", height=3, width=25, bg="olivedrab1")
b4 = Button(master, text = "TAKE OFF ALL", height=3, width=25, bg="chocolate1")
b5 = Button(master, text = "LAND ALL", height=3, width=25, bg="goldenrod1")
b6 = Button(master, text = "RTL ALL", height=3, width=25, bg="tomato")

# arranging button widgets
b3.grid(row = 4, column = 0, sticky = W)
b4.grid(row = 4, column = 1, sticky = W)
b5.grid(row = 5, column = 0, sticky = W)
b6.grid(row = 5, column = 1, sticky = W)

'''/// BACKEND ////////////////////////////////////////////////////////////////////////////////////////////////////'''

source_ip_list = []
connections = []

def create_udp_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 14550))
    return server_socket

def receive_data(source_ip_list):
    connections.clear()
    source_ip_list.clear()
    
    socket = create_udp_socket()
    start_time = time.time()
    while time.time() - start_time < 3:
        data, addr = socket.recvfrom(1024)

        if addr[0] not in source_ip_list:
            source_ip_list.append(addr[0])

    socket.close()
    
    source_ip_list = sorted(source_ip_list, key=lambda x: (int(x.split('.')[-1]), x))
    print("ESP IP Addresses:")
    print(source_ip_list)

    numDrones.config(text=len(source_ip_list))

    for source_ip in source_ip_list:
        connection = mavutil.mavlink_connection('udpout:' + source_ip + ':14555')
        connections.append(connection)
    
    create_labels_and_buttons(frame_inner)
    print(connections)



def armAll():
    for connection in connections:
        connection.mav.sys_status_send(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)


def arm1():
    connections[1].mav.system_time_send(1, 1)



def disarmAll():
    for connection in connections:
        connection.mav.param_request_list_send(1, 0)

b1 = Button(master, text = "ARM ALL", height=3, width=25, bg="springgreen3", command=armAll)
b1.grid(row = 3, column = 0, sticky = W)

b2 = Button(master, text = "DISARM ALL", height=3, width=25, bg="cyan3", command=disarmAll)
b2.grid(row = 3, column = 1, sticky = W)







'''/////////////////////////////////////////////////'''

def create_labels_and_buttons(frame):

    def arm_button_command(ip):
        # Add the action you want to perform when the ARM button is clicked for the given IP
        print(f"ARM button clicked for {ip}")

    def disarm_button_command(ip):
        # Add the action you want to perform when the DISARM button is clicked for the given IP
        print(f"DISARM button clicked for {ip}")

    def light_button_command(ip):
        # Add the action you want to perform when the LIGHT button is clicked for the given IP
        print(f"LIGHT button clicked for {ip}")

    def takeoff_button_command(ip):
        # Add the action you want to perform when the TAKE OFF button is clicked for the given IP
        print(f"TAKE OFF button clicked for {ip}")


    for i in range(len(source_ip_list)):
        droneIP = Label(frame, text=source_ip_list[i])
        arm = Button(frame, text="ARM", bg="springgreen3", command=lambda ip=source_ip_list[i]: arm_button_command(ip))
        disarm = Button(frame, text="DISARM", bg="cyan3", command=lambda ip=source_ip_list[i]: disarm_button_command(ip))
        light = Button(frame, text="LIGHT", bg="olivedrab1", command=lambda ip=source_ip_list[i]: light_button_command(ip))
        takeOff = Button(frame, text="TAKE OFF", bg="chocolate1", command=lambda ip=source_ip_list[i]: takeoff_button_command(ip))


        droneIP.grid(row=i, column=0, padx=1, pady=1, sticky="w")
        arm.grid(row=i, column=1, padx=1, pady=1, sticky="e")
        disarm.grid(row=i, column=2, padx=1, pady=1, sticky="e")
        light.grid(row=i, column=3, padx=1, pady=1, sticky="e")
        takeOff.grid(row=i, column=4, padx=1, pady=1, sticky="e")


def on_mousewheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create a frame for the canvas and scrollbar
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

frame_inner.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

canvas.bind_all("<MouseWheel>", on_mousewheel)

''''///////////////////////////'''


mainloop()
