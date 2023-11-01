from pymavlink import mavutil
import tkinter as tk

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Start a connection listening on a UDP port
the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.51:14555')

# Function to send the command when the button is pressed
def send_command():
    the_connection_1.mav.system_time_send(1, 1)
    print("Command sent")

# Create a GUI window
root = tk.Tk()
root.title("Send Command")

# Create a button and link it to the send_command function
send_button = tk.Button(root, text="Send Command", command=send_command)
send_button.pack()

# Continuously receive and print messages
while True:
    msg = the_connection.recv_match(blocking=True)
    if msg is not None:
        print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")
    
    # Update the GUI to process events (required for the button to work)
    root.update()
