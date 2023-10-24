from tkinter import *
from pymavlink import mavutil
import socket
import time

'''/// UI ////////////////////////////////////////////////////////////////////////////////////////////////////'''
master = Tk()
master.configure(bg="grey6")
master.title("QRBOTS")

# this will create a label widget
l1 = Label(master, text = "Number of Drones:", fg="white", bg="grey6")
l2 = Label(master, text = "0", fg="white", bg="grey6")
l1.grid(row = 0, column = 0, sticky = E)
l2.grid(row = 0, column = 1, sticky = W)

# Create a Text widget for displaying text
text = Text(master, wrap="word", width=27, height=5)
text.grid(row = 1, column=0, columnspan=2)


def scan():
    receive_data(source_ip_list)

def start():
    the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')


# scan stop buttons
scan = Button(master, text = "SCAN", bg="springgreen3", command=scan)
master.rowconfigure(2, minsize=35)
scan.grid(row = 2, column=0, columnspan=2)

# button widget


b3 = Button(master, text = "HOLD ALL", height=3, width=15, bg="olivedrab1")
b4 = Button(master, text = "RTH ALL", height=3, width=15, bg="chocolate1")
b5 = Button(master, text = "LAND ALL", height=3, width=15, bg="goldenrod1")
b6 = Button(master, text = "SHUTDOWN ALL", height=3, width=15, bg="tomato")

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
    label_text = ""
    text.delete('1.0', 'end')
    connections.clear()
    source_ip_list.clear()
    
    socket = create_udp_socket()
    start_time = time.time()
    while time.time() - start_time < 3:
        data, addr = socket.recvfrom(1024)

        if addr[0] not in source_ip_list:
            source_ip_list.append(addr[0])

    socket.close()
    
    print("ESP IP Addresses:")
    print(source_ip_list)

    for ip in source_ip_list:
        label_text += ip + "\n"
    text.insert("1.0", label_text)

    l2.config(text=len(source_ip_list))

    for source_ip in source_ip_list:
        connection = mavutil.mavlink_connection('udpout:' + source_ip + ':14555')
        connections.append(connection)
    
    print(connections)



def armAll():
    for connection in connections:
        connection.mav.system_time_send(1, 1)

def disarmAll():
    for connection in connections:
        connection.mav.param_request_list_send(1, 0)

b1 = Button(master, text = "ARM ALL", height=3, width=15, bg="springgreen3", command=armAll)
b1.grid(row = 3, column = 0, sticky = W)

b2 = Button(master, text = "DISARM ALL", height=3, width=15, bg="cyan3", command=disarmAll)
b2.grid(row = 3, column = 1, sticky = W)






# Start a connection listening on a UDP port
# the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')
# the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.50:14555')
# the_connection_2 = mavutil.mavlink_connection('udpout:192.168.123.51:14555')

# def send_func1():
#     the_connection_1.mav.system_time_send(1, 1)

# def send_func2():
#     the_connection_2.mav.param_request_list_send(1, 0)


mainloop()
