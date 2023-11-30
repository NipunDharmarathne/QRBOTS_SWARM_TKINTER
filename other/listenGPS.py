from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Continuously receive and print messages
while 1:
    msg = the_connection.recv_match(type='GPS_RAW_INT', blocking=True)

    if msg is not None:
        print(msg)
        # print(msg.lat)
        # print(msg.lon)