import tkinter as tk
from pymavlink import mavutil


# Create a function to be executed when the button is clicked
def button_click():

    # Start a connection listening on a UDP port
    the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

    # Continuously receive and print messages
    while 1:
        msg = the_connection.recv_match(type='ATTITUDE', blocking=True)

        if msg is not None:
            print(msg)
            yaw_1.config(text="Hello, World!")
            pitch_1.config(text="This is a tkinter example.")
            roll_1.config(text="Button clicked!")


# Create the main window
root = tk.Tk()
root.title("QRBOTS")

# Create and configure labels
yaw_1 = tk.Label(root, text="0.0")
yaw_1.pack(anchor='w')

pitch_1 = tk.Label(root, text="0.0")
pitch_1.pack(anchor='w')

roll_1 = tk.Label(root, text="0.0")
roll_1.pack(anchor='w')

# Create a button
button = tk.Button(root, text="Connect", command=button_click)
button.pack()

# Start the tkinter main loop
root.mainloop()
