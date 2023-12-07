from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Continuously receive and print messages
while 1:
    msg = the_connection.recv_match(blocking=True)

    if msg is not None:
        print(msg.get_type())
        # print(msg.lat)
        # print(msg.lon)