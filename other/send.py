from pymavlink import mavutil

the_connection_1 = mavutil.mavlink_connection('udpout:192.168.123.51:14555', source_system=2, source_component=0)
the_connection_1.mav.system_time_send(1, 1)