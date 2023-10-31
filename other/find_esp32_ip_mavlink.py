from pymavlink import mavutil

connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

while True:
    message = connection.recv_msg()
    if message is not None:
        print(f"Received message from {connection.address}")
        # Process the message here
