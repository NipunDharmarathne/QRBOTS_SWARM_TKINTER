from pymavlink import mavutil

# Start a connection listening on a UDP port
the_connection = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Start a connection listening on a UDP port
the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.50:14555')
the_connection_2 = mavutil.mavlink_connection('udpout:192.168.123.51:14555')

the_connection_1.mav.command_long_send(1, 0,
                                    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
the_connection_1.mav.system_time_send(1, 1)
the_connection_2.mav.param_request_list_send(1, 0)

# Continuously receive and print messages
while 1:
    msg = the_connection.recv_match(blocking=True)

    if msg is not None:
        print(f"sysid: {msg.get_srcSystem()}, compid: {msg.get_srcComponent()}, message id: {msg.get_msgId()}")