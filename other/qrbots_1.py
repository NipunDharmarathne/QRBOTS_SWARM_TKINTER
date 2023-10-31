from pymavlink import mavutil
import tkinter as tk

def listen_func():
    msg = the_connection.recv_match(type='ATTITUDE', blocking=True)
    if msg.get_srcSystem()==1 and msg.get_srcComponent()==1:    
        if msg is not None:
            print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")
            roll_1.config(text=f"Roll: {msg.roll:.6f}")
            pitch_1.config(text=f"Pitch: {msg.pitch:.6f}")
            yaw_1.config(text=f"Yaw: {msg.yaw:.6f}")
        root.after(10, listen_func)  
    elif msg.get_srcSystem()==2 and msg.get_srcComponent()==1:
        if msg is not None:
            print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")
            roll_2.config(text=f"Roll: {msg.roll:.6f}")
            pitch_2.config(text=f"Pitch: {msg.pitch:.6f}")
            yaw_2.config(text=f"Yaw: {msg.yaw:.6f}")
        root.after(10, listen_func) 

def send_func1():
    the_connection_1.mav.system_time_send(1, 1)

def send_func2():
    the_connection_2.mav.param_request_list_send(1, 0)

# Create a Tkinter window
root = tk.Tk()
root.title("QRBOTS")

# Create a label to display the roll information
drone_1 = tk.Label(root, text="--------------------Drone 1--------------------")
drone_1.pack(anchor='w')

roll_1 = tk.Label(root, text="Roll: N/A")
roll_1.pack(anchor='w')

pitch_1 = tk.Label(root, text="Pitch: N/A")
pitch_1.pack(anchor='w')

yaw_1 = tk.Label(root, text="Yaw: N/A")
yaw_1.pack(anchor='w')

drone_2 = tk.Label(root, text="--------------------Drone 2--------------------")
drone_2.pack(anchor='w')

roll_2 = tk.Label(root, text="Roll: N/A")
roll_2.pack(anchor='w')

pitch_2 = tk.Label(root, text="Pitch: N/A")
pitch_2.pack(anchor='w')

yaw_2 = tk.Label(root, text="Yaw: N/A")
yaw_2.pack(anchor='w')

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')
the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.50:14555')
the_connection_2 = mavutil.mavlink_connection('udpout:192.168.123.51:14555')

# Create a button and associate the function with it
listen = tk.Button(root, text="Connect", command=listen_func)
listen.pack()

send1 = tk.Button(root, text="Send D1", command=send_func1)
send1.pack()

send2 = tk.Button(root, text="Send D2", command=send_func2)
send2.pack()

# Start the Tkinter main loop
root.mainloop()
