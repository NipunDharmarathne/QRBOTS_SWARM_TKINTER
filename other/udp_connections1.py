import tkinter as tk
from pymavlink import mavutil  # Make sure you have the 'pymavlink' module installed

# Function to establish connections
def establish_connections():
    source_ip_list = ['192.168.123.51', '192.168.123.50']
    connections = []

    for source_ip in source_ip_list:
        connection = mavutil.mavlink_connection('udpout:' + source_ip + ':14555')
        connections.append(connection)
        print(f"Connected to {source_ip}")

    for connection in connections:
        connection.mav.system_time_send(1, 1)

# Create a Tkinter window
root = tk.Tk()
root.title("MAVLink Connection")

# Create a button that will call the establish_connections function when pressed
connect_button = tk.Button(root, text="Connect", command=establish_connections)
connect_button.pack()

# Start the Tkinter main loop
root.mainloop()
