from pymavlink import mavutil
import threading

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Start a connection listening on a UDP port
the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.50:14555')

# Function to send the command when the button is pressed
def send_command():
    the_connection_1.mav.system_time_send(1, 1)

# Function to continuously receive and print messages
def receive_messages():
    while True:
        msg = the_connection.recv_match(blocking=True)

        if msg is not None:
            print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")

# Create threads for sending and receiving
send_thread = threading.Thread(target=send_command)
receive_thread = threading.Thread(target=receive_messages)

# Start both threads
send_thread.start()
receive_thread.start()

# Wait for threads to finish (if needed)
# send_thread.join()
# receive_thread.join()
