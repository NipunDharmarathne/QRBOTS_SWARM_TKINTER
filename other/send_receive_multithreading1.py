from pymavlink import mavutil
import threading
import tkinter as tk

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Start a connection listening on a UDP port
the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.51:14555')

# Function to send the command when the button is pressed
def send_command():
    the_connection_1.mav.system_time_send(1, 1)

# Function to continuously receive and print messages
def receive_messages():
    while True:
        msg = the_connection.recv_match(blocking=True)

        if msg is not None:
            print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")

# # Create threads for sending and receiving
# send_thread = threading.Thread(target=send_command)
receive_thread = threading.Thread(target=receive_messages)

# # Function to start the send thread
# def start_send_thread():
#     send_thread.start()
#     send_thread.join()

# Function to start the receive thread
def start_receive_thread():
    receive_thread.start()

# Create a simple GUI using Tkinter
root = tk.Tk()
root.title("Thread Control")

# Create buttons to start the threads
send_button = tk.Button(root, text="Start Send Thread", command=send_command)
receive_button = tk.Button(root, text="Start Receive Thread", command=start_receive_thread)

# Pack the buttons into the GUI
send_button.pack()
receive_button.pack()

root.mainloop()
